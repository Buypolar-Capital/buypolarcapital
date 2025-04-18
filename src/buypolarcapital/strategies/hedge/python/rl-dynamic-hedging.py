class HedgingEnv(gym.Env):
    def __init__(self, S, v, K=100, r=0.05, T=1.0):
        super(HedgingEnv, self).__init__()
        self.S = S
        self.v = v
        self.K = K
        self.r = r
        self.T = T
        self.n_steps = S.shape[1] - 1
        self.action_space = spaces.Discrete(3)  # -1 (sell), 0 (hold), 1 (buy)
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(3,), dtype=np.float32)
        self.reset()

    def reset(self):
        self.t = 0
        self.position = 0  # Shares held
        self.cash = 0
        self.option_price = self.black_scholes(self.S[0, 0], self.v[0, 0], self.T)
        self.state = [self.S[0, 0], self.v[0, 0], self.delta(self.S[0, 0], self.v[0, 0], self.T)]
        return self.state

    def black_scholes(self, S, v, t):
        from scipy.stats import norm
        d1 = (np.log(S / self.K) + (self.r + 0.5 * v) * t) / np.sqrt(v * t)
        d2 = d1 - np.sqrt(v * t)
        return S * norm.cdf(d1) - self.K * np.exp(-self.r * t) * norm.cdf(d2)

    def delta(self, S, v, t):
        from scipy.stats import norm
        d1 = (np.log(S / self.K) + (self.r + 0.5 * v) * t) / np.sqrt(v * t)
        return norm.cdf(d1)

    def step(self, action):
        self.t += 1
        S_t = self.S[0, self.t]
        v_t = self.v[0, self.t]
        t_left = self.T - (self.t / self.n_steps)
        new_option_price = self.black_scholes(S_t, v_t, t_left)
        delta = self.delta(S_t, v_t, t_left)

        # Action: -1 (sell 1 share), 0 (hold), 1 (buy 1 share)
        trade = action - 1
        self.position += trade
        self.cash -= trade * S_t  # Cost of buying/selling shares

        # Reward: Negative cost of hedging error
        portfolio_value = self.cash + self.position * S_t
        hedging_error = portfolio_value - new_option_price
        reward = -abs(hedging_error)

        self.state = [S_t, v_t, delta]
        done = self.t == self.n_steps
        return self.state, reward, done, {}

# DQN Agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.Sequential([
            layers.Dense(24, input_dim=self.state_size, activation='relu'),
            layers.Dense(24, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        act_values = self.model.predict(np.array([state]), verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = np.random.choice(len(self.memory), batch_size, replace=False)
        states = np.array([self.memory[i][0] for i in minibatch])
        actions = np.array([self.memory[i][1] for i in minibatch])
        rewards = np.array([self.memory[i][2] for i in minibatch])
        next_states = np.array([self.memory[i][3] for i in minibatch])
        dones = np.array([self.memory[i][4] for i in minibatch])

        targets = rewards + self.gamma * np.max(self.model.predict(next_states, verbose=0), axis=1) * (1 - dones)
        target_f = self.model.predict(states, verbose=0)
        for i, action in enumerate(actions):
            target_f[i][action] = targets[i]
        self.model.fit(states, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Train for one stock (AAPL as example)
stock = 'AAPL'
S, v = sim_data[stock]['S'], sim_data[stock]['v']
env = HedgingEnv(S, v)
agent = DQNAgent(state_size=3, action_size=3)
episodes = 100
batch_size = 32

rl_costs = []
delta_costs = []
for e in range(episodes):
    state = env.reset()
    total_cost = 0
    delta_position = 0
    delta_cash = 0
    for t in range(n_steps):
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        total_cost += -reward  # Accumulate hedging cost
        agent.remember(state, action, reward, next_state, done)
        state = next_state

        # Delta hedging benchmark
        delta = env.delta(env.S[0, t], env.v[0, t], env.T - (t / n_steps))
        trade = delta - delta_position
        delta_cash -= trade * env.S[0, t]
        delta_position = delta

        if done:
            rl_costs.append(total_cost)
            delta_costs.append(abs(delta_cash + delta_position * env.S[0, -1] - env.black_scholes(env.S[0, -1], env.v[0, -1], 0)))
            agent.replay(batch_size)
            print(f"Episode {e+1}/{episodes}, RL Cost: {total_cost:.2f}, Delta Cost: {delta_costs[-1]:.2f}")
            break

# Plotting Results
with PdfPages(f'plots/{stock}_hedging.pdf') as pdf:
    # Page 1: Hedging Costs Over Episodes
    plt.figure(figsize=(12, 6))
    plt.plot(rl_costs, label='RL Hedging Cost')
    plt.plot(delta_costs, label='Delta Hedging Cost')
    plt.title(f'{stock} - Hedging Costs Over Episodes')
    plt.xlabel('Episode')
    plt.ylabel('Cost ($)')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Page 2: Cost Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(rl_costs, color='blue', label='RL', kde=True, stat='density')
    sns.histplot(delta_costs, color='orange', label='Delta', kde=True, stat='density')
    plt.title(f'{stock} - Hedging Cost Distribution')
    plt.xlabel('Cost ($)')
    plt.legend()
    pdf.savefig()
    plt.close()

print(f"PDF saved for {stock} with 2 pages!")