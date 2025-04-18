using Plots, Statistics, Random, Distributions, LinearAlgebra

# === Parameters ===
tickers = ["SPY", "QQQ", "AAPL", "MSFT", "GLD", "TSLA"]
n_assets = length(tickers)
n_obs = 252  # 1 year of daily returns
Random.seed!(42)

# === Define correlation structure ===
Σ = Matrix{Float64}(I, n_assets, n_assets)  # Identity matrix from LinearAlgebra.I
Σ[1,2] = Σ[2,1] = 0.9   # SPY-QQQ
Σ[3,4] = Σ[4,3] = 0.85  # AAPL-MSFT
Σ[5,6] = Σ[6,5] = -0.3  # GLD-TSLA inverse

Σ = Symmetric(Σ)
μ = zeros(n_assets)

# === Simulate multivariate normal returns ===
returns = rand(MvNormal(μ, Σ), n_obs)'  # shape: 252 × 6

# === Correlation matrix ===
C = cor(returns)

# === Plot ===
heatmap(
    tickers,
    tickers,
    C,
    c=:coolwarm,
    clim=(-1, 1),
    xlabel="Assets",
    ylabel="Assets",
    title="Asset Correlation Matrix",
    size=(600, 500),
    right_margin=10Plots.mm,
    yflip=true,
    legend=:right
)

# === Export ===
plots_dir = "$(pwd())/plots"
if !isdir(plots_dir)
    mkdir(plots_dir)
end

savefig("$plots_dir/correlation_heatmap.pdf")
