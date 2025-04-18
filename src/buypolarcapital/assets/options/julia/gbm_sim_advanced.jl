using Plots, Statistics, Random

# === Parameters ===
tickers = ["SPY", "QQQ", "AAPL", "MSFT", "GLD"]
n_assets = length(tickers)
S0 = 100
mu = [0.08, 0.10, 0.12, 0.09, 0.05]       # annual drift
sigma = [0.15, 0.18, 0.25, 0.20, 0.12]    # annual volatility
T = 1.0                                   # years
N = 252                                   # trading days
dt = T/N
t = range(0, T, length=N+1)

# === Simulation ===
n_paths = n_assets
paths = zeros(N+1, n_paths)
paths[1, :] .= S0

Random.seed!(1234)  # reproducibility

for j in 1:n_paths
    for i in 2:N+1
        ε = randn()
        drift = (mu[j] - 0.5 * sigma[j]^2) * dt
        shock = sigma[j] * sqrt(dt) * ε
        paths[i, j] = paths[i-1, j] * exp(drift + shock)
    end
end

# === Post-Simulation Stats ===
log_returns = diff(log.(paths), dims=1)
annualized_return = mean(log_returns, dims=1)[:]' .* N
annualized_vol = std(log_returns, dims=1)[:]' .* sqrt(N)
sharpe_ratios = annualized_return ./ annualized_vol

# === Plot with overlays ===
colors = distinguishable_colors(n_assets)
plot(t, paths, lw=2, title="Simulated GBM Paths", xlabel="Time", ylabel="Price", legend=:topright, color=colors)

# Add moving averages
for j in 1:n_paths
    ma = [mean(paths[max(1,i-10):i,j]) for i in 1:N+1]
    plot!(t, ma, ls=:dash, lw=1.0, label="MA - "*tickers[j], color=colors[j])
end

# Annotate final values
for j in 1:n_paths
    final_price = round(paths[end, j]; digits=2)
    sr = round(sharpe_ratios[j]; digits=2)
    annotate!(t[end], paths[end, j], text("$(tickers[j])\n\$$(final_price)\nSR: $(sr)", :left, 9, colors[j]))
end

# === Export ===
plots_dir = "$(pwd())/plots"
if !isdir(plots_dir)
    mkdir(plots_dir)
end

savefig("$plots_dir/gbm_sim_advanced.pdf")
using Plots, Statistics, Random

# === Parameters ===
tickers = ["SPY", "QQQ", "AAPL", "MSFT", "GLD"]
n_assets = length(tickers)
S0 = 100
mu = [0.08, 0.10, 0.12, 0.09, 0.05]       # annual drift
sigma = [0.15, 0.18, 0.25, 0.20, 0.12]    # annual volatility
T = 1.0                                   # years
N = 252                                   # trading days
dt = T/N
t = range(0, T, length=N+1)

# === Simulation ===
n_paths = n_assets
paths = zeros(N+1, n_paths)
paths[1, :] .= S0

Random.seed!(1234)  # reproducibility

for j in 1:n_paths
    for i in 2:N+1
        ε = randn()
        drift = (mu[j] - 0.5 * sigma[j]^2) * dt
        shock = sigma[j] * sqrt(dt) * ε
        paths[i, j] = paths[i-1, j] * exp(drift + shock)
    end
end

# === Post-Simulation Stats ===
log_returns = diff(log.(paths), dims=1)
annualized_return = mean(log_returns, dims=1)[:]' .* N
annualized_vol = std(log_returns, dims=1)[:]' .* sqrt(N)
sharpe_ratios = annualized_return ./ annualized_vol

# === Plot with overlays ===
colors = distinguishable_colors(n_assets)
plot(title="Simulated GBM Paths", xlabel="Time", ylabel="Price", legend=:topright)

# Plot each asset individually
for j in 1:n_paths
    plot!(t, paths[:, j], lw=2, label=tickers[j], color=colors[j])
    
    # Moving average (10-day)
    ma = [mean(paths[max(1,i-10):i,j]) for i in 1:N+1]
    plot!(t, ma, lw=1, ls=:dash, label="", color=colors[j])
    
    # Annotate final price and Sharpe ratio
    final_price = round(paths[end, j]; digits=2)
    sr = round(sharpe_ratios[j]; digits=2)
    annotate!(t[end], paths[end, j], text("$(tickers[j])\n\$$(final_price)\nSR: $(sr)", :left, 9, colors[j]))
end


# === Export ===
plots_dir = "$(pwd())/plots"
if !isdir(plots_dir)
    mkdir(plots_dir)
end

savefig("$plots_dir/gbm_sim_advanced.pdf")
