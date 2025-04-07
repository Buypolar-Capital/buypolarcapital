import os
import sys
import datetime
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from plotting.plotting import plot_prices, set_bpc_style


# --- Setup ---
base_dir = os.path.dirname(__file__)
output_dir = os.path.join(base_dir, 'report_outputs')
data_dir = os.path.join(base_dir, 'data')
summary_dir = os.path.join(data_dir, 'summary')
signals_dir = os.path.join(data_dir, 'signals')
plot_dir = os.path.join(base_dir, 'plots')

os.makedirs(output_dir, exist_ok=True)

# --- Load Data ---
def load_data(path):
    return pd.read_csv(path, sep=';').to_dict(orient='records')

indices = load_data(os.path.join(data_dir, 'indices', 'major_indices.csv'))
commodities = load_data(os.path.join(data_dir, 'commodities', 'commodities.csv'))
fixed_income = load_data(os.path.join(data_dir, 'fixed_income', 'fixed_income.csv'))
crypto = load_data(os.path.join(data_dir, 'crypto', 'crypto.csv'))
summary = pd.read_csv(os.path.join(summary_dir, 'summary.csv'), sep=';').iloc[0]
signals = load_data(os.path.join(signals_dir, 'signals.csv'))

today = datetime.date.today().isoformat()

# --- Get Top Movers ---
def get_top_movers(*datasets, top_n=3):
    combined = []
    for dataset in datasets:
        for row in dataset:
            try:
                ret = float(str(row['1D_return']).replace('%', '').replace(',', '.'))
                combined.append({'name': row['name'], 'return': ret})
            except Exception:
                continue
    sorted_combined = sorted(combined, key=lambda x: x['return'], reverse=True)
    return sorted_combined[:top_n], sorted_combined[-top_n:][::-1]

# --- Generate Price Graphs ---
def simulate_price_data(name):
    dates = pd.date_range(end=datetime.datetime.today(), periods=30)
    prices = pd.Series(100 + (pd.Series(range(30)).apply(lambda x: x * 0.2)).cumsum() +
                       pd.Series(np.random.randn(30)).cumsum())
    df = pd.DataFrame({"date": dates, "price": prices, "ticker": name})
    plot_prices(df, title=f"{name} Price Trend", save_pdf=True, export_png=True,
                filename=f"{name}_trend.png", show=False)

for asset in ["indices", "commodities", "fixed_income", "crypto"]:
    simulate_price_data(asset)

# --- Helper: Make Table ---
def make_table(data, headers):
    table_data = [headers] + [[row.get("name", ""), row.get("1D_return", row.get("return", ""))] for row in data]
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))
    return table

# --- PDF Init ---
doc = BaseDocTemplate(
    os.path.join(output_dir, f"morning_report_{today}.pdf"),
    pagesize=letter,
    leftMargin=0.5*inch,
    rightMargin=0.5*inch,
    topMargin=0.5*inch,
    bottomMargin=0.5*inch,
)

from reportlab.platypus import Frame, PageTemplate
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
doc.addPageTemplates([PageTemplate(id='basic', frames=frame)])

styles = getSampleStyleSheet()
section_style = styles['Heading2']
body_style = ParagraphStyle(name='Body', fontSize=8, leading=10)
content = []

# --- Title ---
content.append(Paragraph(f"<b>📈 BuyPolar Capital Global One-Pager — {today}</b>", styles['Heading1']))
content.append(Spacer(1, 0.1*inch))

# --- Top Gainers & Losers ---
gainers, losers = get_top_movers(indices, commodities, fixed_income, crypto)
content.append(Paragraph("🏆 Top Gainers", section_style))
content.append(make_table(gainers, ["Name", "Return (%)"]))
content.append(Spacer(1, 0.1*inch))

content.append(Paragraph("💔 Top Losers", section_style))
content.append(make_table(losers, ["Name", "Return (%)"]))
content.append(PageBreak())

# --- Section Templates ---
def add_section(title, data, plotname):
    content.append(Paragraph(title, section_style))
    content.append(make_table(data, ["Name", "1D_Return"]))
    plot_path = os.path.join(plot_dir, plotname)
    if os.path.exists(plot_path):
        content.append(Image(plot_path, width=doc.width, height=2.5*inch))
    content.append(PageBreak())

add_section("📊 Major Indices", indices, "indices_trend.png")
add_section("🛢 Commodities", commodities, "commodities_trend.png")
add_section("💰 Fixed Income", fixed_income, "fixed_income_trend.png")
add_section("🪙 Crypto", crypto, "crypto_trend.png")

# --- Commentary ---
content.append(Paragraph("🧠 LLM Commentary", section_style))
commentary_clean = summary['commentary'].replace("#", "").replace("&", "and")
content.append(Paragraph(commentary_clean, body_style))
content.append(PageBreak())

# --- Signals ---
content.append(Paragraph("📈 Signal Selection", section_style))
content.append(make_table(signals, ["Name", "Signal", "Return"]))
content.append(Image(os.path.join(plot_dir, "grid_returns.png"), width=doc.width, height=2*inch))

# --- Finalize PDF ---
doc.build(content)
print(f"✅ Report saved to {doc.filename}")
