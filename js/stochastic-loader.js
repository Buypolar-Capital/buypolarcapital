// Stochastic Loader - Brownian Motion Animation
// A minimalist loading animation using HTML5 Canvas

(function() {
    'use strict';

    const loader = document.getElementById('loader');
    const canvas = document.getElementById('stochastic-canvas');
    
    if (!loader || !canvas) {
        console.warn('Loader elements not found');
        return;
    }

    const ctx = canvas.getContext('2d');
    let path = [];
    let currentStep = 0;
    let animationStartTime = null;
    const animationDuration = 4000; // 4 seconds
    const minDisplayTime = 3000; // Minimum 3 seconds display
    let fadeStartTime = null;
    let hasStartedFade = false;
    let windowLoaded = false;
    let pathGenerated = false;
    let canvasWidth = 0;
    let canvasHeight = 0;

    // Initialize canvas size
    function resizeCanvas() {
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        
        // Store logical dimensions
        canvasWidth = rect.width;
        canvasHeight = rect.height;
        
        // Set actual canvas size accounting for device pixel ratio
        canvas.width = canvasWidth * dpr;
        canvas.height = canvasHeight * dpr;
        
        // Scale context to account for device pixel ratio
        ctx.scale(dpr, dpr);
        
        // Regenerate path if canvas resized after initial generation
        if (pathGenerated) {
            generatePath();
        }
        
        // Redraw if path exists
        if (path.length > 0) {
            drawAxes();
            drawPathUpTo(currentStep);
        } else {
            drawAxes();
        }
    }

    // Draw the axes (X-axis horizontal middle, Y-axis vertical left)
    function drawAxes() {
        ctx.save();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1;
        ctx.shadowBlur = 0;
        ctx.shadowColor = 'transparent';
        
        // X-axis (horizontal middle, full width)
        ctx.beginPath();
        ctx.moveTo(0, canvasHeight / 2);
        ctx.lineTo(canvasWidth, canvasHeight / 2);
        ctx.stroke();
        
        // Y-axis (vertical left, full height)
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(0, canvasHeight);
        ctx.stroke();
        
        ctx.restore();
    }

    // Generate Brownian motion path
    function generatePath() {
        path = [];
        const startY = canvasHeight / 2; // Start at center of Y-axis
        let y = startY;
        
        const dt = 0.01;
        const sigma = canvasHeight / 100; // Scale volatility with screen size
        const pathSteps = Math.floor(canvasWidth);
        
        path.push({ x: 0, y: startY });
        
        for (let i = 1; i <= pathSteps; i++) {
            // Random increment (centered around 0)
            const dW = (Math.random() - 0.5) * 2;
            // Brownian step: dY = sigma * dW * sqrt(dt)
            y += sigma * dW * Math.sqrt(dt);
            
            // Clamp Y to stay within canvas bounds
            y = Math.max(0, Math.min(canvasHeight, y));
            
            path.push({ x: i, y: y });
        }
        
        pathGenerated = true;
    }

    // Draw path up to a specific step
    function drawPathUpTo(step) {
        if (step < 1 || path.length === 0) return;
        
        ctx.save();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.shadowBlur = 12;
        ctx.shadowColor = '#ffffff';
        
        ctx.beginPath();
        ctx.moveTo(path[0].x, path[0].y);
        
        const drawTo = Math.min(step, path.length);
        for (let i = 1; i < drawTo; i++) {
            ctx.lineTo(path[i].x, path[i].y);
        }
        
        ctx.stroke();
        ctx.restore();
    }

    // Animation loop
    function animate(timestamp) {
        if (!animationStartTime) {
            animationStartTime = timestamp;
        }
        
        const elapsed = timestamp - animationStartTime;
        const progress = Math.min(elapsed / animationDuration, 1);
        
        // Calculate how many steps to draw based on progress
        const targetStep = Math.floor(progress * path.length);
        
        if (targetStep > currentStep && targetStep < path.length) {
            // Clear and redraw axes
            ctx.fillStyle = '#000000';
            ctx.fillRect(0, 0, canvasWidth, canvasHeight);
            drawAxes();
            
            // Draw path up to current step
            currentStep = targetStep;
            drawPathUpTo(currentStep);
        }
        
        // Ensure full path is drawn if animation is complete
        if (progress >= 1 && currentStep < path.length) {
            ctx.fillStyle = '#000000';
            ctx.fillRect(0, 0, canvasWidth, canvasHeight);
            drawAxes();
            currentStep = path.length;
            drawPathUpTo(currentStep);
        }
        
        // Check if we should fade out
        const shouldFade = windowLoaded && elapsed >= minDisplayTime;
        
        if (shouldFade && !hasStartedFade) {
            hasStartedFade = true;
            fadeStartTime = timestamp;
            loader.style.transition = 'opacity 0.5s ease-out';
            loader.style.opacity = '0';
        }
        
        if (hasStartedFade && fadeStartTime) {
            const fadeElapsed = timestamp - fadeStartTime;
            if (fadeElapsed >= 500) {
                // Fade complete, hide loader
                loader.style.display = 'none';
                return;
            }
        }
        
        requestAnimationFrame(animate);
    }

    // Handle window load event
    function handleWindowLoad() {
        windowLoaded = true;
    }

    // Initialize
    function init() {
        resizeCanvas();
        generatePath();
        drawAxes();
        
        // Start animation
        requestAnimationFrame(animate);
        
        // Handle window resize
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                resizeCanvas();
            }, 100);
        });
        
        // Handle window load
        if (document.readyState === 'complete') {
            handleWindowLoad();
        } else {
            window.addEventListener('load', handleWindowLoad);
        }
        
        // Safety timeout: fade out after max time even if window hasn't loaded
        setTimeout(() => {
            if (!hasStartedFade) {
                windowLoaded = true;
                hasStartedFade = true;
                loader.style.transition = 'opacity 0.5s ease-out';
                loader.style.opacity = '0';
                setTimeout(() => {
                    loader.style.display = 'none';
                }, 500);
            }
        }, animationDuration + 1000);
    }

    // Start immediately - loader div is already in HTML
    // Use a small timeout to ensure DOM is fully parsed
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM already loaded, but use setTimeout to ensure elements are accessible
        setTimeout(init, 0);
    }
})();
