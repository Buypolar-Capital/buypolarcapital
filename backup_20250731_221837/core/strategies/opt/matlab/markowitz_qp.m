% Markowitz Efficient Frontier (No Toolboxes Required)
% BuyPolar Capital - Optimization Module (MATLAB)

%% Parameters
n_assets = 6;
n_samples = 1000;
n_portfolios = 5000;
rng(1);

% Simulate expected returns and cov matrix
mu = 0.08 + 0.05*rand(n_assets,1);        % expected returns
Sigma = randn(n_assets);
Sigma = Sigma'*Sigma;                     % pos-def cov matrix

%% Generate random portfolios
weights_all = rand(n_portfolios, n_assets);
weights_all = weights_all ./ sum(weights_all, 2);  % normalize to sum to 1

returns = weights_all * mu;
risk = sqrt(sum((weights_all * Sigma) .* weights_all, 2));
rf = 0.01;
sharpe = (returns - rf) ./ risk;

%% Get efficient frontier (top 100 Sharpe ratios)
[~, idx] = maxk(sharpe, 100);
returns_frontier = returns(idx);
risk_frontier = risk(idx);
sharpe_frontier = sharpe(idx);

[~, idx_max] = max(sharpe_frontier);

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
scatter(risk, returns, 10, [0.7 0.7 0.7], 'filled'); hold on;
plot(risk_frontier, returns_frontier, 'b-', 'LineWidth', 2);
plot(risk_frontier(idx_max), returns_frontier(idx_max), 'ro', 'MarkerSize', 8, 'LineWidth', 2);
title('Markowitz Efficient Frontier (No Toolboxes)');
xlabel('Portfolio Risk (Std Dev)'); ylabel('Expected Return');
legend('Random Portfolios', 'Efficient Frontier', 'Max Sharpe', 'Location', 'SouthEast');
grid on;

print(gcf, fullfile('plots','markowitz_qp_frontier'), '-dpdf');

disp('Efficient frontier plotted and saved.');
