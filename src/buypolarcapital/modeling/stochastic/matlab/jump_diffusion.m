% Jump Diffusion Simulation (Merton Model - No Toolboxes)
% BuyPolar Capital - Jump Risk Module (MATLAB)

%% Parameters
S0 = 100; K = 100; r = 0.05; sigma = 0.2;
lambda = 0.5; muJ = -0.1; sigmaJ = 0.3; % jump intensity, mean, std
T = 1; Nsim = 10000;

%% Simulate number of jumps using inverse transform sampling
rng(42);
U = rand(Nsim,1);
N_jump = floor(-log(1 - U) / lambda); % Poisson approx

% Simulate jump sizes (lognormal jumps)
Y_jump = muJ + sigmaJ * randn(Nsim,1);
J_total = N_jump .* Y_jump;

% Simulate Brownian part
Z = randn(Nsim,1);
ST = S0 .* exp((r - 0.5*sigma^2 - lambda*(exp(muJ + 0.5*sigmaJ^2)-1))*T + sigma*sqrt(T).*Z + J_total);

% European Call
payoff = max(ST - K, 0);
price = exp(-r*T) * mean(payoff);

%% Output
fprintf('Jump Diffusion Call Price (Merton model): %.4f\n', price);

%% Plot sample histogram
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
histogram(ST, 100, 'Normalization','pdf');
xline(K, '--r', 'Strike');
title('Jump Diffusion Terminal Price Distribution');
xlabel('Price'); ylabel('Density');

print(gcf, fullfile('plots','jump_diffusion_simulation'), '-dpdf');

disp('Jump diffusion simulation complete.');s