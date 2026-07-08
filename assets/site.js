(function () {
  var btn = document.getElementById('themeToggle');
  var saved = localStorage.getItem('site:theme') || 'light';
  function apply(mode) {
    if (mode === 'dark') { document.body.setAttribute('data-theme', 'dark'); if (btn) btn.textContent = '☀'; }
    else { document.body.removeAttribute('data-theme'); if (btn) btn.textContent = '☾'; }
  }
  apply(saved);
  if (btn) {
    btn.addEventListener('click', function () {
      var next = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      localStorage.setItem('site:theme', next);
      apply(next);
    });
  }

  document.querySelectorAll('.faq-item').forEach(function (item) {
    item.querySelector('.faq-q').addEventListener('click', function () {
      var wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (o) { o.classList.remove('open'); });
      if (!wasOpen) item.classList.add('open');
    });
  });
})();
