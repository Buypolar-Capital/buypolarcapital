from transformers import pipeline
import pandas as pd
import os

# Load market tables
base_dir = os.path.dirname(__file__)
summary_path = os.path.join(base_dir, "data", "summary", "summary.csv")
indices_path = os.path.join(base_dir, "data", "indices", "major_indices.csv")
commodities_path = os.path.join(base_dir, "data", "commodities", "commodities.csv")

indices = pd.read_csv(indices_path, sep=';')
commodities = pd.read_csv(commodities_path, sep=';')

# Build summary input
top_idx = indices.sort_values(by='1D_return', ascending=False).iloc[0]
top_commodity = commodities.sort_values(by='1D_return', ascending=False).iloc[0]

input_text = f"""
Markets saw mixed performance. The top equity index was {top_idx['name']} with a return of {top_idx['1D_return']}%.
In commodities, {top_commodity['name']} led the way with {top_commodity['1D_return']}% daily return.
"""

# Use HuggingFace T5 model for summarization
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
summary = summarizer(input_text, max_length=50, min_length=20, do_sample=False)[0]["summary_text"]

# Save into summary.csv
summary_df = pd.read_csv(summary_path, sep=';')
summary_df["commentary"] = summary
summary_df.to_csv(summary_path, sep=';', index=False)

print("✅ LLM-generated commentary updated.")
