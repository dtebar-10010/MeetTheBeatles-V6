/**
 * Firefox-specific CSS loader
 * Detects Firefox browser and loads firefox-fixes.css
 * Has zero impact on Chrome and other browsers
 */

(function () {
    'use strict';

    // Cache Firefox detection result
    var _isFirefoxCached = null;

    /**
     * Detect if browser is Firefox
     * @returns {boolean} true if Firefox, false otherwise
     */
    function isFirefox() {
        if (_isFirefoxCached !== null) {
            return _isFirefoxCached;
        }

        var ua = navigator.userAgent.toLowerCase();
        // Check user agent for 'firefox' or 'gecko' with Firefox version
        var uaCheck = ua.indexOf('firefox') > -1;
        // Check for Firefox-specific CSS property support
        var cssCheck = CSS.supports('-moz-appearance', 'none');
        
        _isFirefoxCached = uaCheck || cssCheck;
        
        console.log('User Agent:', ua);
        console.log('Firefox detected:', _isFirefoxCached);
        
        return _isFirefoxCached;
    }

    /**
     * Load Firefox-specific CSS file
     */
    function loadFirefoxCSS() {
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = '/static/css/firefox-fixes.css';
        link.id = 'firefox-fixes-css';
        document.head.appendChild(link);
        document.body.setAttribute('data-browser', 'firefox');
        console.log('firefox-fixes.css loaded');
    }

    /**
     * Disable mediaQueries-v2.css for Firefox
     * Finds and disables the link element to prevent conflicts
     */
    function disableMediaQueriesV2() {
        var links = document.querySelectorAll('link[rel="stylesheet"]');
        for (var i = 0; i < links.length; i++) {
            if (links[i].href && links[i].href.indexOf('mediaQueries-v2.css') > -1) {
                links[i].disabled = true;
                console.log('mediaQueries-v2.css disabled for Firefox');
                break;
            }
        }
    }

    /**
     * Get screen resolution info for debugging
     */
    function logScreenInfo() {
        if (window.console && isFirefox()) {
            var screenInfo = {
                width: window.screen.width,
                height: window.screen.height,
                availWidth: window.screen.availWidth,
                availHeight: window.screen.availHeight,
                pixelRatio: window.devicePixelRatio || 1,
                colorDepth: window.screen.colorDepth
            };

            console.log('Firefox Screen Info:', screenInfo);

            // Check if 4K resolution
            if (screenInfo.width >= 3840 && screenInfo.height >= 2160) {
                console.log('4K (3840x2160) display detected');
                document.body.setAttribute('data-resolution', '4k');
            }
        }
    }

    /**
     * Apply Firefox-specific positioning fix for stacked-cards
     * This runs after the stackedCards.js library initializes
     * Moves container down 7cm from center
     */
    function applyFirefoxPositioning() {
        if (!isFirefox()) return;
        // Wait for stackedCards to initialize
        setTimeout(function () {
            var stackedCardsContainer = document.querySelector('.stacked-cards');
            if (stackedCardsContainer) {
                // COMMENTED OUT: Force positioning to persist - moved down 7cm from center
                // stackedCardsContainer.style.setProperty('justify-content', 'center', 'important');
                // stackedCardsContainer.style.setProperty('align-items', 'center', 'important');
                // stackedCardsContainer.style.setProperty('min-height', '100vh', 'important');
                // stackedCardsContainer.style.setProperty('padding-top', '7cm', 'important');
                // stackedCardsContainer.style.setProperty('box-sizing', 'border-box', 'important');
                if (window.console) {
                    console.log('Firefox: (disabled) stacked-cards positioning override');
                }
            }
            // COMMENTED OUT: Force phase button font size at 915px landscape in Firefox
            // if (window.matchMedia('(max-width: 915px) and (orientation: landscape)').matches) {
            //     var phaseButtons = document.querySelectorAll('#phase-selection-container .btn-group .btn');
            //     var overrideFontSize = function() {
            //         phaseButtons.forEach(function(btn, idx) {
            //             if (idx < 4) {
            //                 btn.style.setProperty('font-size', '2.5px', 'important');
            //                 btn.style.fontSize = '2.5px';
            //                 btn.style.setProperty('color', 'red', 'important');
            //             } else if (idx === 4) {
            //                 btn.style.setProperty('font-size', '8px', 'important');
            //                 btn.style.fontSize = '8px';
            //                 btn.style.setProperty('color', 'red', 'important');
            //             }
            //         });
            //     };
            //     overrideFontSize();
            //     var intervalId = setInterval(overrideFontSize, 500);
            //     setTimeout(function() {
            //         clearInterval(intervalId);
            //     }, 5000);
            //     if (window.console) {
            //         console.log('Firefox: (disabled) forced phase button font size for 915px landscape');
            //     }
            // }
        }, 500); // Wait 500ms for stackedCards.js to finish
    }

    /**
     * Dynamically position .stacked-cards at vertical midpoint + percentage of half its height (Firefox only)
     * @param {number} percent - Percentage (0-1) of half the height to add to midpoint
     */
    function positionStackedCardsMidpoint(percent) {
        if (!isFirefox()) return;
        var stackedCards = document.querySelector('.stacked-cards');
        if (!stackedCards) return;
        var viewportHeight = window.innerHeight;
        var cardsHeight = stackedCards.offsetHeight;
        var offset = (viewportHeight / 2) - (cardsHeight / 2) + ((cardsHeight / 2) * percent);
        stackedCards.style.position = 'fixed';
        stackedCards.style.top = offset + 'px';
        stackedCards.style.left = '';
        stackedCards.style.transform = '';
        stackedCards.style.margin = '0';
        stackedCards.style.paddingTop = '0';
        stackedCards.style.minHeight = '0';
        stackedCards.style.justifyContent = '';
        stackedCards.style.alignItems = '';
        stackedCards.style.boxSizing = 'border-box';
        // Debug output - COMMENTED OUT
        // if (window.console) {
        //     console.log('[Firefox stacked-cards] viewportHeight:', viewportHeight);
        //     console.log('[Firefox stacked-cards] cardsHeight:', cardsHeight);
        //     console.log('[Firefox stacked-cards] percent:', percent);
        //     console.log('[Firefox stacked-cards] offset:', offset);
        //     console.log('[Firefox stacked-cards] top applied:', stackedCards.style.top);
        // }
    }

    // Call on DOM ready, window resize, and orientation change
    function setupStackedCardsPositioning() {
        function updatePosition() {
            // Always get the latest percent value
            var percent = getStackedCardsPercent();
            positionStackedCardsMidpoint(percent);
            // Debug output - COMMENTED OUT
            // if (window.console) {
            //     console.log('Firefox stacked-cards percent:', percent);
            // }
        }
        updatePosition();
        window.addEventListener('resize', updatePosition);
        window.addEventListener('orientationchange', updatePosition);
        window.addEventListener('load', updatePosition); // Recalculate after all content loads
        setTimeout(updatePosition, 1000); // Recalculate after 1 second for late content
    }

    /**
     * Get percent parameter for stacked-cards positioning based on viewport/media queries
     */
    function getStackedCardsPercent() {
        if (window.matchMedia('(max-width: 375px)').matches) {
            return -0.35;
        } else if (window.matchMedia('(max-width: 412px)').matches) {
            return -0.45;
        } else if (window.matchMedia('(max-width: 667px)').matches) {
            return -0.25;
        } else if (window.matchMedia('(max-width: 760px)').matches) {
            return -0.20;
        } else if (window.matchMedia('(max-width: 800px)').matches) {
            return -0.21;
        } else if (window.matchMedia('(max-width: 812px)').matches) {
            return -0.25;
        } else if (window.matchMedia('(max-width: 844px)').matches) {
            return -0.23;
        } else if (window.matchMedia('(max-width: 854px)').matches) {
            return -0.23;
        } else if (window.matchMedia('(max-width: 883px)').matches) {
            return -0.23;
        } else if (window.matchMedia('(max-width: 896px)').matches) {
            return -0.23;
        } else if (window.matchMedia('(max-width: 915px)').matches) {
            return -0.23;
        } else if (window.matchMedia('(max-width: 926px)').matches) {
            return -0.24;
        } else if (window.matchMedia('(max-width: 1080px)').matches) {
            return -0.40;
        } else if (window.matchMedia('(max-width: 1280px)').matches) {
            return -0.40;
        } else if (window.matchMedia('(max-width: 1292px)').matches) {
            return -0.20;
        } else if (window.matchMedia('(max-width: 3840px)').matches) {
            return -0.20;
        }
        // Add more conditions as needed
        return -0.20; // Default
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        // Only proceed if Firefox
        if (isFirefox()) {
            disableMediaQueriesV2();
            loadFirefoxCSS();
            logScreenInfo();
            // Apply positioning fix after everything loads
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', applyFirefoxPositioning);
                document.addEventListener('DOMContentLoaded', setupStackedCardsPositioning);
            } else {
                applyFirefoxPositioning();
                setupStackedCardsPositioning();
            }
            // Also reapply on window load (double-check)
            window.addEventListener('load', applyFirefoxPositioning);
            window.addEventListener('load', setupStackedCardsPositioning);
        } else {
            console.log('Non-Firefox browser detected - Chrome styles will be used');
        }
    }

    //Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM already loaded
        init();
    }

    //// Expose functions to global window for debugging
    //window.isFirefox = isFirefox;
    //window.positionHistoryEntryMidpoint = positionHistoryEntryMidpoint;

})();
