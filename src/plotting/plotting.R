library(ggplot2)
library(dplyr)
library(stringr)
library(showtext)
library(sysfonts)

# Add Google Font (Montserrat) ??? runs only once per session
if (!"Montserrat" %in% font_families()) {
  font_add_google("Montserrat", "gs_font")
  showtext_auto()
}

plot_prices <- function(df, title = "Price over Time", y_label = "Price",
                        save_pdf = FALSE, filename = NULL, source = "Yahoo Finance") {
  tickers <- df %>% distinct(ticker) %>% pull(ticker) %>% paste(collapse = ", ")
  subtitle_text <- paste("Tickers:", tickers)
  caption_text <- paste("Source:", source, "| Strategy: BuyPolar Capital")
  
  # Goldman-style line colors
  color_palette <- c(
    "#003366",  # deep navy (BuyPolar / Goldman core)
    "#b30000",  # strong red
    "#006d2c",  # deep green
    "#f0ab00",  # muted gold
    "#4d4d4d",  # dark grey
    "#5c5cff"   # electric blue
  )
  
  # Match number of tickers to color length
  colors <- setNames(color_palette[1:length(unique(df$ticker))], unique(df$ticker))
  
  p <- ggplot(df, aes(x = date, y = price, color = ticker)) +
    geom_line(size = 0.6) +
    scale_color_manual(values = colors) +
    labs(
      title = title,
      subtitle = subtitle_text,
      x = "Date",
      y = y_label,
      caption = caption_text,
      color = NULL
    ) +
    theme_light(base_family = "gs_font", base_size = 13) +
    theme(
      plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
      plot.subtitle = element_text(size = 11, hjust = 0.5, margin = margin(b = 10)),
      axis.title = element_text(size = 11),
      axis.text = element_text(size = 10, color = "#333333"),
      legend.position = "top",
      legend.title = element_blank(),
      legend.text = element_text(size = 10),
      panel.grid.major = element_line(color = "#dddddd", size = 0.3),
      panel.border = element_rect(color = "#cccccc", fill = NA),
      plot.caption = element_text(size = 9, face = "italic", hjust = 0)
    )
  
  print(p)
  
  if (save_pdf) {
    if (is.null(filename)) {
      filename <- paste0(str_replace_all(tickers, ", ", "_"), "_price_plot.pdf")
    }
    
    if (!dir.exists("plots")) dir.create("plots")
    ggsave(file.path("plots", filename), plot = p, width = 10, height = 6, device = cairo_pdf)
    cat("Saved plot to:", file.path("plots", filename), "\n")
  }
}
