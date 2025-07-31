import datetime
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import subprocess
import os
import shutil
import time

# --- Setup ---
base_dir = os.path.dirname(__file__)
template_dir = os.path.join(base_dir, 'templates')
output_dir = os.path.join(base_dir, 'report_outputs')
data_dir = os.path.join(base_dir, 'data')
summary_dir = os.path.join(data_dir, 'summary')
signals_dir = os.path.join(data_dir, 'signals')
plot_dir = os.path.join(base_dir, 'plots')

os.makedirs(output_dir, exist_ok=True)

# --- Load data ---
def load_data(path):
    return pd.read_csv(path, sep=';').to_dict(orient='records')

indices = load_data(os.path.join(data_dir, 'indices', 'major_indices.csv'))
commodities = load_data(os.path.join(data_dir, 'commodities', 'commodities.csv'))
fixed_income = load_data(os.path.join(data_dir, 'fixed_income', 'fixed_income.csv'))
crypto = load_data(os.path.join(data_dir, 'crypto', 'crypto.csv'))
summary = pd.read_csv(os.path.join(summary_dir, 'summary.csv'), sep=';').iloc[0]
signals = load_data(os.path.join(signals_dir, 'signals.csv'))

today = datetime.date.today().isoformat()

# --- Render markdown with Jinja2 ---
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("report.md.j2")

# Pass absolute output_dir for image paths
markdown_content = template.render(
    date=today,
    indices=indices,
    commodities=commodities,
    fixed_income=fixed_income,
    crypto=crypto,
    commentary=summary['commentary'],
    signals=signals,
    output_dir=output_dir.replace('\\', '/')  # Forward slashes for LaTeX
)

# --- Save .md file ---
md_file = os.path.join(output_dir, f"report_{today}.md")
with open(md_file, "w", encoding="utf-8") as f:
    f.write(markdown_content)

# --- Copy required plots (PNG) ---
plot_names = [
    "sparkline_indices.png",
    "sparkline_crypto.png",
    "indices_returns.png",
    "commodities_returns.png",
    "fixed_income_returns.png",
    "crypto_returns.png",
    "grid_returns.png"
]

for plot in plot_names:
    src = os.path.join(plot_dir, plot)
    dst = os.path.join(output_dir, plot)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        print(f"✅ Copied {plot} to report_outputs/")
    else:
        print(f"[WARNING] Plot file not found: {src}")

# Wait for filesystem
time.sleep(1)

# --- Compile with Pandoc ---
pdf_file = os.path.join(output_dir, f"morning_report_{today}.pdf")
try:
    subprocess.run([
        "pandoc", md_file,
        "-o", pdf_file,
        "--pdf-engine=xelatex",
        f"--resource-path={output_dir}"
    ], check=True)
    print(f"✅ Report saved to: {pdf_file}")
except subprocess.CalledProcessError as e:
    print("❌ Error producing PDF.")
    print(e)

