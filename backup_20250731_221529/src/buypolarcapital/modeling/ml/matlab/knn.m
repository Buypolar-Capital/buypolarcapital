% K-Nearest Neighbors (KNN) Classification
% BuyPolar Capital - Classical ML Series (MATLAB)

%% Simulate 2D classification data
rng(3);
N = 200;
X1 = randn(N,2) + [1,1];
X2 = randn(N,2) + [3,3];
X = [X1; X2];
y = [zeros(N,1); ones(N,1)];

%% Create mesh grid for prediction
grid_x = linspace(min(X(:,1))-1, max(X(:,1))+1, 100);
grid_y = linspace(min(X(:,2))-1, max(X(:,2))+1, 100);
[x1g, x2g] = meshgrid(grid_x, grid_y);
Xg = [x1g(:), x2g(:)];

%% Simple KNN implementation (k = 5)
k = 5;
yg = zeros(size(Xg,1),1);

for i = 1:size(Xg,1)
    dists = sum((X - Xg(i,:)).^2, 2);
    [~, idx] = sort(dists);
    neighbors = y(idx(1:k));
    yg(i) = round(mean(neighbors));
end

%% Plot results
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
contourf(x1g, x2g, reshape(yg, size(x1g)), 'LineColor','none'); hold on;
scatter(X1(:,1), X1(:,2), 20, 'b', 'filled');
scatter(X2(:,1), X2(:,2), 20, 'r', 'filled');
title(sprintf('KNN Classification (k = %d)', k));
xlabel('Feature 1'); ylabel('Feature 2'); legend('Decision Region', 'Class 0', 'Class 1');

print(gcf, fullfile('plots','knn_classification'), '-dpdf');

disp('KNN classification complete.');
