
library(tidyverse)
library(tidyquant)
library(Quandl)

pdf(file="plots/aapl.pdf", width = 12, height = 6)
aapl <- tq_get("AAPL", get = "stock.prices", start = "2010-01-01")

aapl %>% ggplot(aes(x = date)) +
  geom_line(aes(y = open), col = "red") +
  geom_line(aes(y = high), col = "blue") +
  geom_line(aes(y = low), col = "green") +
  theme_light()
dev.off()

pdf(file = "plots/wti.pdf", 
    width = 12, height = 6)
wti <- tq_get("DCOILWTICO", get = "economic.data")

wti %>% ggplot(aes(x = date, y = price)) +
  geom_line() +
  theme_light()

dev.off()

pdf(file="plots/fang.pdf",
    width = 12, 
    height = 6)

FANG %>% ggplot(aes(x = date, y = high, colour = symbol)) +
  geom_line() +
  theme_light()

dev.off()

pdf(file="plots/fang-return.pdf",
    width = 12, 
    height = 6)

FANG %>% 
  mutate(return = high/lag(high)) %>% 
  ggplot(aes(x = date, y = return, colour = symbol)) +
  geom_line() +
  theme_light()

dev.off()


  


