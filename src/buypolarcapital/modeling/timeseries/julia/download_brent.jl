using PyCall, CSV, DataFrames, Dates

# Initialize Python's yfinance via PyCall
yf = pyimport("yfinance")

function download_brent_csv(start::Date, end_date::Date)
    # Download Brent Crude Oil Futures (BZ=F) data
    ticker = yf.Ticker("BZ=F")
    df = ticker.history(start=start, end=end_date, interval="1d")
    
    # Convert to Julia DataFrame
    jdf = DataFrame(
        Date = Date.(py"$df.index.strftime('%Y-%m-%d')"),
        Price = py"$df['Close'].values"
    )
    
    return jdf
end

# Set the date range
start_date = Date(2022, 1, 1)
end_date = today()

# Ensure data directory exists
isdir("data") || mkdir("data")

# Download and save
brent_data = download_brent_csv(start_date, end_date)
CSV.write("data/brent.csv", brent_data)

println("✔ Brent crude data saved to data/brent.csv")