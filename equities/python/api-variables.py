import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import os

# Create plots/ folder
if not os.path.exists('plots'):
    os.makedirs('plots')

# Pick Apple (AAPL)
stock = 'AAPL'
ticker = yf.Ticker(stock)

# Fetch all available data
info = ticker.info
history = ticker.history(period="1y")
actions = ticker.actions
financials = ticker.financials
quarterly_financials = ticker.quarterly_financials
balance_sheet = ticker.balance_sheet
quarterly_balance_sheet = ticker.quarterly_balance_sheet
cashflow = ticker.cashflow
quarterly_cashflow = ticker.quarterly_cashflow
income_stmt = ticker.income_stmt
quarterly_income_stmt = ticker.quarterly_income_stmt
major_holders = ticker.major_holders
institutional_holders = ticker.institutional_holders
recommendations = ticker.recommendations
sustainability = ticker.sustainability

# Combine all variables into a list
variables = []

# Info variables (scalars)
for key, value in info.items():
    if value is not None and not isinstance(value, (list, dict)):
        variables.append([key, str(value)])

# History variables (latest values)
if not history.empty:
    for col in history.columns:
        variables.append([f"history_{col}", str(history[col].iloc[-1])])

# Actions (latest values)
if actions is not None and not actions.empty:
    for col in actions.columns:
        variables.append([f"actions_{col}", str(actions[col].iloc[-1])])

# Financials (latest year)
if financials is not None and not financials.empty:
    for col in financials.index:
        variables.append([f"financials_{col}", str(financials.loc[col].iloc[0])])

# Quarterly Financials (latest quarter)
if quarterly_financials is not None and not quarterly_financials.empty:
    for col in quarterly_financials.index:
        variables.append([f"quarterly_financials_{col}", str(quarterly_financials.loc[col].iloc[0])])

# Balance Sheet (latest year)
if balance_sheet is not None and not balance_sheet.empty:
    for col in balance_sheet.index:
        variables.append([f"balance_sheet_{col}", str(balance_sheet.loc[col].iloc[0])])

# Quarterly Balance Sheet (latest quarter)
if quarterly_balance_sheet is not None and not quarterly_balance_sheet.empty:
    for col in quarterly_balance_sheet.index:
        variables.append([f"quarterly_balance_sheet_{col}", str(quarterly_balance_sheet.loc[col].iloc[0])])

# Cashflow (latest year)
if cashflow is not None and not cashflow.empty:
    for col in cashflow.index:
        variables.append([f"cashflow_{col}", str(cashflow.loc[col].iloc[0])])

# Quarterly Cashflow (latest quarter)
if quarterly_cashflow is not None and not quarterly_cashflow.empty:
    for col in quarterly_cashflow.index:
        variables.append([f"quarterly_cashflow_{col}", str(quarterly_cashflow.loc[col].iloc[0])])

# Income Statement (latest year)
if income_stmt is not None and not income_stmt.empty:
    for col in income_stmt.index:
        variables.append([f"income_stmt_{col}", str(income_stmt.loc[col].iloc[0])])

# Quarterly Income Statement (latest quarter)
if quarterly_income_stmt is not None and not quarterly_income_stmt.empty:
    for col in quarterly_income_stmt.index:
        variables.append([f"quarterly_income_stmt_{col}", str(quarterly_income_stmt.loc[col].iloc[0])])

# Major Holders
if major_holders is not None and not major_holders.empty:
    for i in range(len(major_holders)):
        variables.append([f"major_holders_row_{i}", str(major_holders.iloc[i].to_list())])

# Institutional Holders (top 10)
if institutional_holders is not None and not institutional_holders.empty:
    for i in range(min(10, len(institutional_holders))):
        variables.append([f"institutional_holders_row_{i}", str(institutional_holders.iloc[i].to_list())])

# Recommendations (latest)
if recommendations is not None and not recommendations.empty:
    for col in recommendations.columns:
        variables.append([f"recommendations_{col}", str(recommendations[col].iloc[-1])])

# Sustainability
if sustainability is not None and not sustainability.empty:
    for col in sustainability.index:
        variables.append([f"sustainability_{col}", str(sustainability.loc[col].iloc[0])])

# Print total variables fetched
print(f"Total variables fetched: {len(variables)}")

