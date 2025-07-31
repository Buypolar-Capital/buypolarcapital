import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from datetime import datetime, timedelta
import yfinance as yf

# Tickers and labels
tickers = {
    '^IRX': '3M',
    '^FVX': '5Y',
    '^TNX': '10Y',
    '^TYX': '30Y'
}
maturity_order = ['3M', '5Y', '10Y', '30Y']

# Date range: last 5 years
end_date = datetime.today().date()
start_date = end_date - timedelta(days=5 * 365)

# Download data
data = yf.download(list(tickers.keys()), start=start_date, end=end_date)['Close']
data.columns = [tickers[t] for t in data.columns]
data = data[maturity_order].dropna()
recent_data = data.tail(30)

# --- Plot 1: Yield Curves ---
fig1, ax1 = plt.subplots(figsize=(12, 6))
cmap = plt.colormaps.get_cmap('viridis')  # no second arg!
norm = mcolors.Normalize(vmin=0, vmax=29)
colors = [cmap(i / 29) for i in range(30)]  # 0.0 to 1.0 scaled


for i, date in enumerate(recent_data.index):
    label = date.strftime('%Y-%m-%d') if i == 29 else None
    ax1.plot(recent_data.columns, recent_data.loc[date], color=colors[i], label=label, linewidth=2)

ax1.set_title('U.S. Treasury Yield Curves – Last 30 Trading Days')
ax1.set_xlabel('Maturity')
ax1.set_ylabel('Yield (%)')
ax1.grid(True)
if label:
    ax1.legend(title='Most Recent Date')
fig1.tight_layout()

# --- Plot 2: Yield Spreads ---
spreads = pd.DataFrame(index=recent_data.index)
spreads['10Y - 5Y'] = recent_data['10Y'] - recent_data['5Y']
spreads['30Y - 3M'] = recent_data['30Y'] - recent_data['3M']
spreads['10Y - 3M'] = recent_data['10Y'] - recent_data['3M']
spreads['5Y - 3M'] = recent_data['5Y'] - recent_data['3M']

fig2, ax2 = plt.subplots(figsize=(12, 6))
for col in spreads.columns:
    ax2.plot(spreads.index, spreads[col], label=col)

ax2.set_title("Treasury Yield Spreads – Last 30 Trading Days")
ax2.set_ylabel("Spread (percentage points)")
ax2.set_xlabel("Date")
ax2.grid(True)
ax2.legend()
fig2.tight_layout()

# Save to PDF
with PdfPages("plots/yield_curves_and_spreads.pdf") as pdf:
    pdf.savefig(fig1)
    pdf.savefig(fig2)
