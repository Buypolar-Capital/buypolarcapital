using Plots

S0 = 100
mu = 0.05
sigma = 0.2
T = 1
N = 252
dt = T/N
t = range(0, T, length=N+1)
n_paths = 5

paths = zeros(N+1, n_paths)
paths[1, :] .= S0

for j in 1:n_paths
    for i in 2:N+1
        ε = randn()
        paths[i, j] = paths[i-1, j] * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*ε)
    end
end

plot(t, paths, lw=2, title="GBM Paths", xlabel="Time", ylabel="Price", legend=false)

# === Plotting ===
plot(t, paths, lw=2, title="GBM Paths", xlabel="Time", ylabel="Price", legend=false)

# === Export plot to ./plots ===
plots_dir = "$(pwd())/plots"
if !isdir(plots_dir)
    mkdir(plots_dir)
end

savefig("$plots_dir/gbm_sim.pdf")

