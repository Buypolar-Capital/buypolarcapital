
library(fpp3)
library(tidyverse)

recent <- aus_production %>% 
  filter(year(Quarter) >= 2000)

recent %>% 
  gg_lag(Beer, geom = "point")


recent %>% 
  ACF(Beer, lag_max = 9) %>% 
  autoplot()

aus_production %>% 
  ACF(Tobacco, lag_max = 48) %>% 
  autoplot()

