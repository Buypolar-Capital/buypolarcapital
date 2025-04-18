% Malliavin Delta Estimation for Barrier Option
% BuyPolar Capital - Malliavin Module (Barrier Payoff)

%% Parameters
S0 = 100; K = 100; B = 120; r = 0.05; sigma = 0.2;
T = 1; N = 10000; M = 252; dt = T/M;

%% Simulate paths and barriers
rng(42);
Z = randn(N,M);
S = zeros(N,M+1); S(:,1) = S0;

for t = 2:M+1
    S(:,t) = S(:,t-1) .* exp((r - 0.5*sigma^2)*dt + sigma*sqrt(dt).*Z(:,t-1));
end

hit = max(S,[],2) >= B; % barrier hit
ST = S(:,end);
payoff = max(ST - K, 0) .* (~hit);
disc = exp(-r*T);

%% Finite Difference Delta
dS = 0.01 * S0;
S_fd = zeros(N,M+1); S_fd(:,1) = S0 + dS;

for t = 2:M+1
    S_fd(:,t) = S_fd(:,t-1) .* exp((r - 0.5*sigma^2)*dt + sigma*sqrt(dt).*Z(:,t-1));
end

hit_fd = max(S_fd,[],2) >= B;
ST_fd = S_fd(:,end);
payoff_fd = max(ST_fd - K, 0) .* (~hit_fd);
price = disc * mean(payoff);
price_fd = disc * mean(payoff_fd);
delta_fd = (price_fd - price) / dS;

%% Malliavin Delta (approximate)
Z1 = sum(Z,2) / sqrt(M); % approximate single draw from sum
ST_mall = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T).*Z1);
barrier_mask = max(S,[],2) < B;
weight = Z1 ./ (S0 * sigma * sqrt(T));
delta_malliavin = disc * mean(max(ST_mall - K,0) .* weight .* barrier_mask);

%% Output
fprintf('Barrier Option Price: %.4f\n', price);
fprintf('Delta (FD): %.4f\n', delta_fd);
fprintf('Delta (Malliavin Approx): %.4f\n', delta_malliavin);

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
plot(1:M+1, S(1:20,:)'); hold on;
yline(B, '--r', 'Barrier');
title('Sample Barrier Option Paths'); xlabel('Time Step'); ylabel('Price');

print(gcf, fullfile('plots','malliavin_delta_barrier_option'), '-dpdf');

disp('Barrier option Malliavin delta estimation complete.');
