// Buypolar Capital - Professional Quant Fund Website
// Interactive JavaScript with real data and comprehensive tools

// Global variables
let performanceChart;
let isNavScrolled = false;

// Modern chart layout helper function
function getModernChartLayout(title, xTitle, yTitle, showLegend = false) {
    return {
        title: {
            text: title,
            font: { 
                family: 'Inter, sans-serif',
                size: 18,
                color: '#000000',
                weight: 600
            },
            x: 0.5,
            xanchor: 'center',
            y: 0.95
        },
        xaxis: { 
            title: { 
                text: xTitle,
                font: { family: 'Inter, sans-serif', size: 13, color: '#666666', weight: 500 }
            },
            gridcolor: '#f8f8f8',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 11, color: '#666666' },
            showline: true,
            linecolor: '#e0e0e0',
            linewidth: 1
        },
        yaxis: { 
            title: { 
                text: yTitle,
                font: { family: 'Inter, sans-serif', size: 13, color: '#666666', weight: 500 }
            },
            gridcolor: '#f8f8f8',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 11, color: '#666666' },
            showline: true,
            linecolor: '#e0e0e0',
            linewidth: 1
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 70, r: 40, t: 80, b: 70 },
        showlegend: showLegend,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 12, color: '#ffffff' },
            bordercolor: '#000000'
        }
    };
}

// Sample data for charts
const cryptoData = {
    BTC: [45000, 46000, 44000, 47000, 48000, 46500, 47500, 49000, 48500, 50000],
    ETH: [3200, 3300, 3150, 3400, 3500, 3350, 3450, 3600, 3550, 3700],
    SOL: [120, 125, 118, 130, 135, 128, 132, 140, 138, 145],
    BNB: [320, 330, 315, 340, 350, 335, 345, 360, 355, 370]
};

const ipoData = {
    companies: ['DBX', 'SPOT', 'META', 'BABA', 'TSLA', 'PLTR', 'LYFT', 'UBER', 'COIN', 'RIVN', 'SNOW', 'ABNB'],
    returns: [15.2, 8.7, 12.3, 18.9, 25.4, 11.2, 6.8, 9.1, 22.7, 14.5, 16.8, 13.2]
};

// Initialize the website
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
});

function initializeWebsite() {
    // Show loading spinner initially
    showLoadingSpinner();
    
    // Initialize navigation
    initializeNavigation();
    
    // Initialize performance chart
    initializePerformanceChart();
    
    // Initialize research charts
    initializeResearchCharts();
    
    // Initialize plots gallery
    initializePlotsGallery();
    
    // Initialize games
    initializeGames();
    
    // Initialize scroll animations
    initializeScrollAnimations();
    
    // Initialize form handlers
    initializeFormHandlers();
    
    // Initialize cookie consent
    initializeCookieConsent();
    
    // Initialize enhanced features
    initializeEnhancedFeatures();
    
    // Hide loading spinner after everything is loaded
    setTimeout(hideLoadingSpinner, 1000);
}

// Enhanced initialization functions
function showLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.classList.remove('hidden');
    }
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.classList.add('hidden');
    }
}

function initializeCookieConsent() {
    const cookieBanner = document.getElementById('cookie-banner');
    const acceptBtn = document.getElementById('accept-cookies');
    const rejectBtn = document.getElementById('reject-cookies');
    
    // Check if user has already made a choice
    const cookieChoice = localStorage.getItem('cookieConsent');
    
    if (!cookieChoice && cookieBanner) {
        // Show cookie banner after a delay
        setTimeout(() => {
            cookieBanner.classList.add('show');
        }, 2000);
    }
    
    if (acceptBtn) {
        acceptBtn.addEventListener('click', () => {
            localStorage.setItem('cookieConsent', 'accepted');
            cookieBanner.classList.remove('show');
        });
    }
    
    if (rejectBtn) {
        rejectBtn.addEventListener('click', () => {
            localStorage.setItem('cookieConsent', 'rejected');
            cookieBanner.classList.remove('show');
        });
    }
}

function initializeEnhancedFeatures() {
    // Update current year in footer
    const currentYearElement = document.getElementById('current-year');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }
    
    // Add smooth scrolling to all internal links
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add input validation
    initializeInputValidation();
    
    // Add tooltips
    initializeTooltips();
}

function initializeInputValidation() {
    const inputs = document.querySelectorAll('input[type="number"], input[type="email"]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });
        
        input.addEventListener('input', function() {
            clearInputError(this);
        });
    });
}

function validateInput(input) {
    const value = input.value.trim();
    const type = input.type;
    
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showInputError(input, 'Please enter a valid email address');
        }
    }
    
    if (type === 'number' && value) {
        const numValue = parseFloat(value);
        if (isNaN(numValue) || numValue < 0) {
            showInputError(input, 'Please enter a valid positive number');
        }
    }
}

function showInputError(input, message) {
    clearInputError(input);
    input.classList.add('error');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'input-error';
    errorDiv.textContent = message;
    errorDiv.style.color = 'var(--accent-red)';
    errorDiv.style.fontSize = '0.8rem';
    errorDiv.style.marginTop = '0.25rem';
    
    input.parentNode.appendChild(errorDiv);
}

function clearInputError(input) {
    input.classList.remove('error');
    const errorDiv = input.parentNode.querySelector('.input-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function initializeTooltips() {
    // Add tooltips to complex tools
    const tooltips = {
        'kelly-fraction': 'The Kelly Fraction determines the optimal percentage of your bankroll to bet based on your edge and odds.',
        'risk-of-ruin': 'Risk of Ruin calculates the probability of losing your entire bankroll before reaching a target profit.',
        'black-scholes': 'The Black-Scholes model is used to price European-style options based on current stock price, strike price, time to expiration, risk-free rate, and volatility.'
    };
    
    Object.keys(tooltips).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.setAttribute('title', tooltips[id]);
        }
    });
}

// Add loading animations
addLoadingAnimations();

