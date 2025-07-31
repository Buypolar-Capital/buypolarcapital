import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# === CONFIG ===
SYMBOL = "BTCUSDT"
DATE = "2024-03-01"
FILE = f"tick_data/{SYMBOL}_{DATE}_max10000.parquet"
REPORT_DIR = Path("report")
REPORT_PATH = REPORT_DIR / f"{SYMBOL}_{DATE}_report.pdf"
LOGO_PATH = Path("buypolarcapital.png")

# === CREATE LOGO IF NEEDED ===
if not LOGO_PATH.exists():
    img = Image.new("RGB", (500, 120), color=(10, 10, 10))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    draw.text((20, 30), "BuyPolar Capital", fill=(255, 255, 255), font=font)
    img.save(LOGO_PATH)

# === LOAD & PREPARE DATA ===
df = pd.read_parquet(FILE)
df["T"] = pd.to_datetime(df["T"])
df["p"] = df["p"].astype(float)
df["q"] = df["q"].astype(float)

df.set_index("T", inplace=True)
ohlcv = df.resample("1min").agg({
    "p": ["first", "max", "min", "last"],
    "q": "sum"
})
ohlcv.columns = ["open", "high", "low", "close", "volume"]
ohlcv.dropna(inplace=True)

# === ANALYTICS ===
ohlcv["sma_5"] = ohlcv["close"].rolling(5).mean()
ohlcv["sma_20"] = ohlcv["close"].rolling(20).mean()
ohlcv["returns"] = ohlcv["close"].pct_change()
ohlcv["volatility"] = ohlcv["returns"].rolling(5).std()

# Flag top 5 volatility spikes
vol_spikes = ohlcv["volatility"].nlargest(5)

# === 🤖 LLM SUMMARY ===
vol = ohlcv["volume"]
summary_prompt = f"""
BuyPolar Capital | {SYMBOL} Market Summary | {DATE}

• Open: ${ohlcv['open'].iloc[0]:.2f} | Close: ${ohlcv['close'].iloc[-1]:.2f}
• High: ${ohlcv['high'].max():.2f} | Low: ${ohlcv['low'].min():.2f}
• Volume: {vol.sum():,.2f} {SYMBOL.replace('USDT','')} over {len(ohlcv)} minutes
• Avg Volume/min: {vol.mean():.2f} | Peak Volume: {vol.max():.2f}
• Max 1-min return: {ohlcv['returns'].max()*100:.2f}% | Max Volatility: {ohlcv['volatility'].max()*100:.2f}%

⚠ Volatility spikes occurred at:
{vol_spikes.index.strftime('%H:%M:%S').to_list()}

Note price trend, trend reversals, and volume surges. Useful for short-term strat tuning.
"""

print("\n--- LLM PROMPT ---")
print(summary_prompt.strip())

# === GENERATE PDF ===
REPORT_DIR.mkdir(parents=True, exist_ok=True)
with PdfPages(REPORT_PATH) as pdf:
    # Cover Page
    plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    plt.title("BuyPolar Capital\nMarket Summary Report", fontsize=16, fontweight='bold', pad=20)
    plt.text(0.05, 0.85, f"{SYMBOL} | {DATE}", fontsize=14)
    plt.text(0.05, 0.75, summary_prompt.strip(), fontsize=10, wrap=True)
    if LOGO_PATH.exists():
        logo = plt.imread(LOGO_PATH)
        plt.figimage(logo, xo=480, yo=720, alpha=0.3, zorder=10)
    pdf.savefig()
    plt.close()

    # Price Plot w/ Annotations
    plt.figure(figsize=(10, 4))
    plt.plot(ohlcv.index, ohlcv["close"], label="Close", lw=0.7)
    plt.plot(ohlcv["sma_5"], label="SMA 5", linestyle="--", alpha=0.6)
    plt.plot(ohlcv["sma_20"], label="SMA 20", linestyle="--", alpha=0.6)
    plt.scatter(ohlcv["high"].idxmax(), ohlcv["high"].max(), color='green', label='High', zorder=5)
    plt.scatter(ohlcv["low"].idxmin(), ohlcv["low"].min(), color='red', label='Low', zorder=5)
    plt.title(f"{SYMBOL} Price (1-min) + SMAs")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Volatility Plot
    ohlcv["volatility"].plot(figsize=(10, 4), title="Rolling Volatility (5-min)", color="purple")
    plt.xlabel("Time")
    plt.ylabel("Volatility")
    plt.grid(True)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Volume Plot
    ohlcv["volume"].plot(kind="bar", figsize=(10, 4), title="1-Min Volume", color="orange")
    plt.xlabel("Time")
    plt.ylabel("Volume")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Correlation Matrix
    plt.figure(figsize=(6, 5))
    corr = ohlcv[["open", "high", "low", "close", "volume"]].corr()
    im = plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
    plt.colorbar(im)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # OHLCV Table
    plt.figure(figsize=(10, 5))
    plt.axis('off')
    table_data = ohlcv[["open", "high", "low", "close", "volume"]].round(2).head(10)
    table = plt.table(cellText=table_data.values, colLabels=table_data.columns, loc='center')
    table.scale(1, 2)
    plt.title("Sample OHLCV Data", fontsize=14)
    pdf.savefig()
    plt.close()

print(f"\n✅ PDF report saved to: {REPORT_PATH.resolve()}")
