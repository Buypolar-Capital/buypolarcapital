
library(fpp3)
library(tidyverse)

google <- gafa_stock %>% 
  filter(Symbol == "GOOG", 
         year(Date) >= 2015) %>% 
  mutate(day = row_number()) %>% 
  update_tsibble(index = day, 
                 regular = TRUE)

google %>% 
  model(NAIVE(Close)) %>% 
  gg_tsresiduals()



fc <- fpp3::prices |>
  filter(!is.na(eggs)) |>
  model(RW(log(eggs) ~ drift())) |>
  forecast(h = 50) |>
  mutate(.median = median(eggs))




