
# File: goog_zscore_strategy.R
library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(zoo)

tickers <- c("GOOG", "GOOGL")
full_prices <- tq_get(tickers, from = "2014-01-01", to = Sys.Date()) %>%
  select(date, symbol, adjusted) %>%
  pivot_wider(names_from = symbol, values_from = adjusted) %>%
  tidyr::drop_na() %>%
  mutate(
    ratio = GOOG / GOOGL,
    rolling_mean = rollmean(ratio, 30, fill = NA, align = "right"),
    rolling_sd = rollapply(ratio, 30, sd, fill = NA, align = "right"),
    z_score = (ratio - rolling_mean) / rolling_sd
  ) %>% drop_na()

simulate_strategy <- function(prices, threshold = 1, initial_capital = 1e7) {
  portfolio <- tibble(date = prices$date, cash = NA, A = NA, B = NA, value = NA)
  rebalance_dates <- c()
  first <- prices[1, ]
  if (first$z_score > 0) {
    shares_B <- floor(initial_capital / first$GOOGL)
    shares_A <- 0
    cash <- initial_capital - shares_B * first$GOOGL
  } else {
    shares_A <- floor(initial_capital / first$GOOG)
    shares_B <- 0
    cash <- initial_capital - shares_A * first$GOOG
  }
  for (i in seq_len(nrow(prices))) {
    row <- prices[i, ]
    z <- row$z_score
    rebalance_now <- (z > threshold && shares_A > 0) || (z < -threshold && shares_B > 0)
    if (rebalance_now) {
      rebalance_dates <- c(rebalance_dates, row$date)
      cash <- shares_A * row$GOOG + shares_B * row$GOOGL + cash
      if (z > 0) {
        shares_A <- 0
        shares_B <- floor(cash / row$GOOGL)
        cash <- cash - shares_B * row$GOOGL
      } else {
        shares_B <- 0
        shares_A <- floor(cash / row$GOOG)
        cash <- cash - shares_A * row$GOOG
      }
    }
    value <- shares_A * row$GOOG + shares_B * row$GOOGL + cash
    portfolio[i, c("cash", "A", "B", "value")] <- list(cash, shares_A, shares_B, value)
  }
  portfolio <- portfolio %>%
    mutate(GOOG_only = initial_capital * prices$GOOG / prices$GOOG[1],
           GOOGL_only = initial_capital * prices$GOOGL / prices$GOOGL[1])
  list(portfolio = portfolio, rebalances = rebalance_dates)
}

plot_strategy <- function(simulation) {
  portfolio <- simulation$portfolio
  rebal <- tibble(date = as.Date(simulation$rebalances), y = max(portfolio$value, na.rm = TRUE) * 1.01)
  df <- portfolio %>%
    select(date, Strategy = value, GOOG = GOOG_only, GOOGL = GOOGL_only) %>%
    pivot_longer(-date, names_to = "Series", values_to = "Value")
  ggplot(df, aes(x = date, y = Value, color = Series)) +
    geom_line(size = 1.1) +
    geom_point(data = rebal, aes(x = date, y = y), inherit.aes = FALSE, color = "red", size = 0.5, shape = 18) +
    labs(title = "Z-score Strategy: GOOG vs GOOGL", y = "Portfolio Value (USD)") +
    theme_economist_white() +
    scale_color_manual(values = c("Strategy" = "#2c3e50", "GOOG" = "#e74c3c", "GOOGL" = "#3498db")) +
    theme(legend.title = element_blank()) +
    scale_y_continuous(labels = dollar_format(scale = 1e-6, suffix = "M"))
}

sim <- simulate_strategy(full_prices)
p <- plot_strategy(sim)
if (!dir.exists("plots")) dir.create("plots")
ggsave("plots/goog_zscore_strategy.pdf", p, width = 10, height = 6)
