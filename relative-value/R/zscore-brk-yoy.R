library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(zoo)

# SETTINGS
tickerA <- "GOOG"
tickerB <- "GOOGL"
initial_capital <- 1e7
threshold <- 1
rolling_window <- 30

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

# Fetch & prepare data
prices <- tq_get(c(tickerA, tickerB), from = "2010-01-01", to = Sys.Date()) %>%
  select(date, symbol, adjusted) %>%
  pivot_wider(names_from = symbol, values_from = adjusted) %>%
  drop_na()

prices <- prices %>%
  mutate(
    ratio = !!sym(tickerA) / !!sym(tickerB),
    roll_mean = rollmean(ratio, rolling_window, fill = NA, align = "right"),
    roll_sd = rollapply(ratio, rolling_window, sd, fill = NA, align = "right"),
    z_score = (ratio - roll_mean) / roll_sd,
    year = year(date)
  ) %>%
  drop_na()

years <- unique(prices$year)
plot_list <- list()

for (yr in years) {
  df_year <- prices %>% filter(year == yr)
  if (nrow(df_year) < rolling_window) next
  
  # Strategy simulation
  strat <- simulate_strategy(df_year, tickerA, tickerB, threshold, initial_capital) %>%
    select(date, value) %>%
    rename(strategy = value)
  
  # Benchmarks scaled to same initial capital
  rebased <- df_year %>%
    select(date, !!sym(tickerA), !!sym(tickerB)) %>%
    mutate(
      A_val = !!sym(tickerA) / first(!!sym(tickerA)) * initial_capital,
      B_val = !!sym(tickerB) / first(!!sym(tickerB)) * initial_capital
    ) %>%
    select(date, A_val, B_val)
  
  # Merge all
  merged <- left_join(strat, rebased, by = "date") %>%
    pivot_longer(cols = c("strategy", "A_val", "B_val"), names_to = "type", values_to = "value")
  
  label_map <- c(strategy = "Dual Strategy", A_val = tickerA, B_val = tickerB)
  
  p <- ggplot(merged, aes(x = date, y = value, color = type)) +
    geom_line(size = 1.1) +
    labs(
      title = paste("Year", yr, "-", tickerA, "vs", tickerB),
      subtitle = paste("Dual Arbitrage vs Benchmarks | Rolling", rolling_window, "d | Threshold ??", threshold),
      x = "Date", y = "Portfolio Value (USD)",
      caption = "Data: Yahoo Finance | Strategy: BuyPolar Capital"
    ) +
    scale_color_manual(values = c("Dual Strategy" = "#1b9e77", tickerA = "#d95f02", tickerB = "#7570b3"),
                       labels = label_map, name = NULL) +
    scale_y_continuous(labels = dollar_format(scale = 1e-6, suffix = "M")) +
    theme_economist_white()
  
  plot_list[[as.character(yr)]] <- p
}

# Export PDF
if (!dir.exists("plots")) dir.create("plots")
pdf("plots/dual_arbitrage_yoy_vs_benchmarks_GOOG_GOOGL.pdf", width = 11, height = 7)
for (p in plot_list) print(p)
dev.off()
