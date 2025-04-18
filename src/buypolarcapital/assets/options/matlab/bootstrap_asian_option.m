% bootstrap_asian_option.m
% Bootstrap-based simulation of Asian option payoff (no parametric model)

%% Parameters
S0 = 100;                 % Initial price
K = 105;                  % Strike
r = 0.01;                 % Risk-free rate
T = 1;                    % Maturity (1 year)
n_days = 252;             % Trading days
n_sim = 10000;            % Sim paths
dt = T / n_days;

%% Load or simulate historical log returns (e.g. from real data)
% For demo: synthetic data mimicking daily returns
rng(42);
daily_returns = randn(1000,1) * 0.01;   % mean ~ 0, std ~ 1%

%% Bootstrap simulation
boot_idx = randi(length(daily_returns), n_days, n_sim);  % resample with replacement
boot_ret = daily_returns(boot_idx);                      % n_days x n_sim

% Cumulative log returns
log_paths = cumsum(boot_ret, 1);
S_paths = S0 * exp(log_paths);                           % price paths
S_avg = mean(S_paths, 1);                                % Asian average price

% Asian call payoff
payoff = max(S_avg - K, 0);
price = exp(-r * T) * mean(payoff);

%% Plot
figure('Units','inches','Position',[0,0,6,4.2]);
histogram(S_avg, 50, 'Normalization', 'pdf', 'FaceAlpha', 0.6)
xlabel('Average Price over T', 'FontSize', 10)
ylabel('Density', 'FontSize', 10)
title(sprintf('Bootstrap Asian Call Option Price ≈ %.2f', price), 'FontSize', 12)
grid on
box off
set(gca, 'FontName', 'Helvetica', 'FontSize', 10, 'LineWidth', 1.2)

%% Export
set(gcf, 'PaperPositionMode', 'auto');
if ~exist('plots', 'dir')
    mkdir('plots');
end
print(gcf, 'plots/bootstrap_asian_option', '-dpdf', '-painters', '-r300');
