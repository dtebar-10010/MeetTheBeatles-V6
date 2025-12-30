document.addEventListener("DOMContentLoaded", function () {
 // Initialize the stacked cards
 var stackedCardSlide = new stackedCards({
  selector: ".stacked-cards-slide",
  layout: "slide",
  transformOrigin: "center",
  onClick: function (el) {
   document.querySelectorAll(".stacked-cards video").forEach((video) => {
    if (video.parentElement === el) {
     video.controls = true;
     video.parentElement.classList.add("active");
    } else {
     video.controls = false;
     video.pause();
     video.parentElement.classList.remove("active");
    }
   });
  },
  onTouch: function (el) {
   // Add touch support for mobile devices
   document.querySelectorAll(".stacked-cards video").forEach((video) => {
    if (video.parentElement === el) {
     video.controls = true;
     video.parentElement.classList.add("active");
    } else {
     video.controls = false;
     video.pause();
     video.parentElement.classList.remove("active");
    }
   });
  },
 });
 stackedCardSlide.init();
 // Accordion Logic
 const accordionHeaders = document.querySelectorAll(".accordion.hide-initially");
 accordionHeaders.forEach(function (header) {
  header.classList.add("show-initially");
 });
 // Phase Selection Container Logic
 const phaseSelectionContainer = document.querySelector("#phase-selection-container");
 if (phaseSelectionContainer) {
  phaseSelectionContainer.classList.remove("hide-initially");
  // Remove conflicting inline styles to let CSS handle layout
  phaseSelectionContainer.style.removeProperty("width");
  phaseSelectionContainer.style.removeProperty("margin");
  phaseSelectionContainer.style.removeProperty("display");
 }
 // Video Controls Logic with touch support
 const videos = document.querySelectorAll(".video-slide");
 videos.forEach(function (video) {
  // Mouse events
  video.addEventListener("mouseover", function () {
   if (video.closest("li").classList.contains("active")) {
    video.setAttribute("controls", "controls");
   }
  });
  video.addEventListener("mouseout", function () {
   if (!video.paused) {
    video.setAttribute("controls", "controls");
   } else {
    video.removeAttribute("controls");
   }
  });
  
  // Touch events for mobile
  video.addEventListener("touchstart", function (e) {
   if (video.closest("li").classList.contains("active")) {
    video.setAttribute("controls", "controls");
   }
  }, { passive: true });
  
  video.addEventListener("play", function () {
   document.querySelectorAll(".video-slide").forEach((v) => {
    if (v !== video) {
     v.pause();
     v.removeAttribute("controls");
     v.closest("li").classList.remove("active");
    }
   });
   video.setAttribute("controls", "controls");
   video.closest("li").classList.add("active");
  });
  video.addEventListener("pause", function () {
   video.removeAttribute("controls");
  });
 });
 
 // Add touch support to stacked cards container and individual cards
 const stackedCardsContainer = document.querySelector(".stacked-cards");
 if (stackedCardsContainer) {
  // Ensure touch events work on cards
  const cards = document.querySelectorAll(".stacked-cards li");
  cards.forEach(function(card) {
   card.addEventListener("touchend", function(e) {
    // Only trigger if not interacting with active video
    const isActiveCard = card.classList.contains("active");
    const touchedVideo = e.target.closest("video");
    
    if (!isActiveCard || !touchedVideo) {
     // Prevent default and trigger click for card navigation
     e.preventDefault();
     e.stopPropagation();
     card.click();
    }
   }, { passive: false });
  });
 }
 
 // Update current year
 const currentYearElement = document.getElementById("currentYear");
 if (currentYearElement) {
  currentYearElement.textContent = String(new Date().getFullYear());
 }
 // Text Container Border Color Logic
 const textContainer = document.querySelector(".text-container");
 const phaseButtons = document.querySelectorAll(".btn-group .btn");
 let currentPhaseColor;

 // Function to update text container border color only
 function updateTextContainerBorder() {
  // Apply the current phase border color
  if (currentPhaseColor) {
   textContainer.style.borderColor = currentPhaseColor;
  }
 }

 // Get the initial active button color
 const activeButton = document.querySelector(".btn.active");
 if (activeButton) {
  currentPhaseColor = window.getComputedStyle(activeButton).backgroundColor;
 }

 // Make text container visible and update border
 setTimeout(() => {
  updateTextContainerBorder();
 }, 0);

 // Add event listeners for phase buttons
 phaseButtons.forEach((button) => {
  button.addEventListener("click", () => {
   // Update active button state
   phaseButtons.forEach((btn) => btn.classList.remove("active"));
   button.classList.add("active");
   // Update the current phase color
   currentPhaseColor = window.getComputedStyle(button).backgroundColor;
   // Update the text container border
   updateTextContainerBorder();
  });
 });

});

// Function to check if the device is mobile (Android or iOS)
function isMobileDevice() {
 return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Function to check orientation and show prompt only on mobile devices
function checkOrientation() {
 // Only proceed if it's a mobile device
 if (!isMobileDevice()) return;

 const rotationPrompt = document.querySelector('.rotation-prompt');
 if (!rotationPrompt) return;

 // Check orientation using screen orientation API if available
 if (window.screen && window.screen.orientation) {
  const orientation = window.screen.orientation.type;
  const show = (orientation === "portrait-primary" || orientation === "portrait-secondary");
  if (show) {
   rotationPrompt.classList.remove('d-none');
   rotationPrompt.setAttribute('aria-hidden', 'false');
  } else {
   rotationPrompt.classList.add('d-none');
   rotationPrompt.setAttribute('aria-hidden', 'true');
  }
 } else {
  // Fallback to matchMedia for browsers that don't support screen orientation API
  const isPortrait = window.matchMedia("(orientation: portrait)").matches;
  if (isPortrait) {
   rotationPrompt.classList.remove('d-none');
   rotationPrompt.setAttribute('aria-hidden', 'false');
  } else {
   rotationPrompt.classList.add('d-none');
   rotationPrompt.setAttribute('aria-hidden', 'true');
  }
 }
}

// Set up event listeners for orientation changes
if (window.screen && window.screen.orientation) {
 window.screen.orientation.addEventListener('change', checkOrientation);
} else {
 // Fallback for browsers without screen orientation API
 const portraitMediaQuery = window.matchMedia("(orientation: portrait)");
 if (portraitMediaQuery.addEventListener) {
  portraitMediaQuery.addEventListener('change', checkOrientation);
 } else {
  // Older browsers
  portraitMediaQuery.addListener(checkOrientation);
 }
}

// Check initial orientation when page loads
document.addEventListener('DOMContentLoaded', checkOrientation);
// Also handle resize events for good measure
window.addEventListener('resize', checkOrientation);
