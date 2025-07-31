
library(quantmod)
library(tidyverse)
library(writexl)

getSymbols("TSLA", src = "yahoo", from = "2024-01-01", to = "2024-12-28")
getSymbols("GOOGL", src = "yahoo", from = "2024-01-01", to = "2024-12-28")

tesla <- TSLA %>% 
  as.data.frame() %>%
  mutate(date = index(TSLA)) %>% 
  select(date, everything()) %>% 
  as_tibble()

google <- GOOGL %>% 
  as.data.frame() %>% 
  mutate(date = index(GOOGL)) %>% 
  select(date, everything()) %>% 
  as_tibble()

stock_data <- list(
  TSLA = tesla,
  GOOGL = google
)

write_xlsx(stock_data, path = "stock_data.xlsx")

sdasda


