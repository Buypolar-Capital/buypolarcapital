using CSV, DataFrames, Dates, Turing, StatsPlots, Distributions, YahooFinance, Statistics, Random

# --- Load Data (S&P 500 via YahooFinance.jl) ---
data = get_prices("^GSPC"; interval="1d", start=Date(2022,1,1), end=Date(2024,1,1))
df = DataFrame(data)
df[!, :Return] = [missing; diff(log.(df.AdjClose))]

df = dropmissing(df)
df = df[end-199:end, :]  # last 200 observations

y = df.Return
N = length(y)
period = 7  # Weekly seasonality

# --- BSTS Model with Seasonality ---
@model function bsts_model_seasonal(y, period)
    σ_trend ~ InverseGamma(2, 2)
    σ_obs ~ InverseGamma(2, 2)
    σ_season ~ InverseGamma(2, 2)

    level = Vector{Real}(undef, N)
    season = Vector{Real}(undef, N)

    level[1] ~ Normal(0, 0.5)
    for t in 2:N
        level[t] ~ Normal(level[t-1], σ_trend)
    end

    for t in 1:period
        season[t] ~ Normal(0, σ_season)
    end

    for t in (period+1):N
        season[t] ~ Normal(-sum(season[(t-period):(t-1)]), σ_season)
    end

    for t in 1:N
        y[t] ~ Normal(level[t] + season[t], σ_obs)
    end
end

# --- Inference ---
model = bsts_model_seasonal(y, period)
chain = sample(model, NUTS(), 1000)

# --- Extract summaries ---
mean_level = mean(chain[:level], dims=1) |> vec
q025 = mapslices(x -> quantile(x, 0.025), chain[:level], dims=1) |> vec
q975 = mapslices(x -> quantile(x, 0.975), chain[:level], dims=1) |> vec

# --- Plot Trend + CI ---
plot(df.Date, mean_level, label="Estimated Trend", lw=2)
plot!(df.Date, q025, ribbon=(q975 .- q025), fillalpha=0.2, label="95% Credible Interval")
plot!(df.Date, y, label="Observed Return", lw=1, legend=:bottomright)

mkpath("plots")
savefig("plots/bsts_trend_ci.pdf")

# --- Multi-step Forecasting ---
num_forecast = 30
n_samples = 500
posterior_level = chain[:level]
posterior_season = chain[:season]

simulated_forecasts = zeros(n_samples, num_forecast)

Random.seed!(1234)
for i in 1:n_samples
    l = posterior_level[i, end]
    s = posterior_season[i, end-period+1:end]
    σ_trend = chain[:σ_trend][i]
    σ_obs = chain[:σ_obs][i]
    σ_season = chain[:σ_season][i]

    for t in 1:num_forecast
        l = rand(Normal(l, σ_trend))
        push!(s, -sum(s[end-period+1:end]) + rand(Normal(0, σ_season)))
        push!(s, s[end])
        y_hat = l + s[end] + rand(Normal(0, σ_obs))
        simulated_forecasts[i, t] = y_hat
    end
end

forecast_mean = vec(mean(simulated_forecasts, dims=1))
forecast_lo = vec(mapslices(x -> quantile(x, 0.025), simulated_forecasts, dims=1))
forecast_hi = vec(mapslices(x -> quantile(x, 0.975), simulated_forecasts, dims=1))
forecast_dates = [df.Date[end] + Day(i) for i in 1:num_forecast]

plot(forecast_dates, forecast_mean, label="Forecasted Return", lw=2)
plot!(forecast_dates, forecast_lo, ribbon=(forecast_hi .- forecast_lo), fillalpha=0.2, label="95% CI", legend=:bottomright)
savefig("plots/bsts_forecast_advanced.pdf")
