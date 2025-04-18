% Local Volatility Surface Simulation (Dupire Framework - No Toolboxes)
% BuyPolar Capital - Dupire Local Volatility Module (MATLAB)

%% Synthetic implied vol surface setup
S0 = 100;
strikes = 80:2:120;
maturities = [0.25 0.5 1.0];

[K, T] = meshgrid(strikes, maturities);

% Toy implied vol surface (smile + term structure)
IV = 0.2 + 0.1*((K - S0)/20).^2 + 0.05*T;

%% Dupire local volatility (approx via finite differences)
dK = 1; dT = 0.01;

% Black-Scholes price grid (manual normcdf)
norm_cdf = @(x) 0.5 * (1 + erf(x / sqrt(2)));
d1 = (log(S0./K) + (0.5 .* IV.^2) .* T) ./ (IV .* sqrt(T));
d2 = d1 - IV .* sqrt(T);
C = S0 .* norm_cdf(d1) - K .* norm_cdf(d2);

% Partial derivatives
[CT, CK] = gradient(C, dT, dK);
[CKK, ~] = gradient(CK, dK);

% Dupire formula
numerator = (CT + 0.05 .* K .* CK);
denominator = (0.5 .* K.^2 .* CKK);
local_vol = sqrt(abs(numerator ./ denominator)); % enforce real values

%% Plot
if ~exist('plots', 'dir')
    mkdir('plots');
end

figure;
surf(K, T, local_vol, 'EdgeColor','none');
title('Approximate Dupire Local Volatility Surface');
xlabel('Strike'); ylabel('Maturity'); zlabel('Local Volatility');
view(135, 30); colorbar;

print(gcf, fullfile('plots','dupire_local_vol_surface'), '-dpdf');

disp('Dupire local volatility surface simulated.');