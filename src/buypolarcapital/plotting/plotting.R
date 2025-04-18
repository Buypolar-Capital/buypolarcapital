library(ggplot2)
library(dplyr)
library(stringr)
library(scales)
library(showtext)
library(sysfonts)

# Load Montserrat once
if (!"Montserrat" %in% font_families()) {
  font_add_google("Montserrat", "gs_font")
  showtext_auto()
}

# Define the BuyPolar Capital ggplot2 theme
theme_buypolar <- function() {
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
}

plot_prices <- function(df,
                        title = "Price over Time",
                        y_label = "Price",
                        save_pdf = FALSE,
                        filename = NULL,
                        source = "Yahoo Finance",
                        event_date = NULL,
                        export_png = TRUE) {
  tickers <- df %>% distinct(ticker) %>% pull(ticker) %>% paste(collapse = ", ")
  subtitle_text <- paste("Tickers:", tickers)
  caption_text <- paste("Source:", source, "| Strategy: BuyPolar Capital")
  
  # Goldman-style color palette
  color_palette <- c("#003366", "#b30000", "#006d2c", "#f0ab00", "#4d4d4d", "#5c5cff")
  colors <- setNames(color_palette[1:length(unique(df$ticker))], unique(df$ticker))
  
  # Find peak and trough
  max_point <- df[which.max(df$price), ]
  min_point <- df[which.min(df$price), ]
  
  # Build plot
  p <- ggplot(df, aes(x = date, y = price, color = ticker)) +
    geom_line(size = 0.6) +
    scale_color_manual(values = colors) +
    scale_y_continuous(labels = dollar_format()) +
    labs(
      title = title,
      subtitle = subtitle_text,
      x = "Date",
      y = y_label,
      caption = caption_text
    ) +
    theme_buypolar() +
    geom_point(data = max_point, aes(x = date, y = price), color = "darkgreen", size = 2) +
    geom_text(data = max_point, aes(label = paste0("Peak: $", round(price, 2))),
              vjust = -1, size = 3, fontface = "italic", color = "darkgreen", family = "gs_font") +
    geom_point(data = min_point, aes(x = date, y = price), color = "darkred", size = 2) +
    geom_text(data = min_point, aes(label = paste0("Trough: $", round(price, 2))),
              vjust = 1.5, size = 3, fontface = "italic", color = "darkred", family = "gs_font")
  
  # Optional vertical event line
  if (!is.null(event_date)) {
    p <- p +
      geom_vline(xintercept = as.Date(event_date), linetype = "dashed", color = "grey30") +
      annotate("text", x = as.Date(event_date), y = max(df$price), label = "Event", vjust = -1, size = 3.2)
  }
  
  # Summary stats box
  total_return <- (last(df$price) / first(df$price) - 1) * 100
  stats_text <- sprintf(
    " BuyPolar Metrics\n\n Return:     %+.1f%%\n Max:        $%.2f\n Min:        $%.2f\n Avg:        $%.2f\n Volatility: %.2f\n Days:       %d",
    total_return,
    max(df$price),
    min(df$price),
    mean(df$price),
    sd(df$price),
    nrow(df)
  )
  
  p <- p +
    annotate("label",
             x = min(df$date),
             y = max(df$price),
             label = stats_text,
             hjust = -0.05,  # nudges slightly outside left edge
             vjust = 1.1,     # tucks closer to top
             size = 3.1,
             fill = "white",
             color = "#111111",
             alpha = 0.85,
             label.size = 0.2,
             label.r = unit(0.15, "lines"),
             family = "mono"
    )
  
  print(p)
  
  # Export
  if (save_pdf) {
    if (is.null(filename)) {
      filename <- paste0(str_replace_all(tickers, ", ", "_"), "_price_plot.pdf")
    }
    if (!dir.exists("plots")) dir.create("plots")
    ggsave(file.path("plots", filename), plot = p, width = 10, height = 6, device = cairo_pdf)
    cat("Saved PDF to:", file.path("plots", filename), "\n")
    
    if (export_png) {
      png_file <- str_replace(filename, "\\.pdf$", ".png")
      ggsave(file.path("plots", png_file), plot = p, width = 10, height = 6, dpi = 300)
      cat("Saved PNG to:", file.path("plots", png_file), "\n")
    }
  }
}
