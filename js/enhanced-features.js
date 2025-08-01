// Enhanced Features for Buypolar Capital Website
// Contact Form Validation and Submission
// Real-time Data Integration
// Accessibility Improvements









// Real-time Data Integration
class RealTimeDataManager {
    constructor() {
        this.updateInterval = 30000; // 30 seconds
        this.isActive = false;
    }
    
    start() {
        if (this.isActive) return;
        this.isActive = true;
        this.updateData();
        this.interval = setInterval(() => this.updateData(), this.updateInterval);
    }
    
    stop() {
        this.isActive = false;
        if (this.interval) {
            clearInterval(this.interval);
        }
    }
    
    async updateData() {
        try {
            // Update Bitcoin price (example)
            await this.updateBitcoinPrice();
            
            // Update other real-time data as needed
            this.updateMarketIndicators();
            
        } catch (error) {
            console.error('Error updating real-time data:', error);
        }
    }
    
    async updateBitcoinPrice() {
        try {
            // Simulate API call to get Bitcoin price
            const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd');
            const data = await response.json();
            const btcPrice = data.bitcoin.usd;
            
            // Update BTC price display if element exists
            const btcPriceElement = document.getElementById('btc-price');
            if (btcPriceElement) {
                btcPriceElement.textContent = `$${btcPrice.toLocaleString()}`;
            }
            
        } catch (error) {
            console.error('Error fetching Bitcoin price:', error);
        }
    }
    
    updateMarketIndicators() {
        // Update other market indicators
        const indicators = document.querySelectorAll('.market-indicator');
        indicators.forEach(indicator => {
            // Simulate real-time updates
            const currentValue = parseFloat(indicator.dataset.value || 0);
            const change = (Math.random() - 0.5) * 0.02; // ±1% change
            const newValue = currentValue * (1 + change);
            indicator.dataset.value = newValue;
            indicator.textContent = newValue.toFixed(2);
        });
    }
}

// Initialize real-time data manager
const realTimeData = new RealTimeDataManager();

// Start real-time updates when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Start real-time data updates
    realTimeData.start();
    
    // Add keyboard navigation support
    addKeyboardNavigation();
    
    // Add focus management for accessibility
    addFocusManagement();
});

// Accessibility Improvements
function addKeyboardNavigation() {
    // Add keyboard support for navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                this.click();
            }
        });
    });
    
    // Add keyboard support for buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                this.click();
            }
        });
    });
}

function addFocusManagement() {
    // Add focus indicators
    const focusableElements = document.querySelectorAll('a, button, input, textarea, select');
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.classList.add('focus-visible');
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('focus-visible');
        });
    });
    
    // Skip link functionality
    const skipLink = document.querySelector('.skip-link');
    if (skipLink) {
        skipLink.addEventListener('click', function(event) {
            event.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.focus();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
}

// Performance Optimization
function optimizeImages() {
    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize performance optimizations
document.addEventListener('DOMContentLoaded', function() {
    optimizeImages();
});

// Export for use in other modules
window.enhancedFeatures = {
    realTimeData,
    validateForm,
    handleContactForm
}; 