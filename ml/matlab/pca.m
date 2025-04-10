% Principal Component Analysis (PCA) Demo
% BuyPolar Capital - Classical ML Series (MATLAB)

%% Simulate 2D Gaussian data with correlation
rng(6);
N = 300;
X = randn(N,2) * [2 1.5; 0 1] + [5 5];

%% Center the data
X_centered = X - mean(X);

%% Compute covariance and eigen decomposition
C = cov(X_centered);
[V, D] = eig(C);
[~, idx] = sort(diag(D), 'descend');
V = V(:,idx); % sort eigenvectors by descending eigenvalues

%% Project onto first PC
X_proj = X_centered * V(:,1);
X_recon = X_proj * V(:,1)' + mean(X);

%% Plot original data + principal components
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
scatter(X(:,1), X(:,2), 15, 'filled'); hold on;
quiver(mean(X(:,1)), mean(X(:,2)), V(1,1)*2, V(2,1)*2, 'r', 'LineWidth', 2);
quiver(mean(X(:,1)), mean(X(:,2)), V(1,2)*2, V(2,2)*2, 'g', 'LineWidth', 2);
title('PCA on Correlated 2D Data');
legend('Data', 'PC1', 'PC2');
xlabel('X_1'); ylabel('X_2'); axis equal;

print(gcf, fullfile('plots','pca_demo'), '-dpdf');

disp('PCA analysis complete.');
