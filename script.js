// Black/White Theme JavaScript

// Global variables
let currentStrategy = null;
let liveData = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    createLiveChart();
    startLiveData();
    setupModals();
});

// Live chart
function createLiveChart() {
    const trace = {
        x: Array.from({length: 100}, (_, i) => i),
        y: Array.from({length: 100}, (_, i) => Math.sin(i * 0.1) * 10 + Math.random() * 2),
        type: 'scatter',
        mode: 'lines',
        line: {color: '#ffffff', width: 2},
        fill: 'tonexty',
        fillcolor: 'rgba(255, 255, 255, 0.1)'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            showgrid: false,
            showticklabels: false,
            color: '#ffffff'
        },
        yaxis: {
            showgrid: false,
            showticklabels: false,
            color: '#ffffff'
        },
        margin: {l: 0, r: 0, t: 0, b: 0}
    };

    Plotly.newPlot('live-chart', [trace], layout, {displayModeBar: false});
}

// Live data simulation
function startLiveData() {
    setInterval(() => {
        updateMarketData();
        updateRiskMetrics();
    }, 2000);
}

function updateMarketData() {
    const data = {
        'S&P 500': (4200 + Math.random() * 100).toFixed(2),
        'NASDAQ': (14000 + Math.random() * 200).toFixed(2),
        'VIX': (15 + Math.random() * 5).toFixed(2),
        'BTC': (45000 + Math.random() * 1000).toFixed(2)
    };
    
    const container = document.getElementById('market-data');
    container.innerHTML = Object.entries(data).map(([key, value]) => 
        `<div class="data-row"><span>${key}:</span> <span class="value">${value}</span></div>`
    ).join('');
}

function updateRiskMetrics() {
    const metrics = {
        'VaR (95%)': (2.5 + Math.random() * 1).toFixed(2) + '%',
        'Sharpe Ratio': (1.8 + Math.random() * 0.4).toFixed(2),
        'Max Drawdown': (8.5 + Math.random() * 2).toFixed(2) + '%',
        'Beta': (0.95 + Math.random() * 0.1).toFixed(2)
    };
    
    const container = document.getElementById('risk-dashboard');
    container.innerHTML = Object.entries(metrics).map(([key, value]) => 
        `<div class="data-row"><span>${key}:</span> <span class="value">${value}</span></div>`
    ).join('');
}

// Plot viewer functions
function viewPlot(type) {
    const modal = document.getElementById('plot-modal');
    const content = document.getElementById('plot-content');
    
    switch(type) {
        case 'arbitrage':
            content.innerHTML = createArbitragePlot();
            break;
        case 'hft':
            content.innerHTML = createHFTPlot();
            break;
        case 'risk':
            content.innerHTML = createRiskPlot();
            break;
        case 'equities':
            content.innerHTML = createEquitiesPlot();
            break;
    }
    
    modal.style.display = 'block';
}

function createArbitragePlot() {
    return `
        <h2>Arbitrage Analysis</h2>
        <div id="arbitrage-chart"></div>
        <script>
            const trace = {
                x: ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
                y: [2.5, 1.8, 3.2, 1.5, 4.1],
                type: 'bar',
                marker: {color: '#ffffff'}
            };
            
            const layout = {
                title: 'Arbitrage Opportunities (%)',
                paper_bgcolor: '#000000',
                plot_bgcolor: '#000000',
                font: {color: '#ffffff'},
                xaxis: {color: '#ffffff'},
                yaxis: {color: '#ffffff'}
            };
            
            Plotly.newPlot('arbitrage-chart', [trace], layout);
        </script>
    `;
}

function createHFTPlot() {
    return `
        <h2>HFT Performance</h2>
        <div id="hft-chart"></div>
        <script>
            const trace = {
                x: Array.from({length: 50}, (_, i) => i),
                y: Array.from({length: 50}, () => Math.random() * 2 + 0.5),
                type: 'scatter',
                mode: 'lines',
                line: {color: '#ffffff', width: 2}
            };
            
            const layout = {
                title: 'Latency Monitor (ms)',
                paper_bgcolor: '#000000',
                plot_bgcolor: '#000000',
                font: {color: '#ffffff'},
                xaxis: {color: '#ffffff'},
                yaxis: {color: '#ffffff'}
            };
            
            Plotly.newPlot('hft-chart', [trace], layout);
        </script>
    `;
}

function createRiskPlot() {
    return `
        <h2>Risk Analysis</h2>
        <div id="risk-chart"></div>
        <script>
            const trace = {
                values: [30, 25, 20, 25],
                labels: ['Equity Risk', 'Credit Risk', 'Liquidity Risk', 'Operational Risk'],
                type: 'pie',
                marker: {
                    colors: ['#ffffff', '#cccccc', '#999999', '#666666']
                }
            };
            
            const layout = {
                title: 'Risk Distribution',
                paper_bgcolor: '#000000',
                font: {color: '#ffffff'}
            };
            
            Plotly.newPlot('risk-chart', [trace], layout);
        </script>
    `;
}

