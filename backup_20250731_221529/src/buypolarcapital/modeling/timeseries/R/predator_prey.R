# Parameters
a <- 1.05
b <- 0.02
c <- 0.95
d <- 0.005

# Initial values
x0 <- 40    # Initial prey population
y0 <- 9     # Initial predator population
N <- 2000  # Number of time steps

# Vectors to store values
x <- numeric(N)
y <- numeric(N)
x[1] <- x0
y[1] <- y0

# Simulate the system
for (n in 1:(N-1)) {
  x[n+1] <- a * x[n] - b * x[n] * y[n]
  y[n+1] <- c * y[n] + d * x[n] * y[n]
}

# Optional: Create 'plots' folder if it doesn't exist
if (!dir.exists("plots")) dir.create("plots")

# Downsample safely
step <- 10
time_plot <- seq(1, N, by = step)
x_plot <- x[time_plot]
y_plot <- y[time_plot]

# Only plot if data is finite
if (all(is.finite(x_plot)) && all(is.finite(y_plot))) {
  pdf("plots/predator_prey_dynamics.pdf", width = 8, height = 5)
  plot(time_plot, x_plot, type = "l", col = "blue", lwd = 1.5,
       ylim = range(c(x_plot, y_plot), finite = TRUE), ylab = "Population", xlab = "Time",
       main = paste("Predator-Prey Dynamics (N =", N, ")"))
  lines(time_plot, y_plot, col = "red", lwd = 1.5)
  legend("topright", legend = c("Prey", "Predator"),
         col = c("blue", "red"), lty = 1, lwd = 2)
  dev.off()
} else {
  warning("Data contains non-finite values. Skipping plot.")
}
