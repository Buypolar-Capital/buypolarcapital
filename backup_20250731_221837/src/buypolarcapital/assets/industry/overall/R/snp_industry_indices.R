library(tidyverse)
library(tidyquant)

# Define tickers for selected industry/sub-industry indices
tickers <- c(
  "^SP500-401010",      # Banks (Financials)
  "^SP500-352020",      # Biotechnology (Health Care)
  "^SP500-45301020",    # Semiconductors (Information Technology)
  "^SP500-201010",      # Aerospace & Defense (Industrials)
  "^SP500-25502020"     # Internet & Direct Marketing Retail (Consumer Discretionary)
)

# Set date range
start_date <- "2000-01-01"
end_date <- Sys.Date()

# Fetch data
industry_data <- tq_get(tickers,
                        from = start_date,
                        to = end_date,
                        get = "stock.prices")

# Normalize to 100 at start_date
industry_normalized <- industry_data %>%
  group_by(symbol) %>%
  mutate(normalized = 100 * adjusted / first(adjusted)) %>%
  ungroup()

# Create plot and save as PDF
pdf(file = "plots/sp500_industries.pdf",
    width = 12,
    height = 8)

industry_normalized %>%
  select(symbol, date, normalized) %>%
  pivot_longer(cols = normalized, names_to = "metric", values_to = "value") %>%
  mutate(symbol = case_when(
    symbol == "^SP500-401010" ~ "Banks",
    symbol == "^SP500-352020" ~ "Biotechnology",
    symbol == "^SP500-45301020" ~ "Semiconductors",
    symbol == "^SP500-201010" ~ "Aerospace & Defense",
    symbol == "^SP500-25502020" ~ "Internet & Direct Marketing Retail"
  )) %>%
  ggplot(aes(x = date, y = value, colour = symbol)) +
  geom_line() +
  labs(
    title = "S&P 500 Industry Indices (Normalized, 2000=100)",
    x = "Date",
    y = "Index Value (Normalized to 100)",
    colour = "Industry"
  ) +
  theme_bw() +
  scale_y_continuous(labels = scales::comma) +
  theme(
    legend.position = "bottom",
    legend.title = element_text(size = 10),
    legend.text = element_text(size = 8),
    plot.title = element_text(hjust = 0.5)
  ) +
  guides(colour = guide_legend(nrow = 1))

dev.off()