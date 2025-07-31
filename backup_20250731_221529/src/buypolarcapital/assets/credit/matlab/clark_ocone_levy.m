% clark_ocone_levy.m
% Simulate Clark–Ocone-like decomposition for a digital option under a jump process (no toolboxes)

%% Helper Functions
function N = my_poissonrnd(lambda, n)
    % Generate n Poisson random numbers with mean lambda using Knuth's algorithm
    N = zeros(n,1);
    L = exp(-lambda);
    for i = 1:n
        k = 0;
        p = 1;
        while p > L
            k = k + 1;
            p = p * rand;
        end
        N(i) = k - 1;
    end
end

function x = my_normrnd(mu, sigma, m, n)
    % Generate normal random numbers using Box-Muller
    u1 = rand(m, n);
    u2 = rand(m, n);
    z = sqrt(-2 * log(u1)) .* cos(2 * pi * u2);
    x = mu + sigma * z;
end

%% Parameters
lambda = 5;                 % Jump intensity
mu = 0.0;                   % Jump mean
sigma = 0.2;                % Jump std
S0 = 100;
K = 105;
r = 0.03;
T = 1;
n_sim = 100000;

%% Simulate Compound Poisson Jump Process
N = my_poissonrnd(lambda * T, n_sim);  % Jump counts

% Total jump sum for each path
total_jumps = zeros(n_sim,1);
for i = 1:n_sim
    if N(i) > 0
        total_jumps(i) = sum(my_normrnd(mu, sigma, N(i), 1));
    end
end

X_T = total_jumps;                 % Lévy process (pure jump)
S_T = S0 .* exp(X_T);              % Exponential Lévy model

%% Payoff and Pricing
F = double(S_T > K);                       % Digital payoff
price = exp(-r * T) * mean(F);             % True price

%% Malliavin Derivative via Finite Difference
eps = 0.01;
X_T_eps = X_T + eps;
S_T_eps = S0 .* exp(X_T_eps);
F_eps = double(S_T_eps > K);
D_F = (F_eps - F) / eps;

%% Clark–Ocone Approximation
hedge_integrand = mean(D_F); 
replicated = exp(-r * T) * hedge_integrand * lambda * T;

%% Plotting
figure('Units','inches','Position',[0, 0, 6, 4.2]);
bar([price replicated])
set(gca, 'XTickLabel', {'True Price', 'Clark-Ocone Approx'}, 'FontSize', 10)
ylabel('Value', 'FontSize', 10)
title('Clark–Ocone Replication of Digital Option (Jump Process)', 'FontSize', 12)
grid on
box off
set(gca, 'FontName', 'Helvetica', 'FontSize', 10, 'LineWidth', 1.2)

%% Export to PDF
set(gcf, 'PaperPositionMode', 'auto');
if ~exist('plots', 'dir')
    mkdir('plots');
end
print(gcf, 'plots/clark_ocone_levy', '-dpdf', '-painters', '-r300');
