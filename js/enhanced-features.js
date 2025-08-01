// Enhanced Features for Buypolar Capital Website
// Contact Form Validation and Submission
// Real-time Data Integration
// Accessibility Improvements

// Contact Form Handler
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
    
    // Real-time validation
    const formInputs = contactForm?.querySelectorAll('input, textarea');
    formInputs?.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
});

// Contact Form Validation and Submission
async function handleContactForm(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    const formSuccess = document.getElementById('form-success');
    
    // Clear previous errors
    clearAllErrors();
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    // Show loading state
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    submitBtn.disabled = true;
    
    try {
        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Verify reCAPTCHA
        const recaptchaResponse = grecaptcha.getResponse();
        if (!recaptchaResponse) {
            showFieldError('captcha-error', 'Please complete the reCAPTCHA verification');
            return;
        }
        
        // Simulate form submission (replace with actual endpoint)
        await simulateFormSubmission(data);
        
        // Show success message
        form.reset();
        grecaptcha.reset();
        formSuccess.style.display = 'block';
        form.style.display = 'none';
        
        // Hide success message after 5 seconds
        setTimeout(() => {
            formSuccess.style.display = 'none';
            form.style.display = 'block';
        }, 5000);
        
    } catch (error) {
        console.error('Form submission error:', error);
        showFieldError('form-error', 'An error occurred. Please try again.');
    } finally {
        // Reset button state
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Form Validation Functions
function validateForm() {
    let isValid = true;
    
    // Validate name
    const name = document.getElementById('contact-name');
    if (!name.value.trim()) {
        showFieldError('name-error', 'Name is required');
        isValid = false;
    } else if (name.value.trim().length < 2) {
        showFieldError('name-error', 'Name must be at least 2 characters');
        isValid = false;
    }
    
    // Validate email
    const email = document.getElementById('contact-email');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.value.trim()) {
        showFieldError('email-error', 'Email is required');
        isValid = false;
    } else if (!emailRegex.test(email.value)) {
        showFieldError('email-error', 'Please enter a valid email address');
        isValid = false;
    }
    
    // Validate subject
    const subject = document.getElementById('contact-subject');
    if (!subject.value.trim()) {
        showFieldError('subject-error', 'Subject is required');
        isValid = false;
    } else if (subject.value.trim().length < 5) {
        showFieldError('subject-error', 'Subject must be at least 5 characters');
        isValid = false;
    }
    
    // Validate message
    const message = document.getElementById('contact-message');
    if (!message.value.trim()) {
        showFieldError('message-error', 'Message is required');
        isValid = false;
    } else if (message.value.trim().length < 10) {
        showFieldError('message-error', 'Message must be at least 10 characters');
        isValid = false;
    }
    
    return isValid;
}

function validateField(event) {
    const field = event.target;
    const fieldId = field.id;
    const errorId = fieldId.replace('contact-', '') + '-error';
    
    // Clear previous error
    clearFieldError(event);
    
    // Validate based on field type
    switch (fieldId) {
        case 'contact-name':
            if (!field.value.trim()) {
                showFieldError(errorId, 'Name is required');
            } else if (field.value.trim().length < 2) {
                showFieldError(errorId, 'Name must be at least 2 characters');
            }
            break;
            
        case 'contact-email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!field.value.trim()) {
                showFieldError(errorId, 'Email is required');
            } else if (!emailRegex.test(field.value)) {
                showFieldError(errorId, 'Please enter a valid email address');
            }
            break;
            
        case 'contact-subject':
            if (!field.value.trim()) {
                showFieldError(errorId, 'Subject is required');
            } else if (field.value.trim().length < 5) {
                showFieldError(errorId, 'Subject must be at least 5 characters');
            }
            break;
            
        case 'contact-message':
            if (!field.value.trim()) {
                showFieldError(errorId, 'Message is required');
            } else if (field.value.trim().length < 10) {
                showFieldError(errorId, 'Message must be at least 10 characters');
            }
            break;
    }
}

function showFieldError(errorId, message) {
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function clearFieldError(event) {
    const field = event.target;
    const fieldId = field.id;
    const errorId = fieldId.replace('contact-', '') + '-error';
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}

function clearAllErrors() {
    const errorElements = document.querySelectorAll('.error-message');
    errorElements.forEach(element => {
        element.textContent = '';
        element.style.display = 'none';
    });
}

// Simulate form submission (replace with actual API call)
async function simulateFormSubmission(data) {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log('Form data submitted:', data);
            resolve();
        }, 2000);
    });
}

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