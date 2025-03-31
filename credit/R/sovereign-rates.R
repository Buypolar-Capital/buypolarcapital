# credit/R/credit_report.R

library(tidyverse)
library(tidyquant)
library(lubridate)
library(gridExtra)
library(patchwork)
library(zoo)

# Load BuyPolar Capital plotting style
source("../../src/plotting/plotting.R")

# Setup folders
dir.create("../data", recursive = TRUE, showWarnings = FALSE)
dir.create("../plots", recursive = TRUE, showWarnings = FALSE)

# Define credit yield tickers
credit_series <- c(
  "BAMLC0A1CAAAEY"     = "AAA",
  "BAMLC0A3CAEY"       = "BBB",
  "BAMLHYH0A0HYM2TRIV" = "High_Yield"
)

# Download available series from FRED
credit_data <- tq_get(names(credit_series), get = "economic.data") %>%
  mutate(ticker = credit_series[symbol]) %>%
  rename(yield = price) %>%
  select(date, ticker, yield) %>%
  filter(!is.na(yield))

# Save data
write_csv(credit_data, "../data/credit_extended.csv")

# Wide format for calculations
credit_wide <- credit_data %>%
  pivot_wider(names_from = ticker, values_from = yield) %>%
  arrange(date)

# Check available tickers
available_yields <- intersect(names(credit_series), colnames(credit_wide))

# Plot 1: Raw yields over time
p1 <- ggplot(credit_data, aes(x = date, y = yield, color = ticker)) +
  geom_line() +
  labs(title = "Credit Yields Over Time", y = "Yield (%)") +
  theme_buypolar()

# Plot 2: BBB - AAA Spread (if both available)
p2 <- NULL
if (all(c("BBB", "AAA") %in% colnames(credit_wide))) {
  credit_wide <- credit_wide %>%
    mutate(spread_BBB_AAA = BBB - AAA)
  
  p2 <- ggplot(credit_wide, aes(x = date, y = spread_BBB_AAA)) +
    geom_line(color = "#b30000") +
    labs(title = "BBB - AAA Yield Spread", y = "Spread (%)") +
    theme_buypolar()
}

# Recalculate truly available tickers based on existing columns
available_yields <- intersect(credit_series, colnames(credit_wide)) |> unname()

# Only continue if we have valid tickers
if (length(available_yields) > 0) {
  # Construct volatility column names
  volatility_cols <- paste0(available_yields, "_vol")
  
  # Apply rolling volatility calculation
  vol_data <- credit_wide %>%
    mutate(across(all_of(available_yields), 
                  ~ rollapply(.x, width = 60, FUN = sd, fill = NA, align = "right"), 
                  .names = "{.col}_vol")) %>%
    select(date, all_of(volatility_cols)) %>%
    pivot_longer(cols = all_of(volatility_cols), names_to = "ticker", values_to = "volatility") %>%
    mutate(ticker = str_remove(ticker, "_vol")) %>%
    filter(!is.na(volatility))
  
  # Plot 3: Volatility chart
  p3 <- ggplot(vol_data, aes(x = date, y = volatility, color = ticker)) +
    geom_line() +
    labs(title = "Rolling 60-Day Yield Volatility", y = "Volatility (SD)") +
    theme_buypolar()
} else {
  warning("No valid yield columns available for volatility calculation.")
  p3 <- NULL
}



# Plot 4: Cumulative Return
if (length(available_yields) > 0) {
  returns_data <- credit_wide %>%
    mutate(across(all_of(available_yields), ~ c(NA, diff(.x)))) %>%
    pivot_longer(cols = all_of(available_yields), names_to = "ticker", values_to = "daily_return") %>%
    filter(!is.na(daily_return)) %>%
    group_by(ticker) %>%
    mutate(cumulative_return = cumsum(daily_return)) %>%
    ungroup()
  
  p4 <- ggplot(returns_data, aes(x = date, y = cumulative_return, color = ticker)) +
    geom_line() +
    labs(title = "Cumulative Return (Based on ?? Yield)", y = "Cumulative Change") +
    theme_buypolar()
} else {
  warning("No valid yield columns available for return calculation.")
  p4 <- NULL
}


# Save to multi-page PDF
pdf("plots/credit_multipage_report.pdf", width = 10, height = 6)
print(p1)
if (!is.null(p2)) print(p2)
if (!is.null(p3)) print(p3)
if (!is.null(p4)) print(p4)
dev.off()

cat("??? Multi-page credit report saved to: credit/plots/credit_multipage_report.pdf\n")
