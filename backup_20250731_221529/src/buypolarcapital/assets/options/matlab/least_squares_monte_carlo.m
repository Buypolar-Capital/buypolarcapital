% American Option Pricing using Least Squares Monte Carlo (LSM)
% BuyPolar Capital - American Options Module (MATLAB)

%% Parameters
S0 = 100;      % initial price
K = 100;       % strike
r = 0.05;      % risk-free rate
sigma = 0.2;   % volatility
T = 1;         % maturity in years
M = 50;        % time steps
N = 10000;     % number of paths
dt = T / M;

%% Simulate price paths
rng(42);
S = zeros(N, M+1);
S(:,1) = S0;

for t = 2:M+1
    dW = sqrt(dt) * randn(N,1);
    S(:,t) = S(:,t-1) .* exp((r - 0.5*sigma^2)*dt + sigma*dW);
end

%% Payoff matrix
h = max(K - S, 0);  % American PUT

V = h(:,end);  % terminal payoff

%% Backward induction
for t = M:-1:2
    itm = find(h(:,t) > 0);  % in-the-money paths
    X = S(itm,t);
    Y = V(itm) .* exp(-r*dt);  % discounted future value

    % Regression: continuation value ~ basis functions
    A = [ones(size(X)) X X.^2];
    coeff = A \ Y;

    continuation = A * coeff;

    exercise = h(itm,t) > continuation;

    V(itm(exercise)) = h(itm(exercise), t);
    V(itm(~exercise)) = V(itm(~exercise)) * exp(-r*dt);
end

% Discount back to today
price = mean(V) * exp(-r*dt);
fprintf('Estimated American PUT price (LSM): %.4f\n', price);

%% Plot sample paths and early exercise boundary
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
plot(1:M+1, S(1:30,:)', 'Color', [0.6 0.6 0.6]); hold on;
yline(K, '--r', 'Strike');
title('Sample Price Paths for American Put'); xlabel('Time Step'); ylabel('Price');
print(gcf, fullfile('plots','american_option_lsm'), '-dpdf');
