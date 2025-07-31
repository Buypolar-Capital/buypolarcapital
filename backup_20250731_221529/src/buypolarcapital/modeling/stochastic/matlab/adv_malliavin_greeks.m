% Malliavin Calculus Module (Extended)
% BuyPolar Capital - Advanced Malliavin Greeks (MATLAB)

%% Parameters
S0 = 100; K = 100; r = 0.05; sigma = 0.2; T = 1; N = 10000;
rng(42); Z = randn(N,1);
ST = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T)*Z);
payoff = max(ST - K, 0); disc = exp(-r*T);

%% Delta (recap)
weight_delta = Z / (S0 * sigma * sqrt(T));
delta_malliavin = disc * mean(payoff .* weight_delta);

%% Vega (∂Price/∂sigma)
term1 = Z.^2 - 1;
weight_vega = (Z .* term1) / sigma;
vega_malliavin = disc * mean(payoff .* weight_vega / sqrt(T));

%% Gamma (∂²Price/∂S₀²)
term2 = (Z.^2 - 1) ./ (S0^2 * sigma^2 * T);
gamma_malliavin = disc * mean(payoff .* term2);

%% Rho (∂Price/∂r)
weight_rho = T;
rho_malliavin = disc * mean(payoff .* weight_rho);

%% Theta (∂Price/∂T) - Approximate with d/dT of expectation
dT = 1e-3;
ZT2 = randn(N,1);
ST2 = S0 * exp((r - 0.5*sigma^2)*(T+dT) + sigma*sqrt(T+dT)*ZT2);
payoff2 = max(ST2 - K, 0);
price2 = exp(-r*(T+dT)) * mean(payoff2);
price1 = disc * mean(payoff);
theta_fd = (price2 - price1) / dT;

%% Display all
fprintf('Delta (Malliavin): %.4f\n', delta_malliavin);
fprintf('Vega (Malliavin): %.4f\n', vega_malliavin);
fprintf('Gamma (Malliavin): %.4f\n', gamma_malliavin);
fprintf('Rho (Malliavin): %.4f\n', rho_malliavin);
fprintf('Theta (FD approx): %.4f\n', theta_fd);

%% Plot all Greeks as bar chart
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
bars = bar(categorical({'Delta','Vega','Gamma','Rho','Theta'}), ...
           [delta_malliavin, vega_malliavin, gamma_malliavin, rho_malliavin, theta_fd]);
title('Malliavin-Based Greeks (European Call)'); ylabel('Sensitivity');

print(gcf, fullfile('plots','malliavin_greeks_all')), '-dpdf';

disp('Full Malliavin Greeks module complete.');