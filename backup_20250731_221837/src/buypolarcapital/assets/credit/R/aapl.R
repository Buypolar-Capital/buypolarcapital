
library(tidyquant)
library(tidyverse)

aapl <- tq_get("AAPL",
                    from = "2015-01-01",
                    to   = "2025-01-01",
                    get  = "stock.prices")

aapl %>% 
  ggplot(aes(x = date, y = close)) +
  geom_line()
