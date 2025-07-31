
library(tidyverse)
library(tidyquant)
library(scales)

tickers <- c("BRK-A", "BRK-B")
stocks <- tq_get(tickers, from="2000-01-01", 
                 to="2024-12-31") %>% 
  select(symbol, date, close, volume)

stocks %>% 
  ggplot(aes(x = date, y = volume, col = symbol)) +
  geom_line() +
  theme_void()

stocks %>% 
  ggplot(aes(x = date, y = adjusted, col = symbol)) +
  geom_line() +
  theme_void()

relative <- stocks %>% 
  select(symbol, date, close) %>% 
  group_by(date) %>% 
  pivot_wider(names_from = symbol,
              values_from = close) %>% 
  ungroup() %>% 
  rename(BRK_A = `BRK-A`,
         BRK_B = `BRK-B`) %>% 
  mutate(ratio=BRK_A/BRK_B)

relative %>% 
  # filter(date > "2020-01-01") %>%
  # filter(date < "2021-01-01") %>% 
  ggplot(aes(x = date, y = ratio)) +
  geom_line() +
  geom_hline(yintercept = 1500, lty = "dashed", col = "red") +
  theme_classic()

relative %>% 
  ggplot(aes(x=date)) +
  geom_line(aes(y=))


df <- stocks %>% 
  select(symbol, date, close) %>% 
  group_by(date) %>% 
  pivot_wider(names_from = symbol,
              values_from = close) %>% 
  ungroup() %>% 
  rename(BRK_A = `BRK-A`,
         BRK_B = `BRK-B`)

df %>% ggplot(aes(x=date)) +
  geom_line(aes(y=BRK_A), col="blue") +
  geom_line(aes(y=BRK_B*max(BRK_A)/max(BRK_B)), col="red") +
  scale_y_continuous(sec.axis = sec_axis(~.*max(df$BRK_B)/max(df$BRK_A))) +
  theme_minimal()

scale_factor <- max(df$BRK_A) / max(df$BRK_B)

ggplot(df, aes(date)) +
  geom_line(aes(y = BRK_A), col = "blue") +
  geom_line(aes(y = BRK_B * scale_factor), col = "red") +
  scale_y_continuous(
    name = "BRK_A",
    labels = comma,  # removes scientific notation
    sec.axis = sec_axis(~ ./scale_factor, name = "BRK_B")
  ) +
  theme_minimal() +
  theme(
    axis.title.y.left = element_text(color = "blue"),
    axis.title.y.right = element_text(color = "red"),
    panel.border = element_rect(color = "black", fill = NA),
    panel.grid = element_blank(),
    axis.ticks = element_line(color = "black"),
    axis.text = element_text(color = "black"),
    axis.ticks.length = unit(-0.15, "cm")
  ) +
  coord_cartesian(clip = "off")


ggplot(df, aes(date)) +
  geom_line(aes(y = BRK_A), col = "blue") +
  geom_line(aes(y = BRK_B * scale_factor), col = "red") +
  scale_y_continuous(
    name = "BRK_A",
    labels = comma,
    breaks = pretty_breaks(n = 10), # more ticks on primary y-axis
    sec.axis = sec_axis(~ ./scale_factor, name = "BRK_B",
                        breaks = pretty_breaks(n = 10))
  ) +
  theme_minimal() +
  theme(
    axis.title.y.left = element_text(color = "blue"),
    axis.title.y.right = element_text(color = "red"),
    panel.border = element_rect(color = "black", fill = NA),
    panel.grid.major.y = element_line(color = "gray90"),  # horizontal grid
    panel.grid.major.x = element_blank(),
    panel.grid.minor = element_blank(),
    axis.ticks = element_line(color = "black"),
    axis.text = element_text(color = "black"),
    axis.ticks.length = unit(-0.15, "cm")
  ) +
  coord_cartesian(clip = "off")




scale_factor <- max(df$BRK_A) / max(df$BRK_B)

ggplot(df, aes(date)) +
  geom_line(aes(y = BRK_A), col = "blue") +
  geom_line(aes(y = BRK_B * scale_factor), col = "red") +
  scale_y_continuous(
    name = NULL,  # Remove default axis titles
    labels = comma,
    breaks = pretty_breaks(n = 10),
    sec.axis = sec_axis(~ ./scale_factor, name = NULL, breaks = pretty_breaks(n = 10))
  ) +
  scale_x_date(
    breaks = pretty_breaks(n = 10)  # More ticks on x-axis
  ) +
  theme_minimal() +
  theme(
    panel.border = element_rect(color = "black", fill = NA),
    panel.grid.major.y = element_line(color = "gray90"),
    panel.grid.major.x = element_blank(),
    panel.grid.minor = element_blank(),
    axis.ticks = element_line(color = "black"),
    axis.text = element_text(color = "black"),
    axis.ticks.length = unit(-0.15, "cm")
  ) +
  coord_cartesian(clip = "off") +
  # Add text labels inside plot
  annotate("text", x = min(df$date), y = max(df$BRK_A), 
           label = "BRK_A", color = "blue", hjust = 0, vjust = 1, size = 4) +
  annotate("text", x = max(df$date), y = min(df$BRK_B * scale_factor), 
           label = "BRK_B", color = "red", hjust = 1, vjust = -1, size = 4)







scale_factor <- max(relative$BRK_A) / max(relative$BRK_B)

ggplot(relative, aes(x = date)) +
  # Background ratio plot as shaded ribbon
  geom_ribbon(aes(ymin = 1500, ymax = ratio), fill = "gray80", alpha = 0.3) +
  geom_hline(yintercept = 1500, lty = "dashed", col = "red") +
  
  # Main price lines
  geom_line(aes(y = BRK_A), color = "blue") +
  geom_line(aes(y = BRK_B * scale_factor), color = "red") +
  
  scale_y_continuous(
    name = NULL,
    labels = comma,
    breaks = pretty_breaks(n = 10),
    sec.axis = sec_axis(~ ./scale_factor, name = NULL, breaks = pretty_breaks(n = 10))
  ) +
  scale_x_date(breaks = pretty_breaks(n = 10)) +
  
  theme_minimal() +
  theme(
    panel.border = element_rect(color = "black", fill = NA),
    panel.grid.major.y = element_line(color = "gray90"),
    panel.grid.major.x = element_blank(),
    panel.grid.minor = element_blank(),
    axis.ticks = element_line(color = "black"),
    axis.text = element_text(color = "black"),
    axis.ticks.length = unit(-0.15, "cm")
  ) +
  coord_cartesian(clip = "off") +
  
  # Annotations for BRK_A & BRK_B labels
  annotate("text", x = min(relative$date), y = max(relative$BRK_A), 
           label = "BRK_A", color = "blue", hjust = 0, vjust = -0.5, size = 4) +
  annotate("text", x = max(relative$date), y = min(relative$BRK_B * scale_factor), 
           label = "BRK_B", color = "red", hjust = 1, vjust = 1.5, size = 4)









