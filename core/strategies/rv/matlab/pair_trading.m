
% Pair Trading Strategy (Relative Value Arbitrage)
% BuyPolar Capital - Starter MATLAB Script

%% Setup
rng(42); % for reproducibility
n = 500; % number of time steps

% Generate synthetic price series
t = (1:n)';
P1 = cumsum(randn(n,1) * 0.5 + 0.1); % trending series
P2 = P1 + randn(n,1) * 1.0;          % noisy version of P1

%% Compute spread and z-score
spread = P1 - P2;
spread_mean = movmean(spread, 50);
spread_std  = movstd(spread, 50);
zscore = (spread - spread_mean) ./ spread_std;

%% Generate trading signals
entry_threshold = 1;
exit_threshold  = 0;

positions = zeros(n,1);
for i = 2:n
    if zscore(i-1) > entry_threshold
        positions(i) = -1; % short spread: short P1, long P2
    elseif zscore(i-1) < -entry_threshold
        positions(i) = 1;  % long spread: long P1, short P2
    elseif abs(zscore(i-1)) < exit_threshold
        positions(i) = 0;  % exit
    else
        positions(i) = positions(i-1); % hold
    end
end

%% Compute PnL
ret1 = [0; diff(P1)];
ret2 = [0; diff(P2)];
spread_ret = positions .* (ret1 - ret2);
cum_pnl = cumsum(spread_ret);

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
subplot(3,1,1);
plot(t, P1, t, P2);
title('Synthetic Prices');
legend('P1','P2');

subplot(3,1,2);
plot(t, zscore);
hold on; yline(entry_threshold,'--r'); yline(-entry_threshold,'--r');
title('Z-score of Spread');

subplot(3,1,3);
plot(t, cum_pnl);
title('Cumulative PnL'); xlabel('Time');

saveas(gcf, fullfile('plots','pair_trading_demo.pdf'));

%% Done
disp('Pair trading strategy simulation complete. Plot saved.');
