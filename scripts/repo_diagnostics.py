#!/usr/bin/env python3
"""
BuyPolar Capital - Repository Diagnostics Script

This script analyzes the current state of the repository and provides
comprehensive statistics and recommendations for cleanup and improvement.
"""

import os
import sys
from pathlib import Path
from collections import defaultdict, Counter
import json
from datetime import datetime
import re

class RepositoryDiagnostics:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'file_types': Counter(),
            'largest_files': [],
            'duplicate_files': [],
            'empty_files': [],
            'old_backups': [],
            'python_files': [],
            'documentation_files': [],
            'data_files': [],
            'structure_issues': [],
            'website_files': []
        }
        
    def analyze_repository(self):
        """Perform comprehensive repository analysis."""
        print("🔍 Analyzing BuyPolar Capital repository...")
        print("=" * 60)
        
        # Walk through all files and directories
        for root, dirs, files in os.walk(self.base_path):
            root_path = Path(root)
            
            # Skip git and backup directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('backup_')]
            
            self.stats['total_dirs'] += len(dirs)
            
            for file in files:
                file_path = root_path / file
                relative_path = file_path.relative_to(self.base_path)
                
                self.stats['total_files'] += 1
                
                # Analyze file type
                suffix = file_path.suffix.lower()
                self.stats['file_types'][suffix] += 1
                
                # Get file size
                try:
                    file_size = file_path.stat().st_size
                    
                    # Track largest files
                    self.stats['largest_files'].append((str(relative_path), file_size))
                    
                    # Track empty files
                    if file_size == 0:
                        self.stats['empty_files'].append(str(relative_path))
                        
                except (OSError, PermissionError):
                    continue
                
                # Categorize files
                self._categorize_file(file_path, relative_path)
        
        # Sort largest files
        self.stats['largest_files'].sort(key=lambda x: x[1], reverse=True)
        self.stats['largest_files'] = self.stats['largest_files'][:20]
        
        # Find duplicate files
        self._find_duplicates()
        
        # Find old backups
        self._find_old_backups()
        
        # Analyze structure issues
        self._analyze_structure_issues()
        
        # Analyze website
        self._analyze_website()
        
    def _categorize_file(self, file_path, relative_path):
        """Categorize files by type and purpose."""
        suffix = file_path.suffix.lower()
        path_str = str(relative_path)
        
        # Python files
        if suffix == '.py':
            self.stats['python_files'].append(path_str)
            
        # Documentation files
        elif suffix in ['.md', '.txt', '.rst', '.tex']:
            self.stats['documentation_files'].append(path_str)
            
        # Data files
        elif suffix in ['.csv', '.json', '.xlsx', '.xls', '.parquet', '.h5', '.hdf5']:
            self.stats['data_files'].append(path_str)
            
        # Website files
        if 'docs/' in path_str or suffix in ['.html', '.css', '.js']:
            self.stats['website_files'].append(path_str)
    
    def _find_duplicates(self):
        """Find potential duplicate files."""
        file_hashes = defaultdict(list)
        
        for root, dirs, files in os.walk(self.base_path):
            root_path = Path(root)
            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('backup_')]
            
            for file in files:
                file_path = root_path / file
                relative_path = file_path.relative_to(self.base_path)
                
                # Simple duplicate detection based on name and size
                try:
                    file_size = file_path.stat().st_size
                    key = (file, file_size)
                    file_hashes[key].append(str(relative_path))
                except (OSError, PermissionError):
                    continue
        
        # Find duplicates
        for (filename, size), paths in file_hashes.items():
            if len(paths) > 1 and size > 100:  # Only consider files > 100 bytes
                self.stats['duplicate_files'].append({
                    'filename': filename,
                    'size': size,
                    'locations': paths
                })
    
    def _find_old_backups(self):
        """Find old backup directories and files."""
        for item in self.base_path.iterdir():
            if item.is_dir() and item.name.startswith('backup_'):
                self.stats['old_backups'].append(str(item))
    
    def _analyze_structure_issues(self):
        """Analyze folder structure for issues."""
        issues = []
        
        # Check for deep nesting
        for root, dirs, files in os.walk(self.base_path):
            depth = len(Path(root).relative_to(self.base_path).parts)
            if depth > 6:
                issues.append(f"Deep nesting detected: {root} (depth: {depth})")
        
        # Check for inconsistent naming
        for root, dirs, files in os.walk(self.base_path):
            for dir_name in dirs:
                if re.search(r'[A-Z]', dir_name) and not dir_name.startswith('.'):
                    issues.append(f"Mixed case directory: {root}/{dir_name}")
        
        self.stats['structure_issues'] = issues
    
    def _analyze_website(self):
        """Analyze website files and structure."""
        docs_path = self.base_path / 'docs'
        if docs_path.exists():
            html_files = list(docs_path.rglob('*.html'))
            if len(html_files) <= 2:  # Only index.html files
                self.stats['website_issues'] = "Website appears to be just landing pages"
    
    def generate_report(self):
        """Generate comprehensive diagnostic report."""
        print("\n📊 REPOSITORY DIAGNOSTICS REPORT")
        print("=" * 60)
        
        # Basic statistics
        print(f"\n📈 BASIC STATISTICS:")
        print(f"   Total files: {self.stats['total_files']:,}")
        print(f"   Total directories: {self.stats['total_dirs']:,}")
        print(f"   Repository size: {self._get_repo_size():.1f} MB")
        
        # File type breakdown
        print(f"\n📁 FILE TYPE BREAKDOWN:")
        for ext, count in self.stats['file_types'].most_common(10):
            print(f"   {ext or 'no extension'}: {count:,} files")
        
        # Largest files
        print(f"\n📦 LARGEST FILES:")
        for path, size in self.stats['largest_files'][:10]:
            print(f"   {size/1024/1024:.1f} MB: {path}")
        
        # Empty files
        if self.stats['empty_files']:
            print(f"\n⚠️ EMPTY FILES ({len(self.stats['empty_files'])}):")
            for file in self.stats['empty_files'][:10]:
                print(f"   {file}")
            if len(self.stats['empty_files']) > 10:
                print(f"   ... and {len(self.stats['empty_files']) - 10} more")
        
        # Duplicate files
        if self.stats['duplicate_files']:
            print(f"\n🔄 DUPLICATE FILES ({len(self.stats['duplicate_files'])}):")
            for dup in self.stats['duplicate_files'][:5]:
                print(f"   {dup['filename']} ({dup['size']} bytes):")
                for loc in dup['locations']:
                    print(f"     - {loc}")
        
        # Old backups
        if self.stats['old_backups']:
            print(f"\n🗄️ OLD BACKUPS ({len(self.stats['old_backups'])}):")
            for backup in self.stats['old_backups']:
                print(f"   {backup}")
        
        # Structure issues
        if self.stats['structure_issues']:
            print(f"\n🏗️ STRUCTURE ISSUES ({len(self.stats['structure_issues'])}):")
            for issue in self.stats['structure_issues'][:5]:
                print(f"   {issue}")
        
        # Python files analysis
        print(f"\n🐍 PYTHON FILES ({len(self.stats['python_files'])}):")
        py_by_dir = defaultdict(int)
        for py_file in self.stats['python_files']:
            dir_name = str(Path(py_file).parent)
            py_by_dir[dir_name] += 1
        
        for dir_name, count in sorted(py_by_dir.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {dir_name}: {count} files")
        
        # Website analysis
        print(f"\n🌐 WEBSITE ANALYSIS:")
        if 'website_issues' in self.stats:
            print(f"   ⚠️ {self.stats['website_issues']}")
        else:
            print(f"   Website files: {len(self.stats['website_files'])}")
        
        # Generate recommendations
        self._generate_recommendations()
        
        # Save detailed report
        self._save_detailed_report()
    
    def _get_repo_size(self):
        """Calculate total repository size in MB."""
        total_size = 0
        for root, dirs, files in os.walk(self.base_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('backup_')]
            for file in files:
                try:
                    file_path = Path(root) / file
                    total_size += file_path.stat().st_size
                except (OSError, PermissionError):
                    continue
        return total_size / 1024 / 1024
    
    def _generate_recommendations(self):
        """Generate actionable recommendations."""
        print(f"\n💡 RECOMMENDATIONS:")
        
        recommendations = []
        
        # File cleanup
        if self.stats['empty_files']:
            recommendations.append("🗑️ Remove empty files")
        
        if self.stats['duplicate_files']:
            recommendations.append("🔄 Consolidate duplicate files")
        
        if self.stats['old_backups']:
            recommendations.append("🗄️ Clean up old backup directories")
        
        # Structure improvements
        if len(self.stats['python_files']) > 100:
            recommendations.append("📦 Consolidate Python modules into logical packages")
        
        if self.stats['structure_issues']:
            recommendations.append("🏗️ Fix folder structure inconsistencies")
        
        # Website improvements
        if 'website_issues' in self.stats:
            recommendations.append("🌐 Develop proper website with interactive dashboards")
        
        # General cleanup
        if self.stats['total_files'] > 1000:
            recommendations.append("🧹 Implement systematic file organization")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
        print(f"\n🎯 PRIORITY ACTIONS:")
        print("   1. Clean up empty and duplicate files")
        print("   2. Remove old backup directories")
        print("   3. Consolidate Python code structure")
        print("   4. Develop interactive website/dashboards")
        print("   5. Implement proper documentation")
    
    def _save_detailed_report(self):
        """Save detailed report to JSON file."""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'repository_path': str(self.base_path),
            'statistics': {
                'total_files': self.stats['total_files'],
                'total_dirs': self.stats['total_dirs'],
                'file_types': dict(self.stats['file_types']),
                'python_files_count': len(self.stats['python_files']),
                'documentation_files_count': len(self.stats['documentation_files']),
                'data_files_count': len(self.stats['data_files']),
                'empty_files_count': len(self.stats['empty_files']),
                'duplicate_files_count': len(self.stats['duplicate_files']),
                'old_backups_count': len(self.stats['old_backups'])
            },
            'issues': {
                'empty_files': self.stats['empty_files'],
                'duplicate_files': self.stats['duplicate_files'],
                'old_backups': self.stats['old_backups'],
                'structure_issues': self.stats['structure_issues']
            },
            'largest_files': [
                {'path': path, 'size_mb': size/1024/1024} 
                for path, size in self.stats['largest_files'][:20]
            ]
        }
        
        report_path = self.base_path / 'REPOSITORY_DIAGNOSTICS.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed report saved to: REPOSITORY_DIAGNOSTICS.json")

def main():
    """Main function to run diagnostics."""
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "."
    
    diagnostics = RepositoryDiagnostics(base_path)
    diagnostics.analyze_repository()
    diagnostics.generate_report()

if __name__ == "__main__":
    main() 