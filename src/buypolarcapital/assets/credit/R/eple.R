# LOAD LIBRARIES
library(tidyquant)
library(tidyverse)

# CREATE FOLDER IF NOT EXISTS
if (!dir.exists("plots")) dir.create("plots")

# --- DOWNLOAD AAPL ---
aapl <- tq_get("AAPL",
               from = "2015-01-01",
               to   = "2025-01-01",
               get  = "stock.prices")

# AAPL Price Plot
p_aapl_price <- aapl %>% 
  ggplot(aes(x = date, y = close)) +
  geom_line() +
  labs(title = "AAPL Close Price") +
  theme_minimal()

# AAPL Return Plot (365-day lag)
p_aapl_return <- aapl %>% 
  mutate(return = close / lag(close, 365)) %>% 
  select(date, return) %>% 
  ggplot(aes(x = date, y = return)) +
  geom_line() +
  geom_hline(yintercept = 1, lty = "dashed") +
  labs(title = "AAPL ~365-Day Rolling Return") +
  theme_classic()

# AAPL Return Plot (365-day lag)
p_aapl_return_day <- aapl %>% 
  mutate(return = close / lag(close, 1)) %>% 
  select(date, return) %>% 
  ggplot(aes(x = date, y = return)) +
  geom_line() +
  geom_hline(yintercept = 1, lty = "dashed") +
  labs(title = "AAPL ~1-Day Rolling Return") +
  theme_classic()

# EXPORT AAPL Return Plot
ggsave("plots/aapl_return.pdf", p_aapl_return, width = 9, height = 5)
ggsave("plots/aapl_return_day.pdf", p_aapl_return_day, width = 9, height = 5)
ggsave("plots/aapl_price.pdf", p_aapl_price, width = 9, height = 5)

# --- DOWNLOAD TSLA ---
tsla <- tq_get("TSLA",
               from = "2000-01-01",
               to   = "2025-01-01",
               get  = "stock.prices")

# TSLA Price Plot
p_tsla_price <- tsla %>% 
  ggplot(aes(x = date, y = close)) +
  geom_line() +
  labs(title = "TSLA Close Price") +
  theme_minimal()

# TSLA Return Plot (365-day lag)
p_tsla_return <- tsla %>% 
  mutate(return = close / lag(close, 365)) %>% 
  select(date, return) %>% 
  ggplot(aes(x = date, y = return)) +
  geom_line() +
  geom_hline(yintercept = 1, lty = "dashed") +
  labs(title = "TSLA ~365-Day Rolling Return") +
  theme_classic()

# TSLA Return Plot (365-day lag)
p_tsla_return_day <- tsla %>% 
  mutate(return = close / lag(close, 1)) %>% 
  select(date, return) %>% 
  ggplot(aes(x = date, y = return)) +
  geom_line() +
  geom_hline(yintercept = 1, lty = "dashed") +
  labs(title = "TSLA ~1-Day Rolling Return") +
  theme_classic()

# EXPORT TSLA Return Plot
ggsave("plots/tsla_return.pdf", p_tsla_return, width = 9, height = 5)
ggsave("plots/tsla_return_day.pdf", p_tsla_return_day, width = 9, height = 5)
ggsave("plots/tsla_price.pdf", p_tsla_price, width = 9, height = 5)

# DONE
cat("??? Exported AAPL and TSLA plots as PDFs to 'plots/' folder.\n")