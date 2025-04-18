% chaos_expansion_option.m
% Approximate European call option price using Wiener–Itô chaos expansion
% without requiring the Symbolic Math Toolbox.

% Parameters
S0 = 100; K = 105; r = 0.05; sigma = 0.2; T = 1;
N_terms = 10;
n_sim = 100000;

% Simulate Brownian motion and asset price
Z = randn(n_sim,1);
W_T = sqrt(T) * Z;
S_T = S0 * exp((r - 0.5 * sigma^2) * T + sigma * W_T);
payoff = max(S_T - K, 0);
bs_price = exp(-r * T) * mean(payoff);

% Convert S_T to standard Gaussian input x for Hermite basis
theta = (log(S_T / S0) - (r - 0.5 * sigma^2) * T) / sigma;
x = theta / sqrt(T);

% Function to compute Hermite polynomials using recursion
function H = hermite_poly(n, x)
    if n == 0
        H = ones(size(x));
    elseif n == 1
        H = 2 * x;
    else
        H = 2 * x .* hermite_poly(n-1, x) - 2 * (n-1) * hermite_poly(n-2, x);
    end
end

% Approximate chaos expansion of payoff
chaos_estimates = zeros(N_terms,1);
for n = 1:N_terms
    coeffs = zeros(n,1);
    for i = 1:n
        H_i = hermite_poly(i-1, x);
        coeffs(i) = mean(payoff .* H_i) / factorial(i-1);
    end
    approx = zeros(n_sim,1);
    for i = 1:n
        H_i = hermite_poly(i-1, x);
        approx = approx + coeffs(i) .* H_i;
    end
    chaos_estimates(n) = exp(-r * T) * mean(approx);
end

% Plot convergence
figure('Units','inches','Position',[0, 0, 6, 4.2]);
plot(1:N_terms, chaos_estimates, 'o-', 'LineWidth', 1.2, 'DisplayName', 'Chaos Est.')
hold on
yline(bs_price, '--r', 'LineWidth', 1.5, 'DisplayName', 'Black-Scholes')
xlabel('Number of Hermite Terms (N)', 'FontSize', 10)
ylabel('Estimated Option Price', 'FontSize', 10)
title('Chaos Expansion: Convergence to Black-Scholes Price', 'FontSize', 12)
legend('Location', 'best', 'Box', 'off')
grid on
box off
set(gca, 'FontName', 'Helvetica', 'FontSize', 10, 'LineWidth', 1.2)

% Export plot
set(gcf, 'PaperPositionMode', 'auto');
if ~exist('plots', 'dir')
    mkdir('plots');
end
print(gcf, 'plots/chaos_expansion_option', '-dpdf', '-painters', '-r300');
