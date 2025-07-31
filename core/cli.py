#!/usr/bin/env python3
"""
BuyPolar Capital CLI - Updated for New Folder Structure
Command-line interface for the quantitative finance research hub.
"""

import click
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json
import webbrowser

# Add the core directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

@click.group()
@click.version_option(version="2.0.0")
def main():
    """
    BuyPolar Capital - Interactive Quantitative Finance Hub
    
    A comprehensive CLI for trading algorithms, market analysis, and educational resources.
    Updated for the new optimized folder structure.
    """
    pass

@main.group()
def dashboard():
    """Dashboard and market data commands."""
    pass

@dashboard.command()
@click.option('--output', '-o', default='data/processed', help='Output directory for data')
@click.option('--period', '-p', default='7d', help='Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)')
@click.option('--assets', '-a', multiple=True, help='Specific assets to update')
def update_data(output, period, assets):
    """Update market data for dashboards."""
    try:
        from core.data.connectors.market_data import MarketDataConnector
        
        click.echo(f"🔄 Updating market data for {period} period...")
        
        # Initialize data connector
        connector = MarketDataConnector()
        
        # Update data
        if assets:
            connector.update_assets(list(assets), period=period, output_dir=output)
        else:
            connector.update_all(period=period, output_dir=output)
            
        click.echo("✅ Market data updated successfully!")
        
    except ImportError as e:
        click.echo(f"❌ Error importing data connector: {e}")
        click.echo("Make sure the core package is properly installed.")
    except Exception as e:
        click.echo(f"❌ Error updating data: {e}")

@dashboard.command()
@click.option('--port', '-p', default=8501, help='Port to run the dashboard on')
@click.option('--host', '-h', default='localhost', help='Host to bind to')
def serve(port, host):
    """Serve the interactive dashboard locally."""
    try:
        import streamlit as st
        
        dashboard_path = Path(__file__).parent.parent / "dashboards" / "market_overview"
        app_file = dashboard_path / "app.py"
        
        if not app_file.exists():
            click.echo("❌ Dashboard app.py not found!")
            click.echo(f"Expected location: {app_file}")
            return
            
        click.echo(f"🚀 Starting interactive dashboard on {host}:{port}...")
        click.echo(f"📊 Dashboard will be available at: http://{host}:{port}")
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_file), 
            "--server.port", str(port),
            "--server.address", host
        ])
        
    except ImportError:
        click.echo("❌ Streamlit not installed. Install with: pip install streamlit")
    except Exception as e:
        click.echo(f"❌ Error starting dashboard: {e}")

@dashboard.command()
def build():
    """Build static dashboard files for GitHub Pages."""
    try:
        from core.utils.build import DashboardBuilder
        
        click.echo("🔨 Building static dashboard files...")
        
        builder = DashboardBuilder()
        builder.build_all()
        
        click.echo("✅ Dashboard build completed!")
        click.echo("📁 Static files available in docs/")
        
    except ImportError as e:
        click.echo(f"❌ Error importing dashboard builder: {e}")
    except Exception as e:
        click.echo(f"❌ Error building dashboard: {e}")

@main.group()
def strategy():
    """Trading strategy commands."""
    pass

@strategy.command()
@click.argument('strategy_name')
@click.option('--data', '-d', help='Data file path')
@click.option('--params', '-p', help='Strategy parameters (JSON)')
@click.option('--output', '-o', default='research/reports', help='Output directory')
def backtest(strategy_name, data, params, output):
    """Run backtest for a trading strategy."""
    try:
        from core.strategies.backtesting.backtester import Backtester
        
        click.echo(f"📊 Running backtest for strategy: {strategy_name}")
        
        # Parse parameters
        strategy_params = {}
        if params:
            try:
                strategy_params = json.loads(params)
            except json.JSONDecodeError:
                click.echo("❌ Invalid JSON parameters")
                return
        
        # Initialize backtester
        backtester = Backtester()
        
        # Run backtest
        results = backtester.run(strategy_name, data_path=data, params=strategy_params)
        
        # Save results
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results_file = output_path / f"{strategy_name}_backtest_{datetime.now().strftime('%Y%m%d')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        click.echo(f"✅ Backtest completed! Results saved to: {results_file}")
        
    except ImportError as e:
        click.echo(f"❌ Error importing backtester: {e}")
    except Exception as e:
        click.echo(f"❌ Error running backtest: {e}")

