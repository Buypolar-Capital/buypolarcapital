
library(tidyverse)
library(tidyquant)

tickers <- c("BRK-A", "BRK-B")
berkshr <- tq_get(x = tickers, get = "stock.prices", 
       from = "2020-01-01", to = Sys.Date()) %>% 
  select(symbol, date, adjusted) %>% 
  pivot_wider(names_from = symbol,
              values_from = adjusted) %>% 
  tidyr::drop_na() %>% 
  mutate(ratio = `BRK-A`/`BRK-B`) %>% 
  rename("BRK_A" = `BRK-A`,
         "BRK_B" = `BRK-B`)

berkshr
