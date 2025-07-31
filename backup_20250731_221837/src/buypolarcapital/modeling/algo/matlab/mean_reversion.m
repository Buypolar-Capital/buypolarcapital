% Mean Reversion Signal Classifier (No Toolboxes)
% BuyPolar Capital - Machine Learning Module (MATLAB)

%% Simulate synthetic mean-reverting time series
n = 500;
k = 0.1;               % speed of mean reversion
sigma = 0.5;
mu = 100;             % long-term mean
rng(42);

X = zeros(n,1);
X(1) = mu + sigma*randn;
for t = 2:n
    X(t) = X(t-1) + k*(mu - X(t-1)) + sigma*randn;
end

%% Generate lag features and labels
lags = 5;
X_lagged = zeros(n-lags, lags);
for i = 1:lags
    X_lagged(:,i) = X(lags-i+1:end-i);
end

dY = sign(X(lags+1:end) - X(lags:end-1)); % +1 = up, -1 = down
labels = (dY > 0); % binary classification

%% Split into train/test
split = round(0.7*size(X_lagged,1));
X_train = X_lagged(1:split,:);
y_train = labels(1:split);
X_test = X_lagged(split+1:end,:);
y_test = labels(split+1:end);

%% Simple classifier: logistic regression (manual implementation)
X_aug = [ones(size(X_train,1),1), X_train];
w = (X_aug' * X_aug) \ (X_aug' * y_train); % least squares approximation

X_test_aug = [ones(size(X_test,1),1), X_test];
y_pred_prob = 1 ./ (1 + exp(-X_test_aug * w));
y_pred = y_pred_prob > 0.5;

acc = mean(y_pred == y_test);

%% Plot prediction vs true
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
plot(lags+1:n, X(lags+1:end), 'k'); hold on;
plot(lags+1+split:n, X(lags+1+split:end), 'b');
scatter(find(y_pred==1)+lags+split, X(find(y_pred==1)+lags+split), 20, 'g', 'filled');
title(sprintf('Mean Reversion Classifier Predictions (Accuracy = %.2f%%)', acc*100));
xlabel('Time'); ylabel('Price');
legend('Full Series','Test Set','Predicted Up Moves');

print(gcf, fullfile('plots','mean_reversion_classifier'), '-dpdf');

disp('Mean reversion classifier simulation complete.');