// Enhanced Navigation functionality
function initializeNavigation() {
    const navbar = document.querySelector('.navbar');
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100 && !isNavScrolled) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
            isNavScrolled = true;
        } else if (window.scrollY <= 100 && isNavScrolled) {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
            isNavScrolled = false;
        }
        
        // Update active navigation link
        updateActiveNavLink();
    });
    
    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            // Update ARIA attributes for accessibility
            const isExpanded = hamburger.classList.contains('active');
            hamburger.setAttribute('aria-expanded', isExpanded);
        });
    }
    
    // Close mobile menu when clicking on links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (hamburger) {
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            }
            if (navMenu) {
                navMenu.classList.remove('active');
            }
        });
    });
    
    // Keyboard navigation support
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (hamburger && hamburger.classList.contains('active')) {
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
            }
        }
    });
}

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    const scrollPosition = window.scrollY + 100; // Offset for header
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// Performance chart initialization
function initializePerformanceChart() {
    const chartContainer = document.getElementById('performance-chart');
    if (!chartContainer) return;
    
    // Generate sample performance data
    const dates = [];
    const values = [];
    const benchmark = [];
    let currentValue = 100;
    let benchmarkValue = 100;
    
    for (let i = 0; i < 252; i++) {
        const date = new Date();
        date.setDate(date.getDate() - (252 - i));
        dates.push(date.toISOString().split('T')[0]);
        
        // Generate realistic performance with volatility
        const dailyReturn = (Math.random() - 0.5) * 0.02 + 0.0005; // Slight positive bias
        const benchmarkReturn = (Math.random() - 0.5) * 0.015 + 0.0003;
        
        currentValue *= (1 + dailyReturn);
        benchmarkValue *= (1 + benchmarkReturn);
        
        values.push(currentValue);
        benchmark.push(benchmarkValue);
    }
    
    const trace1 = {
        x: dates,
        y: values,
        type: 'scatter',
        mode: 'lines',
        name: 'Buypolar Capital',
        line: {
            color: '#000000',
            width: 3
        },
        fill: 'tonexty',
        fillcolor: 'rgba(0, 0, 0, 0.1)'
    };
    
    const trace2 = {
        x: dates,
        y: benchmark,
        type: 'scatter',
        mode: 'lines',
        name: 'S&P 500',
        line: {
            color: '#666666',
            width: 2,
            dash: 'dash'
        }
    };
    
    const layout = {
        title: {
            text: 'Portfolio Performance vs Benchmark',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Date',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Portfolio Value ($)',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        legend: {
            orientation: 'h',
            y: -0.2,
            bgcolor: 'rgba(255, 255, 255, 0.8)',
            bordercolor: '#e0e0e0',
            borderwidth: 1,
            font: { family: 'Inter, sans-serif', size: 11 }
        },
        margin: { l: 60, r: 30, t: 60, b: 80 },
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    const config = {
        responsive: true,
        displayModeBar: false
    };
    
    Plotly.newPlot('performance-chart', [trace1, trace2], layout, config);
}

// Initialize research charts
function initializeResearchCharts() {
    // Bitcoin Price Chart
    createBitcoinChart();
    
    // Crypto Portfolio Chart
    createCryptoPortfolioChart();
    
    // IPO Performance Chart
    createIPOChart();
    
    // CAR Chart
    createCARChart();
    
    // Unilever Arbitrage Chart
    createUnileverChart();
    
    // Arbitrage Signals Chart
    createArbitrageSignalsChart();
    
    // Latency Distribution Chart
    createLatencyChart();
    
    // Order Book Chart
    createOrderBookChart();
}

function createBitcoinChart() {
    const dates = [];
    const prices = [];
    let currentPrice = 45000;
    
    for (let i = 0; i < 30; i++) {
        const date = new Date();
        date.setDate(date.getDate() - (30 - i));
        dates.push(date.toISOString().split('T')[0]);
        
        const dailyChange = (Math.random() - 0.5) * 0.1; // ±5% daily change
        currentPrice *= (1 + dailyChange);
        prices.push(currentPrice);
    }
    
    const trace = {
        x: dates,
        y: prices,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'BTC/USDT',
        line: {
            color: '#f7931a',
            width: 2
        },
        marker: {
            size: 4,
            color: '#f7931a'
        }
    };
    
    const layout = getModernChartLayout('Bitcoin Price Movement', 'Date', 'Price (USDT)');
    
    Plotly.newPlot('btc-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

function createCryptoPortfolioChart() {
    const assets = Object.keys(cryptoData);
    const returns = assets.map(asset => {
        const prices = cryptoData[asset];
        return ((prices[prices.length - 1] - prices[0]) / prices[0] * 100).toFixed(1);
    });
    
    const trace = {
        x: assets,
        y: returns,
        type: 'bar',
        marker: {
            color: ['#f7931a', '#627eea', '#9945ff', '#f3ba2f'],
            line: { color: '#000000', width: 1 }
        }
    };
    
    const layout = getModernChartLayout('Crypto Portfolio Returns (%)', 'Asset', 'Return (%)');
    
    Plotly.newPlot('crypto-portfolio', [trace], layout, { responsive: true, displayModeBar: false });
}

function createIPOChart() {
    const trace = {
        x: ipoData.companies,
        y: ipoData.returns,
        type: 'bar',
        marker: {
            color: ipoData.returns.map(r => r > 15 ? '#4CAF50' : r > 10 ? '#FF9800' : '#f44336'),
            line: { color: '#000000', width: 1 }
        }
    };
    
    const layout = getModernChartLayout('IPO Performance Comparison', 'Company', 'Return (%)');
    
    Plotly.newPlot('ipo-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

function createCARChart() {
    const eventDays = Array.from({length: 21}, (_, i) => i - 10);
    const carValues = eventDays.map(day => {
        if (day < 0) return Math.random() * 2 - 1; // Pre-event noise
        if (day === 0) return 5 + Math.random() * 3; // IPO day jump
        return 5 + Math.random() * 3 + day * 0.1; // Post-event drift
    });
    
    const trace = {
        x: eventDays,
        y: carValues,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Cumulative Abnormal Returns',
        line: { color: '#1976d2', width: 2 },
        marker: { size: 4, color: '#1976d2' }
    };
    
    const layout = {
        title: {
            text: 'Cumulative Abnormal Returns (Event Study)',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Event Day',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'CAR (%)',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: false,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('car-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

function createUnileverChart() {
    const timePoints = Array.from({length: 100}, (_, i) => i);
    const unileverPrices = timePoints.map(t => 50 + Math.sin(t * 0.1) * 2 + Math.random() * 0.5);
    const ulPrices = timePoints.map(t => 50 + Math.sin(t * 0.1 + 0.1) * 2 + Math.random() * 0.5);
    const spread = unileverPrices.map((u, i) => ((u - ulPrices[i]) / ulPrices[i] * 100).toFixed(2));
    
    const trace1 = {
        x: timePoints,
        y: unileverPrices,
        type: 'scatter',
        mode: 'lines',
        name: 'Unilever (EUR)',
        line: { color: '#1976d2', width: 2 }
    };
    
    const trace2 = {
        x: timePoints,
        y: ulPrices,
        type: 'scatter',
        mode: 'lines',
        name: 'UL (USD)',
        line: { color: '#f44336', width: 2 }
    };
    
    const layout = {
        title: {
            text: 'Unilever vs UL Price Spread',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Time',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Price',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: true,
        legend: {
            x: 0.02,
            y: 0.98,
            bgcolor: 'rgba(255, 255, 255, 0.8)',
            bordercolor: '#e0e0e0',
            borderwidth: 1,
            font: { family: 'Inter, sans-serif', size: 11 }
        },
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('unilever-chart', [trace1, trace2], layout, { responsive: true, displayModeBar: false });
}

function createArbitrageSignalsChart() {
    const timePoints = Array.from({length: 50}, (_, i) => i);
    const signals = timePoints.map(() => Math.random() > 0.7 ? 1 : 0);
    const signalStrength = timePoints.map(() => Math.random() * 100);
    
    const trace = {
        x: timePoints,
        y: signalStrength,
        type: 'bar',
        marker: {
            color: signalStrength.map(s => s > 70 ? '#4CAF50' : s > 40 ? '#FF9800' : '#f44336'),
            line: { color: '#000000', width: 1 }
        }
    };
    
    const layout = {
        title: {
            text: 'Arbitrage Signal Strength',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Time',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Signal Strength (%)',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: false,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('arbitrage-signals', [trace], layout, { responsive: true, displayModeBar: false });
}

function createLatencyChart() {
    const latencies = Array.from({length: 1000}, () => Math.random() * 100);
    
    const trace = {
        x: latencies,
        type: 'histogram',
        nbinsx: 50,
        marker: {
            color: '#1976d2',
            line: { color: '#000000', width: 1 }
        }
    };
    
    const layout = {
        title: {
            text: 'HFT Latency Distribution',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Latency (microseconds)',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Frequency',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: false,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('latency-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

function createOrderBookChart() {
    const prices = Array.from({length: 20}, (_, i) => 100 + i * 0.5);
    const bids = prices.map(p => Math.random() * 1000);
    const asks = prices.map(p => Math.random() * 1000);
    
    const trace1 = {
        x: bids,
        y: prices,
        type: 'bar',
        orientation: 'h',
        name: 'Bids',
        marker: { color: '#4CAF50' }
    };
    
    const trace2 = {
        x: asks,
        y: prices,
        type: 'bar',
        orientation: 'h',
        name: 'Asks',
        marker: { color: '#f44336' }
    };
    
    const layout = {
        title: {
            text: 'Order Book Snapshot',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Volume',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Price',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        barmode: 'overlay',
        showlegend: true,
        legend: {
            x: 0.02,
            y: 0.98,
            bgcolor: 'rgba(255, 255, 255, 0.8)',
            bordercolor: '#e0e0e0',
            borderwidth: 1,
            font: { family: 'Inter, sans-serif', size: 11 }
        },
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('orderbook-chart', [trace1, trace2], layout, { responsive: true, displayModeBar: false });
}

// Scroll animations
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.approach-card, .stat-item, .tool-card, .position, .research-card').forEach(el => {
        observer.observe(el);
    });
}

// Form handlers
function initializeFormHandlers() {
    // Application form
    const applicationForm = document.querySelector('.application-form');
    if (applicationForm) {
        applicationForm.addEventListener('submit', handleApplicationSubmit);
    }
    
    // Contact form
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
    }
}

function handleApplicationSubmit(e) {
    e.preventDefault();
    
    // Simulate form submission
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        submitBtn.textContent = 'Application Submitted!';
        submitBtn.style.backgroundColor = '#4CAF50';
        
        setTimeout(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.backgroundColor = '';
            e.target.reset();
        }, 2000);
    }, 1500);
}

function handleContactSubmit(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        submitBtn.textContent = 'Message Sent!';
        submitBtn.style.backgroundColor = '#4CAF50';
        
        setTimeout(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.backgroundColor = '';
            e.target.reset();
        }, 2000);
    }, 1500);
}

// Enhanced Loading animations
function addLoadingAnimations() {
    // Add fade-in animations to sections
    const sections = document.querySelectorAll('section');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('loading', 'loaded');
            }
        });
    }, { threshold: 0.1 });
    
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // Add lazy loading for images and charts
    const lazyElements = document.querySelectorAll('[data-src]');
    const lazyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                if (element.tagName === 'IMG') {
                    element.src = element.dataset.src;
                    element.removeAttribute('data-src');
                }
                lazyObserver.unobserve(element);
            }
        });
    }, { threshold: 0.1 });
    
    lazyElements.forEach(element => {
        lazyObserver.observe(element);
    });
    
    // Enhanced card animations
    const elements = document.querySelectorAll('.approach-card, .stat-item, .tool-card, .position, .research-card');
    
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Enhanced error handling
function handleError(error, context) {
    console.error(`Error in ${context}:`, error);
    
    // Show user-friendly error message
    const errorMessage = document.createElement('div');
    errorMessage.className = 'error-message';
    errorMessage.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-red);
            color: white;
            padding: var(--spacing-md);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-medium);
            z-index: 10000;
            max-width: 300px;
        ">
            <strong>Error:</strong> ${context} failed to load. Please refresh the page.
            <button onclick="this.parentElement.remove()" style="
                background: none;
                border: none;
                color: white;
                float: right;
                cursor: pointer;
                font-size: 1.2rem;
            ">&times;</button>
        </div>
    `;
    
    document.body.appendChild(errorMessage);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorMessage.parentElement) {
            errorMessage.remove();
        }
    }, 5000);
}

// Performance monitoring
function trackPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
                
                console.log(`Page load time: ${loadTime}ms`);
                
                // Send to analytics if available
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'timing_complete', {
                        name: 'load',
                        value: loadTime
                    });
                }
            }, 0);
        });
    }
}

// Initialize performance tracking
trackPerformance();

// Utility functions
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Black-Scholes Calculator
function calculateBlackScholes() {
    const S = parseFloat(document.getElementById('bs-stock').value);
    const K = parseFloat(document.getElementById('bs-strike').value);
    const T = parseFloat(document.getElementById('bs-time').value);
    const r = parseFloat(document.getElementById('bs-rate').value);
    const sigma = parseFloat(document.getElementById('bs-vol').value);
    
    if (!S || !K || !T || !r || !sigma) {
        document.getElementById('bs-result').innerHTML = 'Please fill in all fields';
        return;
    }
    
    // Black-Scholes calculation
    const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
    const d2 = d1 - sigma * Math.sqrt(T);
    
    const callPrice = S * normalCDF(d1) - K * Math.exp(-r * T) * normalCDF(d2);
    const putPrice = K * Math.exp(-r * T) * normalCDF(-d2) - S * normalCDF(-d1);
    
    const result = `
        <strong>Option Prices:</strong><br>
        Call Option: $${callPrice.toFixed(4)}<br>
        Put Option: $${putPrice.toFixed(4)}<br>
        <small>d1: ${d1.toFixed(4)}, d2: ${d2.toFixed(4)}</small>
    `;
    
    document.getElementById('bs-result').innerHTML = result;
}

// Monte Carlo Simulation
function runMonteCarlo() {
    const S0 = parseFloat(document.getElementById('mc-price').value);
    const steps = parseInt(document.getElementById('mc-steps').value);
    const simulations = parseInt(document.getElementById('mc-sims').value);
    const mu = parseFloat(document.getElementById('mc-drift').value);
    const sigma = parseFloat(document.getElementById('mc-vol').value);
    
    if (!S0 || !steps || !simulations || !mu || !sigma) {
        document.getElementById('mc-result').innerHTML = 'Please fill in all fields';
        return;
    }
    
    const dt = 1 / 252; // Daily steps
    const results = [];
    
    for (let sim = 0; sim < simulations; sim++) {
        let S = S0;
        const path = [S];
        
        for (let i = 1; i <= steps; i++) {
            const z = Math.random() * 2 - 1; // Simple random walk
            S = S * Math.exp((mu - 0.5 * sigma * sigma) * dt + sigma * Math.sqrt(dt) * z);
            path.push(S);
        }
        
        results.push(path[path.length - 1]);
    }
    
    // Calculate statistics
    const mean = results.reduce((a, b) => a + b, 0) / results.length;
    const variance = results.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / results.length;
    const stdDev = Math.sqrt(variance);
    
    const percentiles = results.sort((a, b) => a - b);
    const p5 = percentiles[Math.floor(0.05 * results.length)];
    const p95 = percentiles[Math.floor(0.95 * results.length)];
    
    const result = `
        <strong>Monte Carlo Results:</strong><br>
        Mean Final Price: $${mean.toFixed(2)}<br>
        Standard Deviation: $${stdDev.toFixed(2)}<br>
        5th Percentile: $${p5.toFixed(2)}<br>
        95th Percentile: $${p95.toFixed(2)}<br>
        <small>${simulations} simulations, ${steps} time steps</small>
    `;
    
    document.getElementById('mc-result').innerHTML = result;
}

// Portfolio Optimization
function optimizePortfolio() {
    const assetType = document.getElementById('portfolio-assets').value;
    const riskTolerance = parseInt(document.getElementById('risk-tolerance').value);
    const targetReturn = parseFloat(document.getElementById('target-return').value);
    
    let assets, returns, volatilities;
    
    switch(assetType) {
        case 'tech':
            assets = ['AAPL', 'GOOGL', 'MSFT', 'TSLA'];
            returns = [0.15, 0.12, 0.18, 0.25];
            volatilities = [0.20, 0.18, 0.22, 0.35];
            break;
        case 'crypto':
            assets = ['BTC', 'ETH', 'SOL', 'BNB'];
            returns = [0.30, 0.25, 0.40, 0.20];
            volatilities = [0.60, 0.50, 0.80, 0.45];
            break;
        case 'global':
            assets = ['SPY', 'QQQ', 'IWM', 'EFA'];
            returns = [0.10, 0.12, 0.08, 0.06];
            volatilities = [0.15, 0.18, 0.20, 0.16];
            break;
    }
    
    // Simple optimization based on risk tolerance
    const weights = assets.map((_, i) => {
        const riskFactor = riskTolerance / 10;
        return Math.max(0.1, (1 - volatilities[i] * (1 - riskFactor)) / assets.length);
    });
    
    // Normalize weights
    const totalWeight = weights.reduce((a, b) => a + b, 0);
    const normalizedWeights = weights.map(w => w / totalWeight);
    
    // Calculate portfolio metrics
    const portfolioReturn = normalizedWeights.reduce((sum, w, i) => sum + w * returns[i], 0);
    const portfolioVol = Math.sqrt(normalizedWeights.reduce((sum, w, i) => sum + w * w * volatilities[i] * volatilities[i], 0));
    const sharpeRatio = portfolioReturn / portfolioVol;
    
    const result = `
        <strong>Optimized Portfolio:</strong><br>
        ${assets.map((asset, i) => `${asset}: ${(normalizedWeights[i] * 100).toFixed(1)}%`).join('<br>')}<br><br>
        <strong>Portfolio Metrics:</strong><br>
        Expected Return: ${(portfolioReturn * 100).toFixed(2)}%<br>
        Volatility: ${(portfolioVol * 100).toFixed(2)}%<br>
        Sharpe Ratio: ${sharpeRatio.toFixed(2)}
    `;
    
    document.getElementById('portfolio-result').innerHTML = result;
}

// Risk Metrics Calculator
function calculateRiskMetrics() {
    const returnsText = document.getElementById('returns-data').value;
    const confidenceLevel = parseFloat(document.getElementById('confidence-level').value);
    
    let returns;
    try {
        returns = returnsText.split(',').map(r => parseFloat(r.trim()));
    } catch (e) {
        document.getElementById('risk-result').innerHTML = 'Invalid returns data format';
        return;
    }
    
    if (returns.length < 2) {
        document.getElementById('risk-result').innerHTML = 'Need at least 2 data points';
        return;
    }
    
    // Calculate metrics
    const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
    const variance = returns.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / returns.length;
    const stdDev = Math.sqrt(variance);
    
    // Sort returns for percentiles
    const sortedReturns = returns.sort((a, b) => a - b);
    const varIndex = Math.floor((1 - confidenceLevel) * returns.length);
    const var95 = sortedReturns[varIndex];
    const cvar95 = sortedReturns.slice(0, varIndex + 1).reduce((a, b) => a + b, 0) / (varIndex + 1);
    
    // Maximum drawdown
    let maxDrawdown = 0;
    let peak = returns[0];
    for (let i = 1; i < returns.length; i++) {
        if (returns[i] > peak) {
            peak = returns[i];
        }
        const drawdown = (peak - returns[i]) / peak;
        if (drawdown > maxDrawdown) {
            maxDrawdown = drawdown;
        }
    }
    
    const result = `
        <strong>Risk Metrics:</strong><br>
        Mean Return: ${(mean * 100).toFixed(2)}%<br>
        Volatility: ${(stdDev * 100).toFixed(2)}%<br>
        VaR (${(confidenceLevel * 100).toFixed(0)}%): ${(var95 * 100).toFixed(2)}%<br>
        CVaR (${(confidenceLevel * 100).toFixed(0)}%): ${(cvar95 * 100).toFixed(2)}%<br>
        Max Drawdown: ${(maxDrawdown * 100).toFixed(2)}%<br>
        Sharpe Ratio: ${(mean / stdDev).toFixed(2)}
    `;
    
    document.getElementById('risk-result').innerHTML = result;
}

// Options Strategy Builder
function buildOptionsStrategy() {
    const strategyType = document.getElementById('strategy-type').value;
    const underlyingPrice = parseFloat(document.getElementById('underlying-price').value);
    const daysToExpiry = parseInt(document.getElementById('days-to-expiry').value);
    
    if (!underlyingPrice || !daysToExpiry) {
        document.getElementById('options-result').innerHTML = 'Please fill in all fields';
        return;
    }
    
    const timeToExpiry = daysToExpiry / 365;
    const volatility = 0.3;
    const riskFreeRate = 0.05;
    
    let strategy, maxProfit, maxLoss, breakeven;
    
    switch(strategyType) {
        case 'bull-call':
            const call1Strike = underlyingPrice * 0.95;
            const call2Strike = underlyingPrice * 1.05;
            const call1Price = blackScholesCall(underlyingPrice, call1Strike, timeToExpiry, riskFreeRate, volatility);
            const call2Price = blackScholesCall(underlyingPrice, call2Strike, timeToExpiry, riskFreeRate, volatility);
            const netCost = call1Price - call2Price;
            maxProfit = call2Strike - call1Strike - netCost;
            maxLoss = netCost;
            breakeven = call1Strike + netCost;
            strategy = `Buy ${call1Strike.toFixed(2)} Call, Sell ${call2Strike.toFixed(2)} Call`;
            break;
            
        case 'bear-put':
            const put1Strike = underlyingPrice * 1.05;
            const put2Strike = underlyingPrice * 0.95;
            const put1Price = blackScholesPut(underlyingPrice, put1Strike, timeToExpiry, riskFreeRate, volatility);
            const put2Price = blackScholesPut(underlyingPrice, put2Strike, timeToExpiry, riskFreeRate, volatility);
            const netCost2 = put1Price - put2Price;
            maxProfit = put1Strike - put2Strike - netCost2;
            maxLoss = netCost2;
            breakeven = put1Strike - netCost2;
            strategy = `Buy ${put1Strike.toFixed(2)} Put, Sell ${put2Strike.toFixed(2)} Put`;
            break;
            
        default:
            strategy = 'Strategy not implemented';
            maxProfit = maxLoss = breakeven = 0;
    }
    
    const result = `
        <strong>${strategyType.replace('-', ' ').toUpperCase()}:</strong><br>
        Strategy: ${strategy}<br>
        Max Profit: $${maxProfit.toFixed(2)}<br>
        Max Loss: $${maxLoss.toFixed(2)}<br>
        Breakeven: $${breakeven.toFixed(2)}<br>
        <small>Time to expiry: ${daysToExpiry} days</small>
    `;
    
    document.getElementById('options-result').innerHTML = result;
}

// Technical Analysis
function calculateTechnicalIndicators() {
    const indicator = document.getElementById('technical-indicator').value;
    const symbol = document.getElementById('symbol').value;
    const period = parseInt(document.getElementById('period').value);
    
    if (!symbol || !period) {
        document.getElementById('technical-result').innerHTML = 'Please fill in all fields';
        return;
    }
    
    // Generate sample price data
    const prices = Array.from({length: 50}, () => 100 + Math.random() * 20);
    
    let result = `<strong>${symbol} - ${indicator.toUpperCase()}:</strong><br>`;
    
    switch(indicator) {
        case 'rsi':
            const rsi = calculateRSI(prices, period);
            result += `RSI (${period}): ${rsi.toFixed(2)}<br>`;
            result += rsi > 70 ? 'Overbought' : rsi < 30 ? 'Oversold' : 'Neutral';
            break;
            
        case 'macd':
            const macd = calculateMACD(prices);
            result += `MACD: ${macd.toFixed(2)}<br>`;
            result += macd > 0 ? 'Bullish' : 'Bearish';
            break;
            
        case 'bollinger':
            const bb = calculateBollingerBands(prices, period);
            result += `Upper Band: ${bb.upper.toFixed(2)}<br>`;
            result += `Middle Band: ${bb.middle.toFixed(2)}<br>`;
            result += `Lower Band: ${bb.lower.toFixed(2)}<br>`;
            result += `Current Price: ${prices[prices.length - 1].toFixed(2)}`;
            break;
            
        case 'moving-average':
            const sma = calculateSMA(prices, period);
            const ema = calculateEMA(prices, period);
            result += `SMA (${period}): ${sma.toFixed(2)}<br>`;
            result += `EMA (${period}): ${ema.toFixed(2)}<br>`;
            result += `Current Price: ${prices[prices.length - 1].toFixed(2)}`;
            break;
    }
    
    document.getElementById('technical-result').innerHTML = result;
}

// Helper functions for technical analysis
function calculateRSI(prices, period) {
    const gains = [];
    const losses = [];
    
    for (let i = 1; i < prices.length; i++) {
        const change = prices[i] - prices[i-1];
        gains.push(Math.max(0, change));
        losses.push(Math.max(0, -change));
    }
    
    const avgGain = gains.slice(-period).reduce((a, b) => a + b, 0) / period;
    const avgLoss = losses.slice(-period).reduce((a, b) => a + b, 0) / period;
    
    return 100 - (100 / (1 + avgGain / avgLoss));
}

function calculateMACD(prices) {
    const ema12 = calculateEMA(prices, 12);
    const ema26 = calculateEMA(prices, 26);
    return ema12 - ema26;
}

function calculateBollingerBands(prices, period) {
    const sma = calculateSMA(prices, period);
    const variance = prices.slice(-period).reduce((sum, price) => sum + Math.pow(price - sma, 2), 0) / period;
    const stdDev = Math.sqrt(variance);
    
    return {
        upper: sma + (2 * stdDev),
        middle: sma,
        lower: sma - (2 * stdDev)
    };
}

function calculateSMA(prices, period) {
    return prices.slice(-period).reduce((a, b) => a + b, 0) / period;
}

function calculateEMA(prices, period) {
    const multiplier = 2 / (period + 1);
    let ema = prices[0];
    
    for (let i = 1; i < prices.length; i++) {
        ema = (prices[i] * multiplier) + (ema * (1 - multiplier));
    }
    
    return ema;
}

// Black-Scholes helper functions
function blackScholesCall(S, K, T, r, sigma) {
    const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
    const d2 = d1 - sigma * Math.sqrt(T);
    return S * normalCDF(d1) - K * Math.exp(-r * T) * normalCDF(d2);
}

function blackScholesPut(S, K, T, r, sigma) {
    const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
    const d2 = d1 - sigma * Math.sqrt(T);
    return K * Math.exp(-r * T) * normalCDF(-d2) - S * normalCDF(-d1);
}

// Normal cumulative distribution function (approximation)
function normalCDF(x) {
    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const p = 0.3275911;
    
    const sign = x >= 0 ? 1 : -1;
    x = Math.abs(x) / Math.sqrt(2.0);
    
    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    
    return 0.5 * (1.0 + sign * y);
}

// Real-time market data simulation
function updateMarketData() {
    const metrics = document.querySelectorAll('.metric-value');
    
    metrics.forEach(metric => {
        const currentValue = parseFloat(metric.textContent);
        const change = (Math.random() - 0.5) * 0.01; // ±0.5% change
        const newValue = currentValue * (1 + change);
        
        // Animate the change
        metric.style.color = change > 0 ? '#4CAF50' : '#f44336';
        metric.textContent = newValue.toFixed(2);
        
        setTimeout(() => {
            metric.style.color = '';
        }, 1000);
    });
}

// Update market data every 30 seconds
setInterval(updateMarketData, 30000);

// Smooth scrolling for all internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        animation: fadeInUp 0.6s ease forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .approach-card:hover,
    .stat-item:hover,
    .tool-card:hover,
    .position:hover,
    .research-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    
    .cta-primary:hover,
    .cta-secondary:hover {
        transform: translateY(-2px);
    }
    
    .nav-link:hover::after {
        width: 100%;
    }
`;
document.head.appendChild(style);

