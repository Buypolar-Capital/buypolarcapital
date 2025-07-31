
source("../../src/data/fetch_data.R")
source("../../src/plotting/plotting.R")

# Define 10 tickers
tickers <- c("AAPL", "MSFT", "GOOG", "AMZN", "TSLA",
             "NVDA", "META", "JPM", "UNH", "NFLX")

# Set time period
start_date <- "2023-01-01"
end_date <- "2023-10-01"

# Prepare output file
output_file <- "plots/buypolar_10_ticker_report.pdf"
if (!dir.exists("plots")) dir.create("plots")
pdf(output_file, width = 10, height = 6)

# Loop through each ticker and generate a plot per page
for (ticker in tickers) {
  cat("Plotting", ticker, "\n")
  df <- get_prices(ticker, start_date = start_date, end_date = end_date)
  
  plot_prices(
    df,
    title = paste(ticker, "Stock Price", format(as.Date(start_date), "%b %Y"), "???", format(as.Date(end_date), "%b %Y")),
    save_pdf = FALSE  # we don't want to export each page again
  )
}

dev.off()
cat("Multi-page PDF saved to:", output_file, "\n")
