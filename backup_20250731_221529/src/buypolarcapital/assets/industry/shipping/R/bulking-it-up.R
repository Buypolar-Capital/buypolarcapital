# INSTALL IF NEEDED
library(tidyquant)
library(tidyverse)
library(lubridate)
library(gridExtra)
library(ggcorrplot)
library(zoo)

# --- PARAMETERS ---
tickers <- c("FRO", "GOGL", "STNG", "DHT", "EURN", "ZIM", "MATX", "CL=F")  # CL=F = Oil
commodities <- c("CL=F", "KOL", "PICK")  # Oil, Coal ETF, Metals/Mining ETF
start_date <- "2005-01-01"
end_date <- "2025-01-01"

# --- DOWNLOAD DATA ---
all_data <- tq_get(unique(c(tickers, commodities)),
                   from = start_date,
                   to   = end_date,
                   get = "stock.prices")

# --- DAILY LAG-1 RETURN ---
returns_data <- all_data %>%
  group_by(symbol) %>%
  arrange(date) %>%
  mutate(return = close / lag(close, 1),
         log_return = log(close / lag(close))) %>%
  ungroup()

# --- RECESSION PERIODS ---
recessions <- tibble(
  start = as.Date(c("2007-10-01", "2020-02-01")),
  end   = as.Date(c("2009-06-01", "2020-05-01")),
  label = c("Financial Crisis", "COVID-19")
)

# --- PAGE 1: 2x2 FACET RETURN PLOTS ---
grouped_syms <- split(tickers, ceiling(seq_along(tickers)/4))
plots1 <- map(grouped_syms, function(group_syms) {
  returns_data %>%
    filter(symbol %in% group_syms) %>%
    ggplot(aes(x = date, y = return)) +
    geom_rect(data = recessions,
              aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf, fill = label),
              inherit.aes = FALSE, alpha = 0.2) +
    geom_line(size = 0.3) +
    facet_wrap(~symbol, ncol = 2, scales = "free_y") +
    scale_fill_manual(values = c("Financial Crisis" = "blue", "COVID-19" = "green")) +
    labs(title = "Lag-1 Daily Returns",
         subtitle = paste(group_syms, collapse = ", "),
         y = "Return", x = "Date", fill = "Recession") +
    theme_minimal(base_size = 10)
})

# --- PAGE 2: TIME SERIES OF COMMODITY PRICES ---
commod_data <- returns_data %>%
  filter(symbol %in% commodities)

plots2 <- commod_data %>%
  ggplot(aes(x = date, y = close)) +
  geom_line() +
  facet_wrap(~symbol, ncol = 2, scales = "free_y") +
  labs(title = "Commodity Prices (Oil, Coal ETF, Metals ETF)",
       y = "Price", x = "Date") +
  theme_minimal(base_size = 10)

# --- PAGE 3: CORRELATION HEATMAP ---
wide_returns <- returns_data %>%
  filter(symbol %in% c(tickers, commodities)) %>%
  select(date, symbol, log_return) %>%
  pivot_wider(names_from = symbol, values_from = log_return)

cor_mat <- cor(wide_returns %>% select(-date), use = "pairwise.complete.obs")
plot3 <- ggcorrplot(cor_mat, lab = TRUE, title = "Correlation: Shipping vs Commodities")

# --- PAGE 4: SIMULATED SHIPPING INDICES (BDI & Harpex) ---
set.seed(2025)
shipping_index <- tibble(
  date = seq(as.Date("2005-01-01"), as.Date("2025-01-01"), by = "week"),
  BDI = cumsum(rnorm(length(date), 0, 10)) + 1500,
  Harpex = cumsum(rnorm(length(date), 0, 5)) + 1000
) %>%
  pivot_longer(-date, names_to = "index", values_to = "value")

plot4 <- shipping_index %>%
  ggplot(aes(x = date, y = value)) +
  geom_line() +
  facet_wrap(~index, ncol = 2, scales = "free_y") +
  labs(title = "Simulated Baltic Dry Index & Harpex",
       y = "Index Value", x = "Date") +
  theme_minimal()

# --- PAGE 5: 30-DAY ROLLING VOLATILITY ---
vol_data <- returns_data %>%
  filter(symbol %in% tickers) %>%
  group_by(symbol) %>%
  arrange(date) %>%
  mutate(roll_vol = rollapply(log_return, width = 30, FUN = sd, fill = NA, align = "right")) %>%
  ungroup()

plot5 <- vol_data %>%
  ggplot(aes(x = date, y = roll_vol)) +
  geom_line() +
  facet_wrap(~symbol, ncol = 2, scales = "free_y") +
  labs(title = "30-Day Rolling Volatility (Log Returns)",
       y = "Volatility", x = "Date") +
  theme_minimal()

# --- PAGE 6: RISK-RETURN SCATTERPLOT ---
scatter_data <- returns_data %>%
  filter(symbol %in% tickers) %>%
  group_by(symbol) %>%
  summarise(mean_return = mean(log_return, na.rm = TRUE),
            sd_return = sd(log_return, na.rm = TRUE))

plot6 <- ggplot(scatter_data, aes(x = sd_return, y = mean_return, label = symbol)) +
  geom_point(color = "steelblue", size = 3) +
  geom_text(nudge_y = 0.0005) +
  labs(title = "Risk vs Return (Log Returns)",
       x = "Standard Deviation (Risk)",
       y = "Mean Log Return") +
  theme_minimal()

# --- EXPORT 6-PAGE PDF ---
if (!dir.exists("plots")) dir.create("plots")

pdf("plots/bpc_shipping_mega_report.pdf", width = 11, height = 8.5)

walk(plots1, print)       # Page 1: Returns
print(plots2)             # Page 2: Commodities
print(plot3)              # Page 3: Correlation heatmap
print(plot4)              # Page 4: Shipping indices
print(plot5)              # Page 5: Volatility
print(plot6)              # Page 6: Risk-return

dev.off()

cat("??? Mega shipping report saved as: plots/bpc_shipping_mega_report.pdf\n")
