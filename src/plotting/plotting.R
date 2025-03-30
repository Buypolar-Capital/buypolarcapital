library(ggplot2)

plot_prices <- function(df, title = "Price over Time", y_label = "Price", save_pdf = FALSE, filename = NULL) {
  p <- ggplot(df, aes(x = date, y = price, color = ticker)) +
    geom_line() +
    labs(title = title, x = "Date", y = y_label) +
    theme_minimal(base_size = 12) +
    theme(legend.title = element_blank())
  
  print(p)
  
  if (save_pdf) {
    if (is.null(filename)) {
      tickers <- df %>% distinct(ticker) %>% pull(ticker) %>% paste(collapse = "-")
      filename <- paste0(tickers, "_price_plot.pdf")
    }
    
    # Save to local working directory's ./plots folder
    if (!dir.exists("plots")) dir.create("plots")
    ggsave(file.path("plots", filename), plot = p, width = 10, height = 6)
    cat("??? Saved plot to:", file.path("plots", filename), "\n")
  }
}

