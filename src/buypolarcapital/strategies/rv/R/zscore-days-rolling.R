# File: dual_arbitrage_window_comparison_top5.R
library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(zoo)

# Best-performing pairs
top_pairs <- list(
  c("GOOG", "GOOGL"),
  c("BRK-A", "BRK-B"),
  c("NOVO-B.CO", "NVO"),
  c("NESN.SW", "NSRGY"),
  c("AZN.L", "AZN")
)

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

# Master plot list
plot_list <- list()

# Loop through pairs and create rolling comparison plots
for (pair in top_pairs) {
  tickerA <- pair[1]
  tickerB <- pair[2]
  
  tryCatch({
    prices <- tq_get(c(tickerA, tickerB), from = "2010-01-01", to = Sys.Date()) %>%
      select(date, symbol, adjusted) %>%
      pivot_wider(names_from = symbol, values_from = adjusted) %>%
      drop_na()
    
    strategy_results <- list()
    
    for (win in rolling_windows) {
      df <- prices %>%
        mutate(
          ratio = !!sym(tickerA) / !!sym(tickerB),
          roll_mean = rollmean(ratio, win, fill = NA, align = "right"),
          roll_sd = rollapply(ratio, win, sd, fill = NA, align = "right"),
          z_score = (ratio - roll_mean) / roll_sd
        ) %>% drop_na()
      
      strat <- simulate_strategy(df, tickerA, tickerB, threshold, initial_capital)
      strat <- strat %>% select(date, value) %>% mutate(window = paste0(win, "d"))
      strategy_results[[as.character(win)]] <- strat
    }
    
    df_all <- bind_rows(strategy_results)
    
    p <- ggplot(df_all, aes(x = date, y = value, color = window)) +
      geom_line(size = 1.1) +
      labs(
        title = paste("Dual Arbitrage:", tickerA, "vs", tickerB),
        subtitle = "Portfolio value over time using various rolling z-score windows (threshold ??1)",
        y = "Portfolio Value (USD)", x = "Date",
        caption = "Data: Yahoo Finance | Strategy: BuyPolar Capital"
      ) +
      theme_economist_white() +
      scale_color_brewer(palette = "Dark2") +
      scale_y_continuous(labels = dollar_format(scale = 1e-6, suffix = "M")) +
      theme(legend.title = element_blank())
    
    plot_list[[paste0(tickerA, "_", tickerB)]] <- p
    
  }, error = function(e) {
    message(paste("Error on pair:", tickerA, "/", tickerB, "-", e$message))
  })
}

# Save all plots
if (!dir.exists("plots")) dir.create("plots")
pdf("plots/dual_arbitrage_rolling_window_comparison_top5.pdf", width = 11, height = 7)
for (p in plot_list) print(p)
dev.off()
