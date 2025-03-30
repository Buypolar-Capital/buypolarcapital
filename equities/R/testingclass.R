source("../../src/data/fetch_data.R")
source("../../src/plotting/plotting.R")

df <- get_prices(c("AAPL"), start_date = "2023-01-01", end_date = "2023-10-01")
print(head(df))

plot_prices(
  df,
  title = "AAPL Stock Price Jan???Oct 2023",
  save_pdf = TRUE,
  filename = "aapl_2023_price.pdf"
)
