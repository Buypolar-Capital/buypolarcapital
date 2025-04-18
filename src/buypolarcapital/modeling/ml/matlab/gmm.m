% Gaussian Mixture Model (GMM) Clustering (Manual EM)
% BuyPolar Capital - Classical ML Series (MATLAB)

%% Simulate 2D Gaussian clusters
rng(7);
N = 150;
X1 = randn(N,2) + [2 2];
X2 = randn(N,2) + [6 6];
X = [X1; X2];

%% Init EM params
K = 2;
[N, d] = size(X);
mu = X(randperm(N,K), :);
sigma = repmat(eye(d), [1,1,K]);
pi_k = ones(1,K) / K;
gamma = zeros(N,K);

max_iter = 50;

for iter = 1:max_iter
    % E-step: responsibilities
    for k = 1:K
        diff = X - mu(k,:);
        inv_sigma = inv(sigma(:,:,k));
        det_sigma = det(sigma(:,:,k));
        norm_factor = 1 / ((2*pi)^(d/2) * sqrt(det_sigma));
        exponent = sum((diff * inv_sigma) .* diff, 2);
        gamma(:,k) = pi_k(k) * norm_factor * exp(-0.5 * exponent);
    end
    gamma = gamma ./ sum(gamma, 2);

    % M-step: update parameters
    Nk = sum(gamma);
    for k = 1:K
        mu(k,:) = sum(gamma(:,k) .* X) / Nk(k);
        diff = X - mu(k,:);
        sigma(:,:,k) = (diff' * (diff .* gamma(:,k))) / Nk(k);
        pi_k(k) = Nk(k) / N;
    end
end

[~, y_pred] = max(gamma, [], 2);

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
scatter(X(:,1), X(:,2), 20, y_pred, 'filled');
title('GMM Clustering via EM');
xlabel('Feature 1'); ylabel('Feature 2'); grid on;

print(gcf, fullfile('plots','gmm_clustering'), '-dpdf');

disp('GMM clustering complete.');