@strategy.command()
def list():
    """List available trading strategies."""
    try:
        from core.strategies import StrategyRegistry
        
        registry = StrategyRegistry()
        strategies = registry.list_strategies()
        
        click.echo("📈 Available Trading Strategies:")
        click.echo("=" * 50)
        
        for category, strategy_list in strategies.items():
            click.echo(f"\n{category}:")
            for strategy in strategy_list:
                click.echo(f"  • {strategy['name']} - {strategy['description']}")
                click.echo(f"    Risk Level: {strategy['risk_level']}")
                click.echo(f"    Asset Class: {strategy['asset_class']}")
                click.echo()
        
    except ImportError as e:
        click.echo(f"❌ Error importing strategy registry: {e}")
    except Exception as e:
        click.echo(f"❌ Error listing strategies: {e}")

@strategy.command()
@click.argument('strategy_name')
@click.option('--live', is_flag=True, help='Run in live mode')
def run(strategy_name, live):
    """Run a trading strategy."""
    try:
        from core.strategies.runner import StrategyRunner
        
        click.echo(f"🚀 Running strategy: {strategy_name}")
        
        runner = StrategyRunner()
        
        if live:
            click.echo("⚠️ Running in LIVE mode - real money will be used!")
            if not click.confirm("Are you sure you want to continue?"):
                click.echo("❌ Strategy execution cancelled.")
                return
        
        runner.run(strategy_name, live=live)
        
        click.echo("✅ Strategy execution completed!")
        
    except ImportError as e:
        click.echo(f"❌ Error importing strategy runner: {e}")
    except Exception as e:
        click.echo(f"❌ Error running strategy: {e}")

@main.group()
def research():
    """Research and analysis commands."""
    pass

@research.command()
@click.argument('asset_class')
@click.option('--period', '-p', default='1y', help='Analysis period')
@click.option('--output', '-o', default='research/reports', help='Output directory')
def analyze(asset_class, period, output):
    """Analyze a specific asset class."""
    try:
        from core.models.analysis import AssetAnalyzer
        
        click.echo(f"🔍 Analyzing {asset_class} for {period} period...")
        
        analyzer = AssetAnalyzer()
        results = analyzer.analyze_asset_class(asset_class, period=period)
        
        # Save results
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        report_file = output_path / f"{asset_class}_analysis_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        click.echo(f"✅ Analysis completed! Report saved to: {report_file}")
        
    except ImportError as e:
        click.echo(f"❌ Error importing asset analyzer: {e}")
    except Exception as e:
        click.echo(f"❌ Error analyzing asset class: {e}")

@research.command()
@click.option('--output', '-o', default='research/reports', help='Output directory')
@click.option('--format', '-f', type=click.Choice(['pdf', 'html', 'markdown']), default='pdf')
def generate_report(output, format):
    """Generate comprehensive market report."""
    try:
        from core.utils.reporting import ReportGenerator
        
        click.echo(f"📋 Generating market report in {format.upper()} format...")
        
        generator = ReportGenerator()
        report_file = generator.generate_report(output_dir=output, format=format)
        
        click.echo(f"✅ Report generated successfully!")
        click.echo(f"📄 Report saved to: {report_file}")
        
    except ImportError as e:
        click.echo(f"❌ Error importing report generator: {e}")
    except Exception as e:
        click.echo(f"❌ Error generating report: {e}")

@main.group()
def education():
    """Educational content commands."""
    pass

@education.command()
@click.option('--questions', '-n', default=3, help='Number of questions')
@click.option('--difficulty', '-d', type=click.Choice(['easy', 'medium', 'hard']), default='medium')
@click.option('--output', '-o', default='education/quizzes', help='Output directory')
def generate_quiz(questions, difficulty, output):
    """Generate daily finance quiz."""
    try:
        from education.quizzes.generator import QuizGenerator
        
        click.echo(f"🎯 Generating {questions} {difficulty} quiz questions...")
        
        generator = QuizGenerator()
        quiz_file = generator.generate_quiz(
            num_questions=questions, 
            difficulty=difficulty, 
            output_dir=output
        )
        
        click.echo(f"✅ Quiz generated successfully!")
        click.echo(f"📝 Quiz saved to: {quiz_file}")
        
    except ImportError as e:
        click.echo(f"❌ Error importing quiz generator: {e}")
    except Exception as e:
        click.echo(f"❌ Error generating quiz: {e}")

