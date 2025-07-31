import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from datetime import datetime

# Parameters
tickers = ['AAPL', 'TSLA', 'MSFT']
start_date = "2024-01-01"
end_date = "2025-04-18"  # Use current date to avoid future data issues

# Helper to compute curvature
def compute_curvature(price, volatility):
    """
    Computes the curvature of the price-volatility trajectory.
    Ensures input arrays are long enough and volatility is non-negative.
    """
    if len(price) < 3 or len(volatility) < 3:
        return np.zeros_like(price, dtype=float)
    
    # Ensure volatility is non-negative
    volatility = np.maximum(volatility, 0)
    
    # Calculate first derivatives
    dy = np.gradient(price)
    dz = np.gradient(volatility)
    
    # Calculate second derivatives
    ddy = np.gradient(dy)
    ddz = np.gradient(dz)
    
    # Compute curvature: |dy*ddz - dz*ddy| / (dy^2 + dz^2)^1.5
    denominator = (dy**2 + dz**2)**1.5
    curvature = np.zeros_like(price, dtype=float)
    non_zero_denom_mask = denominator != 0
    
    if np.any(non_zero_denom_mask):
        dy_masked = dy[non_zero_denom_mask]
        dz_masked = dz[non_zero_denom_mask]
        ddy_masked = ddy[non_zero_denom_mask]
        ddz_masked = ddz[non_zero_denom_mask]
        denominator_masked = denominator[non_zero_denom_mask]
        curvature[non_zero_denom_mask] = np.abs(
            dy_masked * ddz_masked - dz_masked * ddy_masked
        ) / denominator_masked
    
    return np.nan_to_num(curvature, nan=0.0, posinf=0.0, neginf=0.0)

# Prepare plot
fig = plt.figure(figsize=(14, 9))
ax = fig.add_subplot(111, projection='3d')
plotted = False  # Track if any data is plotted

# Loop through tickers
for ticker in tickers:
    print(f"Processing {ticker}...")
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # Check for empty or insufficient data
        if data.empty or len(data) < 10:
            print(f"Skipping {ticker}: not enough raw data ({len(data)} rows).")
            continue

        # Data processing: fill NaNs in Close price
        price = data['Close'].ffill()
        
        # Calculate rolling volatility
        vol = price.rolling(window=10).std()
        
        # Combine data and drop NaNs
        analysis_data = pd.DataFrame({
            'price': price,
            'vol': vol,
            'volume': data['Volume']
        }).dropna()
        
        # Check if enough data points remain
        if len(analysis_data) < 3:
            print(f"Skipping {ticker}: not enough data points ({len(analysis_data)} rows) after processing.")
            continue
        
        # Extract cleaned data
        clean_price = analysis_data['price'].values
        clean_vol = analysis_data['vol'].values
        clean_volume = analysis_data['volume'].values
        
        # Normalize volume to [0,1] for consistent marker sizes
        if clean_volume.max() > clean_volume.min():
            normalized_volume = (clean_volume - clean_volume.min()) / (clean_volume.max() - clean_volume.min())
        else:
            normalized_volume = np.ones_like(clean_volume) * 0.5  # Default to mid-range if constant volume
        
        # Compute curvature
        curvature = compute_curvature(clean_price, clean_vol)
        
        # Time index
        t = np.arange(len(clean_price))
        
        # 3D scatter plot
        sc = ax.scatter(t, clean_price, clean_vol, c=curvature, cmap='plasma',
                        s=20 + 100 * normalized_volume, label=ticker, alpha=0.8)
        plotted = True
    
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        continue

# Labels and title
ax.set_xlabel("Time (days since start)")
ax.set_ylabel("Price ($)")
ax.set_zlabel("Volatility ($)")
ax.set_title("3D Price–Volatility–Time Trajectories\nColor = Curvature | Size = Volume")
ax.grid(True)  # Add gridlines

# Colorbar and legend
if plotted:
    fig.colorbar(sc, ax=ax, label='Curvature')
    ax.legend()
else:
    print("No data plotted for any ticker.")

# Adjust view angle for better visibility
ax.view_init(elev=20, azim=45)

# Save plot
os.makedirs("plots", exist_ok=True)
plot_filename = "plots/price_volatility_3D_trajectory_multiasset.pdf"
try:
    plt.savefig(plot_filename, bbox_inches='tight')
    print(f"Plot saved to {plot_filename}")
except Exception as e:
    print(f"Error saving plot: {e}")

# Show plot
plt.show()