% Delta Estimation using Malliavin Calculus vs Finite Difference
% BuyPolar Capital - Malliavin Calculus Module (MATLAB)

%% Parameters
S0 = 100;       % initial asset price
K = 100;        % strike
r = 0.05;       % risk-free rate
sigma = 0.2;    % volatility
T = 1;          % maturity
N = 10000;      % number of paths

%% Simulate paths
rng(42);
Z = randn(N,1);
ST = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T)*Z);

%% Payoff and price
payoff = max(ST - K, 0);
price = exp(-r*T) * mean(payoff);

%% Delta via finite difference
dS = 0.01 * S0;
ST_up = (S0 + dS) * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T)*Z);
payoff_up = max(ST_up - K, 0);
price_up = exp(-r*T) * mean(payoff_up);
delta_fd = (price_up - price) / dS;

%% Delta via Malliavin calculus (lognormal)
malliavin_weight = Z / (S0 * sigma * sqrt(T));
delta_malliavin = exp(-r*T) * mean(payoff .* malliavin_weight);

%% Output
fprintf('European Call Price: %.4f\n', price);
fprintf('Delta (Finite Difference): %.4f\n', delta_fd);
fprintf('Delta (Malliavin Calculus): %.4f\n', delta_malliavin);

%% Plot histogram of Malliavin weights
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
histogram(payoff .* malliavin_weight, 50, 'Normalization','pdf');
title('Distribution of Malliavin Delta Contributions');
xlabel('Pathwise Delta Contribution'); ylabel('Density');

print(gcf, fullfile('plots','malliavin_delta_comparison'), '-dpdf');

disp('Malliavin calculus delta estimation complete.');
