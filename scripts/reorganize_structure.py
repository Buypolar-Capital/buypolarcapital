#!/usr/bin/env python3
"""
BuyPolar Capital - Streamlined Folder Structure Reorganization

This script creates a simplified, focused folder structure for the repository.
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

class StreamlinedReorganizer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.backup_path = self.base_path / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def create_simplified_structure(self):
        """Create a simplified, focused folder structure."""
        print("Creating simplified folder structure...")
        
        # Essential directories only
        essential_dirs = [
            "core/data",
            "core/strategies", 
            "core/utils",
            "assets/equities",
            "assets/fixed_income",
            "assets/commodities",
            "assets/crypto",
            "dashboards",
            "data/processed",
            "docs",
            "tests"
        ]
        
        for dir_path in essential_dirs:
            full_path = self.base_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {dir_path}")
            
        # Create __init__.py files for Python packages
        python_dirs = [
            "core", "core/data", "core/strategies", "core/utils",
            "assets", "assets/equities", "assets/fixed_income", 
            "assets/commodities", "assets/crypto"
        ]
        
        for dir_path in python_dirs:
            init_file = self.base_path / dir_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
                print(f"Created: {dir_path}/__init__.py")
    
    def backup_existing_structure(self):
        """Create a backup of the existing structure."""
        print(f"Creating backup at: {self.backup_path}")
        
        if self.base_path.exists():
            shutil.copytree(self.base_path, self.backup_path, 
                           ignore=shutil.ignore_patterns('backup_*', '.git', '__pycache__', '*.pyc'))
    
    def migrate_essential_files(self):
        """Migrate only essential files to the new structure."""
        print("Migrating essential files...")
        
        # Simple migration mapping
        migrations = {
            "src/buypolarcapital/data_engine": "core/data",
            "src/buypolarcapital/strategies": "core/strategies",
            "src/buypolarcapital/utils": "core/utils",
            "src/buypolarcapital/assets/equities": "assets/equities",
            "src/buypolarcapital/assets/fi": "assets/fixed_income",
            "src/buypolarcapital/assets/commodities": "assets/commodities",
            "src/buypolarcapital/assets/crypto": "assets/crypto",
            "dashboards": "dashboards",
            "notebooks": "docs/notebooks"
        }
        
        for old_path, new_path in migrations.items():
            old_full = self.base_path / old_path
            new_full = self.base_path / new_path
            
            if old_full.exists():
                print(f"Moving {old_path} -> {new_path}")
                try:
                    if new_full.exists():
                        self.merge_directories(old_full, new_full)
                    else:
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
    
    def create_simplified_setup(self):
        """Create a simplified setup.py."""
        setup_content = '''#!/usr/bin/env python3
"""
BuyPolar Capital - Quantitative Finance Research Hub
"""

from setuptools import setup, find_packages

def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="buypolarcapital",
    version="2.0.0",
    author="BuyPolar Capital",
    description="Interactive Quantitative Finance Research Hub",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/buypolarcapital",
    packages=find_packages(include=['core*', 'assets*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "buypolar=core.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
'''
        
        setup_path = self.base_path / "setup.py"
        with open(setup_path, 'w') as f:
            f.write(setup_content)
        
        print("Created simplified setup.py")
    
    def create_migration_guide(self):
        """Create a simple migration guide."""
        guide_content = f"""# BuyPolar Capital - Simplified Migration Guide

## Simplified Folder Structure

The repository has been reorganized for better focus and maintainability.

### Key Changes

#### New Structure:
```
buypolarcapital/
├── core/                    # Core functionality
│   ├── data/               # Data management
│   ├── strategies/         # Trading strategies
│   └── utils/              # Utility functions
├── assets/                 # Asset-specific analysis
│   ├── equities/           # Equity analysis
│   ├── fixed_income/       # Fixed income analysis
│   ├── commodities/        # Commodity analysis
│   └── crypto/             # Cryptocurrency analysis
├── dashboards/             # Interactive dashboards
├── data/                   # Data storage
├── docs/                   # Documentation
└── tests/                  # Test suite
```

### Updating Import Statements

#### Before:
```python
from buypolarcapital.data_engine import DataConnector
from buypolarcapital.strategies.hft import HFTStrategy
```

#### After:
```python
from core.data import DataConnector
from core.strategies.hft import HFTStrategy
```

### Rollback

If needed, the original structure is backed up at: `{self.backup_path}`

Migration completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        guide_path = self.base_path / "MIGRATION_GUIDE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print("Created migration guide: MIGRATION_GUIDE.md")
    
    def cleanup_redundant_files(self):
        """Remove redundant files and directories."""
        print("Cleaning up redundant files...")
        
        # Files to remove
        files_to_remove = [
            "FOLDER_STRUCTURE_OPTIMIZATION.md",
            "OPTIMIZATION_SUMMARY.md", 
            "INTERACTIVE_OPTIMIZATION_SUMMARY.md",
            "repo.txt",
            "repo – Kopi.txt"
        ]
        
        for file_name in files_to_remove:
            file_path = self.base_path / file_name
            if file_path.exists():
                file_path.unlink()
                print(f"Removed: {file_name}")
        
        # Directories to remove (if empty)
        dirs_to_remove = [
            "ideas",
            "scripts/articles",
            "scripts/deployment", 
            "scripts/ingestion",
            "scripts/backtesting",
            "scripts/reporting"
        ]
        
        for dir_name in dirs_to_remove:
            dir_path = self.base_path / dir_name
            if dir_path.exists() and not any(dir_path.iterdir()):
                dir_path.rmdir()
                print(f"Removed empty directory: {dir_name}")
    
    def run_migration(self):
        """Run the complete streamlined migration process."""
        print("Starting BuyPolar Capital streamlined migration...")
        print("=" * 60)
        
        # Step 1: Create backup
        self.backup_existing_structure()
        
        # Step 2: Create simplified structure
        self.create_simplified_structure()
        
        # Step 3: Migrate essential files
        self.migrate_essential_files()
        
        # Step 4: Create simplified setup
        self.create_simplified_setup()
        
        # Step 5: Create migration guide
        self.create_migration_guide()
        
        # Step 6: Cleanup redundant files
        self.cleanup_redundant_files()
        
        print("=" * 60)
        print("Streamlined migration completed successfully!")
        print(f"Backup available at: {self.backup_path}")
        print("Please review MIGRATION_GUIDE.md for next steps")
        print("Repository is now focused and streamlined!")

def main():
    """Main function to run the migration."""
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "."
    
    reorganizer = StreamlinedReorganizer(base_path)
    reorganizer.run_migration()

if __name__ == "__main__":
    main() 