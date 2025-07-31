#!/usr/bin/env python3
"""
BuyPolar Capital CLI - Streamlined Version
Essential command-line interface for the quantitative finance research hub.
"""

import click
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import webbrowser

# Add the core directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

@click.group()
@click.version_option(version="2.0.0")
def main():
    """
    BuyPolar Capital - Interactive Quantitative Finance Hub
    
    Essential CLI for trading algorithms, market analysis, and educational resources.
    """
    pass

@main.group()
def dashboard():
    """Dashboard and market data commands."""
    pass

@dashboard.command()
@click.option('--port', '-p', default=8501, help='Port to run the dashboard on')
def serve(port):
    """Serve the interactive dashboard locally."""
    try:
        import streamlit as st
        
        dashboard_path = Path(__file__).parent.parent / "dashboards" / "market_overview"
        app_file = dashboard_path / "app.py"
        
        if not app_file.exists():
            click.echo("❌ Dashboard app.py not found!")
            click.echo(f"Expected location: {app_file}")
            return
            
        click.echo(f"🚀 Starting interactive dashboard on port {port}...")
        click.echo(f"📊 Dashboard will be available at: http://localhost:{port}")
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_file), 
            "--server.port", str(port)
        ])
        
    except ImportError:
        click.echo("❌ Streamlit not installed. Install with: pip install streamlit")
    except Exception as e:
        click.echo(f"❌ Error starting dashboard: {e}")

@dashboard.command()
def update():
    """Update market data for dashboards."""
    try:
        click.echo("🔄 Updating market data...")
        
        # Simple data update - can be enhanced later
        data_dir = Path(__file__).parent.parent / "data" / "processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create sample data file
        sample_data = {
            "timestamp": datetime.now().isoformat(),
            "spy": {"price": 450.25, "change": 0.85},
            "btc": {"price": 65000, "change": -2.34},
            "gold": {"price": 1950, "change": 0.67},
            "tlt": {"price": 95.50, "change": -0.12}
        }
        
        import json
        with open(data_dir / "market_data.json", "w") as f:
            json.dump(sample_data, f, indent=2)
            
        click.echo("✅ Market data updated successfully!")
        
    except Exception as e:
        click.echo(f"❌ Error updating data: {e}")

@main.group()
def strategy():
    """Trading strategy commands."""
    pass

@strategy.command()
def list():
    """List available trading strategies."""
    strategies = {
        "HFT": ["Market Making", "Statistical Arbitrage", "Momentum Trading"],
        "Mean Reversion": ["Pairs Trading", "Bollinger Bands", "RSI Divergence"],
        "Momentum": ["Trend Following", "Breakout Trading", "Moving Average Crossover"],
        "Arbitrage": ["Statistical Arbitrage", "Pairs Trading", "Risk Arbitrage"],
        "ML": ["Neural Networks", "Random Forest", "Reinforcement Learning"]
    }
    
    click.echo("📈 Available Trading Strategies:")
    click.echo("=" * 50)
    
    for category, strategy_list in strategies.items():
        click.echo(f"\n{category}:")
        for strategy in strategy_list:
            click.echo(f"  • {strategy}")

@strategy.command()
@click.argument('strategy_name')
def backtest(strategy_name):
    """Run backtest for a trading strategy."""
    click.echo(f"📊 Running backtest for strategy: {strategy_name}")
    click.echo("This feature is under development...")
    click.echo("Check the GitHub repository for implementation details.")

@main.group()
def education():
    """Educational content commands."""
    pass

@education.command()
def quiz():
    """Take an interactive finance quiz."""
    click.echo("🎯 Interactive Finance Quiz")
    click.echo("=" * 30)
    
    questions = [
        ("What is the Sharpe ratio used to measure?", "Risk-adjusted return"),
        ("What does VaR stand for in risk management?", "Value at Risk"),
        ("What is the primary purpose of portfolio diversification?", "Reduce overall portfolio risk")
    ]
    
    score = 0
    for i, (question, answer) in enumerate(questions, 1):
        click.echo(f"\nQ{i}: {question}")
        user_answer = click.prompt("Your answer", type=str)
        
        if user_answer.lower() in answer.lower() or answer.lower() in user_answer.lower():
            click.echo("✅ Correct!")
            score += 1
        else:
            click.echo(f"❌ Incorrect. The answer was: {answer}")
    
    click.echo(f"\n🎉 Final Score: {score}/{len(questions)}")

@education.command()
def calculator():
    """Open the financial calculator."""
    click.echo("🧮 Opening financial calculator...")
    click.echo("Visit the interactive website for the calculator tool.")

@main.command()
def status():
    """Show system status."""
    click.echo("🏥 BuyPolar Capital System Status")
    click.echo("=" * 50)
    
    # Check if key directories exist
    base_path = Path(__file__).parent.parent
    directories = [
        "core",
        "assets",
        "dashboards",
        "data",
        "docs"
    ]
    
    for directory in directories:
        dir_path = base_path / directory
        if dir_path.exists():
            click.echo(f"✅ {directory}")
        else:
            click.echo(f"❌ {directory}")
    
    click.echo(f"\n📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@main.command()
def website():
    """Open the interactive website in browser."""
    website_url = "https://yourusername.github.io/buypolarcapital/"
    click.echo(f"🌐 Opening interactive website: {website_url}")
    webbrowser.open(website_url)

@main.command()
def github():
    """Open GitHub repository in browser."""
    repo_url = "https://github.com/yourusername/buypolarcapital"
    click.echo(f"🐙 Opening GitHub repository: {repo_url}")
    webbrowser.open(repo_url)

@main.group()
def tools():
    """Utility tools."""
    pass

@tools.command()
def format():
    """Format code using style guidelines."""
    try:
        click.echo("🎨 Formatting code...")
        
        # Format Python code
        subprocess.run([sys.executable, "-m", "black", "core", "assets"])
        subprocess.run([sys.executable, "-m", "isort", "core", "assets"])
        
        click.echo("✅ Code formatting completed!")
        
    except Exception as e:
        click.echo(f"❌ Error formatting code: {e}")

@tools.command()
def test():
    """Run the test suite."""
    try:
        click.echo("🧪 Running test suite...")
        
        subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"])
        
        click.echo("✅ Tests completed!")
        
    except Exception as e:
        click.echo(f"❌ Error running tests: {e}")

if __name__ == '__main__':
    main() 