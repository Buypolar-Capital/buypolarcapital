
library(fpp3)
library(tidyquant)
library(tidyverse)

if (!dir.exists("plots")) dir.create("plots")
pdf("plots/all_plots.pdf", onefile = TRUE, width = 10, height = 6)
# dev.off()

aus_production %>% 
  autoplot(Beer) +
  theme_minimal() 

aapl <- tq_get(x = "AAPL", get = "stock.prices", 
              from = "2010-01-01", to = "2025-01-01")

aapl %>%
  as_tsibble(index = date) %>% 
  autoplot(close) +
  theme_minimal()

y <- tsibble(
  Year = 2015:2019,
  Observation = c(123, 39, 78, 52, 110),
  index = Year
)

y %>% autoplot()

olympic_running %>% distinct(Sex)
unique(olympic_running$Sex)

PBS %>% 
  filter(ATC2 == "A10") %>% 
  select(Month, Concession, Type, Cost) %>% 
  summarise(TotalC = sum(Cost)) %>% 
  mutate(Cost = TotalC/1e6) %>% 
  autoplot(Cost)


ansett %>% 
  filter(Airports == "MEL-SYD", 
         Class == "Economy") %>% 
  mutate(Passengers = Passengers/1000) %>% 
  autoplot(Passengers) +
  labs(title = "Ansett airlines economy class",
       subtitle = "Melbourne-Sydney",
       y = "Passengers ('000)") +
  theme_grey()

aus_production %>% 
  autoplot(Bricks)

aus_production %>% 
  gg_season(Beer, labels = "both")

# vic_elec %>% 
#   gg_season(Demand, period = "day") +
#   theme(legend.position = "none") +
#   labs(y = "MWh", title = "Electricity demand: Victoria")

vic_elec %>%  
  gg_season(Demand, period = "year") 

aus_production %>% 
  gg_subseries(Beer) 

aus_accommodation %>%
  filter(State == "Australian Capital Territory") %>% 
  gg_subseries(Occupancy)

holidays <- tourism %>% 
  filter(Purpose == "Holiday") %>% 
  group_by(State) %>% 
  summarise(Trips = sum(Trips))

autoplot(holidays, Trips)

vic_elec %>% 
  filter(year(Time) == 2014) %>% 
  autoplot(Demand)

vic_elec %>% 
  filter(year(Time) == 2014) %>% 
  autoplot(Temperature)

vic_elec %>% 
  filter(year(Time) == 2014) %>% 
  ggplot(aes(x = Temperature, y = Demand)) +
  geom_point()

visitors <- tourism %>% 
  group_by(State) %>% 
  summarise(Trips = sum(Trips))

visitors %>% 
  ggplot(aes(x = Quarter, y = Trips)) +
  geom_line() +
  facet_grid(vars(State), scales = "free_y")

visitors %>% 
  pivot_wider(values_from = Trips, 
              names_from = State) %>% 
  GGally::ggpairs(columns = 2:9)

dev.off()








