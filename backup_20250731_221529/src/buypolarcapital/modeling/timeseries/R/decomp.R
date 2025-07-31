
library(fpp3)
library(tidyverse)
library(tidyquant)
library(slider)
library(seasonal)

if (!dir.exists("plots")) dir.create("plots")
pdf("plots/decomp_plots.pdf", onefile = TRUE, width = 10, height = 6)

global_economy %>% 
  filter(Country == "Australia") %>% 
  autoplot(GDP/Population)

lambda <- aus_production %>% 
  features(Gas, features = guerrero) %>% 
  pull(lambda_guerrero)

aus_production %>% autoplot(box_cox(Gas, lambda = lambda))

us_employment %>% 
  filter(year(Month) >= 1990, Title == "Retail Trade") %>% 
  select(-Series_ID) %>% 
  autoplot(Employed)

us_employment %>% 
  filter(year(Month) >= 1990, Title == "Retail Trade") %>% 
  model(stl = STL(Employed)) %>% 
  components() %>% 
  autoplot() +
  theme_minimal()

us_employment %>% 
  filter(year(Month) >= 1990, Title == "Retail Trade") %>% 
  model(stl = STL(Employed)) %>% 
  components() %>% 
  as_tsibble() %>% 
  autoplot() +
  geom_line(aes(y = trend), col = "red") 

us_employment %>% 
  filter(year(Month) >= 1990, Title == "Retail Trade") %>% 
  model(stl = STL(Employed)) %>% 
  components() %>% 
  as_tsibble() %>% 
  autoplot(Employed, col = "grey", alpha = .5) +
  geom_line(aes(y = season_adjust), col = "blue") +
  theme_classic()

global_economy %>% 
  filter(Country == "Australia") %>% 
  autoplot(Exports)

global_economy %>% 
  filter(Country == "Australia") %>% 
  mutate(
    MA3 = slide_dbl(Exports, mean, .before = 1, .after = 1, .complete = TRUE),
    MA5 = slide_dbl(Exports, mean, .before = 2, .after = 2, .complete = TRUE),
    MA7 = slide_dbl(Exports, mean, .before = 3, .after = 3, .complete = TRUE),
    MA9 = slide_dbl(Exports, mean, .before = 4, .after = 4, .complete = TRUE)
  ) %>% 
  pivot_longer(cols = starts_with("MA"), names_to = "MA", values_to = "MA_value") %>% 
  ggplot(aes(x = Year)) +
  geom_line(aes(y = Exports), color = "black") +
  geom_line(aes(y = MA_value, color = MA)) +
  facet_wrap(~ MA) +
  theme_bw() +
  labs(title = "Exports with Moving Averages", y = "Exports")


us_retail <- 
  us_employment %>% 
  filter(year(Month) >= 1990, Title == "Retail Trade") %>% 
  select(-Series_ID)

us_retail %>% 
  model(classical_decomposition(Employed, type = "additive")) %>% 
  components() %>% 
  autoplot()

x11_dcmp <-
  us_retail %>% 
  model(x11 = X_13ARIMA_SEATS(Employed ~ x11())) %>% 
  components()

x11_dcmp %>% 
  autoplot()

x11_dcmp %>% 
  ggplot(aes(x = Month)) +
  geom_line(aes(y = Employed, col = "Data")) +
  geom_line(aes(y = season_adjust, col = "Seasonally Adjusted")) +
  geom_line(aes(y = trend, col = "Trend")) +
  scale_colour_manual(
    values = c("gray", "blue", "green"),
    breaks = c("Data", "Seasonally Adjusted", "Trend")
  )

x11_dcmp %>% 
  gg_subseries(seasonal)

seats_dcmp <- us_retail %>% 
  model(seats = X_13ARIMA_SEATS(Employed ~ seats())) %>% 
  components()

seats_dcmp %>% 
  autoplot()

seats_dcmp %>% 
  gg_subseries(seasonal)

  
  
  