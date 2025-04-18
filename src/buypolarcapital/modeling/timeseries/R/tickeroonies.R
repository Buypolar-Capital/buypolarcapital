
library(tidyverse)
library(fpp3)
library(tidyquant)
library(ggfortify)
library(fable)
library(fabletools)
library(lubridate)

aapl <- tq_get("AAPL",
               from="2020-01-01",
               to="2024-12-31") %>% 
  select(symbol, date, close, volume) %>% 
  as_tsibble(index = date)

aapl %>% 
  autoplot(close) +
  theme_bw()

aapl %>% 
  autoplot(volume) +
  theme_bw()

plot(aapl$close)
plot(aapl$volume)

aapl_m <- aapl %>% 
  mutate(month=as.Date(cut(date,"month"))) %>% 
  group_by(month) %>% 
  summarise(close = mean(close),
          volume = sum(volume),
          .groups = "drop")

close_ts <- ts(aapl_m$close,
               start=c(2020,1),
               frequency = 12)

close_stl <- stl(close_ts,
                 s.window="periodic")

plot(close_stl)
autoplot(close_stl) +
  theme_bw()

aapl_monthly <- aapl %>%
  index_by(month = yearmonth(date)) %>%
  summarise(close = mean(close, na.rm = TRUE))  # keep it simple

fit_all <- aapl_monthly %>%
  model(
    ets     = ETS(close),
    arima   = ARIMA(close),
    stl_ets = decomposition_model(STL(close ~ season(window = "periodic")),
                                  ETS(season_adjust)),
    naive   = NAIVE(close),
    drift   = RW(close ~ drift()),
    mean    = MEAN(close)
  )

fc_all <- fit_all %>%
  forecast(h = "12 months")

fc_all %>%
  autoplot(aapl_monthly, level = NULL) +
  facet_wrap(~ .model, scales = "free_y") +
  labs(title = "AAPL Close Forecasts: Model Comparison", y = "Price") +
  theme_bw()

fit_all %>% accuracy()

