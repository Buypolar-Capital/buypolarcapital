% Heston Model Simulation and Option Pricing (Euler Discretization)
% BuyPolar Capital - Stochastic Volatility Module (MATLAB)

%% Parameters
S0 = 100;
v0 = 0.04;        % initial variance
r = 0.03;         % risk-free rate
kappa = 2;        % mean reversion speed
theta = 0.04;     % long-term variance
xi = 0.3;         % volatility of volatility
rho = -0.7;       % correlation
T = 1;            % maturity
N = 1000;         % steps
dt = T/N;
M = 10000;        % paths

%% Simulate Heston paths
rng(1);
S = zeros(M, N+1); S(:,1) = S0;
v = zeros(M, N+1); v(:,1) = v0;

for t = 2:N+1
    Z1 = randn(M,1);
    Z2 = rho*Z1 + sqrt(1 - rho^2)*randn(M,1);

    v(:,t) = max(v(:,t-1) + kappa*(theta - v(:,t-1))*dt + xi*sqrt(v(:,t-1).*dt).*Z2, 0);
    S(:,t) = S(:,t-1) .* exp((r - 0.5*v(:,t-1))*dt + sqrt(v(:,t-1)*dt).*Z1);
end

%% Price European call option
K = 100;
payoff = max(S(:,end) - K, 0);
price = exp(-r*T) * mean(payoff);
fprintf('Heston Call Price (MC): %.4f\n', price);

%% Plot sample paths
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
plot(0:dt:T, S(1:30,:)'); hold on;
yline(K, '--r', 'Strike');
title('Heston Model Sample Price Paths'); xlabel('Time'); ylabel('Price');
print(gcf, fullfile('plots','heston_model_simulation'), '-dpdf');

disp('Heston model simulation complete.');
