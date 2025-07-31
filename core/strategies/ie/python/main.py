import subprocess
import os
from pathlib import Path

# Define the base directory for scripts
BASE_DIR = Path(__file__).resolve().parent

# List of scripts to execute in sequence
scripts = [
    "scripts/download_prices.py",
    "scripts/gen_features.py",
    "scripts/train_model.py",
    "scripts/plot_predictions.py",
    "scripts/backtest_predictions.py",
    "scripts/plot_long_short_vs_osebx.py",
    "scripts/summarize_results.py"
]

print("🚀 Running full OSEBX Index Effect Pipeline\n")

# Loop through each script and execute it
for script in scripts:
    script_path = BASE_DIR / script  # Construct the full path for each script
    
    # Check if the script exists before attempting to run it
    if not script_path.exists():
        print(f"❌ {script_path} not found! Skipping this script.")
        continue

    print(f"\n▶️ Executing: {script}")
    
    # Run the script using subprocess
    result = subprocess.run(["python", str(script_path)], capture_output=True, text=True)

    # Check for errors and print the result
    if result.returncode != 0:
        print(f"❌ Error in {script}:\n{result.stderr}")
        break
    else:
        print(result.stdout.strip())

print("\n✅ All steps completed.")
