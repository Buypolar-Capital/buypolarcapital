# Load required packages
library(tidyverse)
library(tidyquant)
library(fpp3)

# Define tickers
tickers <- c("EQNR.OL", "NHY.OL", "YAR.OL", "TEL.OL", "ORK.OL",
             "DNB.OL", "SALM.OL", "MOWI.OL", "TOM.OL")

# Download stock prices
stock_data <- tq_get(tickers,
                     from = "2023-01-01",
                     to = Sys.Date(),
                     get = "stock.prices") %>%
  select(symbol, date, adjusted)

# Compute daily log returns and convert to tsibble
returns_ts <- stock_data %>%
  group_by(symbol) %>%
  arrange(date) %>%
  mutate(return = difference(log(adjusted))) %>%
  ungroup() %>%
  filter(!is.na(return)) %>%
  as_tsibble(index = date, key = symbol)

# Create faceted plot of returns
returns_plot <- returns_ts %>%
  ggplot(aes(x = date, y = return)) +
  geom_line(color = "steelblue") +
  geom_hline(yintercept = 0, linetype = "dotted", color = "red") +
  facet_wrap(~ symbol, scales = "free_y", ncol = 3) +
  labs(
    title = "Daily Log Returns of Selected Norwegian Stocks",
    subtitle = "Simulated white-noise style series",
    x = "Date", y = "Log Return"
  ) +
  theme_minimal()

# Save plot to PDF
ggsave(
  filename = "all_returns.pdf",
  path = "../plots",
  plot = returns_plot,
  width = 12,
  height = 8
)
