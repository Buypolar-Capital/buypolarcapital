% Decision Tree Classification (Mock Implementation)
% BuyPolar Capital - Classical ML Series (MATLAB)

%% Simulate 2D data
rng(4);
N = 200;
X1 = randn(N,2) + [1,1];
X2 = randn(N,2) + [3,3];
X = [X1; X2];
y = [zeros(N,1); ones(N,1)];

%% Mock decision tree with axis-aligned split (no toolbox)
% We'll just split at the midpoint between means as a basic tree
split_dim = 1;
split_val = (mean(X1(:,split_dim)) + mean(X2(:,split_dim))) / 2;

% Predict on grid
[x1g,x2g] = meshgrid(linspace(min(X(:,1))-1,max(X(:,1))+1,100), linspace(min(X(:,2))-1,max(X(:,2))+1,100));
Xg = [x1g(:), x2g(:)];
yg = double(Xg(:,split_dim) > split_val);

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
contourf(x1g,x2g,reshape(yg,size(x1g)),'LineColor','none'); hold on;
scatter(X1(:,1), X1(:,2), 20, 'b', 'filled');
scatter(X2(:,1), X2(:,2), 20, 'r', 'filled');
plot([split_val split_val], ylim, '--k', 'LineWidth', 2);
title('Mock Decision Tree (Single Axis-Aligned Split)');
xlabel('Feature 1'); ylabel('Feature 2'); legend('Decision Region','Class 0','Class 1');

print(gcf, fullfile('plots','decision_tree_classification'), '-dpdf');

disp('Mock decision tree classification complete.');