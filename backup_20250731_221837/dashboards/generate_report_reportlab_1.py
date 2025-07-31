import os
import sys
import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Frame, PageTemplate
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
plot_dir = os.path.abspath(os.path.join(base_dir, '..', 'plots'))
os.makedirs(output_dir, exist_ok=True)

today = datetime.date.today().isoformat()

def load_data(path):
    if not os.path.exists(path):
        print(f"[⚠] Skipping missing file: {path}")
        return []
    return pd.read_csv(path, sep=';').to_dict(orient='records')

# Load datasets
indices = load_data(os.path.join(data_dir, 'indices', 'indices.csv'))
commodities = load_data(os.path.join(data_dir, 'commodities', 'commodities.csv'))
crypto = load_data(os.path.join(data_dir, 'crypto', 'crypto.csv'))
fixed_income = load_data(os.path.join(data_dir, 'fixed_income', 'fixed_income.csv'))
signals = load_data(os.path.join(signals_dir, 'signals.csv'))

# Load LLM summary
summary_path = os.path.join(summary_dir, 'summary.csv')
summary = pd.read_csv(summary_path, sep=';').iloc[0] if os.path.exists(summary_path) else {"commentary": ""}

# --- Style ---
styles = getSampleStyleSheet()
section_style = styles['Heading2']
body_style = ParagraphStyle(name='Body', fontSize=8, leading=10)
content = []

# --- PDF Init ---
doc = BaseDocTemplate(
    os.path.join(output_dir, f"morning_report_{today}.pdf"),
    pagesize=letter,
    leftMargin=0.5 * inch,
    rightMargin=0.5 * inch,
    topMargin=0.5 * inch,
    bottomMargin=0.5 * inch,
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
doc.addPageTemplates([PageTemplate(id='basic', frames=frame)])

# --- Helpers ---
def make_table(data, headers):
    table_data = [headers] + [[row.get("name", ""), row.get("1D_return", row.get("return", ""))] for row in data]
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))
    return table

def load_price_csv(asset):
    path = os.path.join(data_dir, asset, f"{asset}_history.csv")
    if not os.path.exists(path):
        print(f"[⚠] Missing price data for {asset}")
        return None
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    return df

def add_section(title, dataset, asset_key):
    if not dataset:
        return
    content.append(Paragraph(title, section_style))
    content.append(make_table(dataset, ["Name", "1D_Return"]))
    df = load_price_csv(asset_key)
    if df is not None:
        plot_prices(df, title=f"{asset_key.title()} Price Trend", filename=f"{asset_key}_trend.png",
                    save_pdf=False, export_png=True, show=False)
        plot_path = os.path.join(plot_dir, f"{asset_key}_trend.png")
        content.append(Image(plot_path, width=doc.width, height=2.5 * inch))
    content.append(PageBreak())

# --- Title ---
content.append(Paragraph(f"<b>📈 BuyPolar Capital Global One-Pager — {today}</b>", styles['Heading1']))
content.append(Spacer(1, 0.1 * inch))

# --- Gainers & Losers ---
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

gainers, losers = get_top_movers(indices, commodities, crypto, fixed_income)
content.append(Paragraph("🏆 Top Gainers", section_style))
content.append(make_table(gainers, ["Name", "Return (%)"]))
content.append(Spacer(1, 0.1 * inch))
content.append(Paragraph("💔 Top Losers", section_style))
content.append(make_table(losers, ["Name", "Return (%)"]))
content.append(PageBreak())

# --- Sections ---
add_section("📊 Major Indices", indices, "indices")
add_section("🛢 Commodities", commodities, "commodities")
add_section("🪙 Crypto", crypto, "crypto")
add_section("💰 Fixed Income", fixed_income, "fixed_income")

# --- Commentary ---
if summary.get("commentary"):
    content.append(Paragraph("🧠 LLM Commentary", section_style))
    clean_text = summary["commentary"].replace("#", "").replace("&", "and")
    content.append(Paragraph(clean_text, body_style))
    content.append(PageBreak())

# --- Signals ---
if signals:
    content.append(Paragraph("📈 Signal Selection", section_style))
    content.append(make_table(signals, ["Name", "Signal", "Return"]))
    grid_plot = os.path.join(plot_dir, "grid_returns.png")
    if os.path.exists(grid_plot):
        content.append(Image(grid_plot, width=doc.width, height=2 * inch))

# --- Finalize PDF ---
set_bpc_style()
doc.build(content)
print(f"✅ Report saved to {doc.filename}")
