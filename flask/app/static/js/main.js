/* RT Voyage — main.js */
'use strict';

/* ─── Navbar scroll behaviour ─── */
const navbar = document.querySelector('.navbar');
if (navbar) {
  const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 60);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* ─── Mobile hamburger ─── */
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
if (hamburger && navMenu) {
  hamburger.addEventListener('click', () => {
    const open = navMenu.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  document.addEventListener('click', (e) => {
    if (!navbar.contains(e.target)) {
      navMenu.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
  });
}

/* ─── Search overlay ─── */
const searchToggle = document.querySelector('.search-toggle');
const searchOverlay = document.querySelector('.search-overlay');
const searchClose = document.querySelector('.search-close');
const searchInput = document.getElementById('globalSearch');
const searchResults = document.getElementById('searchResults');

function openSearch() {
  searchOverlay?.classList.add('active');
  setTimeout(() => searchInput?.focus(), 100);
  document.body.style.overflow = 'hidden';
}
function closeSearch() {
  searchOverlay?.classList.remove('active');
  document.body.style.overflow = '';
  if (searchResults) searchResults.innerHTML = '';
}

searchToggle?.addEventListener('click', openSearch);
searchClose?.addEventListener('click', closeSearch);
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeSearch();
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); openSearch(); }
});

let searchTimer;
searchInput?.addEventListener('input', () => {
  clearTimeout(searchTimer);
  const q = searchInput.value.trim();
  if (q.length < 2) { if (searchResults) searchResults.innerHTML = ''; return; }
  searchTimer = setTimeout(async () => {
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
      const data = await res.json();
      renderSearchResults(data);
    } catch (_) {}
  }, 300);
});

function renderSearchResults(data) {
  if (!searchResults) return;
  if (!data.results?.length) {
    searchResults.innerHTML = '<p style="text-align:center;color:var(--text-sub);padding:24px;">Aucun résultat trouvé</p>';
    return;
  }
  searchResults.innerHTML = data.results.map(item => `
    <a href="${item.url}" class="search-result-item" style="display:flex;align-items:center;gap:14px;padding:12px 16px;border-radius:var(--radius-sm);text-decoration:none;transition:background 0.15s;" onmouseover="this.style.background='var(--bg-card2)'" onmouseout="this.style.background=''">
      ${item.image ? `<img src="${item.image}" alt="" style="width:48px;height:48px;object-fit:cover;border-radius:var(--radius-sm);flex-shrink:0;">` : `<div style="width:48px;height:48px;border-radius:var(--radius-sm);background:var(--gold-dim);display:flex;align-items:center;justify-content:center;flex-shrink:0;"><i class="fa fa-${item.type==='destination'?'globe':item.type==='program'?'map':'newspaper'}" style="color:var(--gold);"></i></div>`}
      <div>
        <p style="font-size:0.9rem;font-weight:600;color:var(--text-light);">${escHtml(item.name)}</p>
        <p style="font-size:0.76rem;color:var(--text-sub);text-transform:capitalize;">${escHtml(item.type)}</p>
      </div>
    </a>
  `).join('');
}

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/* ─── Back to top ─── */
const btt = document.querySelector('.back-to-top');
if (btt) {
  window.addEventListener('scroll', () => btt.classList.toggle('visible', window.scrollY > 400), { passive: true });
  btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ─── Hero particles ─── */
(function initParticles() {
  const container = document.querySelector('.hero__particles');
  if (!container) return;
  const COUNT = 50;
  const frag = document.createDocumentFragment();
  for (let i = 0; i < COUNT; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 4 + 1;
    const x = Math.random() * 100;
    const delay = Math.random() * 8;
    const dur = Math.random() * 6 + 6;
    p.style.cssText = `left:${x}%;width:${size}px;height:${size}px;animation-delay:${delay}s;animation-duration:${dur}s;opacity:${Math.random()*0.6+0.1};`;
    frag.appendChild(p);
  }
  container.appendChild(frag);
})();

/* ─── Hero search ─── */
const heroSearchBtn = document.querySelector('.hero-search__btn');
const heroSearchInput = document.querySelector('.hero-search__input');
if (heroSearchBtn && heroSearchInput) {
  heroSearchBtn.addEventListener('click', () => {
    const q = heroSearchInput.value.trim();
    if (q) window.location.href = `/destinations?q=${encodeURIComponent(q)}`;
  });
  heroSearchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') heroSearchBtn.click();
  });
}

/* ─── Destination tabs ─── */
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + target)?.classList.add('active');
  });
});

/* ─── Flash messages auto-dismiss ─── */
document.querySelectorAll('.flash').forEach(flash => {
  setTimeout(() => flash.classList.add('dismiss'), 5000);
  flash.querySelector('.flash__close')?.addEventListener('click', () => flash.classList.add('dismiss'));
});

/* ─── Promo banner countdown ─── */
const countdown = document.querySelector('.promo-countdown');
if (countdown) {
  const end = new Date(countdown.dataset.end);
  const tick = () => {
    const diff = end - Date.now();
    if (diff <= 0) { countdown.textContent = 'Expirée'; return; }
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    countdown.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
  };
  tick();
  setInterval(tick, 1000);
}

/* ─── Newsletter form inline feedback ─── */
document.querySelectorAll('.newsletter-form').forEach(form => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('[type=submit]');
    const orig = btn.textContent;
    btn.disabled = true;
    btn.textContent = '…';
    try {
      const res = await fetch(form.action, { method: 'POST', body: new FormData(form) });
      btn.textContent = res.ok ? '✓ Inscrit !' : 'Erreur';
      btn.style.background = res.ok ? 'var(--gold)' : '#c0392b';
    } catch (_) {
      btn.textContent = orig;
    } finally {
      setTimeout(() => { btn.disabled = false; btn.textContent = orig; btn.style.background = ''; }, 3000);
    }
  });
});
