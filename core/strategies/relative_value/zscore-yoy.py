import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from pathlib import Path

# ---------------- USER INPUT ----------------
tickerA = "BRK-A"
tickerB = "BRK-B"
tickerA_safe = tickerA.replace("-", "").replace(".", "")
tickerB_safe = tickerB.replace("-", "").replace(".", "")
start_date = "2023-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')
rolling_windows = [10, 20, 30, 60]
initial_capital = 1e7
threshold = 1
output_file = f"plots/dual_arbitrage_facet_{tickerA_safe}_{tickerB_safe}.pdf"
# --------------------------------------------

# Ensure output folder exists
Path("plots").mkdir(parents=True, exist_ok=True)

# Download and rename data
data_a = yf.download(tickerA, start=start_date, end=end_date, auto_adjust=False)[['Adj Close']]
data_b = yf.download(tickerB, start=start_date, end=end_date, auto_adjust=False)[['Adj Close']]
data_a.columns = [tickerA_safe]
data_b.columns = [tickerB_safe]

# Merge and clean
prices = pd.concat([data_a, data_b], axis=1).dropna().reset_index()
prices['year'] = prices['Date'].dt.year

def simulate_strategy(df, colA, colB, threshold, initial_capital):
    portfolio = pd.DataFrame({'date': df['Date'], 'cash': np.nan, 'A': np.nan, 'B': np.nan, 'value': np.nan})
    first = df.iloc[0]

    if first['z_score'] > 0:
        shares_B = np.floor(initial_capital / first[colB])
        shares_A = 0
        cash = initial_capital - shares_B * first[colB]
    else:
        shares_A = np.floor(initial_capital / first[colA])
        shares_B = 0
        cash = initial_capital - shares_A * first[colA]

    for i in range(len(df)):
        row = df.iloc[i]
        z = row['z_score']
        rebalance = (z > threshold and shares_A > 0) or (z < -threshold and shares_B > 0)

        if rebalance:
            value = shares_A * row[colA] + shares_B * row[colB] + cash
            cash = value
            if z > 0:
                shares_A = 0
                shares_B = np.floor(cash / row[colB])
                cash -= shares_B * row[colB]
            else:
                shares_B = 0
                shares_A = np.floor(cash / row[colA])
                cash -= shares_A * row[colA]

        value = shares_A * row[colA] + shares_B * row[colB] + cash
        portfolio.loc[i] = [row['Date'], cash, shares_A, shares_B, value]

    return portfolio

# Generate PDF
with PdfPages(output_file) as pdf:
    for yr in sorted(prices['year'].unique()):
        df_year = prices[prices['year'] == yr].copy()
        if len(df_year) < max(rolling_windows):
            continue

        yearly_results = []
        for win in rolling_windows:
            df = df_year.copy()
            df['ratio'] = df[tickerA_safe] / df[tickerB_safe]
            df['roll_mean'] = df['ratio'].rolling(window=win).mean()
            df['roll_sd'] = df['ratio'].rolling(window=win).std()
            df['z_score'] = (df['ratio'] - df['roll_mean']) / df['roll_sd']
            df = df.dropna()

            if len(df) < win:
                continue

            strat = simulate_strategy(df, tickerA_safe, tickerB_safe, threshold, initial_capital)
            strat = strat[['date', 'value']].rename(columns={'value': 'strategy'})

            rebased = df[['Date', tickerA_safe, tickerB_safe]].copy()
            rebased['A_val'] = rebased[tickerA_safe] / rebased[tickerA_safe].iloc[0] * initial_capital
            rebased['B_val'] = rebased[tickerB_safe] / rebased[tickerB_safe].iloc[0] * initial_capital
            rebased = rebased[['Date', 'A_val', 'B_val']]

            merged = pd.merge(strat, rebased, left_on='date', right_on='Date')
            melted = pd.melt(merged, id_vars='date', value_vars=['strategy', 'A_val', 'B_val'],
                             var_name='type', value_name='value')
            melted['window'] = f"{win}d"
            yearly_results.append(melted)

        if not yearly_results:
            continue

        all_df = pd.concat(yearly_results)

        sns.set(style="whitegrid")
        g = sns.FacetGrid(all_df, col="window", hue="type", col_wrap=2, height=4, aspect=1.5, sharey=False)
        g.map_dataframe(sns.lineplot, x="date", y="value", linewidth=1.3)
        g.add_legend(title="")
        g.set_axis_labels("Date", "Portfolio Value (USD)")
        g.set_titles(col_template="{col_name}")
        g.fig.suptitle(f"Dual Arbitrage Strategy vs Benchmarks — {yr}\n{tickerA} vs {tickerB} | Threshold ±{threshold}",
                       fontsize=14, weight='bold', y=1.04)
        for ax in g.axes.flat:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

        pdf.savefig(g.fig, bbox_inches='tight')
        plt.close()


