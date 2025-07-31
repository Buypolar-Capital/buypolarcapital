

library(tidyverse)
library(fpp3)

datasets::lynx %>% 
  as_tsibble() %>% 
  autoplot()
