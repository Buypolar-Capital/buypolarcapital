# Research Plots Gallery

This feature automatically discovers and displays all your PDF plots from various simulation directories on your website.

## How It Works

### 1. Automatic Plot Discovery
The system uses a Python script (`scripts/discover_plots.py`) to automatically scan your project directories for PDF plots and categorize them based on:
- Directory structure (e.g., `core/strategies/hft/` → HFT category)
- Filename keywords (e.g., "vwap" → VWAP category)
- Content analysis

### 2. Plot Categories
Plots are automatically categorized into:
- **VWAP Strategies** - Volume Weighted Average Price analysis
- **Arbitrage** - Cross-listing and relative value analysis
- **High-Frequency Trading** - HFT latency and order book analysis
- **Hedging** - Options hedging strategies
- **IPO Analysis** - Event studies and market reactions
- **Equities** - Stock market analysis
- **Cryptocurrency** - Crypto price analysis
- **Fixed Income** - Yield curves and bond analysis

### 3. Website Integration
The plots are displayed in a beautiful gallery with:
- Category filtering
- Search and browse functionality
- Modal viewer for full-screen PDF viewing
- Download and share capabilities
- Responsive design for mobile devices

## Getting Started

### Step 1: Run the Plot Discovery Script
```bash
python scripts/discover_plots.py
```

This will:
- Scan all directories for PDF files
- Generate metadata for each plot
- Create a `plots_data.json` file
- Show a summary of discovered plots

### Step 2: View on Website
1. Open your website (`index.html`)
2. Navigate to the "Plots" section in the navigation
3. Browse plots by category or view all plots
4. Click on any plot to open it in a full-screen modal

## File Structure

```
buypolarcapital/
├── scripts/
│   └── discover_plots.py          # Plot discovery script
├── plots_data.json               # Generated plot metadata
├── index.html                    # Website with plots gallery
├── styles.css                    # Gallery styling
├── script.js                     # Gallery functionality
└── [your plot directories]/
    ├── core/strategies/hft/plots/
    ├── core/strategies/hedge/plots/
    ├── assets/equities/plots/
    └── ... (other plot directories)
```

## Customization

### Adding New Plot Categories
Edit `scripts/discover_plots.py` and add new categories to the `categories` dictionary:

```python
"new_category": {
    "directories": ["path/to/directory"],
    "keywords": ["keyword1", "keyword2"]
}
```

### Modifying Plot Descriptions
The script automatically generates descriptions based on category and filename. You can customize the `_generate_description()` method to create more specific descriptions.

### Styling the Gallery
The gallery uses CSS classes that you can customize in `styles.css`:
- `.plot-card` - Individual plot cards
- `.plot-modal` - Full-screen modal
- `.category-btn` - Category filter buttons

## Features

### Automatic Discovery
- Scans all directories recursively
- Filters out temporary/test files
- Extracts file metadata (size, date, etc.)
- Generates human-readable titles

### Smart Categorization
- Directory-based categorization
- Keyword-based categorization
- Fallback categorization for unknown types

### Interactive Gallery
- Category filtering
- Responsive grid layout
- Hover effects and animations
- Full-screen PDF viewer

### Mobile Optimized
- Responsive design
- Touch-friendly interface
- Optimized for small screens

## Troubleshooting

### No Plots Found
1. Make sure you have PDF files in your project
2. Check that files are not in `.gitignore`
3. Verify file permissions
4. Run the discovery script from the project root

### Plots Not Displaying
1. Check browser console for JavaScript errors
2. Verify `plots_data.json` was generated
3. Ensure PDF files are accessible via web server
4. Check file paths in the JSON file

### Performance Issues
1. Consider generating thumbnails for large PDFs
2. Implement pagination for many plots
3. Use CDN for better loading times
4. Optimize PDF file sizes

## Future Enhancements

- **Thumbnail Generation**: Automatically create preview images
- **Search Functionality**: Full-text search across plot titles and descriptions
- **Advanced Filtering**: Filter by date, size, tags
- **Plot Analytics**: Track which plots are most viewed
- **Export Features**: Export plot collections as reports
- **Collaboration**: Share plot collections with team members

## Support

If you encounter any issues:
1. Check the browser console for errors
2. Verify the plot discovery script runs successfully
3. Ensure all required files are present
4. Test with a simple PDF file first

The plots gallery is designed to be robust and handle various edge cases, but if you need help, the discovery script provides detailed logging to help diagnose issues. 