@education.command()
def take_quiz():
    """Take an interactive finance quiz."""
    try:
        from education.quizzes.interactive import InteractiveQuiz
        
        click.echo("🎯 Interactive Finance Quiz")
        click.echo("=" * 30)
        
        quiz = InteractiveQuiz()
        score = quiz.run()
        
        click.echo(f"\n🎉 Quiz completed! Final Score: {score}")
        
    except ImportError as e:
        click.echo(f"❌ Error importing interactive quiz: {e}")
    except Exception as e:
        click.echo(f"❌ Error taking quiz: {e}")

@education.command()
@click.argument('topic')
@click.option('--format', '-f', type=click.Choice(['notebook', 'pdf', 'html']), default='notebook')
def create_tutorial(topic, format):
    """Create a tutorial on a specific topic."""
    try:
        from education.tutorials.generator import TutorialGenerator
        
        click.echo(f"📚 Creating tutorial on: {topic}")
        
        generator = TutorialGenerator()
        tutorial_file = generator.create_tutorial(topic, format=format)
        
        click.echo(f"✅ Tutorial created successfully!")
        click.echo(f"📖 Tutorial saved to: {tutorial_file}")
        
    except ImportError as e:
        click.echo(f"❌ Error importing tutorial generator: {e}")
    except Exception as e:
        click.echo(f"❌ Error creating tutorial: {e}")

@main.command()
def status():
    """Show system status and recent updates."""
    click.echo("🏥 BuyPolar Capital System Status")
    click.echo("=" * 50)
    
    # Check if key directories exist
    base_path = Path(__file__).parent.parent
    directories = [
        "core",
        "assets",
        "dashboards",
        "research",
        "education",
        "tools",
        "tests",
        "docs"
    ]
    
    for directory in directories:
        dir_path = base_path / directory
        if dir_path.exists():
            click.echo(f"✅ {directory}")
        else:
            click.echo(f"❌ {directory}")
    
    # Check data availability
    data_path = base_path / "data" / "processed"
    if data_path.exists() and any(data_path.iterdir()):
        click.echo("✅ Market data available")
    else:
        click.echo("❌ No market data found")
    
    click.echo(f"\n📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@main.command()
def docs():
    """Open documentation in browser."""
    docs_url = "https://yourusername.github.io/buypolarcapital/"
    click.echo(f"📚 Opening documentation: {docs_url}")
    webbrowser.open(docs_url)

@main.command()
def github():
    """Open GitHub repository in browser."""
    repo_url = "https://github.com/yourusername/buypolarcapital"
    click.echo(f"🐙 Opening GitHub repository: {repo_url}")
    webbrowser.open(repo_url)

@main.command()
def website():
    """Open the interactive website in browser."""
    website_url = "https://yourusername.github.io/buypolarcapital/"
    click.echo(f"🌐 Opening interactive website: {website_url}")
    webbrowser.open(website_url)

@main.group()
def tools():
    """Utility tools and automation."""
    pass

@tools.command()
@click.option('--format', '-f', type=click.Choice(['all', 'python', 'r', 'julia']), default='all')
def format_code(format):
    """Format code using style guidelines."""
    try:
        click.echo(f"🎨 Formatting {format} code...")
        
        if format in ['all', 'python']:
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

@tools.command()
def lint():
    """Run code linting and quality checks."""
    try:
        click.echo("🔍 Running code quality checks...")
        
        # Run flake8
        subprocess.run([sys.executable, "-m", "flake8", "core", "assets"])
        
        # Run mypy
        subprocess.run([sys.executable, "-m", "mypy", "core", "assets"])
        
        click.echo("✅ Code quality checks completed!")
        
    except Exception as e:
        click.echo(f"❌ Error running linting: {e}")

if __name__ == '__main__':
    main() 