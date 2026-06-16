/* RT Voyage — admin.js */
'use strict';

/* ─── Sidebar active link ─── */
const currentPath = window.location.pathname;
document.querySelectorAll('.sidebar-nav a').forEach(link => {
  if (link.getAttribute('href') === currentPath || currentPath.startsWith(link.getAttribute('href') + '/')) {
    link.classList.add('active');
  }
});

/* ─── Collapsible sidebar sections ─── */
document.querySelectorAll('.sidebar-section-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const section = btn.closest('.sidebar-section');
    section?.classList.toggle('collapsed');
    const icon = btn.querySelector('.toggle-icon');
    if (icon) icon.style.transform = section?.classList.contains('collapsed') ? 'rotate(-90deg)' : '';
  });
});

/* ─── Delete confirmations ─── */
document.querySelectorAll('[data-confirm]').forEach(el => {
  el.addEventListener('click', (e) => {
    if (!confirm(el.dataset.confirm || 'Confirmer la suppression ?')) e.preventDefault();
  });
});

/* ─── Auto-generate slug from title ─── */
function slugify(str) {
  return str.toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim().replace(/[\s]+/g, '-')
    .replace(/-+/g, '-');
}

const nameField = document.getElementById('name_fr') || document.getElementById('title_fr');
const slugField = document.getElementById('slug');
let slugManuallyEdited = false;
if (slugField) slugField.addEventListener('input', () => { slugManuallyEdited = true; });
if (nameField && slugField) {
  nameField.addEventListener('input', () => {
    if (!slugManuallyEdited) slugField.value = slugify(nameField.value);
  });
}

/* ─── Character counters ─── */
document.querySelectorAll('[data-maxlength]').forEach(el => {
  const max = parseInt(el.dataset.maxlength);
  const counter = document.createElement('small');
  counter.style.cssText = 'display:block;text-align:right;color:var(--text-sub);font-size:0.72rem;margin-top:2px;';
  el.parentNode.appendChild(counter);
  const update = () => {
    const rem = max - el.value.length;
    counter.textContent = `${el.value.length} / ${max}`;
    counter.style.color = rem < 20 ? 'var(--gold)' : 'var(--text-sub)';
  };
  el.addEventListener('input', update);
  update();
});

/* ─── Image preview on file input ─── */
document.querySelectorAll('input[type=file][data-preview]').forEach(input => {
  const previewId = input.dataset.preview;
  const preview = document.getElementById(previewId);
  if (!preview) return;
  input.addEventListener('change', () => {
    const file = input.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.src = e.target.result;
        preview.style.display = 'block';
      };
      reader.readAsDataURL(file);
    }
  });
});

/* ─── Admin stat card counter animation ─── */
document.querySelectorAll('.admin-stat-card .stat-number').forEach(el => {
  const target = parseInt(el.textContent.replace(/\D/g, ''), 10);
  if (!target || isNaN(target)) return;
  let current = 0;
  const step = Math.max(1, Math.floor(target / 40));
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current.toLocaleString('fr-FR');
    if (current >= target) clearInterval(timer);
  }, 30);
});

/* ─── Sortable table (basic) ─── */
document.querySelectorAll('th[data-sort]').forEach(th => {
  th.style.cursor = 'pointer';
  th.addEventListener('click', () => {
    const table = th.closest('table');
    const col = Array.from(th.parentElement.children).indexOf(th);
    const asc = th.dataset.order !== 'asc';
    th.dataset.order = asc ? 'asc' : 'desc';
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    rows.sort((a, b) => {
      const av = a.cells[col]?.textContent.trim() || '';
      const bv = b.cells[col]?.textContent.trim() || '';
      return asc ? av.localeCompare(bv, 'fr') : bv.localeCompare(av, 'fr');
    });
    const tbody = table.querySelector('tbody');
    rows.forEach(r => tbody.appendChild(r));
  });
});

/* ─── Toast notifications ─── */
window.showToast = function(msg, type = 'success') {
  const toast = document.createElement('div');
  toast.textContent = msg;
  toast.style.cssText = `
    position:fixed;bottom:24px;right:24px;z-index:9999;padding:14px 24px;
    background:${type === 'success' ? 'var(--gold)' : '#c0392b'};
    color:${type === 'success' ? 'var(--bg-deep)' : '#fff'};
    border-radius:var(--radius-sm);font-size:0.84rem;font-weight:600;
    box-shadow:0 8px 24px rgba(0,0,0,0.4);transform:translateY(0);
    animation:slideInRight 0.3s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = '0.3s'; setTimeout(() => toast.remove(), 300); }, 3000);
};

/* ─── Confirm bulk-delete ─── */
const bulkForm = document.getElementById('bulkForm');
if (bulkForm) {
  bulkForm.addEventListener('submit', (e) => {
    const checked = bulkForm.querySelectorAll('input[name=ids]:checked').length;
    if (!checked) { e.preventDefault(); return; }
    if (!confirm(`Supprimer ${checked} élément(s) ?`)) e.preventDefault();
  });
  const checkAll = document.getElementById('checkAll');
  checkAll?.addEventListener('change', () => {
    bulkForm.querySelectorAll('input[name=ids]').forEach(cb => cb.checked = checkAll.checked);
  });
}
