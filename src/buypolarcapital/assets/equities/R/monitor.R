

library(tidyverse)
library(lubridate)
library(ggplot2)
library(patchwork)  # for arranging multiple plots
library(quantmod)   # to get price data


# Define symbols (adjust or expand as needed)
indices <- c("^GSPC", "^DJI", "^IXIC", "^OSEBX.OL", "^VIX", "^FTSE", "^N225", "^HSI",
             "^STOXX50E", "^FCHI", "^GDAXI", "^BFX", "^AEX", "^OMX", "^BVSP", "^RUT")

stocks <- c("AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM",
            "BAC", "NFLX", "DIS", "V", "MA", "KO", "PEP", "WMT")

etfs <- c("SPY", "QQQ", "VTI", "IWM", "EFA", "VWO", "LQD", "HYG",
          "XLF", "XLY", "XLK", "XLE", "XLV", "XLI", "XLB", "XLRE")

commodities <- c("GC=F", "CL=F", "SI=F", "BZ=F", "NG=F", "HG=F", "ZC=F", "ZS=F",
                 "ZO=F", "CT=F", "CC=F", "KC=F", "SB=F", "LE=F", "HE=F", "LBS=F")

# Function to get 1-week return
get_return <- function(symbol) {
  tryCatch({
    data <- quantmod::getSymbols(symbol, from = Sys.Date() - 10, auto.assign = FALSE, warnings = FALSE)
    df <- data.frame(date = index(data), close = as.numeric(Cl(data)))
    df <- df %>% arrange(desc(date)) %>% distinct(date, .keep_all = TRUE)
    today <- df$close[1]
    last_week <- df$close[which(df$date <= Sys.Date() - 7)[1]]
    pct_change <- (today - last_week) / last_week * 100
    tibble(symbol = symbol, today = today, last_week = last_week, pct_change = pct_change)
  }, error = function(e) {
    message("Error for symbol: ", symbol)
    tibble(symbol = symbol, today = NA, last_week = NA, pct_change = NA)
  })
}

# Download all data
returns <- bind_rows(
  map(indices, get_return) %>% bind_rows() %>% mutate(type = "Index"),
  map(stocks, get_return) %>% bind_rows() %>% mutate(type = "Stock"),
  map(etfs, get_return) %>% bind_rows() %>% mutate(type = "ETF"),
  map(commodities, get_return) %>% bind_rows() %>% mutate(type = "Commodity")
)

# Drop missing returns
returns <- returns %>% drop_na(pct_change)

# Function to create individual vertical bar plots
make_plot <- function(sym, pct) {
  ggplot(data.frame(symbol = sym, pct_change = pct), aes(x = symbol, y = pct_change, fill = pct_change > 0)) +
    geom_col(show.legend = FALSE) +
    scale_fill_manual(values = c("TRUE" = "darkgreen", "FALSE" = "firebrick")) +
    geom_text(aes(label = sprintf("%.1f%%", pct_change)), vjust = -0.5, size = 3.5) +
    labs(title = sym, x = NULL, y = NULL) +
    theme_minimal(base_size = 10) +
    theme(axis.text.x = element_blank(),
          axis.ticks.x = element_blank(),
          plot.title = element_text(size = 11, hjust = 0.5))
}

# Function to make one page of 16 vertical bar plots
make_page <- function(df, category) {
  df <- df %>% filter(type == category) %>% arrange(desc(pct_change)) %>% head(16)
  plots <- map2(df$symbol, df$pct_change, make_plot)
  wrap_plots(plots, ncol = 4)
}

# Create 4 pages
page1 <- make_page(returns, "Index")
page2 <- make_page(returns, "Stock")
page3 <- make_page(returns, "ETF")
page4 <- make_page(returns, "Commodity")

# Save to PDF
pdf("plots/relative_change_report_full.pdf", width = 11, height = 8.5)  # Landscape
print(page1)
print(page2)
print(page3)
print(page4)
dev.off()
