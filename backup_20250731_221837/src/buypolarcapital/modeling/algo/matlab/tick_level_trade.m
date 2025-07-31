% Tick-Level Trade Execution Simulator (No Toolboxes)
% BuyPolar Capital - Execution Module (MATLAB)

%% Simulate tick-level price and volume
n_ticks = 1000;
price = cumsum(0.01 * randn(n_ticks, 1)) + 100; % tick price path
volume = randi([50, 200], n_ticks, 1);           % volume per tick

%% Define parent order
parent_volume = 10000;
child_volume = 500; % per slice

executed_volume = 0;
avg_price = 0;

execution_log = [];

%% Simulate execution over ticks
for t = 1:n_ticks
    if executed_volume >= parent_volume
        break;
    end

    trade_size = min(child_volume, parent_volume - executed_volume);
    slip = 0.0002 * (trade_size / volume(t)); % simple impact model
    exec_price = price(t) * (1 + slip);

    execution_log = [execution_log; t, exec_price, trade_size];
    avg_price = (avg_price * executed_volume + exec_price * trade_size) / (executed_volume + trade_size);
    executed_volume = executed_volume + trade_size;
end

%% Plot execution path
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
plot(price, 'k'); hold on;
scatter(execution_log(:,1), execution_log(:,2), 20, 'r', 'filled');
title('Tick-Level Execution Path');
xlabel('Tick'); ylabel('Price');
legend('Market Price', 'Execution Price');

print(gcf, fullfile('plots','tick_execution_simulator'), '-dpdf');

fprintf('Executed %.0f/%0.f units. Avg execution price: %.4f\n', executed_volume, parent_volume, avg_price);
disp('Tick-level execution simulation complete.');
