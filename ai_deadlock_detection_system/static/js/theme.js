(function(){
  document.addEventListener('DOMContentLoaded', function(){
    var btn = document.getElementById('themeToggle');

    // Set theme, optionally performing a small cross-fade animation
    function setTheme(t, withFade){
      if(withFade){
        // add class to start fade-out
        document.documentElement.classList.add('theme-fade');
        // force reflow so the opacity transition starts
        void document.documentElement.offsetWidth;
        // change the theme attribute while faded
        document.documentElement.setAttribute('data-theme', t);
        // remove fade class after animation duration to fade back in
        window.setTimeout(function(){
          document.documentElement.classList.remove('theme-fade');
        }, 260);
      } else {
        document.documentElement.setAttribute('data-theme', t);
      }
    }

    var saved = localStorage.getItem('theme') || 'dark';
    // apply without fade on initial load
    setTheme(saved, false);

    if(btn){
      btn.addEventListener('click', function(){
        var current = document.documentElement.getAttribute('data-theme') || 'dark';
        var next = current === 'dark' ? 'light' : 'dark';
        setTheme(next, true);
        localStorage.setItem('theme', next);
      });
    }
  });
})();
