% monte_carlo_call_option.m
% Monte Carlo simulation for European call option pricing

% Parameters
S0 = 100;      % Initial price
K = 105;       % Strike price
r = 0.03;      % Risk-free rate
sigma = 0.2;   % Volatility
T = 1;         % Time to maturity in years
n_steps = 252; % Daily steps
n_paths = 10000;

dt = T / n_steps;
Z = randn(n_steps, n_paths);
S = zeros(n_steps+1, n_paths);
S(1,:) = S0;

for t = 2:n_steps+1
    S(t,:) = S(t-1,:) .* exp((r - 0.5 * sigma^2)*dt + sigma * sqrt(dt) * Z(t-1,:));
end

% Option payoff at maturity
payoff = max(S(end,:) - K, 0);
price_estimate = exp(-r*T) * mean(payoff);

% --- Plot sample paths ---
figure('Units','inches','Position',[0, 0, 6, 4.2]);
plot(0:T/n_steps:T, S(:,1:50), 'LineWidth', 1);
xlabel('Time (Years)', 'FontSize', 10)
ylabel('Simulated Price', 'FontSize', 10)
title(sprintf('Monte Carlo Simulation of Call Option (Est. Price = %.2f)', price_estimate), ...
      'FontSize', 12, 'FontWeight', 'normal')
grid on
box off
set(gca, 'FontName', 'Helvetica', 'FontSize', 10, 'LineWidth', 1.2)

% Save plot as cropped BPC-style PDF
set(gcf, 'PaperPositionMode', 'auto');
if ~exist('plots', 'dir')
    mkdir('plots');
end
print(gcf, 'plots/monte_carlo_call_option', '-dpdf', '-painters', '-r300');
