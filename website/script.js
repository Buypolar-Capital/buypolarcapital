// Interactive JavaScript for BuyPolar Capital Website

// Smooth scrolling for navigation
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Initialize charts and visualizations
document.addEventListener('DOMContentLoaded', function() {
    createHeroChart();
    createMarketChart();
    createRiskChart();
    
    // Add scroll effects
    window.addEventListener('scroll', handleScroll);
});

// Create hero chart
function createHeroChart() {
    const trace = {
        x: Array.from({length: 100}, (_, i) => i),
        y: Array.from({length: 100}, (_, i) => Math.sin(i * 0.1) * 10 + Math.random() * 2),
        type: 'scatter',
        mode: 'lines',
        line: {
            color: 'rgba(255, 255, 255, 0.8)',
            width: 3
        },
        fill: 'tonexty',
        fillcolor: 'rgba(255, 255, 255, 0.1)'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            showgrid: false,
            showticklabels: false
        },
        yaxis: {
            showgrid: false,
            showticklabels: false
        },
        margin: {l: 0, r: 0, t: 0, b: 0}
    };

    Plotly.newPlot('hero-chart', [trace], layout, {displayModeBar: false});
}

// Create market analysis chart
function createMarketChart() {
    const ctx = document.createElement('canvas');
    ctx.id = 'market-canvas';
    document.getElementById('market-chart').appendChild(ctx);
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'S&P 500',
                data: [4200, 4300, 4400, 4350, 4500, 4600],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4
            }, {
                label: 'NASDAQ',
                data: [13000, 13500, 14000, 13800, 14500, 15000],
                borderColor: '#764ba2',
                backgroundColor: 'rgba(118, 75, 162, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Create risk metrics chart
function createRiskChart() {
    const ctx = document.createElement('canvas');
    ctx.id = 'risk-canvas';
    document.getElementById('risk-chart').appendChild(ctx);
    
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Equity Risk', 'Credit Risk', 'Liquidity Risk', 'Operational Risk'],
            datasets: [{
                data: [30, 25, 20, 25],
                backgroundColor: [
                    '#667eea',
                    '#764ba2',
                    '#f093fb',
                    '#f5576c'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });
}

// Handle scroll effects
function handleScroll() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.background = '#ffffff';
        navbar.style.backdropFilter = 'none';
    }
}

// Load dashboard function
function loadDashboard(type) {
    // This would typically load a specific dashboard
    console.log(`Loading ${type} dashboard...`);
    alert(`Loading ${type} dashboard... This would open a new page or modal with the specific dashboard.`);
}

// Add some interactive elements
document.addEventListener('DOMContentLoaded', function() {
    // Add click effects to dashboard cards
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    dashboardCards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'translateY(-5px)';
            }, 150);
        });
    });
    
    // Add hover effects to strategy cards
    const strategyCards = document.querySelectorAll('.strategy-card');
    strategyCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        });
    });
});