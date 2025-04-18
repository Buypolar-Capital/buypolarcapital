
# File: dual_arbitrage_prettified.R
library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(zoo)

# Dual-listed pairs
pair_list <- list(
  c("GOOG", "GOOGL"),
  c("SCHA.OL", "SCHB.OL"),
  c("BRK-A", "BRK-B"),
  c("NOVO-B.CO", "NVO"),
  c("NESN.SW", "NSRGY"),
  c("TM", "7203.T"),
  c("AZN.L", "AZN"),
  c("RIO.L", "RIO"),
  c("BP.L", "BP"),
  c("GLEN.L", "GLNCY")
)

plot_list <- list()

# Strategy simulation with trade tracking
simulate_strategy <- function(prices, colA, colB, threshold = 1, initial_capital = 1e7) {
  portfolio <- tibble(date = prices$date, cash = NA, A = NA, B = NA, value = NA)
  trades <- tibble(date = as.Date(character()), profit = numeric())
  
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
      value_after <- shares_A * row[[colA]] + shares_B * row[[colB]] + cash
      trades <- trades %>% add_row(date = row$date, profit = value_after - value_before)
    }
    
    value <- shares_A * row[[colA]] + shares_B * row[[colB]] + cash
    portfolio[i, c("cash", "A", "B", "value")] <- list(cash, shares_A, shares_B, value)
  }
  
  portfolio <- portfolio %>%
    mutate(
      A_only = initial_capital * prices[[colA]] / prices[[colA]][1],
      B_only = initial_capital * prices[[colB]] / prices[[colB]][1]
    )
  
  list(portfolio = portfolio, trades = trades)
}

# Plotting with annotation
plot_strategy <- function(simulation, nameA, nameB) {
  portfolio <- simulation$portfolio
  trades <- simulation$trades
  rebalance_dates <- trades$date
  
  df <- portfolio %>%
    mutate(date = as.Date(date)) %>%
    select(date, Strategy = value, A = A_only, B = B_only) %>%
    rename(!!nameA := A, !!nameB := B) %>%
    pivot_longer(-date, names_to = "Series", values_to = "Value")
  
  num_trades <- nrow(trades)
  best_trade <- if (num_trades > 0) max(trades$profit) else NA
  final_val <- last(portfolio$value)
  final_A <- last(portfolio$A_only)
  final_B <- last(portfolio$B_only)
  years <- as.numeric(difftime(last(portfolio$date), first(portfolio$date), units = "days")) / 365.25
  cagr <- (final_val / 1e7)^(1 / years) - 1
  
  annotation_text <- paste0(
    "Trades: ", num_trades,
    " | Best Trade: $", round(best_trade, 0),
    "\nFinal: $", round(final_val, 0),
    " | ", nameA, ": $", round(final_A, 0),
    " | ", nameB, ": $", round(final_B, 0),
    "\nCAGR: ", percent(cagr, accuracy = 0.1)
  )
  
  rebal <- tibble(date = as.Date(rebalance_dates), y = max(df$Value, na.rm = TRUE) * 1.01)
  
  ggplot(df, aes(x = date, y = Value, color = Series)) +
    geom_line(size = 1.1) +
    geom_point(data = rebal, aes(x = date, y = y),
               inherit.aes = FALSE, color = "red", size = 0.5, shape = 18) +
    annotate("label", x = min(df$date) + 100, y = max(df$Value, na.rm = TRUE) * 0.80,
             label = annotation_text, hjust = 0, size = 3.5, fill = "white", alpha = 0.8) +
    labs(
      title = paste("Z-score Strategy:", nameA, "vs", nameB),
      subtitle = "Rebalanced when z-score crosses ??1 (30-day rolling)",
      y = "Portfolio Value (USD)",
      caption = "Data: Yahoo Finance | Strategy: BuyPolar Capital"
    ) +
    theme_economist_white() +
    scale_color_manual(values = setNames(c("#2c3e50", "#e74c3c", "#3498db"), c("Strategy", nameA, nameB))) +
    theme(legend.title = element_blank()) +
    scale_y_continuous(labels = dollar_format(scale = 1e-6, suffix = "M"))
}

# Loop through all real pairs
for (pair in pair_list) {
  tickerA <- pair[1]
  tickerB <- pair[2]
  tryCatch({
    prices <- tq_get(c(tickerA, tickerB), from = "2024-01-01", to = Sys.Date()) %>%
      select(date, symbol, adjusted) %>%
      pivot_wider(names_from = symbol, values_from = adjusted) %>%
      tidyr::drop_na()
    
    prices <- prices %>%
      mutate(
        ratio = !!sym(tickerA) / !!sym(tickerB),
        rolling_mean = rollmean(ratio, 30, fill = NA, align = "right"),
        rolling_sd = rollapply(ratio, 30, sd, fill = NA, align = "right"),
        z_score = (ratio - rolling_mean) / rolling_sd
      ) %>% drop_na()
    
    sim <- simulate_strategy(prices, tickerA, tickerB)
    p <- plot_strategy(sim, nameA = tickerA, nameB = tickerB)
    plot_list[[paste0("pair_", tickerA, "_", tickerB)]] <- p
  }, error = function(e) {
    message(paste("Pair error:", tickerA, "/", tickerB, "-", e$message))
  })
}

# Add 5 random pairs as control
set.seed(42)
all_stocks <- c("AAPL", "MSFT", "TSLA", "NVDA", "KO", "PEP", "DIS", "META", "AMZN", "XOM", "JPM", "WMT", "BA", "CRM", "IBM")
random_pairs <- replicate(5, sample(all_stocks, 2, replace = FALSE), simplify = FALSE)

for (pair in random_pairs) {
  tickerA <- pair[1]
  tickerB <- pair[2]
  tryCatch({
    prices <- tq_get(c(tickerA, tickerB), from = "2024-01-01", to = Sys.Date()) %>%
      select(date, symbol, adjusted) %>%
      pivot_wider(names_from = symbol, values_from = adjusted) %>%
      tidyr::drop_na()
    
    prices <- prices %>%
      mutate(
        ratio = !!sym(tickerA) / !!sym(tickerB),
        rolling_mean = rollmean(ratio, 30, fill = NA, align = "right"),
        rolling_sd = rollapply(ratio, 30, sd, fill = NA, align = "right"),
        z_score = (ratio - rolling_mean) / rolling_sd
      ) %>% drop_na()
    
    sim <- simulate_strategy(prices, tickerA, tickerB)
    p <- plot_strategy(sim, nameA = paste("RANDOM:", tickerA), nameB = tickerB)
    plot_list[[paste0("random_", tickerA, "_", tickerB)]] <- p
  }, error = function(e) {
    message(paste("Random pair error:", tickerA, "/", tickerB, "-", e$message))
  })
}

# Save all to PDF
if (!dir.exists("plots")) dir.create("plots")
pdf("plots/dual_arbitrage_2024.pdf", width = 10, height = 7.5)
for (p in plot_list) print(p)
dev.off()
