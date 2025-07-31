% Stochastic Control for Optimal Execution (Almgren_Chriss_Model)
% BuyPolar Capital - Stochastic Control Module (MATLAB)

%% Parameters
T = 1;             % total time (1 day)
N = 100;           % number of time steps
dt = T / N;
t = linspace(0, T, N+1);

X0 = 1e6;          % initial shares to execute
eta = 2e-6;        % temporary impact parameter
gamma_val = 2.5e-6;    % permanent impact parameter
sigma = 0.01;      % volatility of asset price
lambda = 1e-6;     % risk aversion coefficient

%% Optimal trading trajectory
kappa = sqrt(lambda * sigma^2 / eta);
x_star = zeros(N+1,1);

for i = 1:N+1
    tau = T - t(i);
    x_star(i) = X0 * sinh(kappa * tau) / sinh(kappa * T);
end

v_star = -diff(x_star) / dt;  % trading speed per interval

%% Simulate affected price path
rng(42);
P0 = 100;
price = zeros(N+1,1);
price(1) = P0;

for i = 2:N+1
    dP = sigma * sqrt(dt) * randn;
    price(i) = price(i-1) + dP - gamma_val * (x_star(i-1) - x_star(i));
end

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
subplot(2,1,1);
plot(t, x_star, 'b-', 'LineWidth', 2);
title('Optimal Execution Path (Almgren-Chriss)'); ylabel('Shares Remaining');

subplot(2,1,2);
plot(t, price, 'k-', 'LineWidth', 1);
title('Simulated Impacted Price Path'); ylabel('Price'); xlabel('Time');

print(gcf, fullfile('plots','stochastic_control_execution'), '-dpdf');

disp('Stochastic control execution model complete.');