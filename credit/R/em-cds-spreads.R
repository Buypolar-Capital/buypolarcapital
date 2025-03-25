# INSTALL & LOAD
library(fpp3)
library(gridExtra)
library(patchwork)

# SIMULATED EXOTIC DATA (Argentina 5Y CDS weekly)
set.seed(2025)
cds_data <- tibble(
  date = seq(as.Date("2015-01-01"), as.Date("2025-01-01"), by = "week"),
  cds_spread = cumsum(rnorm(522, mean = 0.1, sd = 5)) + 1000
) %>%
  as_tsibble(index = date)

# STL DECOMPOSITION
decomp <- cds_data %>%
  model(STL(cds_spread)) %>%
  components()

# ETS & ARIMA MODELS
models <- cds_data %>%
  model(
    ETS = ETS(cds_spread),
    ARIMA = ARIMA(cds_spread)
  )

# FORECASTS
fcasts <- models %>%
  forecast(h = "2 years")

# RESIDUALS
residuals_data <- models %>% augment()

# --- PLOTS ---
p1 <- cds_data %>%
  autoplot(cds_spread) +
  labs(title = "Argentina CDS (Simulated)", y = "Spread (bps)", x = "Date")

p2 <- autoplot(decomp) +
  labs(title = "STL Decomposition")

p3 <- fcasts %>%
  autoplot(cds_data) +
  labs(title = "Forecast: ETS & ARIMA", y = "Spread (bps)", x = "Date")

p4 <- residuals_data %>%
  ggplot(aes(x = .resid)) +
  geom_histogram(bins = 30, fill = "tomato", color = "white") +
  facet_wrap(~.model, scales = "free") +
  labs(title = "Histogram of Residuals", x = "Residual", y = "Count")

p5 <- residuals_data %>%
  ACF(.resid) %>%
  autoplot() +
  labs(title = "ACF of Residuals")

# --- ACCURACY TABLE (text plot hack) ---
acc <- glance(models)
acc_text <- capture.output(print(acc, n = Inf, width = Inf))
acc_plot <- ggplot() +
  annotate("text", x = 0, y = 1, label = paste(acc_text, collapse = "\n"),
           hjust = 0, vjust = 1, family = "mono") +
  theme_void() +
  labs(title = "Model Accuracy Metrics (glance)")

# --- EXPORT PDF ---
pdf("plots/BuyPolarCapital_Report.pdf", width = 10, height = 7)

print(p1)
print(p2)
print(p3)
print(p4)
print(p5)
print(acc_plot)

dev.off()

cat("??? PDF created: 'BuyPolarCapital_Report.pdf'\n")
