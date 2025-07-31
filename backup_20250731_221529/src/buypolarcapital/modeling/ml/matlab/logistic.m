% Logistic Regression Classification Demo
% BuyPolar Capital - Classical ML Series (MATLAB)

%% Simulate 2D classification data
rng(1);
N = 200;
X1 = randn(N,2) + [1,1];
X2 = randn(N,2) + [3,3];
X = [X1; X2];
y = [zeros(N,1); ones(N,1)];

%% Add intercept term
X_aug = [ones(size(X,1),1), X];

%% Fit logistic regression (closed form using IRLS - basic Newton-Raphson)
w = zeros(size(X_aug,2),1);
for iter = 1:10
    p = 1 ./ (1 + exp(-X_aug*w));
    W = diag(p .* (1 - p));
    z = X_aug*w + W\(y - p);
    w = (X_aug' * W * X_aug) \ (X_aug' * W * z);
end

%% Grid for decision boundary
[x1g,x2g] = meshgrid(linspace(min(X(:,1))-1,max(X(:,1))+1,100), linspace(min(X(:,2))-1,max(X(:,2))+1,100));
Xg = [ones(numel(x1g),1), x1g(:), x2g(:)];
pred_grid = reshape(1./(1 + exp(-Xg*w)), size(x1g));

%% Plot decision boundary
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
contourf(x1g,x2g,pred_grid,[0 0.5 1],'LineColor','none'); hold on;
scatter(X1(:,1), X1(:,2), 20, 'b', 'filled');
scatter(X2(:,1), X2(:,2), 20, 'r', 'filled');
title('Logistic Regression Classification');
xlabel('Feature 1'); ylabel('Feature 2'); legend('Decision Boundary','Class 0','Class 1');

print(gcf, fullfile('plots','logistic_regression_classification'), '-dpdf');

disp('Logistic regression classification complete.');
