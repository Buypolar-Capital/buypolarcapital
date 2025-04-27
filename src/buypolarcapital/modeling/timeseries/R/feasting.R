
library(fpp3)
library(tidyverse)

if (!dir.exists("plots")) dir.create("plots")
pdf("plots/feasting_plots.pdf", onefile = TRUE, width = 10, height = 6)

tourism %>% 
  features(Trips, list(mean = mean)) %>% 
  arrange(mean)

tourism %>% 
  features(Trips, quantile)

tourism %>% 
  features(Trips, feat_acf) 

tourism %>% 
  features(Trips, feat_stl) %>% 
  ggplot(aes(x = trend_strength, 
             y = seasonal_strength_year,
             col = Purpose)) +
  geom_point() +
  facet_wrap(vars(State))


tourism %>% 
  features(Trips, feat_stl) %>% 
  filter(seasonal_strength_year == max(seasonal_strength_year)) %>% 
  left_join(tourism, by = c("State", "Region", "Purpose"), 
            multiple = "all") %>% 
  ggplot(aes(x = Quarter, y = Trips)) +
  geom_line() +
  facet_grid(vars(State, Region, Purpose))



