% VWAP Execution Simulation (No Toolboxes)
% BuyPolar Capital - Execution Module (MATLAB)

%% Parameters
n = 100;                   % number of time intervals
total_volume = 1e6;        % total volume to execute
price_start = 100;
volatility = 0.01;

rng(1);

%% Simulate price and market volume profile
time = (1:n)';
price = price_start + cumsum(volatility * randn(n,1));
market_volume = round(1e4 * (1 + sin(2*pi*time/n) + 0.1*randn(n,1))); % bell-shaped profile
market_volume(market_volume < 0) = 1000;

%% Compute target VWAP schedule
vwap_weights = market_volume / sum(market_volume);
vwap_target = vwap_weights * total_volume;
vwap_cum = cumsum(vwap_target);

%% Simulate execution with slippage model
actual_exec = zeros(n,1);
exec_price = zeros(n,1);
slippage_rate = 0.02; % percent of price impact per volume share

for i = 1:n
    trade_vol = vwap_target(i);
    slip = slippage_rate * (trade_vol / market_volume(i));
    exec_price(i) = price(i) * (1 + slip);
    actual_exec(i) = trade_vol;
end

avg_exec_price = sum(exec_price .* actual_exec) / sum(actual_exec);
vwap_market = sum(price .* market_volume) / sum(market_volume);

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
subplot(3,1,1);
plot(time, price);
title('Simulated Price Path'); ylabel('Price');

subplot(3,1,2);
bar(time, market_volume);
title('Market Volume Profile'); ylabel('Volume');

subplot(3,1,3);
plot(time, cumsum(actual_exec), 'b-', 'LineWidth', 2); hold on;
plot(time, vwap_cum, 'r--');
title('VWAP Execution vs Target'); ylabel('Cumulative Volume'); legend('Executed', 'Target');

print(gcf, fullfile('plots','vwap_execution_simulation'), '-dpdf');

fprintf('VWAP Market Price: %.4f\n', vwap_market);
fprintf('Average Execution Price: %.4f\n', avg_exec_price);

disp('VWAP execution simulation complete.');
