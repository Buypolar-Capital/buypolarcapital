library(tidyverse)
library(fpp3)
library(tidyquant)
library(ggfortify)
library(fable)
library(fabletools)
library(lubridate)

# 1. Get Data
aapl <- tq_get("AAPL", from = "2020-01-01", to = "2024-12-31") %>% 
  select(symbol, date, close, volume) %>% 
  as_tsibble(index = date)

# 2. Plot Raw Series
p1 <- aapl %>% autoplot(close) + theme_bw() + labs(title = "AAPL Close (Daily)")
p2 <- aapl %>% autoplot(volume) + theme_bw() + labs(title = "AAPL Volume (Daily)")

# 3. STL on aggregated series
aapl_m <- aapl %>% 
  mutate(month = as.Date(cut(date, "month"))) %>% 
  group_by(month) %>% 
  summarise(
    close = mean(close),
    volume = sum(volume),
    .groups = "drop"
  )

close_ts <- ts(aapl_m$close, start = c(2020, 1), frequency = 12)
close_stl <- stl(close_ts, s.window = "periodic")
p3 <- autoplot(close_stl) + theme_bw() + labs(title = "STL Decomposition of AAPL Close")

# 4. fpp3 Forecasting
aapl_monthly <- aapl %>%
  index_by(month = yearmonth(date)) %>%
  summarise(close = mean(close, na.rm = TRUE))

fit_all <- aapl_monthly %>%
  model(
    ets     = ETS(close),
    arima   = ARIMA(close),
    stl_ets = decomposition_model(STL(close ~ season(window = "periodic")), ETS(season_adjust)),
    naive   = NAIVE(close),
    drift   = RW(close ~ drift()),
    mean    = MEAN(close)
  )

fc_all <- fit_all %>% forecast(h = "12 months")

# 5. Plot All Forecasts Faceted
p4 <- fc_all %>%
  autoplot(aapl_monthly, level = NULL) +
  facet_wrap(~ .model, scales = "free_y") +
  labs(title = "AAPL Close Forecasts: Model Comparison", y = "Price") +
  theme_bw()

# 6. Save Plots to /plots Folder
dir.create("plots", showWarnings = FALSE)

ggsave("plots/aapl_close_daily.pdf", plot = p1, width = 12, height = 6)
ggsave("plots/aapl_volume_daily.pdf", plot = p2, width = 12, height = 6)
ggsave("plots/aapl_stl_decomposition.pdf", plot = p3, width = 12, height = 6)
ggsave("plots/aapl_forecast_models.pdf", plot = p4, width = 12, height = 6)

# 7. Optional: Show accuracy table
fit_all %>% accuracy()
