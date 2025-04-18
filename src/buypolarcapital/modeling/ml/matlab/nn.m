% Feedforward Neural Network Classification (Manual 1 Hidden Layer)
% BuyPolar Capital - Classical ML Series (MATLAB)

%% Simulate 2D classification data (nonlinear)
rng(8);
N = 200;
t = linspace(0, 2*pi, N)';
X1 = [cos(t), sin(t)] + 0.1*randn(N,2);
X2 = [cos(t)+1.5, sin(t)] + 0.1*randn(N,2);
X = [X1; X2];
y = [zeros(N,1); ones(N,1)];

%% Normalize data
X = (X - mean(X)) ./ std(X);

%% NN architecture
n_input = 2;
n_hidden = 10;
n_output = 1;

% Xavier init
W1 = randn(n_input, n_hidden) / sqrt(n_input);
b1 = zeros(1, n_hidden);
W2 = randn(n_hidden, n_output) / sqrt(n_hidden);
b2 = 0;

%% Activation functions
sigmoid = @(z) 1 ./ (1 + exp(-z));
dsigmoid = @(z) sigmoid(z) .* (1 - sigmoid(z));

%% Training
X_train = X;
y_train = y;
L = 1e-2; % learning rate

for epoch = 1:3000
    % Forward
    Z1 = X_train * W1 + b1;
    A1 = sigmoid(Z1);
    Z2 = A1 * W2 + b2;
    A2 = sigmoid(Z2);

    % Backprop
    dZ2 = A2 - y_train;
    dW2 = A1' * dZ2;
db2 = sum(dZ2);
    dA1 = dZ2 * W2';
    dZ1 = dA1 .* dsigmoid(Z1);
    dW1 = X_train' * dZ1;
    db1 = sum(dZ1);

    % Gradient step
    W1 = W1 - L * dW1;
    b1 = b1 - L * db1;
    W2 = W2 - L * dW2;
    b2 = b2 - L * db2;
end

%% Prediction grid
[x1g, x2g] = meshgrid(linspace(min(X(:,1)),max(X(:,1)),100), linspace(min(X(:,2)),max(X(:,2)),100));
Xg = [x1g(:), x2g(:)];
Z1g = Xg * W1 + b1;
A1g = sigmoid(Z1g);
Z2g = A1g * W2 + b2;
A2g = sigmoid(Z2g);

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
contourf(x1g, x2g, reshape(A2g, size(x1g)), [0 0.5 1], 'LineColor','none'); hold on;
scatter(X1(:,1), X1(:,2), 15, 'b', 'filled');
scatter(X2(:,1), X2(:,2), 15, 'r', 'filled');
title('Manual Feedforward Neural Net Classification');
xlabel('Feature 1'); ylabel('Feature 2');
legend('Decision Region','Class 0','Class 1'); grid on;

print(gcf, fullfile('plots','neural_net_classification'), '-dpdf');

disp('Neural network classification complete.');