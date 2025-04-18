using Turing, CSV, DataFrames, StatsPlots, Dates, Random
using Distributions, MCMCChains, StatsBase
using LinearAlgebra

# Set random seed
Random.seed!(123)

# --- Load Brent Crude Oil data ---
# Assumes CSV in: buypolarcapital/timeseries/julia/data/brent.csv
isdir("data") || error("data/ directory not found")
brent = CSV.read("data/brent.csv", DataFrame)

# Convert Date column and check for Price (map Close to Price)
brent.Date = Date.(brent.Date, "yyyy-mm-dd")
if !hasproperty(brent, :Price)
    if hasproperty(brent, :Close)
        brent.Price = brent.Close
    else
        error("CSV must contain a 'Price' or 'Close' column")
    end
end
first(brent, 5)

# --- Select recent time period & standardize ---
brent = brent[brent.Date .>= Date(2022, 1, 1), :]
price = zscore(brent.Price)
N = length(price)

# --- Bayesian Local Level Model ---
@model function local_level(y, N)
    σ ~ Truncated(Cauchy(0, 1), 0.01, 10)
    τ ~ Truncated(Cauchy(0, 1), 0.01, 10)
    
    μ = Vector{Real}(undef, N)
    μ[1] ~ Normal(0, 1)
    for t in 2:N
        μ[t] ~ Normal(μ[t-1], τ)
    end

    for t in 1:N
        y[t] ~ Normal(μ[t], σ)
    end
    return μ
end

# --- Sample from posterior ---
model = local_level(price, N)
chain = sample(model, NUTS(), MCMCThreads(), 1000, 4)

# --- Extract and plot ---
# Compute mean and std of μ for each time point
μ_post = [mean(chain["μ[$t]"]) for t in 1:N]
μ_std = [std(chain["μ[$t]"]) for t in 1:N]

# Ensure plots directory exists
isdir("plots") || mkdir("plots")

# Plot
p = plot(brent.Date, price, label="Actual (std)", lw=1.5)
plot!(brent.Date, μ_post, ribbon=μ_std, label="Posterior Mean ± SD", lw=2, c=:red)

# Save plot
savefig(p, "plots/brent_bayesian_forecast.pdf")

println("✔ Forecast plot saved to plots/brent_bayesian_forecast.pdf")