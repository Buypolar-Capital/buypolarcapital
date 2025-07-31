#!/usr/bin/env python3
"""
BuyPolar Capital CLI
Command-line interface for the quantitative finance research hub.
"""

import click
import os
import sys
from pathlib import Path
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

@click.group()
@click.version_option(version="1.0.0")
def main():
    """
    BuyPolar Capital - Quantitative Finance Research Hub
    
    A comprehensive CLI for trading algorithms, market analysis, and educational resources.
    """
    pass

@main.group()
def dashboard():
    """Dashboard and market data commands."""
    pass

@dashboard.command()
@click.option('--output', '-o', default='dashboards/data', help='Output directory for data')
@click.option('--period', '-p', default='7d', help='Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)')
def update_data(output, period):
    """Update market data for dashboards."""
    try:
        from dashboards.build_data_v2 import main as update_main
        click.echo(f"🔄 Updating market data for {period} period...")
        update_main()
        click.echo("✅ Market data updated successfully!")
    except ImportError as e:
        click.echo(f"❌ Error importing dashboard module: {e}")
        click.echo("Make sure you're in the correct directory and dependencies are installed.")
    except Exception as e:
        click.echo(f"❌ Error updating data: {e}")

@dashboard.command()
@click.option('--port', '-p', default=8501, help='Port to run the dashboard on')
def serve(port):
    """Serve the dashboard locally."""
    try:
        import streamlit as st
        import subprocess
        
        dashboard_path = Path(__file__).parent.parent.parent / "dashboards"
        if not dashboard_path.exists():
            click.echo("❌ Dashboard directory not found!")
            return
            
        click.echo(f"🚀 Starting dashboard on port {port}...")
        click.echo(f"📊 Dashboard will be available at: http://localhost:{port}")
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_path / "app.py"), 
            "--server.port", str(port)
        ])
        
    except ImportError:
        click.echo("❌ Streamlit not installed. Install with: pip install streamlit")
    except Exception as e:
        click.echo(f"❌ Error starting dashboard: {e}")

@main.group()
def quiz():
    """Daily finance quiz commands."""
    pass

@quiz.command()
@click.option('--questions', '-n', default=3, help='Number of questions')
@click.option('--output', '-o', default='notebooks/reporting/quiz/python/plots', help='Output directory')
def generate(questions, output):
    """Generate daily finance quiz."""
    try:
        import subprocess
        
        quiz_dir = Path(__file__).parent.parent.parent / "notebooks" / "reporting" / "quiz" / "python"
        if not quiz_dir.exists():
            click.echo("❌ Quiz directory not found!")
            return
            
        click.echo(f"🎯 Generating {questions} quiz questions...")
        
        # Run the quiz generator
        subprocess.run([
            sys.executable, str(quiz_dir / "daily_finance_quiz.py")
        ])
        
        click.echo("✅ Quiz generated successfully!")
        
    except Exception as e:
        click.echo(f"❌ Error generating quiz: {e}")

@quiz.command()
def take():
    """Take the daily finance quiz interactively."""
    try:
        # This would be an interactive quiz implementation
        click.echo("🎯 Daily Finance Quiz")
        click.echo("=" * 30)
        
        questions = [
            "What is the Sharpe ratio used to measure?",
            "What does VaR stand for in risk management?",
            "What is the primary purpose of portfolio diversification?"
        ]
        
        answers = [
            "Risk-adjusted return",
            "Value at Risk", 
            "Reduce overall portfolio risk"
        ]
        
        score = 0
        for i, (question, answer) in enumerate(zip(questions, answers), 1):
            click.echo(f"\nQ{i}: {question}")
            user_answer = click.prompt("Your answer", type=str)
            
            if user_answer.lower() in answer.lower() or answer.lower() in user_answer.lower():
                click.echo("✅ Correct!")
                score += 1
            else:
                click.echo(f"❌ Incorrect. The answer was: {answer}")
        
        click.echo(f"\n🎉 Final Score: {score}/{len(questions)}")
        
    except Exception as e:
        click.echo(f"❌ Error taking quiz: {e}")

@main.group()
def strategy():
    """Trading strategy commands."""
    pass

@strategy.command()
@click.argument('strategy_name')
@click.option('--data', '-d', help='Data file path')
@click.option('--params', '-p', help='Strategy parameters (JSON)')
def backtest(strategy_name, data, params):
    """Run backtest for a trading strategy."""
    click.echo(f"📊 Running backtest for strategy: {strategy_name}")
    click.echo("This feature is under development...")
    # Implementation would go here

@strategy.command()
def list():
    """List available trading strategies."""
    strategies = {
        "HFT": ["Market Making", "Statistical Arbitrage", "Momentum Trading"],
        "RV": ["Volatility Breakout", "Volatility Compression", "Volatility Spread"],
        "Options": ["Iron Condor", "Butterfly Spread", "Straddle"],
        "Mean Reversion": ["Pairs Trading", "Bollinger Bands", "RSI Divergence"],
        "ML": ["Neural Networks", "Random Forest", "Reinforcement Learning"]
    }
    
    click.echo("📈 Available Trading Strategies:")
    click.echo("=" * 40)
    
    for category, strategy_list in strategies.items():
        click.echo(f"\n{category}:")
        for strategy in strategy_list:
            click.echo(f"  • {strategy}")

@main.group()
def research():
    """Research and analysis commands."""
    pass

@research.command()
@click.argument('asset_class')
@click.option('--period', '-p', default='1y', help='Analysis period')
def analyze(asset_class, period):
    """Analyze a specific asset class."""
    click.echo(f"🔍 Analyzing {asset_class} for {period} period...")
    click.echo("This feature is under development...")

@research.command()
@click.option('--output', '-o', default='reports', help='Output directory')
def generate_report(output):
    """Generate comprehensive market report."""
    click.echo("📋 Generating market report...")
    click.echo("This feature is under development...")

@main.command()
def status():
    """Show system status and recent updates."""
    click.echo("🏥 BuyPolar Capital System Status")
    click.echo("=" * 40)
    
    # Check if key directories exist
    base_path = Path(__file__).parent.parent.parent
    directories = [
        "dashboards",
        "src/buypolarcapital",
        "notebooks",
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
def docs():
    """Open documentation in browser."""
    import webbrowser
    
    docs_url = "https://yourusername.github.io/buypolarcapital/"
    click.echo(f"📚 Opening documentation: {docs_url}")
    webbrowser.open(docs_url)

@main.command()
def github():
    """Open GitHub repository in browser."""
    import webbrowser
    
    repo_url = "https://github.com/yourusername/buypolarcapital"
    click.echo(f"🐙 Opening GitHub repository: {repo_url}")
    webbrowser.open(repo_url)

if __name__ == '__main__':
    main() 