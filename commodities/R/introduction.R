library(quantmod)
library(tidyverse)
library(lubridate)
library(zoo)

# Set working directory to the script location (if needed)
# setwd("path/to/your/R")

# Make sure plots directory exists
dir.create("plots", showWarnings = FALSE)

# Yahoo Finance tickers and names
commodities <- c(
  "CL=F" = "Crude Oil WTI",
  "BZ=F" = "Brent Oil",
  "NG=F" = "Natural Gas",
  "GC=F" = "Gold",
  "SI=F" = "Silver",
  "HG=F" = "Copper",
  "PL=F" = "Platinum",
  "PA=F" = "Palladium",
  "ZC=F" = "Corn",
  "ZW=F" = "Wheat",
  "ZS=F" = "Soybeans",
  "KC=F" = "Coffee",
  "CT=F" = "Cotton",
  "SB=F" = "Sugar",
  "LE=F" = "Live Cattle",
  "HE=F" = "Lean Hogs"
)

# Download 2 years of daily data
getSymbols(names(commodities), src = "yahoo", from = Sys.Date() - years(2))

# Helper function
tidy_commodity <- function(ticker, name) {
  data <- get(ticker)
  
  # Drop entirely missing rows early
  data <- na.omit(data)
  if (nrow(data) == 0) return(NULL)
  
  # Clean columns: use coredata() and drop to vector
  price_raw <- as.numeric(Cl(data))
  volume_raw <- as.numeric(Vo(data))
  
  price_clean <- na.approx(price_raw, na.rm = FALSE)
  volume_clean <- na.locf(volume_raw, na.rm = FALSE)
  
  # Avoid issues if still full of NAs
  if (all(is.na(price_clean))) return(NULL)
  
  df <- tibble(
    Date = index(data),
    Price = price_clean,
    Volume = volume_clean,
    Commodity = name
  ) %>%
    mutate(Relative_Change = Price / first(na.omit(Price)) * 100)
  
  return(df)
}


# Create tidy data frame
tidy_data <- map2_dfr(names(commodities), commodities, tidy_commodity)

# Add log-transformed columns
tidy_data <- tidy_data %>%
  mutate(
    Log_Price = log(Price),
    Log_Volume = log(Volume),
    Log_Relative_Change = log(Relative_Change)
  )


# 1?????? Prices
p1 <- ggplot(tidy_data, aes(x = Date, y = Price)) +
  geom_line(color = "red") +
  facet_wrap(~ Commodity, scales = "free_y", ncol = 4) +
  labs(title = "Commodity Prices (Last 2 Years)", y = "Price (USD)", x = NULL) +
  theme_minimal()

ggsave("plots/prices.pdf", p1, width = 12, height = 10)

# 2?????? Volumes
p2 <- ggplot(tidy_data, aes(x = Date, y = Volume)) +
  geom_line(color = "red") +
  facet_wrap(~ Commodity, scales = "free_y", ncol = 4) +
  labs(title = "Commodity Trading Volume", y = "Volume", x = NULL) +
  theme_minimal()

ggsave("plots/volumes.pdf", p2, width = 12, height = 10)

# 3?????? Relative Change
p3 <- ggplot(tidy_data, aes(x = Date, y = Relative_Change)) +
  geom_line(color = "red") +
  facet_wrap(~ Commodity, scales = "free_y", ncol = 4) +
  labs(title = "Relative Commodity Price Change (Indexed to 100)", y = "Relative Price", x = NULL) +
  theme_minimal()

ggsave("plots/relative_change.pdf", p3, width = 12, height = 10)

# 1?????? Log Prices
p4 <- ggplot(tidy_data, aes(x = Date, y = Log_Price)) +
  geom_line(color = "red") +
  facet_wrap(~ Commodity, scales = "fixed", ncol = 4) +
  labs(title = "Log-Transformed Commodity Prices", y = "log(Price)", x = NULL) +
  theme_minimal()

ggsave("plots/log_prices.pdf", p4, width = 12, height = 10)

# 2?????? Log Volumes
p5 <- ggplot(tidy_data, aes(x = Date, y = Log_Volume)) +
  geom_line(color = "red") +
  facet_wrap(~ Commodity, scales = "fixed", ncol = 4) +
  labs(title = "Log-Transformed Trading Volume", y = "log(Volume)", x = NULL) +
  theme_minimal()

ggsave("plots/log_volumes.pdf", p5, width = 12, height = 10)

# 3?????? Log Relative Change
p6 <- ggplot(tidy_data, aes(x = Date, y = Log_Relative_Change)) +
  geom_line(color = "darkgreen") +
  facet_wrap(~ Commodity, scales = "fixed", ncol = 4) +
  labs(title = "Log-Transformed Relative Price Change", y = "log(Relative Price)", x = NULL) +
  theme_minimal()

ggsave("plots/log_relative_change.pdf", p6, width = 12, height = 10)
