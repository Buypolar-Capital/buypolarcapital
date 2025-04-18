% yield_curve_pca.m
% PCA on synthetic yield curve data

% Simulate yield curve data (250 days x 10 maturities)
n_obs = 250;
maturities = [0.25 0.5 1 2 3 5 7 10 20 30];
n_maturities = length(maturities);

% Simulate latent factors: level, slope, curvature
level = randn(n_obs,1) * 0.5 + 2.0;
slope = randn(n_obs,1) * 0.2;
curv = randn(n_obs,1) * 0.1;

yield_data = zeros(n_obs, n_maturities);
for i = 1:n_maturities
    tau = maturities(i);
    yield_data(:,i) = level + slope .* exp(-tau/2) + curv .* (exp(-tau) - exp(-2*tau));
end

% PCA
% Manually center the data
Y = yield_data - mean(yield_data);

% PCA via SVD
[U, S, V] = svd(Y, 'econ');
coeff = V;              % Loadings (principal components)
score = U * S;          % Scores (projections)
latent = diag(S).^2;    % Variance explained

% Plot first 3 principal components (loadings)
figure('Units','inches','Position',[0, 0, 6, 4.2]);
plot(maturities, coeff(:,1:3), 'LineWidth', 1.5)
xlabel('Maturity (Years)', 'FontSize', 10)
ylabel('Loading', 'FontSize', 10)
title('PCA of Yield Curve: First 3 Principal Components', 'FontSize', 12, 'FontWeight', 'normal')
legend({'PC1 (Level)', 'PC2 (Slope)', 'PC3 (Curvature)'}, 'Location', 'best', 'Box', 'off')
grid on
box off
set(gca, 'FontName', 'Helvetica', 'FontSize', 10, 'LineWidth', 1.2)

% Save to PDF
set(gcf, 'PaperPositionMode', 'auto');
if ~exist('plots', 'dir')
    mkdir('plots');
end
print(gcf, 'plots/yield_curve_pca', '-dpdf', '-painters', '-r300');
