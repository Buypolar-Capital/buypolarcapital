// Buypolar Capital - Main Script
// This file initializes the website and coordinates all modules

// Initialize the website
document.addEventListener('DOMContentLoaded', function() {
    // Wait for external scripts to load
    waitForExternalScripts().then(() => {
        initializeWebsite();
    }).catch(() => {
        // If external scripts fail, still initialize the website
        console.log('External scripts failed to load, initializing with fallbacks');
        initializeWebsite();
    });
});

function waitForExternalScripts() {
    return new Promise((resolve, reject) => {
        let attempts = 0;
        const maxAttempts = 20; // 2 seconds - reduced timeout
        
        function checkScripts() {
            attempts++;
            
            // Check if Plotly is loaded
            if (typeof Plotly !== 'undefined') {
                console.log('External scripts loaded successfully');
                resolve();
                return;
            }
            
            if (attempts >= maxAttempts) {
                console.log('External scripts failed to load within timeout');
                resolve(); // Resolve instead of reject to continue initialization
                return;
            }
            
            setTimeout(checkScripts, 100);
        }
        
        checkScripts();
    });
}

function initializeWebsite() {
    try {
        // Show loading spinner
        showLoadingSpinner();
        
        // Initialize core features
        initializeEnhancedFeatures();
        initializeInputValidation();
        initializeTooltips();
        initializeNavigation();
        initializeScrollAnimations();
        initializeHeaderScrollEffect();
        initializeFormHandlers();
        initializeProgressBars();
        
        // Initialize performance chart
        initializePerformanceChartWithRetry();
        
        // Initialize research charts with better error handling
        setTimeout(() => {
            try {
                if (typeof Plotly !== 'undefined') {
                    initializeResearchCharts();
                } else {
                    console.log('Plotly not available for research charts');
                }
            } catch (error) {
                console.log('Research charts failed to load:', error);
            }
        }, 500);
        
        // Initialize plots gallery
        setTimeout(() => {
            try {
                initializePlotsGallery();
            } catch (error) {
                console.log('Plots gallery failed to load:', error);
            }
        }, 800);
        

        
        // Add loading animations
        addLoadingAnimations();
        
        // Track performance
        trackPerformance();
        
        // Hide loading spinner after a delay
        setTimeout(() => {
            hideLoadingSpinner();
        }, 1000);
        
        // Force hide spinner after 3 seconds
        setTimeout(() => {
            hideLoadingSpinner();
        }, 3000);
        
    } catch (error) {
        handleError(error, 'initializing website');
        hideLoadingSpinner();
    }
}

function showLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.style.display = 'flex';
    }
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.style.display = 'none';
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
    
    // Initialize progress bars
    initializeProgressBars();
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
            return false;
        }
    }
    
    if (type === 'number' && value) {
        const numValue = parseFloat(value);
        if (isNaN(numValue)) {
            showInputError(input, 'Please enter a valid number');
            return false;
        }
        
        const min = input.min;
        const max = input.max;
        
        if (min && numValue < parseFloat(min)) {
            showInputError(input, `Value must be at least ${min}`);
            return false;
        }
        
        if (max && numValue > parseFloat(max)) {
            showInputError(input, `Value must be at most ${max}`);
            return false;
        }
    }
    
    return true;
}

function showInputError(input, message) {
    clearInputError(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'input-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#f44336';
    errorDiv.style.fontSize = '0.8rem';
    errorDiv.style.marginTop = '0.25rem';
    
    input.parentNode.appendChild(errorDiv);
    input.style.borderColor = '#f44336';
}

function clearInputError(input) {
    const errorDiv = input.parentNode.querySelector('.input-error');
    if (errorDiv) {
        errorDiv.remove();
    }
    input.style.borderColor = '';
}

function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            tooltip.style.position = 'absolute';
            tooltip.style.backgroundColor = '#333';
            tooltip.style.color = '#fff';
            tooltip.style.padding = '0.5rem';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '0.8rem';
            tooltip.style.zIndex = '1000';
            tooltip.style.pointerEvents = 'none';
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
            
            this.tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this.tooltip) {
                this.tooltip.remove();
                this.tooltip = null;
            }
        });
    });
}

