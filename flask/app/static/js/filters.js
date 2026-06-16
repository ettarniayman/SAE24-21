/* RT Voyage — filters.js : filter bar interactions */
'use strict';

/* Live filter-bar URL sync — push state on change */
(function () {
  const filterBar = document.querySelector('.filter-bar');
  if (!filterBar) return;

  /* Type toggle buttons */
  filterBar.querySelectorAll('[data-filter-type]').forEach(btn => {
    btn.addEventListener('click', () => {
      filterBar.querySelectorAll('[data-filter-type]').forEach(b => b.classList.remove('active', 'btn-gold'));
      btn.classList.add('active', 'btn-gold');
      syncForm(filterBar);
    });
  });

  /* Sort selects & search inputs — debounce auto-submit */
  let debounceTimer;
  filterBar.querySelectorAll('select[name=sort], select[name=stars], select[name=theme], select[name=duration]').forEach(sel => {
    sel.addEventListener('change', () => syncForm(filterBar));
  });
  filterBar.querySelectorAll('input[type=text], input[type=search]').forEach(inp => {
    inp.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => syncForm(filterBar), 500);
    });
  });

  function syncForm(bar) {
    const form = bar.querySelector('form') || bar.closest('form');
    if (form) form.submit();
  }
})();

/* ─── Range slider with dual handle (price) ─── */
(function () {
  const rangeWrap = document.querySelector('.price-range');
  if (!rangeWrap) return;
  const min = rangeWrap.querySelector('[data-range=min]');
  const max = rangeWrap.querySelector('[data-range=max]');
  const minOut = document.getElementById('priceMin');
  const maxOut = document.getElementById('priceMax');

  function update() {
    const lo = Math.min(parseInt(min.value), parseInt(max.value) - 100);
    const hi = Math.max(parseInt(max.value), parseInt(min.value) + 100);
    min.value = lo;
    max.value = hi;
    if (minOut) minOut.textContent = lo.toLocaleString('fr-FR') + ' MAD';
    if (maxOut) maxOut.textContent = hi.toLocaleString('fr-FR') + ' MAD';
    const pct1 = ((lo - min.min) / (min.max - min.min)) * 100;
    const pct2 = ((hi - max.min) / (max.max - max.min)) * 100;
    rangeWrap.style.setProperty('--range-lo', pct1 + '%');
    rangeWrap.style.setProperty('--range-hi', pct2 + '%');
  }
  min?.addEventListener('input', update);
  max?.addEventListener('input', update);
  update();
})();

/* ─── Tag-toggle (multi-select theme chips) ─── */
document.querySelectorAll('.tag-toggle').forEach(tag => {
  tag.addEventListener('click', () => {
    tag.classList.toggle('active');
    const hidden = document.getElementById('selectedThemes');
    if (!hidden) return;
    const active = Array.from(document.querySelectorAll('.tag-toggle.active')).map(t => t.dataset.value);
    hidden.value = active.join(',');
  });
});

/* ─── Sticky filter bar shadow on scroll ─── */
const filterBar = document.querySelector('.filter-bar');
if (filterBar) {
  const sentinel = document.createElement('div');
  sentinel.style.height = '1px';
  filterBar.parentNode.insertBefore(sentinel, filterBar);
  new IntersectionObserver(([entry]) => {
    filterBar.classList.toggle('sticky-shadow', !entry.isIntersecting);
  }).observe(sentinel);
}
