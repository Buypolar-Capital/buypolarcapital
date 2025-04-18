% kalman_price_filter.m
% Simple Kalman filter on noisy price observations

n = 100;
true_price = cumsum(randn(n,1));               % Hidden state (e.g. real price)
observed_price = true_price + randn(n,1)*2;     % Observed with noise

% Kalman filter setup
x_hat = zeros(n,1);      % state estimate
P = zeros(n,1);          % estimation error
Q = 1;                   % process noise covariance
R = 4;                   % measurement noise covariance

x_hat(1) = observed_price(1);
P(1) = 1;

for t = 2:n
    % Predict
    x_pred = x_hat(t-1);
    P_pred = P(t-1) + Q;

    % Update
    K = P_pred / (P_pred + R);
    x_hat(t) = x_pred + K * (observed_price(t) - x_pred);
    P(t) = (1 - K) * P_pred;
end

% Plot
figure('Position', [100, 100, 800, 500]);
plot(true_price, '-', 'LineWidth', 1.5, 'DisplayName', 'True Price')
hold on
plot(observed_price, '.', 'DisplayName', 'Observed Price', 'Color', [0.6 0.6 0.6])
plot(x_hat, '-', 'LineWidth', 2, 'DisplayName', 'Kalman Estimate')
xlabel('Time', 'FontSize', 12)
ylabel('Price', 'FontSize', 12)
title('Kalman Filter: True vs Observed vs Estimated', 'FontSize', 14)
legend('Location', 'best')
grid on
set(gca, 'FontName', 'Helvetica', 'FontSize', 11)

% Save to PDF
if ~exist('plots', 'dir')
    mkdir('plots');
end
print('plots/kalman_price_filter', '-dpdf', '-bestfit');
