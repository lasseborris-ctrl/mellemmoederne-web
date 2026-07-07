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

  var grid = document.getElementById('tools-grid');
  if (grid) {
    fetch('/assets/tools.json')
      .then(function (r) { return r.json(); })
      .then(function (tools) {
        if (!tools.length) {
          grid.innerHTML = '<div class="tools-empty">Det første værktøj er på vej. Kig forbi igen snart.</div>';
          return;
        }
        grid.innerHTML = tools.map(function (t) {
          return '' +
            '<div class="tool-card">' +
              '<h3>' + t.title + '</h3>' +
              '<p>' + t.description + '</p>' +
              '<div class="tool-meta">' + t.date + '</div>' +
              '<a class="btn-ghost" href="/assets/pdfs/' + encodeURIComponent(t.filename) + '" download>Download PDF</a>' +
            '</div>';
        }).join('');
      })
      .catch(function () {
        grid.innerHTML = '<div class="tools-empty">Værktøjerne kunne ikke indlæses lige nu.</div>';
      });
  }
})();
