// Buypolar Capital - Plots Gallery Module

// Initialize plots gallery
function initializePlotsGallery() {
    try {
        loadPlotsData();
        initializeCategoryFilters();
        initializePlotModal();
    } catch (error) {
        handleError(error, 'initializing plots gallery');
    }
}

// Load plots data
function loadPlotsData() {
    // Try to load real data first, fallback to sample data
    fetch('plots_data.json')
        .then(response => response.json())
        .then(data => {
            plotsData = data.plots.map(plot => ({
                id: plot.id,
                title: plot.title,
                category: plot.category,
                description: plot.description,
                image: plot.thumbnail || `https://via.placeholder.com/400x250/2196F3/ffffff?text=${encodeURIComponent(plot.title)}`,
                date: plot.modified_date,
                tags: plot.tags,
                filename: plot.filename,
                path: plot.path
            }));
            renderPlotsGrid();
        })
        .catch(error => {
            console.log('Failed to load plots data, using sample data:', error);
            createSamplePlotsData();
            renderPlotsGrid();
        });
}

// Create sample plots data
function createSamplePlotsData() {
    plotsData = [
        {
            id: 1,
            title: 'Bitcoin Price Analysis',
            category: 'crypto',
            description: 'Comprehensive analysis of Bitcoin price movements with technical indicators',
            image: 'https://via.placeholder.com/400x250/2196F3/ffffff?text=Bitcoin+Analysis',
            date: '2024-01-15',
            tags: ['bitcoin', 'crypto', 'technical-analysis']
        },
        {
            id: 2,
            title: 'S&P 500 Volatility Study',
            category: 'equities',
            description: 'Analysis of S&P 500 volatility patterns and market regime changes',
            image: 'https://via.placeholder.com/400x250/4CAF50/ffffff?text=S%26P+500+Volatility',
            date: '2024-01-10',
            tags: ['sp500', 'volatility', 'equities']
        },
        {
            id: 3,
            title: 'Yield Curve Dynamics',
            category: 'fixed-income',
            description: 'Treasury yield curve analysis and economic indicator relationships',
            image: 'https://via.placeholder.com/400x250/FF9800/ffffff?text=Yield+Curve',
            date: '2024-01-08',
            tags: ['yield-curve', 'treasury', 'fixed-income']
        },
        {
            id: 4,
            title: 'Gold vs USD Correlation',
            category: 'commodities',
            description: 'Correlation analysis between gold prices and US dollar strength',
            image: 'https://via.placeholder.com/400x250/FFC107/ffffff?text=Gold+vs+USD',
            date: '2024-01-05',
            tags: ['gold', 'usd', 'correlation', 'commodities']
        },
        {
            id: 5,
            title: 'Ethereum Network Metrics',
            category: 'crypto',
            description: 'Ethereum network activity and gas price analysis',
            image: 'https://via.placeholder.com/400x250/9C27B0/ffffff?text=Ethereum+Metrics',
            date: '2024-01-03',
            tags: ['ethereum', 'gas', 'network', 'crypto']
        },
        {
            id: 6,
            title: 'European Banking Sector',
            category: 'equities',
            description: 'Performance analysis of major European banking institutions',
            image: 'https://via.placeholder.com/400x250/607D8B/ffffff?text=European+Banks',
            date: '2023-12-28',
            tags: ['european-banks', 'financial-sector', 'equities']
        },
        {
            id: 7,
            title: 'Corporate Bond Spreads',
            category: 'fixed-income',
            description: 'Investment grade vs high yield corporate bond spread analysis',
            image: 'https://via.placeholder.com/400x250/795548/ffffff?text=Corporate+Spreads',
            date: '2023-12-25',
            tags: ['corporate-bonds', 'credit-spreads', 'fixed-income']
        },
        {
            id: 8,
            title: 'Oil Price Forecasting',
            category: 'commodities',
            description: 'Crude oil price prediction models using machine learning',
            image: 'https://via.placeholder.com/400x250/FF5722/ffffff?text=Oil+Forecasting',
            date: '2023-12-20',
            tags: ['oil', 'forecasting', 'machine-learning', 'commodities']
        },
        {
            id: 9,
            title: 'DeFi Protocol Analysis',
            category: 'crypto',
            description: 'Decentralized finance protocol performance and risk metrics',
            image: 'https://via.placeholder.com/400x250/3F51B5/ffffff?text=DeFi+Analysis',
            date: '2023-12-18',
            tags: ['defi', 'protocols', 'risk', 'crypto']
        },
        {
            id: 10,
            title: 'Asian Market Correlation',
            category: 'equities',
            description: 'Cross-market correlation analysis in Asian equity markets',
            image: 'https://via.placeholder.com/400x250/009688/ffffff?text=Asian+Markets',
            date: '2023-12-15',
            tags: ['asian-markets', 'correlation', 'equities']
        },
        {
            id: 11,
            title: 'Municipal Bond Analysis',
            category: 'fixed-income',
            description: 'Municipal bond performance and tax-equivalent yield analysis',
            image: 'https://via.placeholder.com/400x250/8BC34A/ffffff?text=Municipal+Bonds',
            date: '2023-12-12',
            tags: ['municipal-bonds', 'tax-equivalent', 'fixed-income']
        },
        {
            id: 12,
            title: 'Agricultural Commodities',
            category: 'commodities',
            description: 'Weather impact on agricultural commodity prices',
            image: 'https://via.placeholder.com/400x250/CDDC39/ffffff?text=Agricultural',
            date: '2023-12-10',
            tags: ['agricultural', 'weather', 'commodities']
        }
    ];
}

