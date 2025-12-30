/**
 * Chrome-specific CSS loader
 * Detects non-Firefox browsers (Chrome, Edge, Safari, etc.) and loads mediaQueries-v2.css
 * Has zero impact on Firefox
 */

(function () {
    'use strict';

    /**
     * Detect if browser is NOT Firefox
     * @returns {boolean} true if Chrome/Edge/Safari/etc., false if Firefox
     */
    function isNonFirefox() {
        return navigator.userAgent.toLowerCase().indexOf('firefox') === -1;
    }

    /**
     * Load Chrome/non-Firefox-specific CSS file
     */
    function loadChromeCSS() {
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = '/static/css/mediaQueries-v2.css';
        link.id = 'chrome-media-queries-css';
        document.head.appendChild(link);
        document.body.setAttribute('data-browser', 'chrome');
        console.log('mediaQueries-v2.css loaded for non-Firefox browser');
    }

    /**
     * Get browser name for debugging
     */
    function getBrowserName() {
        var userAgent = navigator.userAgent.toLowerCase();
        if (userAgent.indexOf('chrome') > -1 && userAgent.indexOf('edg') === -1) {
            return 'Chrome';
        } else if (userAgent.indexOf('edg') > -1) {
            return 'Edge';
        } else if (userAgent.indexOf('safari') > -1 && userAgent.indexOf('chrome') === -1) {
            return 'Safari';
        } else if (userAgent.indexOf('firefox') > -1) {
            return 'Firefox';
        } else {
            return 'Unknown';
        }
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        var browserName = getBrowserName();
        
        // Only proceed if NOT Firefox
        if (isNonFirefox()) {
            loadChromeCSS();
            console.log(browserName + ' detected - loading mediaQueries-v2.css');
        } else {
            console.log('Firefox detected - mediaQueries-v2.css will NOT be loaded');
        }
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM already loaded
        init();
    }

})();
