library(tidyverse)
library(fpp3)
library(tidyquant)
library(ggfortify)
library(fable)
library(fabletools)
library(lubridate)
library(patchwork)
# Optional: for Prophet, install via prophet_fable
# devtools::install_github("tidyverts/prophet_fable")
# library(prophet_fable)

# 1. Get Data
aapl <- tq_get("AAPL", from = "2020-01-01", to = "2024-12-31") %>% 
  select(symbol, date, close, volume) %>% 
  as_tsibble(index = date)

# 2. Monthly Aggregation
aapl_monthly <- aapl %>%
  index_by(month = yearmonth(date)) %>%
  summarise(close = mean(close, na.rm = TRUE))

# 3. Define Models
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
    rw         = RW(close)
  )


# 4. Forecast
fc_all <- fit_all %>% forecast(h = "12 months")

# 5. Generate 18 plots individually
plots <- fc_all %>%
  mutate(.model = as.factor(.model)) %>%
  group_split(.model) %>%
  map(~ autoplot(.x, aapl_monthly, level = NULL) +
        labs(title = unique(.x$.model), y = "Close Price") +
        theme_bw())

# 6. Arrange into 3 PDF pages of 6 plots each
dir.create("plots", showWarnings = FALSE)

for (i in 1:3) {
  layout <- wrap_plots(plots[((i-1)*6 + 1):(i*6)], ncol = 3)
  ggsave(sprintf("plots/aapl_forecast_models_page_%d.pdf", i),
         plot = layout, width = 14, height = 9)
}
