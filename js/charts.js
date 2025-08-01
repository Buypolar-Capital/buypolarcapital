// Buypolar Capital - Charts Module

// Initialize research charts
function initializeResearchCharts() {
    try {
        createBitcoinChart();
        createCryptoPortfolioChart();
        createIPOChart();
        createCARChart();
        createUnileverChart();
        createArbitrageSignalsChart();
        createLatencyChart();
        createOrderBookChart();
    } catch (error) {
        handleError(error, 'initializing research charts');
    }
}

// Bitcoin chart
function createBitcoinChart() {
    if (typeof Plotly === 'undefined') return;
    
    const chartContainer = document.getElementById('btc-chart');
    if (!chartContainer) {
        console.log('Bitcoin chart container not found');
        return;
    }
    
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
    
    try {
        Plotly.newPlot('btc-chart', [trace], layout, { responsive: true, displayModeBar: false });
    } catch (error) {
        console.log('Error creating Bitcoin chart:', error);
    }
}

// Crypto portfolio chart
function createCryptoPortfolioChart() {
    if (typeof Plotly === 'undefined') return;
    
    const chartContainer = document.getElementById('crypto-portfolio');
    if (!chartContainer) {
        console.log('Crypto portfolio chart container not found');
        return;
    }
    
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
    
    try {
        Plotly.newPlot('crypto-portfolio', [trace], layout, { responsive: true, displayModeBar: false });
    } catch (error) {
        console.log('Error creating crypto portfolio chart:', error);
    }
}

// IPO chart
function createIPOChart() {
    if (typeof Plotly === 'undefined') return;
    
    const chartContainer = document.getElementById('ipo-chart');
    if (!chartContainer) {
        console.log('IPO chart container not found');
        return;
    }
    
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
    
    try {
        Plotly.newPlot('ipo-chart', [trace], layout, { responsive: true, displayModeBar: false });
    } catch (error) {
        console.log('Error creating IPO chart:', error);
    }
}

// CAR chart
function createCARChart() {
    if (typeof Plotly === 'undefined') return;
    
    const chartContainer = document.getElementById('car-chart');
    if (!chartContainer) {
        console.log('CAR chart container not found');
        return;
    }
    
    const days = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5];
    const car = [-0.5, -0.3, -0.1, 0.2, 0.8, 2.1, 1.8, 1.2, 0.9, 0.6, 0.4];
    
    const trace = {
        x: days,
        y: car,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'CAR',
        line: {
            color: '#2196F3',
            width: 3
        },
        marker: {
            size: 6,
            color: '#2196F3'
        },
        fill: 'tonexty',
        fillcolor: 'rgba(33, 150, 243, 0.1)'
    };
    
    const layout = getModernChartLayout('Cumulative Abnormal Returns', 'Days Relative to Event', 'CAR (%)');
    
    try {
        Plotly.newPlot('car-chart', [trace], layout, { responsive: true, displayModeBar: false });
    } catch (error) {
        console.log('Error creating CAR chart:', error);
    }
}

// Unilever chart
function createUnileverChart() {
    if (typeof Plotly === 'undefined') return;
    
    const dates = [];
    const prices = [];
    let currentPrice = 50;
    
    for (let i = 0; i < 60; i++) {
        const date = new Date();
        date.setDate(date.getDate() - (60 - i));
        dates.push(date.toISOString().split('T')[0]);
        
        const dailyChange = (Math.random() - 0.5) * 0.02; // ±1% daily change
        currentPrice *= (1 + dailyChange);
        prices.push(currentPrice);
    }
    
    const trace = {
        x: dates,
        y: prices,
        type: 'scatter',
        mode: 'lines',
        name: 'Unilever',
        line: {
            color: '#4CAF50',
            width: 2
        }
    };
    
    const layout = getModernChartLayout('Unilever Stock Price', 'Date', 'Price (€)');
    
    try {
        Plotly.newPlot('unilever-chart', [trace], layout, { responsive: true, displayModeBar: false });
    } catch (error) {
        console.log('Error creating Unilever chart:', error);
    }
}

