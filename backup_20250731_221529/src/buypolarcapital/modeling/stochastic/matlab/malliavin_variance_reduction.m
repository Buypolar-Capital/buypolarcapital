% Malliavin Weighting for Variance Reduction
% BuyPolar Capital - Malliavin Variance Reduction Module (MATLAB)

%% Parameters
S0 = 100; K = 100; r = 0.05; sigma = 0.2; T = 1; N = 10000;
rng(42); Z = randn(N,1);
ST = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T)*Z);
payoff = max(ST - K, 0);
disc = exp(-r*T);

%% Standard MC Estimation
price_mc = disc * mean(payoff);
se_mc = disc * std(payoff) / sqrt(N);

%% Malliavin Control Variate (Delta weight)
weight = Z / (S0 * sigma * sqrt(T));
delta_pathwise = payoff .* weight;

% Use Malliavin Delta as control variate
cov_py_w = cov(payoff, delta_pathwise);
beta = cov_py_w(1,2) / var(delta_pathwise);

payoff_cv = payoff - beta * (delta_pathwise - mean(delta_pathwise));
price_cv = disc * mean(payoff_cv);
se_cv = disc * std(payoff_cv) / sqrt(N);

%% Output
fprintf('Standard MC: %.4f ± %.4f\n', price_mc, 1.96*se_mc);
fprintf('Malliavin CV: %.4f ± %.4f\n', price_cv, 1.96*se_cv);

%% Plot variance comparison
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
bar(categorical({'Standard MC','Malliavin CV'}), [se_mc se_cv]);
title('Standard Error Comparison'); ylabel('Standard Error');

print(gcf, fullfile('plots','malliavin_variance_reduction'), '-dpdf');

disp('Malliavin control variate variance reduction complete.');
