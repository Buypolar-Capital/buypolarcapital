library(tidyquant)
library(tidyverse)

get_prices <- function(tickers, start_date = NULL, end_date = Sys.Date()) {
  if (is.null(start_date)) {
    start_date <- as.Date("1900-01-01")
  }
  
  tq_get(tickers, from = start_date, to = end_date) %>%
    select(date, symbol, adjusted) %>%
    rename(ticker = symbol, price = adjusted) %>%
    drop_na()
}
