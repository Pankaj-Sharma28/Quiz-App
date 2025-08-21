<<<<<<< HEAD
(function () {  
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.async = true;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var targetId = 'your-element-selector';
    var el = document.getElementById(targetId);
    if (!el) return; 
    
    Promise.resolve()
      .then(function () {
        return loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js');
      })
      .then(function () {
        return loadScript('https://cdn.jsdelivr.net/npm/vanta/dist/vanta.net.min.js');
      })
      .then(function () {        
        window.VANTA && window.VANTA.NET && window.VANTA.NET({
          el: '#' + targetId,
          mouseControls: true,
          touchControls: true,
          gyroControls: false,
          minHeight: 200.00,
          minWidth: 200.00,
          scale: 1.00,
          scaleMobile: 1.00
        });
      })
      .catch(function (e) {
        console.error('Vanta background failed to load:', e);
      });
  });
})();
=======
(function () {  
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.async = true;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var targetId = 'your-element-selector';
    var el = document.getElementById(targetId);
    if (!el) return; 
    
    Promise.resolve()
      .then(function () {
        return loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js');
      })
      .then(function () {
        return loadScript('https://cdn.jsdelivr.net/npm/vanta/dist/vanta.net.min.js');
      })
      .then(function () {        
        window.VANTA && window.VANTA.NET && window.VANTA.NET({
          el: '#' + targetId,
          mouseControls: true,
          touchControls: true,
          gyroControls: false,
          minHeight: 200.00,
          minWidth: 200.00,
          scale: 1.00,
          scaleMobile: 1.00
        });
      })
      .catch(function (e) {
        console.error('Vanta background failed to load:', e);
      });
  });
})();
>>>>>>> d295fd8 (quiz app initial commit)
