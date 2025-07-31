library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(zoo)
library(ggthemes)
library(showtext)

# Google Fonts ??? close to Goldman Sachs look
font_add_google("Montserrat", "gs_font")
showtext_auto()

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

# Get and prep data
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
  
  # Benchmarks
  rebased <- df_year %>%
    select(date, !!sym(tickerA), !!sym(tickerB)) %>%
    mutate(
      A_val = !!sym(tickerA) / first(!!sym(tickerA)) * initial_capital,
      B_val = !!sym(tickerB) / first(!!sym(tickerB)) * initial_capital
    ) %>%
    select(date, A_val, B_val)
  
  # Merge and rename types
  merged <- left_join(strat, rebased, by = "date") %>%
    pivot_longer(cols = c("strategy", "A_val", "B_val"), names_to = "type", values_to = "value") %>%
    mutate(type = recode(type,
                         strategy = "Dual Strategy",
                         A_val = tickerA,
                         B_val = tickerB))
  
  # Color mapping Goldman style
  color_map <- c(
    "Dual Strategy" = "#003366",  # deep navy
    tickerA = "#b30000",          # GS red
    tickerB = "#006d2c"           # GS green
  )
  
  # GS-style theme
  theme_gs <- theme_minimal(base_family = "gs_font") +
    theme(
      plot.title = element_text(face = "bold", size = 18, hjust = 0.5),
      plot.subtitle = element_text(size = 12, hjust = 0.5, margin = margin(b = 10)),
      axis.title = element_text(size = 11),
      axis.text = element_text(size = 10, color = "#333333"),
      legend.position = "top",
      legend.title = element_blank(),
      legend.margin = margin(b = -5),
      panel.grid.major = element_line(color = "#cccccc", size = 0.2),
      panel.grid.minor = element_blank(),
      plot.caption = element_text(size = 9, face = "italic", hjust = 0)
    )
  
  p <- ggplot(merged, aes(x = date, y = value, color = type)) +
    geom_line(linewidth = .5) +
    scale_color_manual(values = color_map) +
    scale_y_continuous(labels = dollar_format(scale = 1e-6, suffix = "M")) +
    labs(
      title = paste("Dual Arbitrage Strategy vs Benchmarks ???", yr),
      subtitle = paste(tickerA, "vs", tickerB, "| Rolling", rolling_window, "d | Threshold ??", threshold),
      x = NULL, y = "Portfolio Value (USD)",
      caption = "Source: Yahoo Finance ?? Strategy: BuyPolar Capital"
    ) +
    theme_gs
  
  plot_list[[as.character(yr)]] <- p
}

# Output PDF
if (!dir.exists("plots")) dir.create("plots")
pdf("plots/dual_arbitrage_goldman_GOOG_GOOGL.pdf", width = 11, height = 7)
for (p in plot_list) print(p)
dev.off()
