
% Regime-Switching Volatility Model (No Toolboxes)
% BuyPolar Capital - Volatility Module (MATLAB)

%% Simulate two regimes with different volatility
n = 1000;
sigma_low = 0.01;
sigma_high = 0.04;

regime = zeros(n,1);
state = 1; % start in low vol
rng(1);

for t = 2:n
    if state == 1 && rand < 0.01
        state = 2;
    elseif state == 2 && rand < 0.05
        state = 1;
    end
    regime(t) = state;
end

sigma_series = (regime == 1) * sigma_low + (regime == 2) * sigma_high;
returns = sigma_series .* randn(n,1);
price = 100 + cumsum(returns);

%% Rolling volatility estimate
window = 50;
vol_est = zeros(n,1);
for t = window+1:n
    vol_est(t) = std(returns(t-window:t));
end

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
subplot(3,1,1);
plot(price);
title('Simulated Price Path with Regime-Switching Volatility'); ylabel('Price');

subplot(3,1,2);
plot(returns);
title('Returns'); ylabel('Return');

subplot(3,1,3);
plot(vol_est, 'b'); hold on;
plot(find(regime==2), vol_est(regime==2), 'r.');
title('Rolling Volatility Estimate with Regime Overlay'); ylabel('Volatility');
xlabel('Time');

print(gcf, fullfile('plots','regime_switching_volatility'), '-dpdf');

disp('Regime-switching volatility simulation complete.');
