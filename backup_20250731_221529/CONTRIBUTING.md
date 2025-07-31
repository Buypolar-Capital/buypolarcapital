# Contributing to BuyPolar Capital

Thank you for your interest in contributing to BuyPolar Capital! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch
4. **Make** your changes
5. **Test** your changes
6. **Submit** a pull request

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## 🛠️ Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/buypolarcapital.git
cd buypolarcapital

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## 🔧 Development Setup

### Environment Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

3. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```

### Project Structure

```
buypolarcapital/
├── src/buypolarcapital/     # Main package source
│   ├── assets/              # Asset-specific analysis
│   ├── data_engine/         # Data ingestion and processing
│   ├── modeling/            # Quantitative models
│   ├── strategies/          # Trading strategies
│   ├── risk/               # Risk management tools
│   └── utils/              # Utility functions
├── dashboards/             # Market dashboards
├── notebooks/              # Jupyter notebooks
├── tests/                  # Test suite
├── docs/                   # Documentation
└── scripts/                # Automation scripts
```

## 📝 Contributing Guidelines

### Types of Contributions

We welcome contributions in the following areas:

#### 🎯 **Trading Strategies**
- New algorithmic trading strategies
- Strategy improvements and optimizations
- Backtesting frameworks
- Performance analysis

#### 📊 **Market Analysis**
- Asset class analysis
- Technical indicators
- Fundamental analysis tools
- Market sentiment analysis

#### 🛡️ **Risk Management**
- VaR models
- Portfolio optimization
- Stress testing
- Risk metrics

#### 🧠 **Machine Learning**
- ML models for prediction
- Feature engineering
- Model evaluation
- Automated trading systems

#### 📈 **Data & Infrastructure**
- Data connectors
- Data processing pipelines
- API integrations
- Performance optimizations

#### 📚 **Documentation & Education**
- Tutorial notebooks
- API documentation
- Educational content
- Code examples

### Contribution Workflow

1. **Check existing issues** - Avoid duplicating work
2. **Create an issue** - For bugs, features, or improvements
3. **Fork the repository** - Create your own copy
4. **Create a feature branch** - Use descriptive branch names
5. **Make your changes** - Follow coding standards
6. **Test your changes** - Ensure everything works
7. **Update documentation** - Keep docs in sync
8. **Submit a pull request** - With clear description

### Branch Naming Convention

Use descriptive branch names:
- `feature/strategy-name` - New trading strategies
- `feature/analysis-tool` - New analysis tools
- `bugfix/issue-description` - Bug fixes
- `docs/update-description` - Documentation updates
- `refactor/component-name` - Code refactoring

## 🎨 Code Style

### Python Code Style

We follow PEP 8 with some modifications:

- **Line length:** 88 characters (Black default)
- **Import sorting:** isort
- **Code formatting:** Black
- **Type hints:** Required for public APIs

### Code Quality Tools

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Security scan
bandit -r src/
```

### Example Code Style

```python
"""Module docstring with clear description."""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from buypolarcapital.utils.config import Config


class TradingStrategy:
    """Base class for trading strategies.
    
    This class provides the foundation for implementing
    various trading strategies with common functionality.
    """
    
    def __init__(self, name: str, config: Config) -> None:
        """Initialize the trading strategy.
        
        Args:
            name: Strategy name
            config: Configuration object
        """
        self.name = name
        self.config = config
        self.positions: Dict[str, float] = {}
    
    def calculate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Calculate trading signals from market data.
        
        Args:
            data: Market data with OHLCV columns
            
        Returns:
            Series with trading signals (1: buy, -1: sell, 0: hold)
        """
        # Implementation here
        pass
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/buypolarcapital

# Run specific test file
pytest tests/test_strategies.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Test edge cases and error conditions

### Example Test

```python
"""Tests for trading strategy module."""

import pytest
import pandas as pd
import numpy as np

from buypolarcapital.strategies.mean_reversion import MeanReversionStrategy


