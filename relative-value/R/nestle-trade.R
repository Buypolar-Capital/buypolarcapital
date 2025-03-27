
# File: nestle_zscore_strategy.R
library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(zoo)

# Load data: Nestl?? Swiss vs ADR
tickers <- c("NSRGY", "NESN.SW")
full_prices <- tq_get(tickers, from = "2010-01-01", to = Sys.Date()) %>%
  select(date, symbol, adjusted) %>%
  pivot_wider(names_from = symbol, values_from = adjusted) %>%
  tidyr::drop_na() %>%
  rename(ADR = NSRGY, SWISS = `NESN.SW`) %>%
  mutate(
    ratio = ADR / SWISS,
    rolling_mean = rollmean(ratio, 30, fill = NA, align = "right"),
    rolling_sd = rollapply(ratio, 30, sd, fill = NA, align = "right"),
    z_score = (ratio - rolling_mean) / rolling_sd
  ) %>% drop_na()

# Strategy simulation
simulate_strategy <- function(prices, threshold = 1, initial_capital = 1e7) {
  portfolio <- tibble(date = prices$date, cash = NA, adr = NA, swiss = NA, value = NA)
  rebalance_dates <- c()
  first <- prices[1, ]
  if (first$z_score > 0) {
    shares_swiss <- floor(initial_capital / first$SWISS)
    shares_adr <- 0
    cash <- initial_capital - shares_swiss * first$SWISS
  } else {
    shares_adr <- floor(initial_capital / first$ADR)
    shares_swiss <- 0
    cash <- initial_capital - shares_adr * first$ADR
  }
  for (i in seq_len(nrow(prices))) {
    row <- prices[i, ]
    z <- row$z_score
    rebalance_now <- (z > threshold && shares_adr > 0) || (z < -threshold && shares_swiss > 0)
    if (rebalance_now) {
      rebalance_dates <- c(rebalance_dates, row$date)
      cash <- shares_adr * row$ADR + shares_swiss * row$SWISS + cash
      if (z > 0) {
        shares_adr <- 0
        shares_swiss <- floor(cash / row$SWISS)
        cash <- cash - shares_swiss * row$SWISS
      } else {
        shares_swiss <- 0
        shares_adr <- floor(cash / row$ADR)
        cash <- cash - shares_adr * row$ADR
      }
    }
    value <- shares_adr * row$ADR + shares_swiss * row$SWISS + cash
    portfolio[i, c("cash", "adr", "swiss", "value")] <- list(cash, shares_adr, shares_swiss, value)
  }
  portfolio <- portfolio %>%
    mutate(
      ADR_only = initial_capital * prices$ADR / prices$ADR[1],
      SWISS_only = initial_capital * prices$SWISS / prices$SWISS[1]
    )
  list(portfolio = portfolio, rebalances = rebalance_dates)
}

# Plotting
plot_strategy <- function(simulation) {
  portfolio <- simulation$portfolio
  rebal <- tibble(date = as.Date(simulation$rebalances), y = max(portfolio$value, na.rm = TRUE) * 1.01)
  df <- portfolio %>%
    mutate(date = as.Date(date)) %>%
    select(date, Strategy = value, ADR = ADR_only, Switzerland = SWISS_only) %>%
    pivot_longer(-date, names_to = "Series", values_to = "Value")
  
  ggplot(df, aes(x = date, y = Value, color = Series)) +
    geom_line(size = 1.1) +
    geom_point(data = rebal, aes(x = date, y = y),
               inherit.aes = FALSE, color = "red", size = 0.5, shape = 18) +
    labs(
      title = "Z-score Strategy: Nestl?? ADR vs Swiss Listing",
      subtitle = "Rebalanced when z-score crosses ??1 (30-day rolling)",
      y = "Portfolio Value (USD)",
      caption = "Data: Yahoo Finance | Strategy: BuyPolar Capital"
    ) +
    theme_economist_white() +
    scale_color_manual(values = c("Strategy" = "#2c3e50", "ADR" = "#e74c3c", "Switzerland" = "#3498db")) +
    theme(legend.title = element_blank()) +
    scale_y_continuous(labels = dollar_format(scale = 1e-6, suffix = "M"))
}

# Run + Save
sim <- simulate_strategy(full_prices)
p <- plot_strategy(sim)

if (!dir.exists("plots")) dir.create("plots")
ggsave("plots/nestle_zscore_strategy.pdf", p, width = 10, height = 6)
