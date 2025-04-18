% Bayesian Estimation of Volatility without Toolboxes
% BuyPolar Capital - Bayesian Volatility Module (MATLAB)

%% Simulate returns
n = 100;
sigma_true = 0.02; % true volatility (daily)
rng(42);
returns = sigma_true * randn(n,1);

%% Prior parameters for inverse-gamma
alpha0 = 3;   % prior shape
beta0 = 1e-4; % prior scale

%% Sufficient stats for posterior
alpha_post = alpha0 + n/2;
beta_post = beta0 + 0.5 * sum(returns.^2);

%% Posterior distribution (over variance)
var_grid = linspace(1e-6, 0.002, 500);
post_pdf = ((beta_post^alpha_post) ./ gamma(alpha_post)) .* (var_grid.^(-alpha_post-1)) .* exp(-beta_post ./ var_grid);

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
plot(sqrt(var_grid), post_pdf, 'LineWidth', 2);
xline(sigma_true, '--r', 'True Volatility');
title('Posterior Distribution of Volatility');
xlabel('Volatility (sigma)'); ylabel('Posterior Density');
grid on;

print(gcf, fullfile('plots','bayesian_volatility_estimation'), '-dpdf');

disp('Bayesian volatility estimation complete. Plot saved.');