// Initialize category filters
function initializeCategoryFilters() {
    const filterButtons = document.querySelectorAll('.category-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update current category
            currentCategory = this.dataset.category;
            
            // Re-render plots grid
            renderPlotsGrid();
        });
    });
}

// Render plots grid
function renderPlotsGrid() {
    const plotsContainer = document.getElementById('plots-grid');
    if (!plotsContainer) return;
    
    // Filter plots based on current category
    let filteredPlots = plotsData;
    if (currentCategory !== 'all') {
        filteredPlots = plotsData.filter(plot => plot.category === currentCategory);
    }
    
    // Clear container
    plotsContainer.innerHTML = '';
    
    // Create plot cards
    filteredPlots.forEach(plot => {
        const plotCard = createPlotCard(plot);
        plotsContainer.appendChild(plotCard);
    });
    
    // Update results count
    const resultsCount = document.getElementById('plots-results-count');
    if (resultsCount) {
        resultsCount.textContent = `${filteredPlots.length} plot${filteredPlots.length !== 1 ? 's' : ''} found`;
    }
}

// Create plot card
function createPlotCard(plot) {
    const card = document.createElement('div');
    card.className = 'plot-card';
    
    // Generate a nice gradient background based on category
    const categoryColors = {
        'vwap': 'linear-gradient(135deg, #2196F3, #4CAF50)',
        'arbitrage': 'linear-gradient(135deg, #FF9800, #FF5722)',
        'hft': 'linear-gradient(135deg, #9C27B0, #3F51B5)',
        'hedging': 'linear-gradient(135deg, #4CAF50, #8BC34A)',
        'ipo': 'linear-gradient(135deg, #00BCD4, #009688)',
        'equities': 'linear-gradient(135deg, #607D8B, #795548)',
        'crypto': 'linear-gradient(135deg, #FFC107, #FF9800)',
        'fixed-income': 'linear-gradient(135deg, #E91E63, #9C27B0)',
        'commodities': 'linear-gradient(135deg, #CDDC39, #8BC34A)'
    };
    
    const gradient = categoryColors[plot.category] || 'linear-gradient(135deg, #2196F3, #4CAF50)';
    
    card.innerHTML = `
        <div class="plot-image">
            <div class="plot-preview" style="background: ${gradient};">
                <div class="plot-preview-content">
                    <div class="plot-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="plot-category">${plot.category.replace('-', ' ').toUpperCase()}</div>
                </div>
            </div>
            <div class="plot-overlay">
                <button class="view-plot-btn" onclick="handlePlotView('${plot.id}', '${plot.path || ''}')">
                    <i class="fas fa-eye"></i> View Analysis
                </button>
                <div class="plot-actions">
                    <button class="share-btn" onclick="copyPlotLink('${plot.id}')" title="Share">
                        <i class="fas fa-share-alt"></i>
                    </button>
                </div>
            </div>
        </div>
        <div class="plot-content">
            <h3 class="plot-title">${plot.title}</h3>
            <p class="plot-description">${plot.description}</p>
            <div class="plot-meta">
                <span class="plot-date">
                    <i class="fas fa-calendar"></i>
                    ${plot.date || 'N/A'}
                </span>
                <div class="plot-tags">
                    ${(plot.tags || []).map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// Handle plot view (PDF or modal)
function handlePlotView(plotId, plotPath) {
    if (plotPath && plotPath.trim() !== '') {
        // Use GitHub Pages URL instead of raw URL to open PDFs in browser
        const pagesUrl = plotPath.replace('plots/', 'https://buypolar-capital.github.io/buypolarcapital/plots/');
        
        // Open PDF in new tab - GitHub Pages should serve PDFs with proper headers
        window.open(pagesUrl, '_blank', 'noopener,noreferrer');
    } else {
        // Open modal for plots without PDF
        openPlotModal(plotId);
    }
}

// Initialize plot modal
function initializePlotModal() {
    // Create modal backdrop
    const modalBackdrop = document.createElement('div');
    modalBackdrop.id = 'plot-modal-backdrop';
    modalBackdrop.className = 'modal-backdrop';
    modalBackdrop.style.display = 'none';
    modalBackdrop.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modal-title"></h2>
                <button class="close-modal" onclick="closePlotModal()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <div class="modal-image">
                    <img id="modal-image" src="" alt="">
                </div>
                <div class="modal-description">
                    <p id="modal-description"></p>
                    <div class="modal-meta">
                        <span id="modal-date"></span>
                        <div id="modal-tags"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modalBackdrop);
    
    // Close modal when clicking backdrop
    modalBackdrop.addEventListener('click', function(e) {
        if (e.target === this) {
            closePlotModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closePlotModal();
        }
    });
}

// Open plot modal
function openPlotModal(plotId) {
    const plot = plotsData.find(p => p.id === plotId);
    if (!plot) return;
    
    const modalBackdrop = document.getElementById('plot-modal-backdrop');
    const modalTitle = document.getElementById('modal-title');
    const modalImage = document.getElementById('modal-image');
    const modalDescription = document.getElementById('modal-description');
    const modalDate = document.getElementById('modal-date');
    const modalTags = document.getElementById('modal-tags');
    
    // Populate modal content
    modalTitle.textContent = plot.title;
    modalImage.src = plot.image;
    modalImage.alt = plot.title;
    modalDescription.textContent = plot.description;
    modalDate.textContent = new Date(plot.date).toLocaleDateString();
    modalTags.innerHTML = plot.tags.map(tag => `<span class="tag">${tag}</span>`).join('');
    
    // Show modal
    modalBackdrop.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

// Close plot modal
function closePlotModal() {
    const modalBackdrop = document.getElementById('plot-modal-backdrop');
    if (modalBackdrop) {
        modalBackdrop.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}



// Share plot link function
function copyPlotLink(plotId) {
    const plot = plotsData.find(p => p.id === plotId);
    if (!plot) return;
    
    const plotUrl = `${window.location.href}#research-plots-${plotId}`;
    
    navigator.clipboard.writeText(plotUrl).then(() => {
        // Show simple success message
        const message = document.createElement('div');
        message.className = 'copy-success-message';
        message.textContent = 'Link copied to clipboard!';
        document.body.appendChild(message);
        
        setTimeout(() => {
            if (message.parentElement) {
                message.remove();
            }
        }, 2000);
    }).catch(() => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = plotUrl;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        // Show simple success message
        const message = document.createElement('div');
        message.className = 'copy-success-message';
        message.textContent = 'Link copied to clipboard!';
        document.body.appendChild(message);
        
        setTimeout(() => {
            if (message.parentElement) {
                message.remove();
            }
        }, 2000);
    });
} 