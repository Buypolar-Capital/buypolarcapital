% PDE-Based Option Pricing (Explicit Finite Difference Method)
% BuyPolar Capital - Numerical Methods Module (MATLAB)

%% Parameters
Smax = 200;    % max stock price
K = 100;       % strike
T = 1;         % time to maturity
r = 0.05;      % risk-free rate
sigma = 0.2;   % volatility

M = 200;       % number of price steps
N = 500;       % number of time steps

%% Discretization
dS = Smax / M;
dt = T / N;
S = linspace(0, Smax, M+1)';

% Initialize option value grid
V = zeros(M+1, N+1);

% Terminal condition (European Call)
V(:,end) = max(S - K, 0);

%% Explicit finite difference coefficients
for j = N:-1:1
    for i = 2:M
        delta = (V(i+1,j+1) - V(i-1,j+1)) / (2*dS);
        gamma = (V(i+1,j+1) - 2*V(i,j+1) + V(i-1,j+1)) / (dS^2);
        V(i,j) = V(i,j+1) + dt * (0.5*sigma^2*S(i)^2*gamma + r*S(i)*delta - r*V(i,j+1));
    end
    % Boundary conditions
    V(1,j) = 0;
    V(end,j) = Smax - K * exp(-r * (T - (j-1)*dt));
end

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
plot(S, V(:,1), 'b-', 'LineWidth', 2); hold on;
plot(S, max(S - K, 0), 'r--');
title('European Call Option via Explicit FDM');
xlabel('Stock Price'); ylabel('Option Value');
legend('Numerical Solution', 'Payoff'); grid on;

print(gcf, fullfile('plots','pde_option_pricing'), '-dpdf');

disp('PDE-based option pricing complete.');
