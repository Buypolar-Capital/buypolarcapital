// Buypolar Capital - Professional Quant Fund Website
// Interactive JavaScript with sophisticated features

// Global variables
let performanceChart;
let isNavScrolled = false;

// Initialize the website
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
});

function initializeWebsite() {
    // Initialize navigation
    initializeNavigation();
    
    // Initialize performance chart
    initializePerformanceChart();
    
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
    document.querySelectorAll('.approach-card, .stat-item, .tool-card, .position').forEach(el => {
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
    const elements = document.querySelectorAll('.approach-card, .stat-item, .tool-card, .position');
    
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
    .position:hover {
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