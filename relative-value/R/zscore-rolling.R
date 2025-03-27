# Load packages
library(tidyquant)
library(tidyverse)
library(lubridate)
library(scales)
library(ggthemes)
library(zoo)

# Define selected high-performing dual-listed pairs
selected_pairs <- list(
  c("GOOG", "GOOGL"),
  c("BRK-A", "BRK-B"),
  c("NOVO-B.CO", "NVO"),
  c("NESN.SW", "NSRGY"),
  c("AZN.L", "AZN")
)

# Rolling window values to test
window_sizes <- c(5, 10, 20, 30, 60, 120)

# Output list
plot_list <- list()

# Loop through selected pairs
for (pair in selected_pairs) {
  tickerA <- pair[1]
  tickerB <- pair[2]
  
  tryCatch({
    prices <- tq_get(c(tickerA, tickerB), from = "2010-01-01", to = Sys.Date()) %>%
      select(date, symbol, adjusted) %>%
      pivot_wider(names_from = symbol, values_from = adjusted) %>%
      drop_na()
    
    prices <- prices %>%
      mutate(ratio = !!sym(tickerA) / !!sym(tickerB)) %>%
      select(date, ratio)
    
    # Add rolling means
    for (w in window_sizes) {
      prices[[paste0("roll_mean_", w)]] <- rollmean(prices$ratio, w, fill = NA, align = "right")
    }
    
    # Reshape for plotting
    plot_df <- prices %>%
      pivot_longer(cols = starts_with("roll_mean_"), names_to = "Window", values_to = "RollingMean") %>%
      mutate(Window = str_remove(Window, "roll_mean_"))
    
    # Plot
    p <- ggplot(plot_df, aes(x = date, y = RollingMean, color = Window)) +
      geom_line(size = 1) +
      labs(
        title = paste(tickerA, "vs", tickerB, "- Rolling Mean Comparison"),
        subtitle = "Different window sizes for price ratio smoothing (2010-today)",
        y = "Rolling Mean of Price Ratio",
        color = "Window Size",
        caption = "Source: Yahoo Finance | Strategy: BuyPolar Capital"
      ) +
      theme_economist_white() +
      scale_color_brewer(palette = "Dark2") +
      scale_y_continuous(labels = number_format(accuracy = 0.01))
    
    plot_list[[paste0(tickerA, "_", tickerB)]] <- p
  }, error = function(e) {
    message(paste("Error on pair:", tickerA, "/", tickerB, "-", e$message))
  })
}

# Save all to PDF
if (!dir.exists("plots")) dir.create("plots")
pdf("plots/dual_arbitrage_rolling_windows_multi_pairs.pdf", width = 10, height = 7.5)
for (p in plot_list) print(p)
dev.off()
