library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(gridExtra)

# Load BRK.A and BRK.B data
tickers <- c("BRK-A", "BRK-B")
full_prices <- tq_get(tickers, from = "1996-01-01", to = Sys.Date(), get = "stock.prices") %>%
  select(date, symbol, adjusted) %>%
  pivot_wider(names_from = symbol, values_from = adjusted) %>%
  tidyr::drop_na() %>%
  mutate(ratio = `BRK-A` / `BRK-B`)


# Strategy simulation function
simulate_strategy <- function(prices, initial_capital = 1e7) {
  portfolio <- tibble(
    date = prices$date,
    cash = NA_real_,
    brka = NA_real_,
    brkb = NA_real_,
    value = NA_real_
  )
  
  rebalance_dates <- c()
  
  first <- prices[1, ]
  if (first$ratio > 1500) {
    shares_brkb <- floor(initial_capital / first$`BRK-B`)
    shares_brka <- 0
    cash <- initial_capital - shares_brkb * first$`BRK-B`
  } else {
    shares_brka <- floor(initial_capital / first$`BRK-A`)
    shares_brkb <- 0
    cash <- initial_capital - shares_brka * first$`BRK-A`
  }
  
  for (i in seq_len(nrow(prices))) {
    row <- prices[i, ]
    ratio <- row$ratio
    price_a <- row$`BRK-A`
    price_b <- row$`BRK-B`
    
    rebalance_now <- FALSE
    if (ratio > 1500 && shares_brka > 0) rebalance_now <- TRUE
    if (ratio < 1500 && shares_brkb > 0) rebalance_now <- TRUE
    
    if (rebalance_now) {
      rebalance_dates <- c(rebalance_dates, row$date)
      cash <- shares_brka * price_a + shares_brkb * price_b + cash
      if (ratio > 1500) {
        shares_brka <- 0
        shares_brkb <- floor(cash / price_b)
        cash <- cash - shares_brkb * price_b
      } else {
        shares_brkb <- 0
        shares_brka <- floor(cash / price_a)
        cash <- cash - shares_brka * price_a
      }
    }
    
    value <- shares_brka * price_a + shares_brkb * price_b + cash
    portfolio[i, c("cash", "brka", "brkb", "value")] <- list(cash, shares_brka, shares_brkb, value)
  }
  
  portfolio <- portfolio %>%
    mutate(
      brka_only = initial_capital * prices$`BRK-A` / prices$`BRK-A`[1],
      brkb_only = initial_capital * prices$`BRK-B` / prices$`BRK-B`[1]
    )
  
  return(list(portfolio = portfolio, rebalances = rebalance_dates))
}

# Plotting function with top segments for rebalances
plot_strategy <- function(simulation, log_scale = FALSE, label = "") {
  portfolio <- simulation$portfolio
  rebalance_dates <- simulation$rebalances
  
  plot_data <- portfolio %>%
    select(date, Strategy = value, `BRK.A` = brka_only, `BRK.B` = brkb_only) %>%
    pivot_longer(-date, names_to = "Series", values_to = "PortfolioValue")
  
  # Get Y-axis upper value for rebalance markers
  y_max <- max(plot_data$PortfolioValue, na.rm = TRUE)
  y_top <- if (log_scale) y_max * 1.05 else y_max * 1.01
  
  rebalance_segments <- tibble(
    date = as.Date(rebalance_dates),
    xstart = as.Date(rebalance_dates) - 1,
    xend = as.Date(rebalance_dates) + 1,
    y = y_top
  )
  
  p <- ggplot(plot_data, aes(x = date, y = PortfolioValue, color = Series)) +
    geom_line(size = 1.1) +
    geom_segment(data = rebalance_segments,
                 aes(x = xstart, xend = xend, y = y, yend = y),
                 inherit.aes = FALSE,
                 color = "gray40", linewidth = 0.8) +
    labs(
      title = paste("Strategy vs BRK.A and BRK.B", label),
      subtitle = "Simulated $10M portfolio, rebalanced when BRK.A / BRK.B deviates from 1500",
      x = NULL,
      y = "Portfolio Value (USD)",
      caption = "Data: Yahoo Finance | Strategy: BuyPolar Capital"
    ) +
    theme_economist_white() +
    scale_color_manual(values = c("Strategy" = "#2c3e50", "BRK.A" = "#e74c3c", "BRK.B" = "#3498db")) +
    theme(
      text = element_text(family = "serif", size = 12),
      legend.title = element_blank(),
      legend.position = "bottom"
    )
  
  if (log_scale) {
    p <- p + scale_y_log10(labels = dollar_format(scale = 1e-6, suffix = "M"))
  } else {
    p <- p + scale_y_continuous(labels = dollar_format(scale = 1e-6, suffix = "M"))
  }
  
  return(p)
}

# Start dates
start_dates <- list(
  "From 1996" = ymd("1996-01-01"),
  "From 1996 (log scale)" = ymd("1996-01-01"),
  "From 2000" = ymd("2000-01-01"),
  "From 2010" = ymd("2010-01-01"),
  "From 2020" = ymd("2020-01-01")
)

# Run simulations + generate plots
plots <- list()
i <- 1
for (name in names(start_dates)) {
  from_date <- start_dates[[name]]
  filtered_prices <- full_prices %>% filter(date >= from_date)
  sim <- simulate_strategy(filtered_prices)
  
  log_scale <- str_detect(name, "log")
  plots[[i]] <- plot_strategy(sim, log_scale = log_scale, label = name)
  i <- i + 1
}

# Output all to PDF
if (!dir.exists("plots")) dir.create("plots")
pdf("plots/berkshire_strategy_plots.pdf", width = 10, height = 6)
for (plot in plots) print(plot)
dev.off()
