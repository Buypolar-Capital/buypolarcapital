# INSTALL if needed
library(tidyquant)
library(tidyverse)
library(lubridate)
library(gridExtra)

# SELECT 32 long-listed volatile stocks
tickers <- c(
  "AAPL", "MSFT", "NVDA", "AMD", "INTC", "MU", "TXN", "IBM",
  "AMZN", "META", "NFLX", "GOOGL", "ORCL", "EBAY", "QCOM", "CRM",
  "JPM", "GS", "MS", "BAC", "C", "AXP", "USB", "WFC",
  "GE", "BA", "CAT", "F", "GM", "UPS", "HON", "LMT"
)

start_date <- "2000-01-01"
end_date <- "2025-01-01"

# DOWNLOAD PRICE DATA
stock_data <- tq_get(tickers,
                     from = start_date,
                     to   = end_date,
                     get = "stock.prices")

# CALCULATE DAILY LAG-1 RETURNS
returns_data <- stock_data %>%
  group_by(symbol) %>%
  arrange(date) %>%
  mutate(return = close / lag(close, 1)) %>%
  ungroup()

# DEFINE RECESSIONS
recessions <- tibble(
  start = as.Date(c("2000-03-01", "2007-10-01", "2020-02-01")),
  end   = as.Date(c("2002-10-01", "2009-06-01", "2020-05-01")),
  label = c("Tech Bubble", "Financial Crisis", "COVID-19")
)

# SPLIT INTO GROUPS OF 4 STOCKS EACH (2x2 FACETS)
stock_groups <- split(unique(returns_data$symbol), ceiling(seq_along(unique(returns_data$symbol))/4))

# MAKE PLOTS FOR EACH GROUP
plots <- map(stock_groups, function(group_syms) {
  returns_data %>%
    filter(symbol %in% group_syms) %>%
    ggplot(aes(x = date, y = return)) +
    geom_rect(data = recessions,
              aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf, fill = label),
              inherit.aes = FALSE, alpha = 0.2) +
    geom_line(color = "black", size = 0.3) +
    facet_wrap(~symbol, ncol = 2, scales = "free_y") +
    scale_fill_manual(values = c("Tech Bubble" = "red", "Financial Crisis" = "blue", "COVID-19" = "green")) +
    labs(title = "Lag-1 Return (Daily)",
         subtitle = paste("Stocks:", paste(group_syms, collapse = ", ")),
         y = "Return (Close / Lag 1)", x = "Date", fill = "Recession") +
    theme_minimal(base_size = 10) +
    theme(strip.text = element_text(face = "bold"))
})

# EXPORT MULTI-PAGE PDF
if (!dir.exists("plots")) dir.create("plots")

pdf("plots/volatile_stocks_32_multipage_2x2.pdf", width = 11, height = 8.5)  # landscape A4
walk(plots, print)
dev.off()

cat("??? Exported multi-page 2x2 PDF to 'plots/volatile_stocks_32_multipage_2x2.pdf'\n")
