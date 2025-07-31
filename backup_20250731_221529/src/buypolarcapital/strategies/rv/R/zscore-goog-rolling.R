library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(zoo)

tickerA <- "GOOG"
tickerB <- "GOOGL"
rolling_windows <- c(10, 20, 30, 60, 90, 120)
initial_capital <- 1e7
threshold <- 1

simulate_strategy <- function(prices, colA, colB, threshold, initial_capital) {
  portfolio <- tibble(date = prices$date, cash = NA, A = NA, B = NA, value = NA)
  
  first <- prices[1, ]
  if (first$z_score > 0) {
    shares_B <- floor(initial_capital / first[[colB]])
    shares_A <- 0
    cash <- initial_capital - shares_B * first[[colB]]
  } else {
    shares_A <- floor(initial_capital / first[[colA]])
    shares_B <- 0
    cash <- initial_capital - shares_A * first[[colA]]
  }
  
  for (i in seq_len(nrow(prices))) {
    row <- prices[i, ]
    z <- row$z_score
    rebalance_now <- (z > threshold && shares_A > 0) || (z < -threshold && shares_B > 0)
    
    if (rebalance_now) {
      value_before <- shares_A * row[[colA]] + shares_B * row[[colB]] + cash
      cash <- value_before
      if (z > 0) {
        shares_A <- 0
        shares_B <- floor(cash / row[[colB]])
        cash <- cash - shares_B * row[[colB]]
      } else {
        shares_B <- 0
        shares_A <- floor(cash / row[[colA]])
        cash <- cash - shares_A * row[[colA]]
      }
    }
    
    value <- shares_A * row[[colA]] + shares_B * row[[colB]] + cash
    portfolio[i, c("cash", "A", "B", "value")] <- list(cash, shares_A, shares_B, value)
  }
  
  return(portfolio)
}

# Get historical prices for GOOG/GOOGL
prices <- tq_get(c(tickerA, tickerB), from = "2010-01-01", to = Sys.Date()) %>%
  select(date, symbol, adjusted) %>%
  pivot_wider(names_from = symbol, values_from = adjusted) %>%
  drop_na()

# Simulate for different rolling windows
strategy_results <- list()

for (win in rolling_windows) {
  df <- prices %>%
    mutate(
      ratio = !!sym(tickerA) / !!sym(tickerB),
      roll_mean = rollmean(ratio, win, fill = NA, align = "right"),
      roll_sd = rollapply(ratio, win, sd, fill = NA, align = "right"),
      z_score = (ratio - roll_mean) / roll_sd
    ) %>%
    drop_na()
  
  strat <- simulate_strategy(df, tickerA, tickerB, threshold, initial_capital)
  strat <- strat %>% select(date, value) %>% mutate(window = paste0("Rolling_", win, "d"))
  strategy_results[[as.character(win)]] <- strat
}

# Combine all into one df for plotting
df_all <- bind_rows(strategy_results)

# Plot
p <- ggplot(df_all, aes(x = date, y = value, color = window)) +
  geom_line(size = 1.1) +
  labs(
    title = "Dual Arbitrage Strategy: GOOG vs GOOGL",
    subtitle = "Comparison of different rolling window lengths (Z-score threshold ??1)",
    y = "Portfolio Value (USD)",
    x = "Date",
    caption = "Data: Yahoo Finance | Strategy: BuyPolar Capital"
  ) +
  theme_economist_white() +
  scale_color_brewer(palette = "Dark2") +
  scale_y_continuous(labels = dollar_format(scale = 1e-6, suffix = "M")) +
  theme(legend.title = element_blank())

# Save
if (!dir.exists("plots")) dir.create("plots")
ggsave("plots/dual_arbitrage_GOOG_GOOGL_rolling_comparison.pdf", p, width = 12, height = 7)

print(p)
