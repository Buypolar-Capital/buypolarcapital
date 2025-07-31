% efficient_frontier.m
% BPC-style Efficient Frontier plot

rng(1); % reproducibility
mu = [0.1; 0.12; 0.14; 0.09];                    % expected returns
Sigma = [ 0.005 0.001 0.002 0.0015;
          0.001 0.010 0.0025 0.002;
          0.002 0.0025 0.015 0.002;
          0.0015 0.002 0.002 0.007];             % cov matrix

n_assets = length(mu);
N = 100;
w = zeros(n_assets, N);
ret = zeros(N,1);
risk = zeros(N,1);
sharpe = zeros(N,1);

for i = 1:N
    x = rand(n_assets,1);
    x = x / sum(x);                              % normalize
    w(:,i) = x;
    ret(i) = mu' * x;
    risk(i) = sqrt(x' * Sigma * x);
    sharpe(i) = ret(i) / risk(i);
end

[max_sharpe, idx_sharpe] = max(sharpe);
[min_risk, idx_risk] = min(risk);

% Plot
figure('Position', [100, 100, 800, 600]);
scatter(risk, ret, 30, sharpe, 'filled');
hold on
plot(risk(idx_sharpe), ret(idx_sharpe), 'ro', 'MarkerSize', 10, 'LineWidth', 2, 'DisplayName', 'Max Sharpe');
plot(risk(idx_risk), ret(idx_risk), 'go', 'MarkerSize', 10, 'LineWidth', 2, 'DisplayName', 'Min Variance');

xlabel('Risk (Std Dev)', 'FontSize', 12)
ylabel('Expected Return', 'FontSize', 12)
title('Efficient Frontier', 'FontSize', 14)
grid on
colorbar
colormap(parula)
legend('Location', 'southeast')
set(gca, 'FontName', 'Helvetica', 'FontSize', 11)

% Export with BPC styling
set(gcf, 'PaperPositionMode', 'auto')
if ~exist('plots', 'dir')
    mkdir('plots');
end
print(gcf, 'plots/efficient_frontier', '-dpdf', '-bestfit');
