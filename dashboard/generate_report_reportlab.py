import datetime
import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# --- Setup ---
base_dir = os.path.dirname(__file__)
output_dir = os.path.join(base_dir, 'report_outputs')
data_dir = os.path.join(base_dir, 'data')
summary_dir = os.path.join(data_dir, 'summary')
signals_dir = os.path.join(data_dir, 'signals')
plot_dir = os.path.join(base_dir, 'plots')

print(f"Base directory: {base_dir}")
print(f"Output directory: {output_dir}")
print(f"Plot directory: {plot_dir}")

os.makedirs(output_dir, exist_ok=True)

# --- Load data ---
def load_data(path):
    print(f"Loading data from: {path}")
    return pd.read_csv(path, sep=';').to_dict(orient='records')

indices = load_data(os.path.join(data_dir, 'indices', 'major_indices.csv'))
commodities = load_data(os.path.join(data_dir, 'commodities', 'commodities.csv'))
fixed_income = load_data(os.path.join(data_dir, 'fixed_income', 'fixed_income.csv'))
crypto = load_data(os.path.join(data_dir, 'crypto', 'crypto.csv'))
summary = pd.read_csv(os.path.join(summary_dir, 'summary.csv'), sep=';').iloc[0]
signals = load_data(os.path.join(signals_dir, 'signals.csv'))

today = datetime.date.today().isoformat()

# --- Build PDF with reportlab ---
pdf_file = os.path.join(output_dir, f"morning_report_{today}.pdf")
doc = SimpleDocTemplate(pdf_file, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
elements = []

# Styles
styles = getSampleStyleSheet()
title_style = styles['Heading1']
title_style.fontSize = 14
section_style = styles['Heading2']
section_style.fontSize = 10
body_style = ParagraphStyle(name='Body', fontSize=8, leading=10)

# Title
elements.append(Paragraph(f"BuyPolar Capital Global One-Pager - {today}", title_style))
elements.append(Spacer(1, 0.1*inch))

# Two-column layout simulation: We'll stack elements vertically for simplicity
# Major Indices
elements.append(Paragraph("Major Indices", section_style))
indices_data = [["Index", "1D Return (%)"]] + [[row['name'], row['1D_return']] for row in indices]
indices_table = Table(indices_data)
indices_table.setStyle(TableStyle([
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
]))
elements.append(indices_table)
print("Adding sparkline_indices.png")
elements.append(Image(os.path.join(plot_dir, "sparkline_indices.png"), width=3*inch, height=1*inch))
print("Adding indices_returns.png")
elements.append(Image(os.path.join(plot_dir, "indices_returns.png"), width=3*inch, height=1*inch))
elements.append(Spacer(1, 0.1*inch))

# Commodities
elements.append(Paragraph("🛢 Commodities", section_style))
commodities_data = [["Asset", "1D Return (%)"]] + [[row['name'], row['1D_return']] for row in commodities]
commodities_table = Table(commodities_data)
commodities_table.setStyle(TableStyle([
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
]))
elements.append(commodities_table)
print("Adding commodities_returns.png")
elements.append(Image(os.path.join(plot_dir, "commodities_returns.png"), width=3*inch, height=1*inch))
elements.append(Spacer(1, 0.1*inch))

# Fixed Income
elements.append(Paragraph("Fixed Income", section_style))
fixed_income_data = [["Instrument", "1D Return (%)"]] + [[row['name'], row['1D_return']] for row in fixed_income]
fixed_income_table = Table(fixed_income_data)
fixed_income_table.setStyle(TableStyle([
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
]))
elements.append(fixed_income_table)
print("Adding fixed_income_returns.png")
elements.append(Image(os.path.join(plot_dir, "fixed_income_returns.png"), width=3*inch, height=1*inch))
elements.append(Spacer(1, 0.1*inch))

# Crypto
elements.append(Paragraph("Crypto", section_style))
crypto_data = [["Coin", "1D Return (%)"]] + [[row['name'], row['1D_return']] for row in crypto]
crypto_table = Table(crypto_data)
crypto_table.setStyle(TableStyle([
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
]))
elements.append(crypto_table)
print("Adding sparkline_crypto.png")
elements.append(Image(os.path.join(plot_dir, "sparkline_crypto.png"), width=3*inch, height=1*inch))
print("Adding crypto_returns.png")
elements.append(Image(os.path.join(plot_dir, "crypto_returns.png"), width=3*inch, height=1*inch))
elements.append(Spacer(1, 0.1*inch))

# LLM Commentary
elements.append(Paragraph("LLM Commentary", section_style))
elements.append(Paragraph(summary['commentary'].replace("#", ""), body_style))
elements.append(Spacer(1, 0.1*inch))

# Signal Selection
elements.append(Paragraph("Signal Selection", section_style))
signals_data = [["Name", "Signal", "Return"]] + [[row['name'], row['signal'], row['return']] for row in signals]
signals_table = Table(signals_data)
signals_table.setStyle(TableStyle([
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
]))
elements.append(signals_table)
print("Adding grid_returns.png")
elements.append(Image(os.path.join(plot_dir, "grid_returns.png"), width=3*inch, height=1*inch))

# Build PDF
print("Building PDF...")
doc.build(elements)
print(f"✅ Report saved to: {pdf_file}")