% nelson_siegel_fit.m
% Simple Nelson-Siegel yield curve fit with PDF output

% Sample data
maturities = [0.25 0.5 1 2 3 5 7 10 20 30];
yields = [0.5 0.6 0.8 1.0 1.2 1.5 1.8 2.0 2.3 2.4];

% Initial guess: [beta0, beta1, beta2, tau]
params0 = [2, -1, 1, 1];

% Nelson-Siegel function
ns_fun = @(p, t) p(1) + ...
    p(2) .* (1 - exp(-t./p(4))) ./ (t./p(4)) + ...
    p(3) .* ((1 - exp(-t./p(4))) ./ (t./p(4)) - exp(-t./p(4)));

% Loss function
loss_fun = @(p) sum((ns_fun(p, maturities) - yields).^2);
opt_params = fminsearch(loss_fun, params0);

% Plot
t_fit = linspace(0.1, 30, 200);
y_fit = ns_fun(opt_params, t_fit);

figure('Position', [100, 100, 800, 500]);
plot(maturities, yields, 'o', 'MarkerSize', 8, 'LineWidth', 1.5, 'DisplayName', 'Observed')
hold on
plot(t_fit, y_fit, '-', 'LineWidth', 2, 'DisplayName', 'Nelson-Siegel Fit')
xlabel('Maturity (Years)', 'FontSize', 12)
ylabel('Yield (%)', 'FontSize', 12)
title('Nelson-Siegel Yield Curve Fit', 'FontSize', 14)
legend('Location', 'best')
grid on
set(gca, 'FontName', 'Helvetica', 'FontSize', 11)

% Save plot as PDF
if ~exist('plots', 'dir')
    mkdir('plots');
end
print('plots/nelson_siegel_yield_curve', '-dpdf', '-bestfit');