function initializeNavigation() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.nav-container')) {
            if (navMenu) navMenu.classList.remove('active');
            if (navToggle) navToggle.classList.remove('active');
        }
    });
    
    // Update active nav link on scroll
    window.addEventListener('scroll', throttle(updateActiveNavLink, 100));
}

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 200) {
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
    
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));
}

function initializeHeaderScrollEffect() {
    const header = document.querySelector('.header');
    if (!header) return;
    
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', throttle(() => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.classList.add('scrolled');
            isNavScrolled = true;
        } else {
            header.classList.remove('scrolled');
            isNavScrolled = false;
        }
        
        lastScrollTop = scrollTop;
    }, 10));
}

function initializeFormHandlers() {
    // Application form
    const applicationForm = document.getElementById('application-form');
    if (applicationForm) {
        applicationForm.addEventListener('submit', handleApplicationSubmit);
    }
    
    // Contact form
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
    }
}

function handleApplicationSubmit(e) {
    e.preventDefault();
    
    // Validate form
    const inputs = e.target.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showInputError(input, 'This field is required');
            isValid = false;
        }
    });
    
    if (!isValid) return;
    
    // Show success message
    const successMessage = document.createElement('div');
    successMessage.className = 'success-message';
    successMessage.textContent = 'Application submitted successfully! We will contact you soon.';
    successMessage.style.color = '#4CAF50';
    successMessage.style.marginTop = '1rem';
    
    e.target.appendChild(successMessage);
    e.target.reset();
    
    setTimeout(() => {
        successMessage.remove();
    }, 5000);
}

function handleContactSubmit(e) {
    e.preventDefault();
    
    // Validate form
    const inputs = e.target.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showInputError(input, 'This field is required');
            isValid = false;
        }
    });
    
    if (!isValid) return;
    
    // Show success message
    const successMessage = document.createElement('div');
    successMessage.className = 'success-message';
    successMessage.textContent = 'Message sent successfully! We will get back to you soon.';
    successMessage.style.color = '#4CAF50';
    successMessage.style.marginTop = '1rem';
    
    e.target.appendChild(successMessage);
    e.target.reset();
    
    setTimeout(() => {
        successMessage.remove();
    }, 5000);
}

function addLoadingAnimations() {
    const elements = document.querySelectorAll('.fade-in, .slide-in, .scale-in');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0) scale(1)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px) scale(0.95)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

function trackPerformance() {
    // Track page load time
    window.addEventListener('load', () => {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        
        // Track Core Web Vitals
        if ('web-vital' in window) {
            webVitals.getCLS(console.log);
            webVitals.getFID(console.log);
            webVitals.getFCP(console.log);
            webVitals.getLCP(console.log);
            webVitals.getTTFB(console.log);
        }
    });
}

function initializeProgressBars() {
    // Initialize progress bar functionality
    window.addEventListener('scroll', throttle(updateProgressBars, 10));
}

function updateProgressBars() {
    updateTopProgressBar();
    updateCircleProgressBar();
}

function updateTopProgressBar() {
    const progressBar = document.getElementById('progress-bar-top');
    if (!progressBar) return;
    
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    
    progressBar.style.width = scrollPercent + '%';
}

function updateCircleProgressBar() {
    const progressCircle = document.getElementById('progress-bar-circle');
    if (!progressCircle) return;
    
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    
    const degrees = (scrollPercent / 100) * 360;
    progressCircle.style.background = `conic-gradient(var(--accent-blue) 0deg, var(--accent-blue) ${degrees}deg, transparent ${degrees}deg)`;
} 