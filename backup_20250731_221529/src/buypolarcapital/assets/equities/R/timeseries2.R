# Load packages
library(tidyverse)
library(tidyquant)
library(fpp3)

# Set output path
output_dir <- "plots"
if (!dir.exists(output_dir)) {
  dir.create(output_dir)
}

# Define stock groups
tickers_list <- list(
  Norway = c("EQNR.OL", "NHY.OL", "YAR.OL", "TEL.OL", "ORK.OL", "DNB.OL", "SALM.OL", "MOWI.OL", "TOM.OL"),
  USA = c("AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "JNJ", "JPM", "NVDA"),
  China = c("BABA", "TCEHY", "JD", "PDD", "NIO", "BIDU", "XPEV", "LI", "ZTO"),
  UK = c("HSBA.L", "BP.L", "VOD.L", "AZN.L", "GLEN.L", "ULVR.L", "RIO.L", "BARC.L", "LSEG.L"),
  EM = c("VALE", "SBS", "ITUB", "PBR", "TCS", "YPF", "LUKOY", "MBT", "HDB"),  # mix of Latin America, Russia, India
  Commodities = c("GLD", "SLV", "USO", "UNG", "DBC", "PALL", "WEAT", "CORN", "LIT")  # ETFs representing commodities
)

# Helper function to process and save plots
generate_return_plot <- function(tickers, group_name) {
  
  stock_data <- tq_get(tickers,
                       from = "2023-01-01",
                       to = Sys.Date(),
                       get = "stock.prices") %>%
    select(symbol, date, adjusted)
  
  returns_ts <- stock_data %>%
    group_by(symbol) %>%
    arrange(date) %>%
    mutate(return = difference(log(adjusted))) %>%
    ungroup() %>%
    filter(!is.na(return)) %>%
    as_tsibble(index = date, key = symbol)
  
  plot <- returns_ts %>%
    ggplot(aes(x = date, y = return)) +
    geom_line(color = "steelblue") +
    geom_hline(yintercept = 0, linetype = "dotted", color = "red") +
    facet_wrap(~ symbol, scales = "free_y", ncol = 3) +
    labs(
      title = paste("Daily Log Returns:", group_name),
      subtitle = "Simulated white-noise style series",
      x = "Date", y = "Log Return"
    ) +
    theme_minimal()
  
  ggsave(
    filename = paste0(group_name, "_returns.pdf"),
    path = output_dir,
    plot = plot,
    width = 12,
    height = 8
  )
}

# Loop through groups and generate plots
walk2(tickers_list, names(tickers_list), generate_return_plot)
