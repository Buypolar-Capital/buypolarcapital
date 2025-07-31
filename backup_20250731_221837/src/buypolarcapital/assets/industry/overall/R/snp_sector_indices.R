library(tidyverse)
library(tidyquant)

# Create plots directory if it doesn't exist
dir.create("plots", showWarnings = FALSE)

# Define tickers for S&P 500 and all 11 sector indices
tickers <- c(
  "^GSPC",      # S&P 500
  "^SP500-10",  # Energy
  "^SP500-15",  # Materials
  "^SP500-20",  # Industrials
  "^SP500-25",  # Consumer Discretionary
  "^SP500-30",  # Consumer Staples
  "^SP500-35",  # Health Care
  "^SP500-40",  # Financials
  "^SP500-45",  # Information Technology
  "^SP500-50",  # Communication Services
  "^SP500-55",  # Utilities
  "^SP500-60"   # Real Estate
)

# Set date range (start at 2010 to avoid data gaps)
start_date <- "2010-01-01"
end_date <- Sys.Date()

# Fetch data with error handling
sector_data <- map_dfr(tickers, function(ticker) {
  tryCatch({
    tq_get(ticker, from = start_date, to = end_date, get = "stock.prices") %>%
      mutate(symbol = ticker)
  }, error = function(e) {
    message("Failed to fetch data for ticker: ", ticker)
    return(NULL)
  })
})

# Save raw data for debugging
write_csv(sector_data, "plots/sector_data_raw.csv")

# Check for missing tickers
fetched_tickers <- unique(sector_data$symbol)
missing_tickers <- setdiff(tickers, fetched_tickers)
if (length(missing_tickers) > 0) {
  message("Missing data for tickers: ", paste(missing_tickers, collapse = ", "))
}

# Normalize to 100 at start_date
sector_normalized <- sector_data %>%
  group_by(symbol) %>%
  filter(!is.na(adjusted)) %>%
  mutate(normalized = 100 * adjusted / first(adjusted)) %>%
  ungroup()

# Create plot and save as PDF
pdf(file = "plots/sp500_sectors.pdf",
    width = 12,
    height = 8)

sector_normalized %>%
  select(symbol, date, normalized) %>%
  pivot_longer(cols = normalized, names_to = "metric", values_to = "value") %>%
  mutate(symbol = case_when(
    symbol == "^GSPC" ~ "S&P 500",
    symbol == "^SP500-10" ~ "Energy",
    symbol == "^SP500-15" ~ "Materials",
    symbol == "^SP500-20" ~ "Industrials",
    symbol == "^SP500-25" ~ "Consumer Discretionary",
    symbol == "^SP500-30" ~ "Consumer Staples",
    symbol == "^SP500-35" ~ "Health Care",
    symbol == "^SP500-40" ~ "Financials",
    symbol == "^SP500-45" ~ "Information Technology",
    symbol == "^SP500-50" ~ "Communication Services",
    symbol == "^SP500-55" ~ "Utilities",
    symbol == "^SP500-60" ~ "Real Estate"
  )) %>%
  ggplot(aes(x = date, y = value, colour = symbol)) +
  geom_line() +
  labs(
    title = "S&P 500 and Sector Indices (Normalized, 2010=100)",
    x = "Date Surveyed",
    y = "Index Value (Normalized to 100)",
    colour = "Index"
  ) +
  theme_bw() +
  scale_y_continuous(labels = scales::comma) +
  theme(
    legend.position = "bottom",
    legend.title = element_text(size = 10),
    legend.text = element_text(size = 8),
    plot.title = element_text(hjust = 0.5)
  ) +
  guides(colour = guide_legend(nrow = 2))

dev.off()