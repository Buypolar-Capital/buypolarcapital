using Plots, Distributions, Statistics

# === Parameters ===
S0 = 100.0       # Initial price
K = 105.0        # Strike
r = 0.03         # Risk-free rate
sigma = 0.2      # Volatility
T = 1.0          # Time to maturity (in years)
n_trials = 10_000

# === Simulate terminal prices under risk-neutral measure ===
Z = randn(n_trials)
ST = S0 * exp.((r - 0.5 * sigma^2) * T .+ sigma * sqrt(T) .* Z)
payoffs = max.(ST .- K, 0.0)
mc_price = exp(-r * T) * mean(payoffs)

# === Black-Scholes Closed Form ===
function bs_call_price(S, K, r, sigma, T)
    d1 = (log(S / K) + (r + 0.5 * sigma^2)*T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * cdf(Normal(), d1) - K * exp(-r * T) * cdf(Normal(), d2)
end

bs_price = bs_call_price(S0, K, r, sigma, T)

# === Convergence Plot ===
sim_sizes = round.(Int, range(50, n_trials, length=50))
mc_estimates = Float64[]

for N in sim_sizes
    Zs = randn(N)
    ST = S0 * exp.((r - 0.5 * sigma^2) * T .+ sigma * sqrt(T) .* Zs)
    payoff = max.(ST .- K, 0.0)
    price = exp(-r * T) * mean(payoff)
    push!(mc_estimates, price)
end

# === Plot ===
plot(sim_sizes, mc_estimates,
    lw=2,
    label="Monte Carlo Estimate",
    xlabel="Number of Simulations",
    ylabel="Option Price",
    title="Convergence of Monte Carlo Call Option Price")

hline!([bs_price], ls=:dash, lw=2, color=:red, label="Black-Scholes")

# === Export ===
plots_dir = "$(pwd())/plots"
if !isdir(plots_dir)
    mkdir(plots_dir)
end

savefig("$plots_dir/monte_carlo_option.pdf")
