# File: novo_zscore_strategy.R
library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(zoo)

# Load data: Novo Nordisk ADR vs Denmark listing
tickers <- c("NVO", "NOVO-B.CO")
full_prices <- tq_get(tickers, from = "2010-01-01", to = Sys.Date()) %>%
  select(date, symbol, adjusted) %>%
  pivot_wider(names_from = symbol, values_from = adjusted) %>%
  tidyr::drop_na() %>%
  rename(ADR = NVO, DK = `NOVO-B.CO`) %>%
  mutate(
    ratio = ADR / DK,
    rolling_mean = rollmean(ratio, 30, fill = NA, align = "right"),
    rolling_sd = rollapply(ratio, 30, sd, fill = NA, align = "right"),
    z_score = (ratio - rolling_mean) / rolling_sd
  ) %>% drop_na()

# Simulation
simulate_strategy <- function(prices, threshold = 1, initial_capital = 1e7) {
  portfolio <- tibble(date = prices$date, cash = NA, adr = NA, dk = NA, value = NA)
  rebalance_dates <- c()
  first <- prices[1, ]
  if (first$z_score > 0) {
    shares_dk <- floor(initial_capital / first$DK)
    shares_adr <- 0
    cash <- initial_capital - shares_dk * first$DK
  } else {
    shares_adr <- floor(initial_capital / first$ADR)
    shares_dk <- 0
    cash <- initial_capital - shares_adr * first$ADR
  }
  for (i in seq_len(nrow(prices))) {
    row <- prices[i, ]
    z <- row$z_score
    rebalance_now <- (z > threshold && shares_adr > 0) || (z < -threshold && shares_dk > 0)
    if (rebalance_now) {
      rebalance_dates <- c(rebalance_dates, row$date)
      cash <- shares_adr * row$ADR + shares_dk * row$DK + cash
      if (z > 0) {
        shares_adr <- 0
        shares_dk <- floor(cash / row$DK)
        cash <- cash - shares_dk * row$DK
      } else {
        shares_dk <- 0
        shares_adr <- floor(cash / row$ADR)
        cash <- cash - shares_adr * row$ADR
      }
    }
    value <- shares_adr * row$ADR + shares_dk * row$DK + cash
    portfolio[i, c("cash", "adr", "dk", "value")] <- list(cash, shares_adr, shares_dk, value)
  }
  portfolio <- portfolio %>%
    mutate(
      ADR_only = initial_capital * prices$ADR / prices$ADR[1],
      DK_only = initial_capital * prices$DK / prices$DK[1]
    )
  list(portfolio = portfolio, rebalances = rebalance_dates)
}

# Plot
plot_strategy <- function(simulation) {
  portfolio <- simulation$portfolio
  rebal <- tibble(date = as.Date(simulation$rebalances), y = max(portfolio$value, na.rm = TRUE) * 1.01)
  df <- portfolio %>%
    mutate(date = as.Date(date)) %>%
    select(date, Strategy = value, ADR = ADR_only, Denmark = DK_only) %>%
    pivot_longer(-date, names_to = "Series", values_to = "Value")
  
  ggplot(df, aes(x = date, y = Value, color = Series)) +
    geom_line(size = 1.1) +
    geom_point(data = rebal, aes(x = date, y = y),
               inherit.aes = FALSE, color = "red", size = 0.5, shape = 18) +
    labs(
      title = "Z-score Strategy: Novo Nordisk (ADR vs Denmark)",
      subtitle = "Dynamic rebalancing when price ratio z-score exceeds ??1",
      y = "Portfolio Value (USD)",
      caption = "Data: Yahoo Finance | Strategy: BuyPolar Capital"
    ) +
    theme_economist_white() +
    scale_color_manual(values = c("Strategy" = "#2c3e50", "ADR" = "#e74c3c", "Denmark" = "#3498db")) +
    theme(legend.title = element_blank()) +
    scale_y_continuous(labels = dollar_format(scale = 1e-6, suffix = "M"))
}

# Run + Save
sim <- simulate_strategy(full_prices)
p <- plot_strategy(sim)

if (!dir.exists("plots")) dir.create("plots")
ggsave("plots/novo_zscore_strategy.pdf", p, width = 10, height = 6)
