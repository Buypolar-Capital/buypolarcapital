% Linear SVM (Mock Implementation via Max-Margin Classifier)
% BuyPolar Capital - Classical ML Series (MATLAB)

%% Simulate linearly separable 2D data
rng(5);
N = 200;
X1 = randn(N,2) + [1,1];
X2 = randn(N,2) + [4,4];
X = [X1; X2];
y = [ones(N,1); -ones(N,1)]; % SVM uses labels +1 and -1

%% Approximate SVM with hard-margin max-margin linear classifier
% We'll solve: min ||w|| s.t. y_i (w'x + b) >= 1 (simplified setup)

% Add bias term
X_aug = [X, ones(2*N,1)];

% Closed-form solution via pseudo-inverse (not real QP)
w = pinv(X_aug) * y;

% Decision function and boundary
w_vec = w(1:2); b = w(3);
pred = sign(X_aug * w);
acc = mean(pred == y);

%% Grid for boundary
[x1g,x2g] = meshgrid(linspace(min(X(:,1))-1,max(X(:,1))+1,100), linspace(min(X(:,2))-1,max(X(:,2))+1,100));
Xg = [x1g(:), x2g(:), ones(numel(x1g),1)];
pred_grid = reshape(sign(Xg * w), size(x1g));

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
contourf(x1g,x2g,pred_grid,'LineColor','none'); hold on;
scatter(X1(:,1), X1(:,2), 20, 'b', 'filled');
scatter(X2(:,1), X2(:,2), 20, 'r', 'filled');
title(sprintf('Mock Linear SVM Classification (Accuracy = %.2f%%)', acc*100));
xlabel('Feature 1'); ylabel('Feature 2'); legend('Decision Region','Class +1','Class -1');

print(gcf, fullfile('plots','svm_classification'), '-dpdf');

disp('Mock linear SVM classification complete.');