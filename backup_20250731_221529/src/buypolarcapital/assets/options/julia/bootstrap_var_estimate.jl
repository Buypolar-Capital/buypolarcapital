using Plots, Statistics, Random, Distributions

# === Setup ===
tickers = ["SPY", "QQQ", "AAPL", "MSFT", "GLD", "TSLA"]
n_assets = length(tickers)
n_days = 252
Random.seed!(1337)

# === Simulate past returns ===
μ = zeros(n_assets)
Σ = Matrix{Float64}(I, n_assets, n_assets)
Σ[1,2] = Σ[2,1] = 0.9
Σ[3,4] = Σ[4,3] = 0.85
Σ[5,6] = Σ[6,5] = -0.3
returns = rand(MvNormal(μ, Symmetric(Σ)), n_days)'  # 252 × 6

# === Define portfolio ===
weights = normalize(rand(n_assets), 1)
p_returns = returns * weights  # 252 portfolio returns

# === Bootstrap ===
n_boot = 10_000
boot_samples = rand(p_returns, n_boot)
VaR_95 = quantile(boot_samples, 0.05)

# === Plot ===
hist = histogram(
    boot_samples,
    bins=50,
    xlabel="1-Day Portfolio Return",
    title="Bootstrapped VaR Estimate (95%)",
    legend=false,
    c=:lightblue,
    alpha=0.8,
    linewidth=0.5,
    size=(600, 400)
)

vline!([VaR_95], color=:red, lw=2, label="VaR (5%)")

# Safely find Y height from histogram data
yvals = hist[1][1][:y]
ypos = 0.8 * maximum(yvals)
annotate!(VaR_95, ypos, text("VaR = $(round(VaR_95*100,digits=2))%", 10, :red))

# === Export ===
plots_dir = "$(pwd())/plots"
if !isdir(plots_dir)
    mkdir(plots_dir)
end

savefig("$plots_dir/bootstrap_var_estimate.pdf")
