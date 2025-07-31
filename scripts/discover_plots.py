#!/usr/bin/env python3
"""
Plot Discovery Script for Buypolar Capital Website
Automatically discovers and categorizes PDF plots from various simulation directories
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime
import re

class PlotDiscoverer:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.plots_data = []
        
        # Define plot categories and their associated directories/keywords
        self.categories = {
            "vwap": {
                "directories": ["core/", "algorithms_"],
                "keywords": ["vwap", "volume", "weighted", "average", "price"]
            },
            "arbitrage": {
                "directories": ["core/strategies/cross_listing/", "core/strategies/relative_value/"],
                "keywords": ["arbitrage", "cross", "listing", "relative", "value", "dual", "leapfrog"]
            },
            "hft": {
                "directories": ["core/strategies/hft/"],
                "keywords": ["hft", "high", "frequency", "latency", "order", "book"]
            },
            "hedging": {
                "directories": ["core/strategies/hedge/"],
                "keywords": ["hedge", "hedging", "options", "neutral", "portfolio"]
            },
            "ipo": {
                "directories": ["core/strategies/"],
                "keywords": ["ipo", "event", "study", "abnormal", "returns"]
            },
            "equities": {
                "directories": ["assets/equities/", "assets/initial_equity_"],
                "keywords": ["equity", "stock", "sp500", "osebx", "dowjones", "norwegian"]
            },
            "crypto": {
                "directories": ["assets/crypto/", "assets/python_"],
                "keywords": ["crypto", "bitcoin", "btc", "eth", "binance", "tick"]
            },
            "fixed-income": {
                "directories": ["assets/fixed_income/"],
                "keywords": ["yield", "curve", "bond", "fixed", "income", "spread"]
            }
        }
    
    def discover_plots(self):
        """Discover all PDF plots in the project"""
        print("🔍 Discovering PDF plots...")
        
        # Search for PDF files recursively
        pdf_patterns = [
            "**/*.pdf",
            "plots/**/*.pdf",
            "core/**/plots/*.pdf",
            "assets/**/plots/*.pdf",
            "core/strategies/**/plots/*.pdf"
        ]
        
        all_pdfs = []
        for pattern in pdf_patterns:
            pdfs = list(self.base_dir.glob(pattern))
            all_pdfs.extend(pdfs)
        
        # Remove duplicates and filter out temporary/test files
        unique_pdfs = list(set(all_pdfs))
        filtered_pdfs = [pdf for pdf in unique_pdfs if self._is_valid_plot(pdf)]
        
        print(f"📊 Found {len(filtered_pdfs)} valid PDF plots")
        
        # Process each plot
        for pdf_path in filtered_pdfs:
            plot_info = self._extract_plot_info(pdf_path)
            if plot_info:
                self.plots_data.append(plot_info)
        
        return self.plots_data
    
    def _is_valid_plot(self, pdf_path):
        """Check if a PDF file is a valid plot (not temporary/test file)"""
        filename = pdf_path.name.lower()
        
        # Skip temporary and test files
        skip_patterns = [
            "temp", "test", "scratch", "draft", "backup",
            "old_", "new_", "copy", "version"
        ]
        
        for pattern in skip_patterns:
            if pattern in filename:
                return False
        
        # Skip very small files (likely corrupted or empty)
        try:
            if pdf_path.stat().st_size < 1000:  # Less than 1KB
                return False
        except:
            return False
        
        return True
    
    def _extract_plot_info(self, pdf_path):
        """Extract metadata from a PDF plot file"""
        try:
            # Get file stats
            stat = pdf_path.stat()
            file_size = stat.st_size
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            
            # Determine category
            category = self._categorize_plot(pdf_path)
            
            # Generate title from filename
            title = self._generate_title(pdf_path.name)
            
            # Generate description
            description = self._generate_description(pdf_path, category)
            
            # Create relative path for web access (use forward slashes for web compatibility)
            relative_path = str(pdf_path.relative_to(self.base_dir)).replace('\\', '/')
            
            plot_info = {
                "id": self._generate_id(pdf_path.name),
                "title": title,
                "description": description,
                "category": category,
                "filename": pdf_path.name,
                "path": relative_path,
                "size": self._format_file_size(file_size),
                "size_bytes": file_size,
                "modified": modified_time.isoformat(),
                "modified_date": modified_time.strftime("%B %d, %Y"),
                "thumbnail": self._generate_thumbnail_path(pdf_path),
                "tags": self._extract_tags(pdf_path, category)
            }
            
            return plot_info
            
        except Exception as e:
            print(f"⚠️ Error processing {pdf_path}: {e}")
            return None
    
    def _categorize_plot(self, pdf_path):
        """Categorize a plot based on its path and filename"""
        path_str = str(pdf_path).lower()
        filename = pdf_path.name.lower()
        
        # Check each category
        for category, config in self.categories.items():
            # Check directories
            for directory in config["directories"]:
                if directory in path_str:
                    return category
            
            # Check keywords in filename
            for keyword in config["keywords"]:
                if keyword in filename:
                    return category
        
        # Default category based on directory structure
        if "vwap" in path_str or "algorithms" in path_str:
            return "vwap"
        elif "cross_listing" in path_str or "relative_value" in path_str:
            return "arbitrage"
        elif "hft" in path_str:
            return "hft"
        elif "hedge" in path_str:
            return "hedging"
        elif "ipo" in path_str:
            return "ipo"
        elif "equities" in path_str or "stock" in path_str:
            return "equities"
        elif "crypto" in path_str or "binance" in path_str:
            return "crypto"
        elif "fixed_income" in path_str or "yield" in path_str:
            return "fixed-income"
        
        return "other"
    
    def _generate_title(self, filename):
        """Generate a human-readable title from filename"""
        # Remove extension and common prefixes
        name = filename.replace('.pdf', '')
        name = re.sub(r'^[0-9_]+', '', name)  # Remove leading numbers/underscores
        
        # Replace underscores and hyphens with spaces
        name = name.replace('_', ' ').replace('-', ' ')
        
        # Title case
        name = name.title()
        
        # Clean up common abbreviations
        name = name.replace('Vwap', 'VWAP')
        name = name.replace('Hft', 'HFT')
        name = name.replace('Ipo', 'IPO')
        name = name.replace('Btc', 'BTC')
        name = name.replace('Eth', 'ETH')
        
        return name
    
    def _generate_description(self, pdf_path, category):
        """Generate a description based on the plot category and filename"""
        filename = pdf_path.name.lower()
        
        descriptions = {
            "vwap": "Volume Weighted Average Price analysis and trading strategy performance",
            "arbitrage": "Cross-listing arbitrage opportunities and relative value analysis",
            "hft": "High-frequency trading latency analysis and order book dynamics",
            "hedging": "Options hedging strategies and portfolio risk management",
            "ipo": "Initial Public Offering event study and market reaction analysis",
            "equities": "Equity market analysis and stock performance monitoring",
            "crypto": "Cryptocurrency price analysis and market microstructure",
            "fixed-income": "Yield curve analysis and fixed income market dynamics"
        }
        
        base_desc = descriptions.get(category, "Quantitative analysis and research visualization")
        
        # Add specific details based on filename
        if "portfolio" in filename:
            base_desc += " - Portfolio performance and risk metrics"
        elif "comparison" in filename:
            base_desc += " - Comparative analysis across multiple strategies"
        elif "simulation" in filename:
            base_desc += " - Monte Carlo simulation results"
        elif "backtest" in filename:
            base_desc += " - Historical backtesting results"
        
        return base_desc
    
    def _generate_id(self, filename):
        """Generate a unique ID for the plot"""
        # Remove extension and special characters
        id_str = re.sub(r'[^a-zA-Z0-9]', '_', filename.replace('.pdf', ''))
        return id_str.lower()
    
    def _format_file_size(self, size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def _generate_thumbnail_path(self, pdf_path):
        """Generate path for thumbnail image (placeholder for now)"""
        # For now, return a placeholder. In a real implementation,
        # you might generate actual thumbnails from PDFs
        return f"assets/thumbnails/{pdf_path.stem}.png"
    
    def _extract_tags(self, pdf_path, category):
        """Extract relevant tags from the plot"""
        filename = pdf_path.name.lower()
        tags = [category]
        
        # Add tags based on filename content
        if "portfolio" in filename:
            tags.append("portfolio")
        if "performance" in filename:
            tags.append("performance")
        if "risk" in filename:
            tags.append("risk")
        if "simulation" in filename:
            tags.append("simulation")
        if "backtest" in filename:
            tags.append("backtest")
        if "analysis" in filename:
            tags.append("analysis")
        
        return list(set(tags))  # Remove duplicates
    
    def save_to_json(self, output_file="plots_data.json"):
        """Save the plots data to a JSON file"""
        output_path = self.base_dir / output_file
        
        data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_plots": len(self.plots_data),
                "categories": list(set(plot["category"] for plot in self.plots_data))
            },
            "plots": self.plots_data
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved plots data to {output_path}")
        return output_path
    
    def generate_summary(self):
        """Generate a summary of discovered plots"""
        print("\n📈 Plot Discovery Summary:")
        print("=" * 50)
        
        # Count by category
        category_counts = {}
        for plot in self.plots_data:
            category = plot["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        for category, count in sorted(category_counts.items()):
            print(f"{category.title():<15}: {count:>3} plots")
        
        print(f"\nTotal plots discovered: {len(self.plots_data)}")
        
        # Show some examples
        print("\n🎯 Sample plots:")
        for i, plot in enumerate(self.plots_data[:5]):
            print(f"  {i+1}. {plot['title']} ({plot['category']})")

def main():
    """Main function to run the plot discovery"""
    discoverer = PlotDiscoverer()
    
    # Discover plots
    plots = discoverer.discover_plots()
    
    if plots:
        # Save to JSON
        discoverer.save_to_json()
        
        # Generate summary
        discoverer.generate_summary()
        
        print(f"\n✅ Plot discovery complete! Found {len(plots)} plots.")
        print("📄 The plots_data.json file can be used by your website to display the plots gallery.")
    else:
        print("❌ No plots found. Make sure you have PDF files in your project directories.")

if __name__ == "__main__":
    main() 