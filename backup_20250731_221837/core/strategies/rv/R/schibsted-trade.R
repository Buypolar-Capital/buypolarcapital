library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(zoo)

# ??? Load Schibsted A and B (working tickers)
tickers <- c("SCHA.OL", "SCHB.OL")
full_prices <- tq_get(tickers, from = "2005-01-01", to = Sys.Date()) %>%
  select(date, symbol, adjusted) %>%
  pivot_wider(names_from = symbol, values_from = adjusted) %>%
  tidyr::drop_na() %>%
  rename(A = `SCHA.OL`, B = `SCHB.OL`) %>%
  mutate(
    ratio = A / B,
    rolling_mean = rollmean(ratio, k = 30, fill = NA, align = "right"),
    rolling_sd = rollapply(ratio, 30, sd, fill = NA, align = "right"),
    z_score = (ratio - rolling_mean) / rolling_sd
  ) %>%
  drop_na()

# ???? Z-score strategy simulation
simulate_strategy_zscore <- function(prices, threshold = 1, initial_capital = 1e7) {
  portfolio <- tibble(
    date = prices$date,
    cash = NA_real_,
    A = NA_real_,
    B = NA_real_,
    value = NA_real_
  )
  
  rebalance_dates <- c()
  first <- prices[1, ]
  if (first$z_score > 0) {
    shares_B <- floor(initial_capital / first$B)
    shares_A <- 0
    cash <- initial_capital - shares_B * first$B
  } else {
    shares_A <- floor(initial_capital / first$A)
    shares_B <- 0
    cash <- initial_capital - shares_A * first$A
  }
  
  for (i in seq_len(nrow(prices))) {
    row <- prices[i, ]
    z <- row$z_score
    price_A <- row$A
    price_B <- row$B
    
    rebalance_now <- FALSE
    if (z > threshold && shares_A > 0) rebalance_now <- TRUE
    if (z < -threshold && shares_B > 0) rebalance_now <- TRUE
    
    if (rebalance_now) {
      rebalance_dates <- c(rebalance_dates, row$date)
      cash <- shares_A * price_A + shares_B * price_B + cash
      if (z > 0) {
        shares_A <- 0
        shares_B <- floor(cash / price_B)
        cash <- cash - shares_B * price_B
      } else {
        shares_B <- 0
        shares_A <- floor(cash / price_A)
        cash <- cash - shares_A * price_A
      }
    }
    
    value <- shares_A * price_A + shares_B * price_B + cash
    portfolio[i, c("cash", "A", "B", "value")] <- list(cash, shares_A, shares_B, value)
  }
  
  portfolio <- portfolio %>%
    mutate(
      A_only = initial_capital * prices$A / prices$A[1],
      B_only = initial_capital * prices$B / prices$B[1]
    )
  
  return(list(portfolio = portfolio, rebalances = rebalance_dates))
}

# ???? Plotting function
plot_strategy <- function(simulation, label = "") {
  portfolio <- simulation$portfolio
  rebalance_dates <- simulation$rebalances
  
  plot_data <- portfolio %>%
    select(date, Strategy = value, `Schibsted A` = A_only, `Schibsted B` = B_only) %>%
    pivot_longer(-date, names_to = "Series", values_to = "PortfolioValue")
  
  y_max <- max(plot_data$PortfolioValue, na.rm = TRUE)
  y_top <- y_max * 1.01
  
  rebalance_points <- tibble(date = as.Date(rebalance_dates), y = y_top)
  
  p <- ggplot(plot_data, aes(x = date, y = PortfolioValue, color = Series)) +
    geom_line(size = 1.1) +
    geom_point(data = rebalance_points,
               aes(x = date, y = y),
               inherit.aes = FALSE,
               color = "red", size = 0.5, shape = 18) +
    labs(
      title = paste("Z-score Strategy vs Schibsted A and B", label),
      subtitle = "Rebalanced when price ratio z-score crosses ??1 (30-day rolling)",
      x = NULL,
      y = "Portfolio Value (NOK)",
      caption = "Data: Yahoo Finance | Strategy: BuyPolar Capital"
    ) +
    theme_economist_white() +
    scale_color_manual(values = c("Strategy" = "#2c3e50", "Schibsted A" = "#e74c3c", "Schibsted B" = "#3498db")) +
    theme(
      text = element_text(family = "serif", size = 12),
      legend.title = element_blank(),
      legend.position = "bottom"
    ) +
    scale_y_continuous(labels = dollar_format(prefix = "kr", big.mark = " ", scale = 1e-6, suffix = "M"))
  
  return(p)
}

# ???? Run and save
sim <- simulate_strategy_zscore(full_prices)
p <- plot_strategy(sim)

if (!dir.exists("plots")) dir.create("plots")
ggsave("plots/schibsted_zscore_strategy.pdf", p, width = 10, height = 6)
