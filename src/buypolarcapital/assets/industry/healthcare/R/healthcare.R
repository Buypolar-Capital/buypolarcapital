
library(tidyverse)
library(tidyquant)

tickers <- c(
  "^SP500-35"
)

start_date <- "2000-01-01"
end_date <- Sys.Date()

health <- tq_get(tickers,
                 from = start_date,
                 to = end_date)

pdf(file = "plots/healthcarestocks.pdf",
    width = 12,
    height = 6)

health %>% 
  select(-volume) %>% 
  pivot_longer(-c("symbol", "date")) %>% 
  ggplot(aes(x = date, y = value, colour = name)) +
  geom_line() +
  theme_bw()

dev.off()
  