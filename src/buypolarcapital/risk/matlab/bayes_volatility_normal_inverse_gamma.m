% Bayesian Portfolio Volatility Estimation (Normal-Inverse-Gamma Model)
% BuyPolar Capital - Bayesian Modeling Module (MATLAB)

%% Simulate portfolio returns
n_assets = 5;
n_obs = 250;
true_mu = 0.0005 + 0.0005*randn(n_assets,1);
true_sigma = 0.02 + 0.01*randn(n_assets,1);

rng(42);
returns = true_mu' + true_sigma' .* randn(n_obs, n_assets);

%% Portfolio weights (equal-weighted)
w = ones(n_assets,1) / n_assets;
port_returns = returns * w;

%% Prior parameters for Normal-Inverse-Gamma
mu0 = 0;           % prior mean
kappa0 = 0.01;     % prior strength (mean precision)
alpha0 = 3;        % prior shape
beta0 = 1e-4;      % prior scale

%% Posterior parameters
n = length(port_returns);
ybar = mean(port_returns);
s2 = var(port_returns);

kappaN = kappa0 + n;
muN = (kappa0*mu0 + n*ybar) / kappaN;
alphaN = alpha0 + n/2;
betaN = beta0 + 0.5*sum((port_returns - ybar).^2) + (kappa0*n/(kappa0+n))*(ybar - mu0)^2/2;

%% Sample posterior distributions
n_samp = 1000;
sigma2_samples = 1 ./ gamrnd(alphaN, 1/betaN, n_samp, 1);
mu_samples = muN + sqrt(sigma2_samples ./ kappaN) .* randn(n_samp, 1);

%% Plot posterior distribution
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
histogram(sqrt(sigma2_samples), 50, 'Normalization','pdf');
hold on;
xline(std(port_returns), '--r', 'Sample Std');
title('Posterior Distribution of Portfolio Volatility');
xlabel('Volatility (sigma)'); ylabel('Posterior Density'); grid on;

print(gcf, fullfile('plots','bayesian_portfolio_volatility'), '-dpdf');

fprintf('Posterior mean volatility: %.4f\n', mean(sqrt(sigma2_samples)));
disp('Bayesian portfolio volatility estimation complete.');
