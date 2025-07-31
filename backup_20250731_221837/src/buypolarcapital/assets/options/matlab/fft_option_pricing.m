% FFT-Based Option Pricing (Carr-Madan Method)
% BuyPolar Capital - Numerical Methods Module (MATLAB)

%% Parameters
K = 100;         % strike price
S0 = 100;        % spot price
r = 0.05;        % risk-free rate
T = 1;           % time to maturity
sigma = 0.2;     % volatility

N = 2^12;        % FFT grid size
delta = 0.25;    % spacing in log-strike
alpha = 1.5;     % damping factor

%% Characteristic function of log returns under Black-Scholes
cf = @(u) exp(1i*u*(log(S0)+(r - 0.5*sigma^2)*T) - 0.5*sigma^2*T*u.^2);

%% FFT grid
lambda = 2*pi / (N*delta);
k = -N/2:1:N/2-1;
b = N*lambda/2;
v = (0:N-1)';

% Define modified payoff function (Carr-Madan integrand)
psi = exp(-r*T) .* cf(v - (alpha+1)*1i) ./ (alpha^2 + alpha - v.^2 + 1i*(2*alpha+1)*v);
psi(1) = psi(1) * 0.5;  % correction for first term

% Apply FFT
y = real(fft(psi .* exp(1i*b*v*delta) .* delta));
k_strike = exp(-b + lambda*(0:N-1));

% Recover call prices
call_prices = exp(-alpha*log(k_strike)) / pi .* y;

%% Interpolate to get price at strike = K
call_interp = interp1(k_strike, call_prices, K, 'spline');

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
plot(k_strike, call_prices, 'b-', 'LineWidth', 2); hold on;
xline(K, '--r', 'Strike');
title('European Call Prices via Carr-Madan FFT');
xlabel('Strike'); ylabel('Option Price'); grid on;

print(gcf, fullfile('plots','fft_option_pricing'), '-dpdf');

fprintf('Option price at strike %.2f: %.4f\n', K, call_interp);
disp('FFT-based option pricing complete.');