// Performance optimization
window.addEventListener('scroll', throttle(() => {
    // Handle scroll-based animations
}, 16));

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Initialize everything when page loads
window.addEventListener('load', () => {
    // Add final loading animations
    document.body.classList.add('loaded');
    
    // Start performance chart updates
    setInterval(() => {
        if (performanceChart) {
            // Update chart with new data point
            const newDate = new Date().toISOString().split('T')[0];
            const newValue = performanceChart.data[0].y[performanceChart.data[0].y.length - 1] * (1 + (Math.random() - 0.5) * 0.01);
            
            Plotly.extendTraces('performance-chart', {
                x: [[newDate]],
                y: [[newValue]]
            }, [0]);
        }
    }, 5000);
});

// ===== GAMES FUNCTIONALITY =====

// Initialize all games
function initializeGames() {
    initializeRoulette();
    initializeBlackjack();
    initializeDice();
    initializeRandomWalk();
    initializePoker();
    initializeMontyHall();
    initializeKellyCriterion();
    initializeRiskOfRuin();
}

// Roulette Game
let rouletteStats = { red: 0, black: 0, green: 0, total: 0 };
let rouletteHistory = [];

function initializeRoulette() {
    updateRouletteStats();
}

function spinRoulette() {
    const wheel = document.getElementById('roulette-wheel');
    const number = Math.floor(Math.random() * 37); // 0-36
    
    // Determine color
    let color;
    if (number === 0) {
        color = 'green';
        rouletteStats.green++;
    } else if ([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(number)) {
        color = 'red';
        rouletteStats.red++;
    } else {
        color = 'black';
        rouletteStats.black++;
    }
    
    rouletteStats.total++;
    rouletteHistory.push({ number, color });
    
    // Animate wheel
    const rotations = 5 + Math.random() * 5;
    const finalAngle = (360 * rotations) + (number * (360/37));
    wheel.style.transform = `rotate(${finalAngle}deg)`;
    
    // Update display
    document.querySelector('.wheel-number').textContent = number;
    updateRouletteStats();
    updateRouletteChart();
}

function autoPlayRoulette() {
    for (let i = 0; i < 100; i++) {
        setTimeout(() => spinRoulette(), i * 50);
    }
}

function updateRouletteStats() {
    document.getElementById('red-count').textContent = rouletteStats.red;
    document.getElementById('black-count').textContent = rouletteStats.black;
    document.getElementById('green-count').textContent = rouletteStats.green;
    document.getElementById('total-spins').textContent = rouletteStats.total;
}

function updateRouletteChart() {
    const trace = {
        x: ['Red', 'Black', 'Green'],
        y: [rouletteStats.red, rouletteStats.black, rouletteStats.green],
        type: 'bar',
        marker: {
            color: ['#d32f2f', '#000000', '#4CAF50']
        }
    };
    
    const layout = {
        title: {
            text: 'Roulette Results Distribution',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Color',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Frequency',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: false,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('roulette-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

// Blackjack Game
let blackjackStats = { wins: 0, losses: 0 };
let playerHand = [];
let dealerHand = [];
let deck = [];

function initializeBlackjack() {
    updateBlackjackStats();
}

function dealBlackjack() {
    // Reset deck and hands
    deck = createDeck();
    shuffleDeck(deck);
    playerHand = [deck.pop(), deck.pop()];
    dealerHand = [deck.pop(), deck.pop()];
    
    displayBlackjackHands();
    updateBlackjackStats();
}

function hitBlackjack() {
    if (playerHand.length === 0) return;
    
    playerHand.push(deck.pop());
    displayBlackjackHands();
    
    if (calculateHandValue(playerHand) > 21) {
        endBlackjackGame();
    }
}

function standBlackjack() {
    if (playerHand.length === 0) return;
    
    // Dealer plays
    while (calculateHandValue(dealerHand) < 17) {
        dealerHand.push(deck.pop());
    }
    
    endBlackjackGame();
}

function doubleBlackjack() {
    if (playerHand.length === 2) {
        playerHand.push(deck.pop());
        displayBlackjackHands();
        standBlackjack();
    }
}

function endBlackjackGame() {
    const playerValue = calculateHandValue(playerHand);
    const dealerValue = calculateHandValue(dealerHand);
    
    if (playerValue > 21) {
        blackjackStats.losses++;
    } else if (dealerValue > 21 || playerValue > dealerValue) {
        blackjackStats.wins++;
    } else {
        blackjackStats.losses++;
    }
    
    updateBlackjackStats();
    displayBlackjackHands(true);
}

function createDeck() {
    const suits = ['♠', '♥', '♦', '♣'];
    const values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
    const deck = [];
    
    for (let suit of suits) {
        for (let value of values) {
            deck.push({ suit, value });
        }
    }
    
    return deck;
}

function shuffleDeck(deck) {
    for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]];
    }
}

function calculateHandValue(hand) {
    let value = 0;
    let aces = 0;
    
    for (let card of hand) {
        if (card.value === 'A') {
            aces++;
            value += 11;
        } else if (['K', 'Q', 'J'].includes(card.value)) {
            value += 10;
        } else {
            value += parseInt(card.value);
        }
    }
    
    while (value > 21 && aces > 0) {
        value -= 10;
        aces--;
    }
    
    return value;
}

function displayBlackjackHands(showAll = false) {
    const dealerCards = document.getElementById('dealer-cards');
    const playerCards = document.getElementById('player-cards');
    const dealerTotal = document.getElementById('dealer-total');
    const playerTotal = document.getElementById('player-total');
    
    // Display dealer cards
    dealerCards.innerHTML = '';
    dealerHand.forEach((card, index) => {
        if (index === 1 && !showAll) {
            dealerCards.innerHTML += '<div class="card">?</div>';
        } else {
            const cardElement = document.createElement('div');
            cardElement.className = 'card';
            if (['♥', '♦'].includes(card.suit)) cardElement.classList.add('red');
            cardElement.textContent = card.value + card.suit;
            dealerCards.appendChild(cardElement);
        }
    });
    
    // Display player cards
    playerCards.innerHTML = '';
    playerHand.forEach(card => {
        const cardElement = document.createElement('div');
        cardElement.className = 'card';
        if (['♥', '♦'].includes(card.suit)) cardElement.classList.add('red');
        cardElement.textContent = card.value + card.suit;
        playerCards.appendChild(cardElement);
    });
    
    // Display totals
    dealerTotal.textContent = showAll ? calculateHandValue(dealerHand) : '?';
    playerTotal.textContent = calculateHandValue(playerHand);
}

function updateBlackjackStats() {
    document.getElementById('blackjack-wins').textContent = blackjackStats.wins;
    document.getElementById('blackjack-losses').textContent = blackjackStats.losses;
    const rate = blackjackStats.wins + blackjackStats.losses > 0 ? 
        ((blackjackStats.wins / (blackjackStats.wins + blackjackStats.losses)) * 100).toFixed(1) : '0';
    document.getElementById('blackjack-rate').textContent = rate + '%';
}

// Dice Game
let diceStats = { total: 0, rolls: [], average: 0 };

function initializeDice() {
    updateDiceStats();
}

function rollDice() {
    const diceCount = parseInt(document.getElementById('dice-count').value);
    const dice = [];
    
    for (let i = 0; i < diceCount; i++) {
        dice.push(Math.floor(Math.random() * 6) + 1);
    }
    
    const total = dice.reduce((sum, die) => sum + die, 0);
    
    // Animate dice
    const diceElements = document.querySelectorAll('.dice');
    diceElements.forEach((die, index) => {
        if (index < diceCount) {
            die.textContent = getDiceSymbol(dice[index]);
            die.classList.add('rolling');
            setTimeout(() => die.classList.remove('rolling'), 500);
        }
    });
    
    // Update stats
    diceStats.total++;
    diceStats.rolls.push(total);
    diceStats.average = diceStats.rolls.reduce((sum, roll) => sum + roll, 0) / diceStats.rolls.length;
    
    document.getElementById('current-roll').textContent = total;
    document.getElementById('total-rolls').textContent = diceStats.total;
    document.getElementById('dice-average').textContent = diceStats.average.toFixed(2);
    
    updateDiceChart();
}

function rollManyDice() {
    for (let i = 0; i < 1000; i++) {
        const diceCount = parseInt(document.getElementById('dice-count').value);
        const dice = [];
        for (let j = 0; j < diceCount; j++) {
            dice.push(Math.floor(Math.random() * 6) + 1);
        }
        const total = dice.reduce((sum, die) => sum + die, 0);
        diceStats.rolls.push(total);
    }
    
    diceStats.total += 1000;
    diceStats.average = diceStats.rolls.reduce((sum, roll) => sum + roll, 0) / diceStats.rolls.length;
    
    document.getElementById('total-rolls').textContent = diceStats.total;
    document.getElementById('dice-average').textContent = diceStats.average.toFixed(2);
    
    updateDiceChart();
}

function getDiceSymbol(number) {
    const symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
    return symbols[number - 1];
}

function updateDiceStats() {
    document.getElementById('current-roll').textContent = '-';
    document.getElementById('total-rolls').textContent = diceStats.total;
    document.getElementById('dice-average').textContent = diceStats.average.toFixed(2);
}

function updateDiceChart() {
    const counts = {};
    diceStats.rolls.forEach(roll => {
        counts[roll] = (counts[roll] || 0) + 1;
    });
    
    const trace = {
        x: Object.keys(counts),
        y: Object.values(counts),
        type: 'bar',
        marker: { color: '#1976d2' }
    };
    
    const layout = {
        title: {
            text: 'Dice Roll Distribution',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Roll Total',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Frequency',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: false,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('dice-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

// Random Walk
function initializeRandomWalk() {
    // Initialize empty
}

function simulateRandomWalk() {
    const steps = parseInt(document.getElementById('walk-steps').value);
    const prob = parseFloat(document.getElementById('walk-probability').value);
    
    const walk = [0];
    let maxDistance = 0;
    let returnedToOrigin = false;
    
    for (let i = 1; i <= steps; i++) {
        const step = Math.random() < prob ? 1 : -1;
        walk.push(walk[i-1] + step);
        
        if (Math.abs(walk[i]) > maxDistance) {
            maxDistance = Math.abs(walk[i]);
        }
        
        if (walk[i] === 0) {
            returnedToOrigin = true;
        }
    }
    
    document.getElementById('final-position').textContent = walk[steps];
    document.getElementById('max-distance').textContent = maxDistance;
    document.getElementById('return-origin').textContent = returnedToOrigin ? 'Yes' : 'No';
    
    updateRandomWalkChart(walk);
}

function simulateManyWalks() {
    const steps = parseInt(document.getElementById('walk-steps').value);
    const prob = parseFloat(document.getElementById('walk-probability').value);
    const walks = [];
    
    for (let i = 0; i < 1000; i++) {
        const walk = [0];
        for (let j = 1; j <= steps; j++) {
            const step = Math.random() < prob ? 1 : -1;
            walk.push(walk[j-1] + step);
        }
        walks.push(walk);
    }
    
    updateRandomWalkChart(walks[0], walks);
}

function updateRandomWalkChart(walk, allWalks = null) {
    const trace = {
        x: Array.from({length: walk.length}, (_, i) => i),
        y: walk,
        type: 'scatter',
        mode: 'lines',
        name: 'Position',
        line: { color: '#1976d2', width: 2 }
    };
    
    const layout = {
        title: {
            text: 'Random Walk Simulation',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Step',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Position',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: false,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('random-walk-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

// Poker Game
let pokerStats = { total: 0, hands: {} };

function initializePoker() {
    updatePokerStats();
}

function dealPokerHand() {
    const deck = createDeck();
    shuffleDeck(deck);
    const hand = deck.slice(0, 5);
    
    displayPokerHand(hand);
    
    const handType = evaluatePokerHand(hand);
    const probability = calculatePokerProbability(handType);
    
    document.getElementById('hand-type').textContent = handType;
    document.getElementById('hand-probability').textContent = probability.toFixed(4) + '%';
    
    pokerStats.total++;
    pokerStats.hands[handType] = (pokerStats.hands[handType] || 0) + 1;
    document.getElementById('total-hands').textContent = pokerStats.total;
    
    updatePokerChart();
}

function simulatePokerHands() {
    for (let i = 0; i < 1000; i++) {
        const deck = createDeck();
        shuffleDeck(deck);
        const hand = deck.slice(0, 5);
        const handType = evaluatePokerHand(hand);
        
        pokerStats.hands[handType] = (pokerStats.hands[handType] || 0) + 1;
    }
    
    pokerStats.total += 1000;
    document.getElementById('total-hands').textContent = pokerStats.total;
    updatePokerChart();
}

function displayPokerHand(hand) {
    const container = document.getElementById('poker-hand');
    container.innerHTML = '';
    
    hand.forEach(card => {
        const cardElement = document.createElement('div');
        cardElement.className = 'poker-card';
        if (['♥', '♦'].includes(card.suit)) cardElement.classList.add('red');
        
        cardElement.innerHTML = `
            <div>${card.value}</div>
            <div class="suit">${card.suit}</div>
        `;
        
        container.appendChild(cardElement);
    });
}

function evaluatePokerHand(hand) {
    const values = hand.map(card => card.value);
    const suits = hand.map(card => card.suit);
    const valueCounts = {};
    
    values.forEach(value => {
        valueCounts[value] = (valueCounts[value] || 0) + 1;
    });
    
    const counts = Object.values(valueCounts).sort((a, b) => b - a);
    const isFlush = suits.every(suit => suit === suits[0]);
    const isStraight = isSequential(values);
    
    if (isFlush && isStraight) return 'Straight Flush';
    if (counts[0] === 4) return 'Four of a Kind';
    if (counts[0] === 3 && counts[1] === 2) return 'Full House';
    if (isFlush) return 'Flush';
    if (isStraight) return 'Straight';
    if (counts[0] === 3) return 'Three of a Kind';
    if (counts[0] === 2 && counts[1] === 2) return 'Two Pair';
    if (counts[0] === 2) return 'One Pair';
    return 'High Card';
}

function isSequential(values) {
    const valueOrder = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
    const sortedValues = values.sort((a, b) => valueOrder.indexOf(a) - valueOrder.indexOf(b));
    
    for (let i = 1; i < sortedValues.length; i++) {
        if (valueOrder.indexOf(sortedValues[i]) - valueOrder.indexOf(sortedValues[i-1]) !== 1) {
            return false;
        }
    }
    return true;
}

function calculatePokerProbability(handType) {
    const probabilities = {
        'High Card': 50.1,
        'One Pair': 42.3,
        'Two Pair': 4.75,
        'Three of a Kind': 2.11,
        'Straight': 0.39,
        'Flush': 0.20,
        'Full House': 0.14,
        'Four of a Kind': 0.024,
        'Straight Flush': 0.0014
    };
    return probabilities[handType] || 0;
}

function updatePokerStats() {
    document.getElementById('hand-type').textContent = '-';
    document.getElementById('hand-probability').textContent = '-';
    document.getElementById('total-hands').textContent = pokerStats.total;
}

function updatePokerChart() {
    const trace = {
        x: Object.keys(pokerStats.hands),
        y: Object.values(pokerStats.hands),
        type: 'bar',
        marker: { color: '#1976d2' }
    };
    
    const layout = {
        title: {
            text: 'Poker Hand Distribution',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Hand Type',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Frequency',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: false,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('poker-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

// Monty Hall Problem
let montyStats = { wins: 0, losses: 0 };
let selectedDoor = null;
let winningDoor = null;

function initializeMontyHall() {
    updateMontyStats();
}

function selectDoor(doorNumber) {
    // Reset doors
    document.querySelectorAll('.door').forEach(door => {
        door.className = 'door';
    });
    
    selectedDoor = doorNumber;
    document.getElementById(`door${doorNumber}`).classList.add('selected');
}

function playMontyHall() {
    if (selectedDoor === null) {
        alert('Please select a door first!');
        return;
    }
    
    // Set winning door
    winningDoor = Math.floor(Math.random() * 3) + 1;
    
    // Reveal a losing door
    let revealedDoor;
    do {
        revealedDoor = Math.floor(Math.random() * 3) + 1;
    } while (revealedDoor === selectedDoor || revealedDoor === winningDoor);
    
    document.getElementById(`door${revealedDoor}`).classList.add('revealed');
    
    // Check if player should switch
    const shouldSwitch = document.getElementById('switch-strategy').checked;
    const finalChoice = shouldSwitch ? 
        (selectedDoor === 1 ? (revealedDoor === 2 ? 3 : 2) : 
         selectedDoor === 2 ? (revealedDoor === 1 ? 3 : 1) : 
         (revealedDoor === 1 ? 2 : 1)) : selectedDoor;
    
    // Show result
    if (finalChoice === winningDoor) {
        montyStats.wins++;
        document.getElementById(`door${winningDoor}`).classList.add('winner');
    } else {
        montyStats.losses++;
        document.getElementById(`door${finalChoice}`).classList.add('revealed');
        document.getElementById(`door${winningDoor}`).classList.add('winner');
    }
    
    updateMontyStats();
    
    // Reset after delay
    setTimeout(() => {
        document.querySelectorAll('.door').forEach(door => {
            door.className = 'door';
        });
        selectedDoor = null;
        winningDoor = null;
    }, 2000);
}

function simulateMontyHall() {
    const shouldSwitch = document.getElementById('switch-strategy').checked;
    
    for (let i = 0; i < 1000; i++) {
        const winningDoor = Math.floor(Math.random() * 3) + 1;
        const initialChoice = Math.floor(Math.random() * 3) + 1;
        
        if (shouldSwitch) {
            // Switch strategy: always switch
            if (initialChoice !== winningDoor) {
                montyStats.wins++;
            } else {
                montyStats.losses++;
            }
        } else {
            // Stay strategy: never switch
            if (initialChoice === winningDoor) {
                montyStats.wins++;
            } else {
                montyStats.losses++;
            }
        }
    }
    
    updateMontyStats();
}

function updateMontyStats() {
    document.getElementById('monty-wins').textContent = montyStats.wins;
    document.getElementById('monty-losses').textContent = montyStats.losses;
    const rate = montyStats.wins + montyStats.losses > 0 ? 
        ((montyStats.wins / (montyStats.wins + montyStats.losses)) * 100).toFixed(1) : '0';
    document.getElementById('monty-rate').textContent = rate + '%';
}

// Kelly Criterion
function initializeKellyCriterion() {
    // Initialize empty
}

function calculateKelly() {
    const p = parseFloat(document.getElementById('win-probability').value);
    const b = parseFloat(document.getElementById('win-amount').value);
    const a = parseFloat(document.getElementById('loss-amount').value);
    
    if (p <= 0 || p >= 1 || b <= 0 || a <= 0) {
        alert('Please enter valid probabilities and amounts');
        return;
    }
    
    const kellyFraction = (p * b - (1 - p) * a) / (b * a);
    const expectedValue = p * b - (1 - p) * a;
    const growthRate = p * Math.log(1 + kellyFraction * b) + (1 - p) * Math.log(1 - kellyFraction * a);
    
    document.getElementById('kelly-fraction').textContent = kellyFraction.toFixed(4);
    document.getElementById('expected-value').textContent = expectedValue.toFixed(4);
    document.getElementById('growth-rate').textContent = (growthRate * 100).toFixed(2) + '%';
    
    updateKellyChart(p, b, a);
}

function updateKellyChart(p, b, a) {
    const fractions = Array.from({length: 100}, (_, i) => i / 100);
    const growthRates = fractions.map(f => {
        if (f * b >= 1 || f * a >= 1) return -Infinity;
        return p * Math.log(1 + f * b) + (1 - p) * Math.log(1 - f * a);
    });
    
    const trace = {
        x: fractions,
        y: growthRates,
        type: 'scatter',
        mode: 'lines',
        name: 'Growth Rate',
        line: { color: '#1976d2', width: 2 }
    };
    
    const layout = {
        title: {
            text: 'Kelly Criterion Growth Rate',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Fraction of Bankroll',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Growth Rate',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: false,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('kelly-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

// Risk of Ruin
function initializeRiskOfRuin() {
    // Initialize empty
}

function simulateRiskOfRuin() {
    const initialBankroll = parseFloat(document.getElementById('initial-bankroll').value);
    const betSize = parseFloat(document.getElementById('bet-size').value);
    const winRate = parseFloat(document.getElementById('win-rate').value);
    
    if (initialBankroll <= 0 || betSize <= 0 || winRate <= 0 || winRate >= 1) {
        alert('Please enter valid parameters');
        return;
    }
    
    let ruinCount = 0;
    let totalSessions = 0;
    let maxDrawdown = 0;
    
    for (let session = 0; session < 1000; session++) {
        let bankroll = initialBankroll;
        let peak = bankroll;
        let sessions = 0;
        
        while (bankroll > 0 && bankroll < initialBankroll * 2) {
            sessions++;
            if (Math.random() < winRate) {
                bankroll += betSize;
            } else {
                bankroll -= betSize;
            }
            
            if (bankroll > peak) peak = bankroll;
            const drawdown = (peak - bankroll) / peak;
            if (drawdown > maxDrawdown) maxDrawdown = drawdown;
        }
        
        if (bankroll <= 0) {
            ruinCount++;
        }
        totalSessions += sessions;
    }
    
    const ruinProbability = (ruinCount / 1000) * 100;
    const expectedSessions = totalSessions / 1000;
    
    document.getElementById('ruin-probability').textContent = ruinProbability.toFixed(2) + '%';
    document.getElementById('expected-sessions').textContent = expectedSessions.toFixed(0);
    document.getElementById('max-drawdown').textContent = (maxDrawdown * 100).toFixed(1) + '%';
    
    updateRuinChart(initialBankroll, betSize, winRate);
}

function updateRuinChart(initialBankroll, betSize, winRate) {
    const sessions = Array.from({length: 100}, (_, i) => i + 1);
    const bankrolls = sessions.map(session => {
        let bankroll = initialBankroll;
        for (let i = 0; i < session; i++) {
            if (Math.random() < winRate) {
                bankroll += betSize;
            } else {
                bankroll -= betSize;
            }
        }
        return bankroll;
    });
    
    const trace = {
        x: sessions,
        y: bankrolls,
        type: 'scatter',
        mode: 'lines',
        name: 'Bankroll',
        line: { color: '#1976d2', width: 2 }
    };
    
    const layout = {
        title: {
            text: 'Risk of Ruin Simulation',
            font: { 
                family: 'Inter, sans-serif',
                size: 16,
                color: '#000000'
            },
            x: 0.5,
            xanchor: 'center'
        },
        xaxis: { 
            title: { 
                text: 'Session',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        yaxis: { 
            title: { 
                text: 'Bankroll',
                font: { family: 'Inter, sans-serif', size: 12, color: '#666666' }
            },
            gridcolor: '#f0f0f0',
            zerolinecolor: '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 10, color: '#666666' }
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 60, r: 30, t: 60, b: 60 },
        showlegend: false,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: '#000000',
            font: { family: 'Inter, sans-serif', size: 11, color: '#ffffff' }
        }
    };
    
    Plotly.newPlot('ruin-chart', [trace], layout, { responsive: true, displayModeBar: false });
}

// ===== PLOTS GALLERY FUNCTIONALITY =====

let plotsData = [];
let currentCategory = 'all';

function initializePlotsGallery() {
    // Load plots data
    loadPlotsData();
    
    // Initialize category filters
    initializeCategoryFilters();
    
    // Initialize modal
    initializePlotModal();
}

function loadPlotsData() {
    // Try to load from JSON file first
    fetch('plots_data.json')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                // If no JSON file, create sample data
                return createSamplePlotsData();
            }
        })
        .then(data => {
            plotsData = data.plots || data;
            renderPlotsGrid();
        })
        .catch(error => {
            console.log('No plots data found, using sample data');
            plotsData = createSamplePlotsData();
            renderPlotsGrid();
        });
}

function createSamplePlotsData() {
    // Create sample data for demonstration
    return [
        {
            id: 'vwap_portfolio_comparison',
            title: 'VWAP Portfolio Comparison',
            description: 'Volume Weighted Average Price analysis and trading strategy performance',
            category: 'vwap',
            filename: 'portfolio_comparison.pdf',
            path: 'core/plots/portfolio_comparison.pdf',
            size: '2.3 MB',
            modified_date: 'December 15, 2024',
            tags: ['vwap', 'portfolio', 'performance']
        },
        {
            id: 'arbitrage_cross_listing',
            title: 'Cross Listing Arbitrage Analysis',
            description: 'Cross-listing arbitrage opportunities and relative value analysis',
            category: 'arbitrage',
            filename: 'cross_listing_arbitrage.pdf',
            path: 'core/strategies/cross_listing/plots/cross_listing_arbitrage.pdf',
            size: '1.8 MB',
            modified_date: 'December 12, 2024',
            tags: ['arbitrage', 'cross-listing', 'analysis']
        },
        {
            id: 'hft_latency_analysis',
            title: 'HFT Latency Analysis',
            description: 'High-frequency trading latency analysis and order book dynamics',
            category: 'hft',
            filename: 'hft_latency.pdf',
            path: 'core/strategies/hft/plots/hft_latency.pdf',
            size: '3.1 MB',
            modified_date: 'December 10, 2024',
            tags: ['hft', 'latency', 'analysis']
        },
        {
            id: 'hedging_options_strategy',
            title: 'Options Hedging Strategy',
            description: 'Options hedging strategies and portfolio risk management',
            category: 'hedging',
            filename: 'options_hedging.pdf',
            path: 'core/strategies/hedge/plots/options_hedging.pdf',
            size: '2.7 MB',
            modified_date: 'December 8, 2024',
            tags: ['hedging', 'options', 'risk']
        },
        {
            id: 'ipo_event_study',
            title: 'IPO Event Study Analysis',
            description: 'Initial Public Offering event study and market reaction analysis',
            category: 'ipo',
            filename: 'ipo_event_study.pdf',
            path: 'core/strategies/plots/ipo_event_study.pdf',
            size: '4.2 MB',
            modified_date: 'December 5, 2024',
            tags: ['ipo', 'event-study', 'analysis']
        },
        {
            id: 'equities_sp500_analysis',
            title: 'S&P 500 Equity Analysis',
            description: 'Equity market analysis and stock performance monitoring',
            category: 'equities',
            filename: 'sp500_analysis.pdf',
            path: 'assets/equities/plots/sp500_analysis.pdf',
            size: '1.9 MB',
            modified_date: 'December 3, 2024',
            tags: ['equities', 'sp500', 'analysis']
        },
        {
            id: 'crypto_bitcoin_analysis',
            title: 'Bitcoin Market Analysis',
            description: 'Cryptocurrency price analysis and market microstructure',
            category: 'crypto',
            filename: 'bitcoin_analysis.pdf',
            path: 'assets/crypto/plots/bitcoin_analysis.pdf',
            size: '2.5 MB',
            modified_date: 'December 1, 2024',
            tags: ['crypto', 'bitcoin', 'analysis']
        },
        {
            id: 'fixed_income_yield_curves',
            title: 'Yield Curve Analysis',
            description: 'Yield curve analysis and fixed income market dynamics',
            category: 'fixed-income',
            filename: 'yield_curves.pdf',
            path: 'assets/fixed_income/plots/yield_curves.pdf',
            size: '1.6 MB',
            modified_date: 'November 28, 2024',
            tags: ['fixed-income', 'yield-curves', 'analysis']
        }
    ];
}

function initializeCategoryFilters() {
    const categoryButtons = document.querySelectorAll('.category-btn');
    
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update current category
            currentCategory = this.getAttribute('data-category');
            
            // Re-render plots grid
            renderPlotsGrid();
        });
    });
}

function renderPlotsGrid() {
    const plotsGrid = document.getElementById('plots-grid');
    
    // Filter plots by category
    const filteredPlots = currentCategory === 'all' ? 
        plotsData : 
        plotsData.filter(plot => plot.category === currentCategory);
    
    // Clear existing content
    plotsGrid.innerHTML = '';
    
    if (filteredPlots.length === 0) {
        plotsGrid.innerHTML = `
            <div class="no-plots-message">
                <h3>No plots found in this category</h3>
                <p>Try selecting a different category or run the plot discovery script to find your plots.</p>
            </div>
        `;
        return;
    }
    
    // Create plot cards
    filteredPlots.forEach(plot => {
        const plotCard = createPlotCard(plot);
        plotsGrid.appendChild(plotCard);
    });
}

function createPlotCard(plot) {
    const card = document.createElement('div');
    card.className = 'plot-card';
    card.setAttribute('data-plot-id', plot.id);
    
    card.innerHTML = `
        <div class="plot-thumbnail">
            <div class="pdf-icon">📊</div>
        </div>
        <div class="plot-info">
            <div class="plot-category">${plot.category.replace('-', ' ').toUpperCase()}</div>
            <h4 class="plot-title">${plot.title}</h4>
            <p class="plot-description">${plot.description}</p>
            <div class="plot-meta">
                <span class="plot-date">${plot.modified_date}</span>
                <span class="plot-size">${plot.size}</span>
            </div>
        </div>
    `;
    
    // Add click event to open modal
    card.addEventListener('click', () => openPlotModal(plot));
    
    return card;
}

function initializePlotModal() {
    const modal = document.getElementById('plot-modal');
    const closeBtn = document.querySelector('.close-modal');
    const downloadBtn = document.getElementById('download-plot');
    const shareBtn = document.getElementById('share-plot');
    
    // Close modal when clicking X
    closeBtn.addEventListener('click', closePlotModal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closePlotModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            closePlotModal();
        }
    });
    
    // Download button
    downloadBtn.addEventListener('click', function() {
        const currentPlot = this.getAttribute('data-plot-path');
        if (currentPlot) {
            const link = document.createElement('a');
            link.href = currentPlot;
            link.download = '';
            link.click();
        }
    });
    
    // Share button
    shareBtn.addEventListener('click', function() {
        const currentPlot = this.getAttribute('data-plot-path');
        if (currentPlot && navigator.share) {
            navigator.share({
                title: 'Buypolar Capital Research Plot',
                text: 'Check out this quantitative research plot from Buypolar Capital',
                url: window.location.href + '#' + currentPlot
            });
        } else {
            // Fallback: copy URL to clipboard
            const url = window.location.href + '#' + currentPlot;
            navigator.clipboard.writeText(url).then(() => {
                alert('Plot URL copied to clipboard!');
            });
        }
    });
}

function openPlotModal(plot) {
    const modal = document.getElementById('plot-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalDescription = document.getElementById('modal-description');
    const plotIframe = document.getElementById('plot-iframe');
    const downloadBtn = document.getElementById('download-plot');
    const shareBtn = document.getElementById('share-plot');
    
    // Update modal content
    modalTitle.textContent = plot.title;
    modalDescription.textContent = plot.description;
    
    // Set PDF source
    plotIframe.src = plot.path;
    
    // Set button data
    downloadBtn.setAttribute('data-plot-path', plot.path);
    shareBtn.setAttribute('data-plot-path', plot.path);
    
    // Show modal
    modal.style.display = 'block';
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

function closePlotModal() {
    const modal = document.getElementById('plot-modal');
    const plotIframe = document.getElementById('plot-iframe');
    
    // Hide modal
    modal.style.display = 'none';
    
    // Clear iframe source
    plotIframe.src = '';
    
    // Restore body scroll
    document.body.style.overflow = 'auto';
}