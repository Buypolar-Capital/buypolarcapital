
library(fpp3)
library(tidyverse)
library(glue)

if (!dir.exists("plots")) dir.create("plots")
pdf("plots/glue_plots.pdf", onefile = TRUE, width = 10, height = 6)

tourism %>%
  features(Trips, feature_set(pkgs = "feasts")) %>% 
  select_at(vars(contains("season"), Purpose)) %>%
  mutate(
    seasonal_peak_year = seasonal_peak_year +
      4*(seasonal_peak_year==0),
    seasonal_trough_year = seasonal_trough_year +
      4*(seasonal_trough_year==0),
    seasonal_peak_year = glue("Q{seasonal_peak_year}"),
    seasonal_trough_year = glue("Q{seasonal_trough_year}"),
  ) %>%
  GGally::ggpairs(mapping = aes(colour = Purpose))

dev.off()