// Buypolar Capital - Professional Quant Fund Website
// Interactive JavaScript with real data and comprehensive tools

// Global variables
let performanceChart;
let isNavScrolled = false;

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
    // Initialize navigation
    initializeNavigation();
    
    // Initialize performance chart
    initializePerformanceChart();
    
    // Initialize research charts
    initializeResearchCharts();
    
    // Initialize scroll animations
    initializeScrollAnimations();
    
    // Initialize form handlers
    initializeFormHandlers();
    
    // Add loading animations
    addLoadingAnimations();
}

// Navigation functionality
function initializeNavigation() {
    const navbar = document.querySelector('.navbar');
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
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
    });
    
    // Mobile menu toggle
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
    
    // Close mobile menu when clicking on links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
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
                size: 16,
                color: '#000000'
            }
        },
        xaxis: {
            title: 'Date',
            gridcolor: '#e0e0e0',
            showgrid: true
        },
        yaxis: {
            title: 'Portfolio Value ($)',
            gridcolor: '#e0e0e0',
            showgrid: true
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: {
            family: 'Inter, sans-serif',
            color: '#000000'
        },
        legend: {
            orientation: 'h',
            y: -0.2
        },
        margin: {
            l: 60,
            r: 40,
            t: 60,
            b: 80
        },
        hovermode: 'x unified'
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
    
    const layout = {
        title: 'Bitcoin Price Movement',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Price (USDT)' },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 50 }
    };
    
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
    
    const layout = {
        title: 'Crypto Portfolio Returns (%)',
        xaxis: { title: 'Asset' },
        yaxis: { title: 'Return (%)' },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 50 }
    };
    
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
    
    const layout = {
        title: 'IPO Performance Comparison',
        xaxis: { title: 'Company' },
        yaxis: { title: 'Return (%)' },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 50 }
    };
    
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
        title: 'Cumulative Abnormal Returns (Event Study)',
        xaxis: { title: 'Event Day' },
        yaxis: { title: 'CAR (%)' },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 50 }
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
        title: 'Unilever vs UL Price Spread',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Price' },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 50 }
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
        title: 'Arbitrage Signal Strength',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Signal Strength (%)' },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 50 }
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
        title: 'HFT Latency Distribution',
        xaxis: { title: 'Latency (microseconds)' },
        yaxis: { title: 'Frequency' },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 50 }
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
        title: 'Order Book Snapshot',
        xaxis: { title: 'Volume' },
        yaxis: { title: 'Price' },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 50 },
        barmode: 'overlay'
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

// Loading animations
function addLoadingAnimations() {
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