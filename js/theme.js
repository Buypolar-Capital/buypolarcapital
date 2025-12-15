// Buypolar Capital - Theme Management
// Manages dark/light theme toggling with smooth transitions

(function () {
    'use strict';

    // Theme constants
    const THEME_KEY = 'buypolarcapital-theme';
    const THEME_DARK = 'dark';
    const THEME_LIGHT = 'light';

    // Get saved theme or default to light
    function getSavedTheme() {
        const saved = localStorage.getItem(THEME_KEY);
        if (saved) return saved;

        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return THEME_DARK;
        }

        return THEME_LIGHT;
    }

    // Apply theme to document
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(THEME_KEY, theme);

        // Update meta theme-color for mobile browsers
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', theme === THEME_DARK ? '#0a0a0a' : '#ffffff');
        }
    }

    // Toggle between themes
    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme') || THEME_LIGHT;
        const next = current === THEME_LIGHT ? THEME_DARK : THEME_LIGHT;
        applyTheme(next);
    }

    // Initialize theme immediately (before DOMContentLoaded to prevent flash)
    applyTheme(getSavedTheme());

    // Setup theme toggle button when DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        const themeToggle = document.getElementById('theme-toggle');

        if (themeToggle) {
            themeToggle.addEventListener('click', toggleTheme);
        }

        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                // Only auto-switch if user hasn't manually set a theme
                if (!localStorage.getItem(THEME_KEY)) {
                    applyTheme(e.matches ? THEME_DARK : THEME_LIGHT);
                }
            });
        }
    });

    // Export to global scope for manual usage if needed
    window.buypolarcapital = window.buypolarcapital || {};
    window.buypolarcapital.theme = {
        toggle: toggleTheme,
        set: applyTheme,
        get: () => document.documentElement.getAttribute('data-theme') || THEME_LIGHT
    };
})();
