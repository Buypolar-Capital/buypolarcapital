% Linear Discriminant Analysis (LDA) Demo
% BuyPolar Capital - Classical ML Series (MATLAB)

%% Simulate 2D classification data
rng(2);
N = 200;
X1 = randn(N,2) + [1,1];
X2 = randn(N,2) + [3,3];
X = [X1; X2];
y = [zeros(N,1); ones(N,1)];

%% Compute class means and shared covariance
mu0 = mean(X1); mu1 = mean(X2);
Sigma = cov(X);
invSigma = inv(Sigma);

% Compute projection weights and threshold
w = invSigma * (mu1 - mu0)';
c = 0.5 * (mu0 + mu1) * w;

% Decision function
proj = X * w;
y_pred = proj > c;
acc = mean(y_pred == y);

%% Plot LDA decision boundary
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
scatter(X1(:,1), X1(:,2), 20, 'b', 'filled'); hold on;
scatter(X2(:,1), X2(:,2), 20, 'r', 'filled');

% Plot boundary line
xline = linspace(min(X(:,1)), max(X(:,1)), 100);
yline = (-w(1)*(xline - c/w(2)))/w(2);
plot(xline, yline, 'k--', 'LineWidth', 2);

title(sprintf('LDA Classification (Accuracy = %.2f%%)', acc*100));
xlabel('Feature 1'); ylabel('Feature 2');
legend('Class 0', 'Class 1', 'Decision Boundary'); grid on;

print(gcf, fullfile('plots','lda_classification'), '-dpdf');

disp('LDA classification complete.');
