#!/usr/bin/env python3
"""
BuyPolar Capital - Final Aggressive Cleanup

This script removes all unnecessary files and flattens the structure
to be super clean and minimal.
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

class FinalCleanup:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        
    def run_final_cleanup(self):
        """Run final aggressive cleanup."""
        print("🧹 Starting Final Aggressive Cleanup...")
        print("=" * 60)
        
        # Step 1: Remove unnecessary directories
        self.remove_unnecessary_dirs()
        
        # Step 2: Flatten structure
        self.flatten_structure()
        
        # Step 3: Remove random files
        self.remove_random_files()
        
        # Step 4: Create minimal structure
        self.create_minimal_structure()
        
        print("=" * 60)
        print("✅ Final cleanup completed!")
        print("🎯 Repository is now super clean and minimal!")
        
    def remove_unnecessary_dirs(self):
        """Remove unnecessary directories."""
        print("🗑️ Removing unnecessary directories...")
        
        # Directories to remove completely
        dirs_to_remove = [
            "NBIM",
            "ideas", 
            "docs",
            "tests",
            "scripts/articles",
            "scripts/backtesting",
            "scripts/visualization",
            "dashboards/plots",
            "dashboards/report_outputs",
            "dashboards/data",
            "dashboards/templates",
            "core/strategies/ie/R",
            "core/strategies/ipo/R",
            "core/strategies/rv/R",
            "assets/commodities/R",
            "assets/equities/R",
            "assets/crypto/python/data",
            "assets/crypto/python/plots",
            "assets/crypto/python/report",
            "assets/crypto/python/tick_data",
            "assets/equities/python/plots",
            "assets/fixed_income/python/plots",
            "assets/fixed_income/python/pages",
            "core/strategies/initial_equity/scripts",
            "core/strategies/initial_equity/data",
            "core/strategies/relative_value/data",
            "core/strategies/relative_value/plots",
            "core/models/bimn/python",
            "core/models/bimn/matlab",
            "core/models/bimn/R"
        ]
        
        for dir_path in dirs_to_remove:
            full_path = self.base_path / dir_path
            if full_path.exists():
                try:
                    shutil.rmtree(full_path)
                    print(f"✅ Removed: {dir_path}")
                except Exception:
                    continue
    
    def flatten_structure(self):
        """Flatten the directory structure."""
        print("📁 Flattening structure...")
        
        # Move files from deep nested directories to parent
        flatten_mappings = [
            # Move strategy files to core/strategies
            ("core/strategies/cross_listing", "core/strategies"),
            ("core/strategies/relative_value", "core/strategies"),
            ("core/strategies/initial_equity", "core/strategies"),
            ("core/strategies/ipo", "core/strategies"),
            ("core/strategies/hft", "core/strategies"),
            ("core/strategies/hedge", "core/strategies"),
            
            # Move model files to core/models
            ("core/models/algorithms", "core/models"),
            
            # Move asset files to assets
            ("assets/crypto/python", "assets/crypto"),
            ("assets/equities/python", "assets/equities"),
            ("assets/fixed_income/python", "assets/fixed_income"),
            ("assets/commodities/python", "assets/commodities"),
            
            # Move data files to data
            ("data/masterdata", "data"),
            ("data/raw", "data"),
            ("data/processed", "data")
        ]
        
        for old_path, new_path in flatten_mappings:
            old_full = self.base_path / old_path
            new_full = self.base_path / new_path
            
            if old_full.exists():
                try:
                    new_full.mkdir(parents=True, exist_ok=True)
                    for item in old_full.iterdir():
                        if item.is_file():
                            # Avoid conflicts by adding prefix
                            new_name = f"{old_path.split('/')[-1]}_{item.name}"
                            shutil.move(str(item), str(new_full / new_name))
                except Exception:
                    continue
        
        # Remove empty directories
        self._remove_empty_dirs()
        
        print("✅ Structure flattened")
    
    def _remove_empty_dirs(self):
        """Remove empty directories."""
        for root, dirs, files in os.walk(self.base_path, topdown=False):
            root_path = Path(root)
            if root_path != self.base_path:
                try:
                    if not any(root_path.iterdir()):
                        root_path.rmdir()
                except Exception:
                    continue
    
    def remove_random_files(self):
        """Remove random unnecessary files."""
        print("🗑️ Removing random files...")
        
        # File patterns to remove
        patterns_to_remove = [
            "*.pyc",
            "*.log",
            "*.tmp",
            "*.bak",
            "*.old",
            "*.backup",
            "*.cache",
            "*.swp",
            "*.swo",
            "*.DS_Store",
            "Thumbs.db"
        ]
        
        # Specific files to remove
        files_to_remove = [
            "STREAMLINED_SUMMARY.md",
            "REPOSITORY_DIAGNOSTICS.json",
            "FOLDER_STRUCTURE_OPTIMIZATION.md",
            "MIGRATION_GUIDE.md",
            "setup.py",
            "requirements.txt",
            "CONTRIBUTING.md",
            "LICENSE",
            ".gitattributes",
            "logo.svg",
            "CNAME",
            "scripts/reorganize_structure.py"
        ]
        
        # Remove specific files
        for file_name in files_to_remove:
            file_path = self.base_path / file_name
            if file_path.exists():
                try:
                    file_path.unlink()
                    print(f"✅ Removed: {file_name}")
                except Exception:
                    continue
        
        # Remove files by pattern
        for pattern in patterns_to_remove:
            for file_path in self.base_path.rglob(pattern):
                try:
                    file_path.unlink()
                    print(f"✅ Removed: {file_path.relative_to(self.base_path)}")
                except Exception:
                    continue
    
    def create_minimal_structure(self):
        """Create minimal clean structure."""
        print("🏗️ Creating minimal structure...")
        
        # Define minimal structure
        minimal_dirs = [
            "core",
            "assets",
            "data",
            "scripts",
            "plots"
        ]
        
        for dir_path in minimal_dirs:
            full_path = self.base_path / dir_path
            full_path.mkdir(exist_ok=True)
        
        # Create essential __init__.py files
        init_dirs = ["core", "assets", "data", "scripts", "plots"]
        for dir_path in init_dirs:
            init_file = self.base_path / dir_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
        
        # Move remaining files to appropriate locations
        self._organize_remaining_files()
        
        print("✅ Minimal structure created")
    
    def _organize_remaining_files(self):
        """Organize remaining files into minimal structure."""
        # Move Python files to appropriate directories
        for py_file in self.base_path.rglob("*.py"):
            if py_file.parent != self.base_path:
                try:
                    # Move to scripts if it's a utility script
                    if "script" in py_file.name.lower() or "cleanup" in py_file.name.lower():
                        shutil.move(str(py_file), str(self.base_path / "scripts" / py_file.name))
                    # Move to core if it's core functionality
                    elif "strategy" in str(py_file) or "model" in str(py_file):
                        shutil.move(str(py_file), str(self.base_path / "core" / py_file.name))
                    # Move to assets if it's asset-specific
                    elif "crypto" in str(py_file) or "equity" in str(py_file):
                        shutil.move(str(py_file), str(self.base_path / "assets" / py_file.name))
                except Exception:
                    continue
        
        # Move data files
        for data_file in self.base_path.rglob("*.csv"):
            if data_file.parent != self.base_path:
                try:
                    shutil.move(str(data_file), str(self.base_path / "data" / data_file.name))
                except Exception:
                    continue
        
        # Move plot files
        for plot_file in self.base_path.rglob("*.png"):
            if plot_file.parent != self.base_path:
                try:
                    shutil.move(str(plot_file), str(self.base_path / "plots" / plot_file.name))
                except Exception:
                    continue
        
        for plot_file in self.base_path.rglob("*.pdf"):
            if plot_file.parent != self.base_path:
                try:
                    shutil.move(str(plot_file), str(self.base_path / "plots" / plot_file.name))
                except Exception:
                    continue

def main():
    """Main function."""
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "."
    
    cleanup = FinalCleanup(base_path)
    cleanup.run_final_cleanup()

if __name__ == "__main__":
    main() 