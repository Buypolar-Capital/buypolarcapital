# Buypolar Capital

[![Website](https://img.shields.io/badge/Website-Live-blue)](https://buypolarcapital.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Quantitative hedge fund leveraging advanced algorithms and data science to navigate market volatility with precision.

## 🚀 Features

- **Research Plots Gallery**: Comprehensive collection of quantitative research and simulation results
- **Dark/Light Theme**: Seamless theme switching with localStorage persistence
- **Responsive Design**: Optimized for all devices
- **High Performance**: 60fps animations with minimal bundle size
- **Modern Stack**: Vanilla HTML/CSS/JS with Lucide icons

## 📁 Project Structure

```
buypolarcapital/
├── index.html              # Main website
├── css/                    # Modular stylesheets
├── js/                     # JavaScript modules
├── plots/                  # Research plot PDFs
├── plots_data.json        # Plot metadata
├── assets/                 # Static assets
├── docs/                   # Documentation
└── scripts/                # Build & deployment scripts
```

## 📖 Documentation

- [Plot Gallery Guide](./docs/PLOTS_GALLERY_README.md)
- [Redesign Summary](./docs/REDESIGN_SUMMARY.md)

## 🎨 Theme Support

The website features automatic dark/light theme switching:
- Light mode: Clean, professional white background
- Dark mode: Deep black (#0a0a0a) for reduced eye strain
- Theme persists across sessions using localStorage
- Respects system preferences (prefers-color-scheme)

## 🛠️ Development

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Buypolar-Capital/buypolarcapital.git
   cd buypolarcapital
   ```

2. Open `index.html` in your browser or use a local server:
   ```bash
   python -m http.server 8000
   # or
   npx serve
   ```

3. Visit `http://localhost:8000`

### Adding Research Plots

1. Add your plot PDF to the `plots/` directory
2. Update `plots_data.json` with plot metadata
3. The plot will automatically appear in the gallery

See [Plot Gallery Guide](./docs/PLOTS_GALLERY_README.md) for detailed instructions.

## 🌐 Deployment

The site is automatically deployed via GitHub Pages from the `main` branch.

## 📊 Research Focus

- VWAP Strategies
- Cross-Listing Arbitrage
- High-Frequency Trading Analysis
- IPO Event Studies
- Cryptocurrency Analysis
- Fixed Income Research

## 📧 Contact

- Email: [buypolarcapital@gmail.com](mailto:buypolarcapital@gmail.com)
- GitHub: [@Buypolar-Capital](https://github.com/Buypolar-Capital)
- Twitter: [@buypolarcapital](https://twitter.com/buypolarcapital)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

**Built with ❤️ for quantitative research**