function createEquitiesPlot() {
    return `
        <h2>Equity Analysis</h2>
        <div id="equities-chart"></div>
        <script>
            const trace = {
                x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                y: [100, 105, 110, 108, 115, 120],
                type: 'scatter',
                mode: 'lines+markers',
                line: {color: '#ffffff', width: 3},
                marker: {color: '#ffffff', size: 8}
            };
            
            const layout = {
                title: 'Portfolio Performance',
                paper_bgcolor: '#000000',
                plot_bgcolor: '#000000',
                font: {color: '#ffffff'},
                xaxis: {color: '#ffffff'},
                yaxis: {color: '#ffffff'}
            };
            
            Plotly.newPlot('equities-chart', [trace], layout);
        </script>
    `;
}

// Calculator functions
function openCalculator(type) {
    const modal = document.getElementById('calculator-modal');
    const content = document.getElementById('calculator-content');
    
    switch(type) {
        case 'black-scholes':
            content.innerHTML = createBlackScholesCalculator();
            break;
        case 'monte-carlo':
            content.innerHTML = createMonteCarloCalculator();
            break;
        case 'risk-metrics':
            content.innerHTML = createRiskMetricsCalculator();
            break;
        case 'portfolio-opt':
            content.innerHTML = createPortfolioOptimizer();
            break;
    }
    
    modal.style.display = 'block';
}

function createBlackScholesCalculator() {
    return `
        <h2>Black-Scholes Option Pricing</h2>
        <div class="calculator-form">
            <div class="input-group">
                <label>Stock Price (S):</label>
                <input type="number" id="stock-price" value="100" step="0.01">
            </div>
            <div class="input-group">
                <label>Strike Price (K):</label>
                <input type="number" id="strike-price" value="100" step="0.01">
            </div>
            <div class="input-group">
                <label>Time to Expiry (T):</label>
                <input type="number" id="time-expiry" value="1" step="0.01">
            </div>
            <div class="input-group">
                <label>Risk-free Rate (r):</label>
                <input type="number" id="risk-free-rate" value="0.05" step="0.001">
            </div>
            <div class="input-group">
                <label>Volatility (σ):</label>
                <input type="number" id="volatility" value="0.2" step="0.01">
            </div>
            <button class="btn btn-primary" onclick="calculateBlackScholes()">Calculate</button>
        </div>
        <div id="bs-result" class="result"></div>
    `;
}

function calculateBlackScholes() {
    const S = parseFloat(document.getElementById('stock-price').value);
    const K = parseFloat(document.getElementById('strike-price').value);
    const T = parseFloat(document.getElementById('time-expiry').value);
    const r = parseFloat(document.getElementById('risk-free-rate').value);
    const sigma = parseFloat(document.getElementById('volatility').value);
    
    const d1 = (Math.log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*Math.sqrt(T));
    const d2 = d1 - sigma*Math.sqrt(T);
    
    // Simplified Black-Scholes calculation
    const callPrice = S * 0.5 - K * Math.exp(-r*T) * 0.5;
    const putPrice = callPrice - S + K * Math.exp(-r*T);
    
    document.getElementById('bs-result').innerHTML = `
        <h3>Results:</h3>
        <p>Call Price: $${callPrice.toFixed(4)}</p>
        <p>Put Price: $${putPrice.toFixed(4)}</p>
    `;
}

// Strategy functions
function loadStrategy(type) {
    currentStrategy = type;
    alert(`Loading ${type.toUpperCase()} strategy...`);
    
    setTimeout(() => {
        updateStrategyMetrics(type);
    }, 1000);
}

function updateStrategyMetrics(type) {
    const metrics = {
        'hft': {latency: '< 1ms', success: '95%', pnl: '+$12,450'},
        'arb': {sharpe: '2.1', maxdd: '8%', pnl: '+$8,230'},
        'ml': {accuracy: '87%', roi: '15%', pnl: '+$15,670'}
    };
    
    const metric = metrics[type];
    alert(`${type.toUpperCase()} Strategy Loaded!\nLatency: ${metric.latency}\nSuccess: ${metric.success}\nPnL: ${metric.pnl}`);
}

// Utility functions
function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({behavior: 'smooth'});
}

function setupModals() {
    const modals = document.querySelectorAll('.modal');
    const spans = document.querySelectorAll('.close');
    
    spans.forEach(span => {
        span.onclick = function() {
            modals.forEach(modal => modal.style.display = 'none');
        }
    });
    
    window.onclick = function(event) {
        modals.forEach(modal => {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        });
    }
}