#!/usr/bin/env python3
"""
BuyPolar Capital - Folder Structure Reorganization Script

This script reorganizes the repository structure to be more logical and scalable.
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

class FolderReorganizer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.backup_path = self.base_path / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def create_new_structure(self):
        """Create the new optimized folder structure."""
        print("🏗️ Creating new folder structure...")
        
        # Core structure
        core_dirs = [
            "core/data/connectors",
            "core/data/processors", 
            "core/data/storage",
            "core/data/validation",
            "core/models/risk",
            "core/models/pricing",
            "core/models/forecasting",
            "core/models/optimization",
            "core/strategies/hft",
            "core/strategies/systematic",
            "core/strategies/discretionary",
            "core/strategies/backtesting",
            "core/utils/config",
            "core/utils/logging",
            "core/utils/helpers"
        ]
        
        # Assets structure
        asset_dirs = [
            "assets/equities/analysis",
            "assets/equities/screening",
            "assets/equities/valuation",
            "assets/equities/research",
            "assets/fixed_income/yield_curves",
            "assets/fixed_income/credit",
            "assets/fixed_income/duration",
            "assets/fixed_income/research",
            "assets/commodities/energy",
            "assets/commodities/metals",
            "assets/commodities/agriculture",
            "assets/commodities/research",
            "assets/crypto/technical",
            "assets/crypto/on_chain",
            "assets/crypto/sentiment",
            "assets/crypto/research",
            "assets/options/pricing",
            "assets/options/strategies",
            "assets/options/greeks",
            "assets/options/research",
            "assets/fx/technical",
            "assets/fx/fundamental",
            "assets/fx/carry",
            "assets/fx/research"
        ]
        
        # Other directories
        other_dirs = [
            "dashboards/market_overview",
            "dashboards/portfolio",
            "dashboards/risk",
            "dashboards/research",
            "dashboards/analytics",
            "research/papers",
            "research/notebooks",
            "research/reports",
            "research/presentations",
            "education/tutorials",
            "education/courses",
            "education/quizzes",
            "education/examples",
            "tools/cli",
            "tools/api",
            "tools/scripts",
            "tools/automation",
            "tests/unit",
            "tests/integration",
            "tests/performance",
            "tests/fixtures",
            "docs/api",
            "docs/guides",
            "docs/examples",
            "docs/assets",
            "config/environments",
            "config/databases",
            "config/apis",
            "data/raw",
            "data/processed",
            "data/cached",
            "data/external",
            "logs",
            "temp",
            "deployment/docker",
            "deployment/kubernetes",
            "deployment/ci_cd"
        ]
        
        all_dirs = core_dirs + asset_dirs + other_dirs
        
        for dir_path in all_dirs:
            full_path = self.base_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {dir_path}")
            
        # Create __init__.py files for Python packages
        python_dirs = [
            "core", "core/data", "core/models", "core/strategies", "core/utils",
            "assets", "assets/equities", "assets/fixed_income", "assets/commodities",
            "assets/crypto", "assets/options", "assets/fx"
        ]
        
        for dir_path in python_dirs:
            init_file = self.base_path / dir_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
                print(f"📄 Created: {dir_path}/__init__.py")
    
    def backup_existing_structure(self):
        """Create a backup of the existing structure."""
        print(f"💾 Creating backup at: {self.backup_path}")
        
        # Copy existing structure to backup
        if self.base_path.exists():
            shutil.copytree(self.base_path, self.backup_path, 
                           ignore=shutil.ignore_patterns('backup_*', '.git', '__pycache__', '*.pyc'))
    
    def migrate_existing_files(self):
        """Migrate existing files to the new structure."""
        print("🔄 Migrating existing files...")
        
        # Migration mapping: old_path -> new_path
        migrations = {
            # Core functionality
            "src/buypolarcapital/data_engine": "core/data",
            "src/buypolarcapital/modeling": "core/models", 
            "src/buypolarcapital/strategies": "core/strategies",
            "src/buypolarcapital/utils": "core/utils",
            
            # Asset-specific content
            "src/buypolarcapital/assets/equities": "assets/equities",
            "src/buypolarcapital/assets/fi": "assets/fixed_income",
            "src/buypolarcapital/assets/commodities": "assets/commodities",
            "src/buypolarcapital/assets/crypto": "assets/crypto",
            "src/buypolarcapital/assets/options": "assets/options",
            "src/buypolarcapital/assets/fx": "assets/fx",
            
            # Dashboards
            "dashboards": "dashboards/market_overview",
            
            # Research and education
            "notebooks": "research/notebooks",
            "notebooks/reporting/quiz": "education/quizzes",
            
            # Tools
            "scripts": "tools/scripts",
            
            # Documentation
            "docs": "docs/guides",
        }
        
        for old_path, new_path in migrations.items():
            old_full = self.base_path / old_path
            new_full = self.base_path / new_path
            
            if old_full.exists():
                print(f"📦 Moving {old_path} -> {new_path}")
                try:
                    if new_full.exists():
                        # Merge directories
                        self.merge_directories(old_full, new_full)
                    else:
                        # Move directory
                        shutil.move(str(old_full), str(new_full))
                except Exception as e:
                    print(f"⚠️ Error moving {old_path}: {e}")
    
    def merge_directories(self, src: Path, dst: Path):
        """Merge source directory into destination directory."""
        for item in src.iterdir():
            dst_item = dst / item.name
            if item.is_dir():
                if dst_item.exists():
                    self.merge_directories(item, dst_item)
                else:
                    shutil.move(str(item), str(dst_item))
            else:
                if dst_item.exists():
                    # Add suffix to avoid conflicts
                    name = item.stem
                    suffix = item.suffix
                    counter = 1
                    while dst_item.exists():
                        dst_item = dst / f"{name}_{counter}{suffix}"
                        counter += 1
                shutil.move(str(item), str(dst_item))
        
        # Remove empty source directory
        if not any(src.iterdir()):
            src.rmdir()
    
    def create_migration_guide(self):
        """Create a migration guide for developers."""
        guide_content = f"""# BuyPolar Capital - Migration Guide

