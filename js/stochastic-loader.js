// Stochastic Loader - Brownian Motion Animation
// A minimalist loading animation using HTML5 Canvas

(function () {
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
    let hasStartedHide = false;
    let windowLoaded = false;
    let pathGenerated = false;
    let startY = 0; // Starting Y position for comparison
    let pathStopped = false;
    let pathColor = '#ffffff'; // White by default, changes to green/red when stopped
    let canvasWidth = 0;
    let canvasHeight = 0;
    let loaderAreaStart = 0;
    let loaderAreaWidth = 0;
    let plotTopMargin = 0;
    let plotBottomMargin = 0;
    let plotAreaHeight = 0;
    let plotBottom = 0; // Canvas Y coordinate of plot bottom (X-axis)
    let animationComplete = false;
    let completionWaitStart = null;

    // Initialize canvas size
    function resizeCanvas() {
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();

        // Store logical dimensions
        canvasWidth = rect.width;
        canvasHeight = rect.height;

        // Calculate loader area: responsive margins
        // Desktop: 20% empty, 60% loader, 20% empty
        // Mobile: 10% empty, 80% loader, 10% empty (for better use of space)
        const isMobile = canvasWidth <= 768;
        const marginPercent = isMobile ? 0.1 : 0.2;
        loaderAreaStart = canvasWidth * marginPercent;
        loaderAreaWidth = canvasWidth * (1 - 2 * marginPercent);

        // Calculate plot area with top and bottom margins (like a real plot)
        // Margins: 15% top, 15% bottom for breathing room
        plotTopMargin = canvasHeight * 0.15;
        plotBottomMargin = canvasHeight * 0.15;
        plotAreaHeight = canvasHeight - plotTopMargin - plotBottomMargin;
        plotBottom = canvasHeight - plotBottomMargin; // X-axis position (bottom of plot)

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

    // Draw the axes (First quadrant: X-axis at bottom, Y-axis at left)
    function drawAxes() {
        ctx.save();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1;
        ctx.shadowBlur = 0;
        ctx.shadowColor = 'transparent';

        // X-axis (horizontal at bottom of plot area, only in loader area)
        ctx.beginPath();
        ctx.moveTo(loaderAreaStart, plotBottom);
        ctx.lineTo(loaderAreaStart + loaderAreaWidth, plotBottom);
        ctx.stroke();

        // Y-axis (vertical at loader area start, from bottom to top of plot area)
        ctx.beginPath();
        ctx.moveTo(loaderAreaStart, plotTopMargin);
        ctx.lineTo(loaderAreaStart, plotBottom);
        ctx.stroke();

        ctx.restore();
    }

    // Generate Brownian motion path (First quadrant only - positive X, positive Y)
    function generatePath() {
        path = [];
        // Start at middle of plot area (50% of plot height from bottom)
        // In canvas coords: plotBottom - (plotAreaHeight / 2)
        startY = plotBottom - (plotAreaHeight / 2);
        let y = startY; // Canvas Y coordinate (decreases as we go up)

        const dt = 0.01;
        // Much higher variance for dramatic movement
        // Responsive variance: slightly less on mobile
        const isMobile = canvasWidth <= 768;
        const sigma = isMobile ? (plotAreaHeight / 12) * 3 : (plotAreaHeight / 10) * 3; // Increased volatility by 3x
        // Use pixel-based steps for consistent path density
        const pathSteps = Math.floor(loaderAreaWidth);

        // Path starts at origin (bottom-left of plot area)
        path.push({ x: loaderAreaStart, y: startY });

        for (let i = 1; i <= pathSteps; i++) {
            // Random increment (centered around 0) - can go up or down
            const dW = (Math.random() - 0.5) * 2; // -1 to 1
            // Brownian step: dY = -sigma * dW * sqrt(dt)
            // Negative because canvas Y decreases as we go up (positive Y in plot = upward)
            y -= sigma * dW * Math.sqrt(dt);

            // Stop if we reach the bottom (X-axis) - this is "bust" condition
            if (y >= plotBottom) {
                // Path has reached bottom (0 in plot coordinates), stop generating
                break;
            }

            // Clamp Y to stay within plot area bounds
            // Top of plot area is plotTopMargin, bottom is plotBottom
            y = Math.max(plotTopMargin, Math.min(plotBottom, y));

            // X position is relative to loader area start
            path.push({ x: loaderAreaStart + i, y: y });
        }

        pathGenerated = true;
    }

    // Draw path up to a specific step
    function drawPathUpTo(step, color = null) {
        if (step < 1 || path.length === 0) return;

        const drawColor = color || pathColor;

        ctx.save();
        ctx.strokeStyle = drawColor;
        ctx.lineWidth = 2;
        ctx.shadowBlur = 12;
        ctx.shadowColor = drawColor;

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

        // Check if path has been fully drawn (all points rendered)
        if (!pathStopped && path.length > 0 && currentStep >= path.length) {
            pathStopped = true;
            // Determine color based on final position relative to start
            // In canvas coords: lower Y = higher on screen (above start = green)
            // Higher Y = lower on screen (below start = red)
            const finalPoint = path[path.length - 1];
            if (finalPoint.y < startY) {
                pathColor = '#4CAF50'; // Green - ended above start
            } else {
                pathColor = '#f44336'; // Red - ended below start (or at bust)
            }

            // Redraw with the new color
            ctx.fillStyle = '#000000';
            ctx.fillRect(0, 0, canvasWidth, canvasHeight);
            drawAxes();
            drawPathUpTo(path.length, pathColor);
            completionWaitStart = timestamp;
        }

        // Ensure full path is drawn if animation time is complete
        if (progress >= 1 && !animationComplete) {
            animationComplete = true;
            if (!pathStopped && path.length > 0) {
                // Make sure we've drawn all points
                currentStep = path.length;

                // Determine color based on final position
                pathStopped = true;
                const finalPoint = path[path.length - 1];
                if (finalPoint.y < startY) {
                    pathColor = '#4CAF50'; // Green
                } else {
                    pathColor = '#f44336'; // Red
                }

                ctx.fillStyle = '#000000';
                ctx.fillRect(0, 0, canvasWidth, canvasHeight);
                drawAxes();
                drawPathUpTo(path.length, pathColor);
                completionWaitStart = timestamp;
            }
        }

        // Wait a moment after path stops (with color) before hiding
        if (pathStopped && completionWaitStart && !hasStartedHide) {
            const waitElapsed = timestamp - completionWaitStart;
            // Wait 600ms after path stops with color before hiding
            if (waitElapsed >= 600) {
                hasStartedHide = true;
                // Hide directly without fade
                loader.style.display = 'none';
                // Restore scrolling after loader is hidden
                document.documentElement.style.overflow = '';
                document.body.style.overflow = '';
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
        // Force scroll to top on reload
        window.scrollTo(0, 0);
        if ('scrollRestoration' in history) {
            history.scrollRestoration = 'manual';
        }

        // Prevent scrolling while loader is active
        document.documentElement.style.overflow = 'hidden';
        document.body.style.overflow = 'hidden';

        resizeCanvas();
        generatePath();
        drawAxes();

        // Start animation
        requestAnimationFrame(animate);

        // Handle window resize (with debouncing for performance)
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                // Reset animation state if needed (but keep progress if animation is running)
                if (!animationComplete) {
                    resizeCanvas();
                }
            }, 150);
        });

        // Handle orientation change on mobile devices
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                if (!animationComplete) {
                    resizeCanvas();
                }
            }, 100);
        });

        // Handle window load
        if (document.readyState === 'complete') {
            handleWindowLoad();
        } else {
            window.addEventListener('load', handleWindowLoad);
        }

        // Safety timeout: hide after max time even if animation hasn't completed
        // Allow extra time for the wait period after completion
        setTimeout(() => {
            if (!hasStartedHide) {
                windowLoaded = true;
                animationComplete = true;
                if (!pathStopped && path.length > 0) {
                    // Determine final color
                    const finalPoint = path[path.length - 1];
                    if (finalPoint.y < startY) {
                        pathColor = '#4CAF50'; // Green
                    } else {
                        pathColor = '#f44336'; // Red
                    }
                    pathStopped = true;

                    // Redraw with color
                    ctx.fillStyle = '#000000';
                    ctx.fillRect(0, 0, canvasWidth, canvasHeight);
                    drawAxes();
                    drawPathUpTo(path.length, pathColor);
                }
                // Wait a moment then hide
                setTimeout(() => {
                    hasStartedHide = true;
                    loader.style.display = 'none';
                    // Restore scrolling after loader is hidden
                    document.documentElement.style.overflow = '';
                    document.body.style.overflow = '';
                }, 600);
            }
        }, animationDuration + 1500);
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
