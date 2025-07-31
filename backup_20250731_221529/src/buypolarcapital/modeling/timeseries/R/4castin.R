# Load core packages
library(tidyverse)
library(fpp3)              # includes tsibble, fable, feasts
library(fable.prophet)     # Prophet model
library(forecast)          # TBATS, nnetar
library(bsts)              # Bayesian Structural Time Series
library(gridExtra)
library(patchwork)

# Avoid dplyr::lag() issues with xts
conflictRules("dplyr", exclude = "lag")

# Create output folder if it doesn't exist
if (!dir.exists("plots")) dir.create("plots")

# Load and prep data
data <- aus_airpassengers %>%
  mutate(Month = yearmonth(Year)) %>%
  as_tsibble(index = Month)

# Forecast horizon
h <- 12

# -------------------
# MODELS IN FABLE
# -------------------

models_fable <- model(
  data,
  Mean   = MEAN(Passengers),
  Naive  = NAIVE(Passengers),
  Drift  = RW(Passengers ~ drift()),
  ARIMA  = ARIMA(Passengers),
  ETS    = ETS(Passengers)
)

fc_fable <- forecast(models_fable, h = h)

# Robust plot generation: try-catch on each plot
plots_fable_list <- fc_fable %>%
  filter(!is.na(.mean)) %>%
  group_split(.model) %>%
  map(~ tryCatch({
    p <- autoplot(.x, data) +
      labs(title = paste("Forecast:", unique(.x$.model))) +
      theme_minimal() +
      guides(colour = "none")  # Remove legend to avoid guide issues
    p
  }, error = function(e) {
    message("Skipping plot for ", unique(.x$.model), " due to error: ", e$message)
    NULL  # Skip failed plots
  })) %>%
  compact()  # Remove NULLs from failed attempts

# -------------------
# NNETAR + TBATS
# -------------------

data_ts <- ts(data$Passengers, start = c(2000, 1), frequency = 12)

fit_tbats <- tbats(data_ts)
fc_tbats <- forecast::forecast(fit_tbats, h = h)

fit_nnetar <- nnetar(data_ts)
fc_nnetar <- forecast::forecast(fit_nnetar, h = h)

# Convert forecast objects to ggplot for consistency
plot_tbats <- autoplot(fc_tbats) + 
  labs(title = "TBATS Forecast") + 
  theme_minimal()

plot_nnetar <- autoplot(fc_nnetar) + 
  labs(title = "NNETAR Forecast") + 
  theme_minimal()

# -------------------
# BSTS
# -------------------

ss <- AddLocalLinearTrend(list(), data_ts)
model_bsts <- bsts(data_ts, state.specification = ss, niter = 1000)
bsts_samples <- predict(model_bsts, horizon = h, burn = 100, quantiles = NULL)
bsts_draws <- bsts_samples$distribution

# Build BSTS forecast DataFrame
df_bsts <- tibble(
  Date  = index(data) %>% max() %>% yearmonth() %>% seq(., by = 1, length.out = h),
  Mean  = apply(bsts_draws, 2, mean),
  Lower = apply(bsts_draws, 2, quantile, probs = 0.1),
  Upper = apply(bsts_draws, 2, quantile, probs = 0.9)
)

plot_bsts <- data %>%
  ggplot(aes(x = Month, y = Passengers)) +
  geom_line() +
  geom_line(data = df_bsts, aes(x = Date, y = Mean), color = "blue") +
  geom_ribbon(data = df_bsts, aes(x = Date, ymin = Lower, ymax = Upper), alpha = 0.3) +
  labs(title = "BSTS Forecast") +
  theme_minimal()

# -------------------
# SAVE TO MULTI-PAGE PDF
# -------------------

pdf("plots/airport_forecasts_full.pdf", width = 12, height = 8)

# Print fable plots
walk(plots_fable_list, print)

# Print TBATS and NNETAR plots
print(plot_tbats)
print(plot_nnetar)

# Print BSTS plot
print(plot_bsts)

dev.off()