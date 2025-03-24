library(tidyquant)
library(tidyverse)
library(fpp3)
library(scales)
library(zoo)
library(gridExtra)

# Create directory if it doesn't exist
if (!dir.exists("plots")) dir.create("plots")

# === PART 1: Time Series Summary Plots (ggplot2) ===

# Futures tickers from Yahoo Finance
futures_tickers <- c(
  "ES=F",   # S&P 500 E-mini
  "NQ=F",   # Nasdaq
  "CL=F",   # Crude Oil
  "GC=F",   # Gold
  "BTC-USD" # Bitcoin (spot, for flavor)
)

# Download data
futures_data <- tq_get(futures_tickers,
                       from = Sys.Date() - 365,
                       to = Sys.Date(),
                       get = "stock.prices")

# Normalize prices to 1 at the starting point
futures_normalized <- futures_data %>%
  group_by(symbol) %>%
  arrange(date) %>%
  mutate(normalized = close / first(close)) %>%
  ungroup()

# Calculate daily returns
futures_returns <- futures_data %>%
  group_by(symbol) %>%
  arrange(date) %>%
  mutate(daily_return = (close / lag(close)) - 1) %>%
  ungroup()

# Calculate 30-day rolling volatility (std dev of daily returns)
futures_volatility <- futures_returns %>%
  group_by(symbol) %>%
  arrange(date) %>%
  mutate(rolling_vol = rollapply(daily_return, width = 30, FUN = sd, fill = NA, align = "right")) %>%
  ungroup()

# Create PDF with all summary plots
pdf("plots/futures_analysis.pdf", width = 10, height = 6)

# --- Plot 1: Normalized Prices ---
plot1 <- ggplot(futures_normalized, aes(x = date, y = normalized, color = symbol)) +
  geom_line(size = 1) +
  scale_y_continuous(labels = percent_format(accuracy = 1)) +
  labs(title = "Normalized Prices of Futures (Base = 1)",
       y = "Normalized Price", x = "Date", color = "Contract") +
  theme_minimal()

# --- Plot 2: Daily Returns ---
plot2 <- ggplot(futures_returns, aes(x = date, y = daily_return, color = symbol)) +
  geom_line(alpha = 0.7) +
  scale_y_continuous(labels = percent_format(accuracy = 0.1)) +
  labs(title = "Daily Returns of Futures",
       y = "Daily Return", x = "Date", color = "Contract") +
  theme_minimal()

# --- Plot 3: 30-day Rolling Volatility ---
plot3 <- ggplot(futures_volatility, aes(x = date, y = rolling_vol, color = symbol)) +
  geom_line(size = 1) +
  scale_y_continuous(labels = percent_format(accuracy = 0.1)) +
  labs(title = "30-Day Rolling Volatility of Futures",
       y = "Volatility (Std Dev of Daily Returns)", x = "Date", color = "Contract") +
  theme_minimal()

print(plot1)
print(plot2)
print(plot3)
dev.off()

message("??? PDF with all plots saved to /plots/futures_analysis.pdf")