// Arbitrage signals chart
function createArbitrageSignalsChart() {
    if (typeof Plotly === 'undefined') return;
    
    const time = [];
    const spread = [];
    const signal = [];
    
    for (let i = 0; i < 100; i++) {
        time.push(i);
        const baseSpread = 0.5 + Math.sin(i * 0.1) * 0.3;
        spread.push(baseSpread + (Math.random() - 0.5) * 0.2);
        signal.push(baseSpread > 0.7 ? 1 : baseSpread < 0.3 ? -1 : 0);
    }
    
    const trace1 = {
        x: time,
        y: spread,
        type: 'scatter',
        mode: 'lines',
        name: 'Spread',
        line: { color: '#FF9800', width: 2 }
    };
    
    const trace2 = {
        x: time,
        y: signal,
        type: 'scatter',
        mode: 'markers',
        name: 'Signal',
        marker: {
            size: 8,
            color: signal.map(s => s > 0 ? '#4CAF50' : s < 0 ? '#f44336' : '#9E9E9E')
        }
    };
    
    const layout = getModernChartLayout('Arbitrage Signals', 'Time', 'Spread/Signal');
    
    try {
        Plotly.newPlot('arbitrage-chart', [trace1, trace2], layout, { responsive: true, displayModeBar: false });
    } catch (error) {
        console.log('Error creating arbitrage chart:', error);
    }
}

// Latency chart
function createLatencyChart() {
    if (typeof Plotly === 'undefined') return;
    
    const exchanges = ['Binance', 'Coinbase', 'Kraken', 'Bitfinex', 'Huobi'];
    const latencies = [12, 18, 15, 22, 25];
    
    const trace = {
        x: exchanges,
        y: latencies,
        type: 'bar',
        marker: {
            color: latencies.map(l => l < 15 ? '#4CAF50' : l < 20 ? '#FF9800' : '#f44336'),
            line: { color: '#000000', width: 1 }
        }
    };
    
    const layout = getModernChartLayout('Exchange Latency Comparison', 'Exchange', 'Latency (ms)');
    
    try {
        Plotly.newPlot('latency-chart', [trace], layout, { responsive: true, displayModeBar: false });
    } catch (error) {
        console.log('Error creating latency chart:', error);
    }
}

// Order book chart
function createOrderBookChart() {
    if (typeof Plotly === 'undefined') return;
    
    const prices = [];
    const bids = [];
    const asks = [];
    
    const basePrice = 50000;
    for (let i = 0; i < 50; i++) {
        const price = basePrice + (i - 25) * 10;
        prices.push(price);
        
        if (i < 25) {
            bids.push(Math.random() * 10 + 1);
            asks.push(0);
        } else {
            bids.push(0);
            asks.push(Math.random() * 10 + 1);
        }
    }
    
    const trace1 = {
        x: bids,
        y: prices,
        type: 'scatter',
        mode: 'lines',
        name: 'Bids',
        line: { color: '#4CAF50', width: 2 },
        fill: 'tonexty',
        fillcolor: 'rgba(76, 175, 80, 0.1)'
    };
    
    const trace2 = {
        x: asks,
        y: prices,
        type: 'scatter',
        mode: 'lines',
        name: 'Asks',
        line: { color: '#f44336', width: 2 },
        fill: 'tonexty',
        fillcolor: 'rgba(244, 67, 54, 0.1)'
    };
    
    const layout = getModernChartLayout('Order Book Depth', 'Volume', 'Price');
    
    try {
        Plotly.newPlot('orderbook-chart', [trace1, trace2], layout, { responsive: true, displayModeBar: false });
    } catch (error) {
        console.log('Error creating order book chart:', error);
    }
}

// Performance chart initialization
function initializePerformanceChart() {
    if (typeof Chart === 'undefined') return;
    
    const ctx = document.getElementById('performance-chart');
    if (!ctx) return;
    
    const data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: 'Portfolio Performance',
            data: [100, 102, 105, 103, 108, 112, 115, 118, 120, 122, 125, 128],
            borderColor: '#2196F3',
            backgroundColor: 'rgba(33, 150, 243, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4
        }]
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    };
    
    try {
        performanceChart = new Chart(ctx, config);
    } catch (error) {
        console.log('Error creating performance chart:', error);
    }
}

function initializePerformanceChartWithRetry() {
    if (typeof Chart !== 'undefined') {
        initializePerformanceChart();
        return;
    }
    
    function tryInitialize() {
        if (typeof Chart !== 'undefined') {
            initializePerformanceChart();
        } else {
            setTimeout(tryInitialize, 100);
        }
    }
    
    setTimeout(tryInitialize, 100);
} 