# Create a polished PDF
with PdfPages(f'plots/{stock}_summary.pdf') as pdf:
    # Page 1: Price Overview (OHLCV)
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(history['Close'], label='Close', color='blue')
    plt.plot(history['High'], label='High', color='green', alpha=0.5)
    plt.plot(history['Low'], label='Low', color='red', alpha=0.5)
    plt.title(f"{stock} - Price Overview (Last Year)")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.subplot(2, 1, 2)
    plt.plot(history['Volume'], label='Volume', color='gray')
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Page 2: Key Financials (Bar Plot)
    key_financials = {
        'Net Income': income_stmt.loc['Net Income'].iloc[0] if income_stmt is not None else 0,
        'Revenue': income_stmt.loc['Total Revenue'].iloc[0] if income_stmt is not None else 0,
        'Free Cash Flow': cashflow.loc['Free Cash Flow'].iloc[0] if cashflow is not None else 0,
        'Operating Cash Flow': cashflow.loc['Operating Cash Flow'].iloc[0] if cashflow is not None else 0
    }
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(key_financials.keys()), y=list(key_financials.values()), hue=list(key_financials.keys()), palette='viridis', legend=False)
    plt.title(f"{stock} - Key Financial Metrics (Latest Year)")
    plt.ylabel("Value ($)")
    plt.xticks(rotation=45)
    for i, v in enumerate(key_financials.values()):
        plt.text(i, v, f"{v/1e9:.1f}B", ha='center', va='bottom')
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Page 3: Valuation Ratios (Table)
    ratios = {
        'Trailing P/E': info.get('trailingPE', 'N/A'),
        'Forward P/E': info.get('forwardPE', 'N/A'),
        'Price to Book': info.get('priceToBook', 'N/A'),
        'Dividend Yield': info.get('dividendYield', 'N/A'),
        'Market Cap': info.get('marketCap', 'N/A')
    }
    ratios_df = pd.DataFrame(list(ratios.items()), columns=['Ratio', 'Value'])
    plt.figure(figsize=(12, 6))
    plt.table(cellText=ratios_df.values, colLabels=ratios_df.columns, loc='center', cellLoc='center')
    plt.axis('off')
    plt.title(f"{stock} - Valuation Ratios")
    pdf.savefig()
    plt.close()

    # Page 4: Holders (Pie + Table)
    plt.figure(figsize=(12, 8))
    plt.subplot(1, 2, 1)
    holders = [info.get('heldPercentInsiders', 0), info.get('heldPercentInstitutions', 0), 
               1 - info.get('heldPercentInsiders', 0) - info.get('heldPercentInstitutions', 0)]
    plt.pie(holders, labels=['Insiders', 'Institutions', 'Other'], autopct='%1.1f%%', colors=['#FF9999', '#66B2FF', '#99FF99'])
    plt.title(f"{stock} - Ownership Breakdown")
    plt.subplot(1, 2, 2)
    if institutional_holders is not None and not institutional_holders.empty:
        # Dynamically find the percentage column
        percent_col = next((col for col in institutional_holders.columns if '%' in col or 'Percent' in col), None)
        if percent_col:
            top_holders = institutional_holders[['Holder', percent_col]].head(5)
            plt.table(cellText=top_holders.values, colLabels=top_holders.columns, loc='center', cellLoc='center')
            plt.axis('off')
            plt.title("Top 5 Institutional Holders")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Page 5+: Full Variable List (Multi-column Table)
    df = pd.DataFrame(variables, columns=['Variable Name', 'Current Value'])
    rows_per_page = 60  # Increased for more per page
    cols_per_page = 2
    rows_per_col = rows_per_page // cols_per_page
    num_pages = (len(df) + rows_per_page - 1) // rows_per_page
    
    for page in range(num_pages):
        plt.figure(figsize=(12, 10))  # Taller for more rows
        for col in range(cols_per_page):
            start_idx = page * rows_per_page + col * rows_per_col
            end_idx = min(start_idx + rows_per_col, len(df))
            if start_idx >= len(df):
                break
            page_df = df.iloc[start_idx:end_idx]
            plt.table(cellText=page_df.values, colLabels=page_df.columns, 
                      loc='left' if col == 0 else 'right', cellLoc='left', 
                      colWidths=[0.3, 0.2], bbox=[0.05 + col * 0.5, 0.05, 0.45, 0.9], 
                      fontsize=8)  # Smaller font
        plt.axis('off')
        plt.title(f"{stock} - All Variables (Page {page + 1}/{num_pages})", fontsize=10)
        pdf.savefig()
        plt.close()

print(f"PDF saved for {stock} with {num_pages + 4} pages!")