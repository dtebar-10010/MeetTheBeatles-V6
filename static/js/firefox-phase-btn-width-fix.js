// Firefox persistent width enforcement for phase selection buttons using !important (136px)
(function() {
  if (navigator.userAgent.toLowerCase().indexOf('firefox') === -1) return;
  function setBtnWidth() {
    var btns = document.querySelectorAll('#phase-selection-container .btn-group a.btn');
    btns.forEach(function(btn) {
      btn.style.setProperty('width', '136px', 'important');
      btn.style.setProperty('min-width', '136px', 'important');
      btn.style.setProperty('max-width', '136px', 'important');
    });
    requestAnimationFrame(setBtnWidth);
  }
  setBtnWidth();
})();
