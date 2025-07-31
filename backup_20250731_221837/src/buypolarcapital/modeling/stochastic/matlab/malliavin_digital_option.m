% Malliavin Delta Estimation for Digital Option
% BuyPolar Capital - Malliavin Module (Digital Payoff)

%% Parameters
S0 = 100; K = 100; r = 0.05; sigma = 0.2; T = 1; N = 10000;
rng(42); Z = randn(N,1);
ST = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T)*Z);
payoff = double(ST > K);
disc = exp(-r*T);

%% Finite Difference Delta
dS = 0.01 * S0;
ST_up = (S0 + dS) * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T)*Z);
payoff_up = double(ST_up > K);
price_fd = disc * mean(payoff);
price_fd_up = disc * mean(payoff_up);
delta_fd = (price_fd_up - price_fd) / dS;

%% Malliavin Delta for digital option
% Uses distributional identity: Delta = E[delta(ST-K) * dST/dS0]
% Approximate Dirac delta with narrow Gaussian

epsilon = 0.5;
delta_approx = exp(-(ST - K).^2 / (2 * epsilon^2)) / (sqrt(2*pi) * epsilon);
dST_dS0 = ST / S0;
delta_malliavin = disc * mean(delta_approx .* dST_dS0);

%% Output
fprintf('Digital Option Price: %.4f\n', price_fd);
fprintf('Delta (FD): %.4f\n', delta_fd);
fprintf('Delta (Malliavin Approx): %.4f\n', delta_malliavin);

%% Plot density vs delta approximation
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
histogram(ST, 100, 'Normalization','pdf'); hold on;
plot(ST, delta_approx, 'r.');
yline(K, '--k', 'Strike');
title('Dirac Approximation for Malliavin Delta (Digital Call)');
xlabel('Terminal Price'); ylabel('Density');

print(gcf, fullfile('plots','malliavin_delta_digital_option'), '-dpdf');

disp('Digital option Malliavin delta estimation complete.');