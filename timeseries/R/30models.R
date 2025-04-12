# Load required libraries
library(tidyverse)
library(fpp3)
library(tidyquant)
library(ggfortify)
library(fable)
library(fabletools)
library(lubridate)
library(patchwork)

# 1. Get and prepare AAPL data
aapl <- tq_get("AAPL", from = "2020-01-01", to = "2024-12-31") %>% 
  select(symbol, date, close, volume) %>% 
  as_tsibble(index = date)

# 2. Monthly Aggregation
aapl_monthly <- aapl %>%
  index_by(month = yearmonth(date)) %>%
  summarise(close = mean(close, na.rm = TRUE))

# 3. Estimate Box-Cox lambda
lambda <- aapl_monthly %>% 
  features(close, features = guerrero) %>% 
  pull(lambda_guerrero)

# 4. Fit 30 forecasting models
fit_all <- aapl_monthly %>%
  model(
    ets        = ETS(close),
    arima      = ARIMA(close),
    stl_ets    = decomposition_model(STL(close ~ season(window = "periodic")), ETS(season_adjust)),
    naive      = NAIVE(close),
    drift      = RW(close ~ drift()),
    mean       = MEAN(close),
    snaive     = SNAIVE(close),
    tslm       = TSLM(close ~ trend() + season()),
    theta      = THETA(close),
    holt       = ETS(close ~ error("A") + trend("A") + season("N")),
    hw         = ETS(close ~ error("A") + trend("A") + season("A")),
    stl_arima  = decomposition_model(STL(close ~ season(window = "periodic")), ARIMA(season_adjust)),
    nnetar     = NNETAR(close),
    croston    = CROSTON(close),
    dhr        = ARIMA(close ~ fourier(K = 2)),
    rw         = RW(close),
    
    # 12 additional models
    boxcox_arima = ARIMA(box_cox(close, lambda)),
    boxcox_ets   = ETS(box_cox(close, lambda)),
    stl_tslm     = decomposition_model(STL(close ~ season(window = "periodic")), TSLM(season_adjust ~ trend())),
    stl_rw       = decomposition_model(STL(close ~ season(window = "periodic")), RW(season_adjust)),
    stl_theta    = decomposition_model(STL(close ~ season(window = "periodic")), THETA(season_adjust)),
    fourier3     = ARIMA(close ~ fourier(K = 3)),
    fourier4     = ARIMA(close ~ fourier(K = 4)),
    damped_holt  = ETS(close ~ error("A") + trend("Ad", phi = 0.9) + season("N")),
    comb_ets_arima = (ETS(close) + ARIMA(close)) / 2,
    comb_arima_tslm = (ARIMA(close) + TSLM(close ~ trend() + season())) / 2,
    comb_theta_rw   = (THETA(close) + RW(close)) / 2,
    comb_ets_theta  = (ETS(close) + THETA(close)) / 2
  )

# 5. Forecast 12 months ahead
fc_all <- fit_all %>% forecast(h = "12 months")

# 6. Create plots for each model (skip models that error out)
plots <- fc_all %>%
  mutate(.model = as.factor(.model)) %>%
  group_split(.model) %>%
  map(~ safely(function(df) {
    autoplot(df, aapl_monthly, level = NULL) +
      labs(title = unique(df$.model), y = "Close Price") +
      theme_bw()
  })(.x)) %>%
  map("result") %>%
  keep(~ inherits(.x, "gg"))

# 7. Create output directory
dir.create("plots", showWarnings = FALSE)

# 8. Save valid plots into 5 pages (6 plots per page)
for (i in 1:ceiling(length(plots) / 6)) {
  layout <- wrap_plots(plots[((i-1)*6 + 1):min(i*6, length(plots))], ncol = 3)
  ggsave(sprintf("plots/aapl_forecast_models_page_%d.pdf", i),
         plot = layout, width = 14, height = 9)
}
