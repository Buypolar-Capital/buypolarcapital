// Buypolar Capital - Configuration and Global Variables

// Global variables
let performanceChart;
let isNavScrolled = false;
let plotsData = [];
let currentCategory = 'all';

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

// Modern chart layout helper function
function getModernChartLayout(title, xTitle, yTitle, showLegend = false) {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    return {
        title: {
            text: title,
            font: { 
                family: 'Inter, sans-serif',
                size: 18,
                color: isDark ? '#ffffff' : '#000000',
                weight: 600
            },
            x: 0.5,
            xanchor: 'center',
            y: 0.95
        },
        xaxis: { 
            title: { 
                text: xTitle,
                font: { family: 'Inter, sans-serif', size: 13, color: isDark ? '#b0b0b0' : '#666666', weight: 500 }
            },
            gridcolor: isDark ? '#2d2d2d' : '#f8f8f8',
            zerolinecolor: isDark ? '#666666' : '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 11, color: isDark ? '#b0b0b0' : '#666666' },
            showline: true,
            linecolor: isDark ? '#666666' : '#e0e0e0',
            linewidth: 1
        },
        yaxis: { 
            title: { 
                text: yTitle,
                font: { family: 'Inter, sans-serif', size: 13, color: isDark ? '#b0b0b0' : '#666666', weight: 500 }
            },
            gridcolor: isDark ? '#2d2d2d' : '#f8f8f8',
            zerolinecolor: isDark ? '#666666' : '#e0e0e0',
            tickfont: { family: 'Inter, sans-serif', size: 11, color: isDark ? '#b0b0b0' : '#666666' },
            showline: true,
            linecolor: isDark ? '#666666' : '#e0e0e0',
            linewidth: 1
        },
        plot_bgcolor: isDark ? '#121212' : '#ffffff',
        paper_bgcolor: isDark ? '#121212' : '#ffffff',
        font: { family: 'Inter, sans-serif' },
        margin: { l: 70, r: 40, t: 80, b: 70 },
        showlegend: showLegend,
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: isDark ? '#1f1f1f' : '#000000',
            font: { family: 'Inter, sans-serif', size: 12, color: isDark ? '#e0e0e0' : '#ffffff' },
            bordercolor: isDark ? '#1f1f1f' : '#000000'
        }
    };
}

// Utility functions
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
    }
}

function handleError(error, context) {
    console.error(`Error in ${context}:`, error);
    
    // Show user-friendly error message
    const errorMessage = document.createElement('div');
    errorMessage.className = 'error-message';
    errorMessage.innerHTML = `
        <div class="error-content">
            <h3>Something went wrong</h3>
            <p>We encountered an error while ${context}. Please try refreshing the page.</p>
            <button onclick="this.parentElement.parentElement.remove()">Dismiss</button>
        </div>
    `;
    
    // Add error message to page
    document.body.appendChild(errorMessage);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (errorMessage.parentElement) {
            errorMessage.remove();
        }
    }, 10000);
}

function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        const headerHeight = document.querySelector('.header').offsetHeight;
        const targetPosition = element.offsetTop - headerHeight;
        
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
} 