import datetime
import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

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

# --- Styles ---
styles = getSampleStyleSheet()
section_style = styles['Heading2']
section_style.fontSize = 10
body_style = ParagraphStyle(name='Body', fontSize=8, leading=10)

# --- PDF Layout Setup ---
doc = BaseDocTemplate(
    os.path.join(output_dir, f"morning_report_{today}.pdf"),
    pagesize=letter,
    leftMargin=0.5*inch,
    rightMargin=0.5*inch,
    topMargin=0.5*inch,
    bottomMargin=0.5*inch,
)

frame_width = (doc.width - 0.2*inch) / 2
frame_height = doc.height

frame_left = Frame(doc.leftMargin, doc.bottomMargin, frame_width, frame_height, id='left')
frame_right = Frame(doc.leftMargin + frame_width + 0.2*inch, doc.bottomMargin, frame_width, frame_height, id='right')

doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame_left, frame_right])])

# --- Helper: Make a Table from a dict list ---
def make_table(data, display_headers, keys):
    table_data = [display_headers] + [[row[k] for k in keys] for row in data]
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))
    return table

# --- Build Content ---
content = []

# Title
content.append(Paragraph(f"<b>BuyPolar Capital Global One-Pager — {today}</b>", styles['Heading1']))
content.append(Spacer(1, 0.1*inch))

# Section: Major Indices
content.append(Paragraph("📊 Major Indices", section_style))
content.append(make_table(indices, ["Index", "1D Return (%)"], ["name", "1D_return"]))
content.append(Image(os.path.join(plot_dir, "sparkline_indices.png"), width=frame_width, height=0.8*inch))
content.append(Image(os.path.join(plot_dir, "indices_returns.png"), width=frame_width, height=0.8*inch))
content.append(Spacer(1, 0.1*inch))

# Section: Commodities
content.append(Paragraph("🛢 Commodities", section_style))
content.append(make_table(commodities, ["Asset", "1D Return (%)"], ["name", "1D_return"]))
content.append(Image(os.path.join(plot_dir, "commodities_returns.png"), width=frame_width, height=0.8*inch))
content.append(Spacer(1, 0.1*inch))

# Section: Fixed Income
content.append(Paragraph("💰 Fixed Income", section_style))
content.append(make_table(fixed_income, ["Instrument", "1D Return (%)"], ["name", "1D_return"]))
content.append(Image(os.path.join(plot_dir, "fixed_income_returns.png"), width=frame_width, height=0.8*inch))
content.append(Spacer(1, 0.1*inch))

# Section: Crypto
content.append(Paragraph("🪙 Crypto", section_style))
content.append(make_table(crypto, ["Coin", "1D Return (%)"], ["name", "1D_return"]))
content.append(Image(os.path.join(plot_dir, "sparkline_crypto.png"), width=frame_width, height=0.8*inch))
content.append(Image(os.path.join(plot_dir, "crypto_returns.png"), width=frame_width, height=0.8*inch))
content.append(Spacer(1, 0.1*inch))

# Section: Commentary
content.append(Paragraph("🧠 LLM Commentary", section_style))
commentary_clean = summary['commentary'].replace("#", "").replace("&", "and")
content.append(Paragraph(commentary_clean, body_style))
content.append(Spacer(1, 0.1*inch))

# Section: Signals
content.append(Paragraph("📈 Signal Selection", section_style))
content.append(make_table(signals, ["Name", "Signal", "Return"], ["name", "signal", "return"]))
content.append(Image(os.path.join(plot_dir, "grid_returns.png"), width=frame_width, height=0.8*inch))

# --- Finalize ---
doc.build(content)
print(f"✅ Report saved to {doc.filename}")
