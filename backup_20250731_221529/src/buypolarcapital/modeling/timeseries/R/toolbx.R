
library(fpp3)

bricks <- aus_production %>% 
  filter_index("1970 Q1" ~ "2004 Q4") %>% 
  select(Bricks)

bricks %>% model(MEAN(Bricks)) 

bricks %>% 
  ggplot(aes(x = Quarter, y = Bricks)) +
  geom_line() +
  geom_hline(yintercept = 450, 
             col = "blue", 
             lty = "dashed") +
  theme_minimal()

bricks %>% 
  model(SNAIVE(Bricks ~ lag("year"))) %>% 
  augment() %>%
  autoplot(Bricks) +
  geom_line(aes(x = Quarter, y = .resid), col = "blue", lty = "dashed") +
  geom_line(aes(x = Quarter, y = .fitted), col = "red", lty = "dashed") +
  theme_minimal()