## 🚀 New Folder Structure

The repository has been reorganized for better scalability and maintainability.

### Key Changes

#### 1. Core Package Structure
- **Old**: `src/buypolarcapital/`
- **New**: `core/`
  - `core/data/` - Data management
  - `core/models/` - Quantitative models
  - `core/strategies/` - Trading strategies
  - `core/utils/` - Utility functions

#### 2. Asset-Specific Analysis
- **Old**: `src/buypolarcapital/assets/`
- **New**: `assets/`
  - `assets/equities/` - Equity analysis
  - `assets/fixed_income/` - Fixed income analysis
  - `assets/commodities/` - Commodity analysis
  - `assets/crypto/` - Cryptocurrency analysis
  - `assets/options/` - Options analysis
  - `assets/fx/` - Foreign exchange analysis

#### 3. Dashboards
- **Old**: `dashboards/`
- **New**: `dashboards/market_overview/`

#### 4. Research & Education
- **Old**: `notebooks/`
- **New**: `research/notebooks/` and `education/`

### Updating Import Statements

#### Before:
```python
from buypolarcapital.data_engine import DataConnector
from buypolarcapital.strategies.hft import HFTStrategy
```

#### After:
```python
from core.data.connectors import DataConnector
from core.strategies.hft import HFTStrategy
```

### Updating Configuration Files

1. Update `setup.py` package discovery
2. Update import paths in all Python files
3. Update documentation references
4. Update CI/CD configurations

### Rollback

If needed, the original structure is backed up at: `{self.backup_path}`

## 📋 Migration Checklist

- [ ] Update import statements in all Python files
- [ ] Update configuration files
- [ ] Update documentation
- [ ] Update CI/CD pipelines
- [ ] Test all functionality
- [ ] Update README.md
- [ ] Update contributing guidelines

## 🆘 Need Help?

If you encounter issues during migration:
1. Check the backup at `{self.backup_path}`
2. Review the migration logs
3. Create an issue on GitHub
4. Contact the development team

Migration completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        guide_path = self.base_path / "MIGRATION_GUIDE.md"
        with open(guide_path, 'w') as f:
            f.write(guide_content)
        
        print(f"📋 Created migration guide: MIGRATION_GUIDE.md")
    
    def update_setup_py(self):
        """Update setup.py for the new package structure."""
        setup_content = '''#!/usr/bin/env python3
"""
BuyPolar Capital - Quantitative Finance Research Hub
A comprehensive repository for trading algorithms, market analysis, and educational resources.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="buypolarcapital",
    version="1.0.0",
    author="BuyPolar Capital",
    author_email="your.email@example.com",
    description="Quantitative Finance Research Hub with trading algorithms and market analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/buypolarcapital",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/buypolarcapital/issues",
        "Documentation": "https://yourusername.github.io/buypolarcapital/",
        "Source Code": "https://github.com/yourusername/buypolarcapital",
    },
    packages=find_packages(include=['core*', 'assets*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.2.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "jupyterlab>=4.0.0",
            "ipywidgets>=8.0.0",
        ],
        "gpu": [
            "cupy-cuda11x>=12.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "buypolar=core.cli:main",
            "bpc-dashboard=core.dashboards.cli:main",
            "bpc-quiz=core.quiz.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "buypolarcapital": [
            "assets/**/*",
            "data/**/*",
            "templates/**/*",
        ],
    },
    zip_safe=False,
    keywords=[
        "quantitative finance",
        "trading algorithms",
        "market analysis",
        "risk management",
        "machine learning",
        "financial modeling",
        "backtesting",
        "portfolio optimization",
    ],
)
'''
        
        setup_path = self.base_path / "setup.py"
        with open(setup_path, 'w') as f:
            f.write(setup_content)
        
        print("📝 Updated setup.py for new package structure")
    
    def run_migration(self):
        """Run the complete migration process."""
        print("🚀 Starting BuyPolar Capital folder structure migration...")
        print("=" * 60)
        
        # Step 1: Create backup
        self.backup_existing_structure()
        
        # Step 2: Create new structure
        self.create_new_structure()
        
        # Step 3: Migrate files
        self.migrate_existing_files()
        
        # Step 4: Update configuration
        self.update_setup_py()
        
        # Step 5: Create migration guide
        self.create_migration_guide()
        
        print("=" * 60)
        print("✅ Migration completed successfully!")
        print(f"📁 Backup available at: {self.backup_path}")
        print("📋 Please review MIGRATION_GUIDE.md for next steps")
        print("🔄 Remember to update import statements in your code")

def main():
    """Main function to run the migration."""
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "."
    
    reorganizer = FolderReorganizer(base_path)
    reorganizer.run_migration()

if __name__ == "__main__":
    main() 