class TestMeanReversionStrategy:
    """Test cases for MeanReversionStrategy."""
    
    @pytest.fixture
    def sample_data(self) -> pd.DataFrame:
        """Create sample market data for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        prices = np.random.randn(100).cumsum() + 100
        return pd.DataFrame({
            'close': prices,
            'volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
    
    def test_strategy_initialization(self):
        """Test strategy initialization."""
        strategy = MeanReversionStrategy('test', lookback=20)
        assert strategy.name == 'test'
        assert strategy.lookback == 20
    
    def test_signal_generation(self, sample_data):
        """Test signal generation from market data."""
        strategy = MeanReversionStrategy('test', lookback=20)
        signals = strategy.calculate_signals(sample_data)
        
        assert isinstance(signals, pd.Series)
        assert len(signals) == len(sample_data)
        assert all(signal in [-1, 0, 1] for signal in signals)
```

## 📚 Documentation

### Documentation Standards

- **Docstrings:** Use Google style docstrings
- **Type hints:** Include for all public functions
- **Examples:** Provide usage examples
- **API docs:** Keep up to date

### Example Documentation

```python
def calculate_sharpe_ratio(
    returns: pd.Series, 
    risk_free_rate: float = 0.02,
    periods_per_year: int = 252
) -> float:
    """Calculate the Sharpe ratio for a series of returns.
    
    The Sharpe ratio measures the risk-adjusted return of an investment.
    It is calculated as (R_p - R_f) / σ_p, where R_p is the portfolio
    return, R_f is the risk-free rate, and σ_p is the portfolio
    standard deviation.
    
    Args:
        returns: Series of portfolio returns
        risk_free_rate: Annual risk-free rate (default: 0.02)
        periods_per_year: Number of periods per year (default: 252)
        
    Returns:
        Sharpe ratio as a float
        
    Raises:
        ValueError: If returns is empty or contains all NaN values
        
    Example:
        >>> returns = pd.Series([0.01, -0.02, 0.03, 0.01])
        >>> sharpe = calculate_sharpe_ratio(returns)
        >>> print(f"Sharpe ratio: {sharpe:.3f}")
        Sharpe ratio: 0.123
    """
    if returns.empty or returns.isna().all():
        raise ValueError("Returns series cannot be empty or all NaN")
    
    excess_returns = returns - risk_free_rate / periods_per_year
    return excess_returns.mean() / returns.std() * np.sqrt(periods_per_year)
```

## 🔄 Pull Request Process

### Before Submitting

1. **Ensure tests pass** - All tests should be green
2. **Update documentation** - Keep docs in sync with code
3. **Check code style** - Run linting tools
4. **Add type hints** - For all public functions
5. **Write commit messages** - Use conventional commits

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Type hints added

## Related Issues
Closes #(issue number)
```

### Commit Message Format

Use conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(strategies): add mean reversion strategy`
- `fix(dashboard): resolve data loading issue`
- `docs(api): update function documentation`
- `test(risk): add VaR calculation tests`

## 🚀 Release Process

### Versioning

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

### Release Checklist

1. **Update version** in setup.py and __init__.py
2. **Update changelog** with new features/fixes
3. **Run full test suite** - Ensure everything works
4. **Update documentation** - Keep docs current
5. **Create release tag** - Tag the release
6. **Deploy to PyPI** - If applicable
7. **Update GitHub Pages** - Deploy documentation

## 🤝 Getting Help

### Communication Channels

- **GitHub Issues:** For bugs and feature requests
- **GitHub Discussions:** For questions and discussions
- **Email:** For private or sensitive matters

### Resources

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [NumPy Style Guide](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Pandas Contributing Guide](https://pandas.pydata.org/docs/development/contributing.html)

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** - List of contributors
- **Release notes** - Credit for contributions
- **Documentation** - Author attribution

Thank you for contributing to BuyPolar Capital! 🚀 