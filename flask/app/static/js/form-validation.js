/* RT Voyage — form-validation.js */
'use strict';

(function () {
  const RULES = {
    required: (v) => v.trim() !== '' || 'Ce champ est obligatoire',
    email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Email invalide',
    minlength: (v, param) => v.length >= parseInt(param) || `Minimum ${param} caractères`,
    maxlength: (v, param) => v.length <= parseInt(param) || `Maximum ${param} caractères`,
    phone: (v) => !v || /^[+\d\s()\-]{7,20}$/.test(v) || 'Numéro de téléphone invalide',
    match: (v, param) => v === (document.getElementById(param)?.value || '') || 'Les mots de passe ne correspondent pas'
  };

  function validate(field) {
    const val = field.value || '';
    let error = null;
    for (const [rule, param] of Object.entries(field.dataset)) {
      if (rule.startsWith('validate')) {
        const ruleName = rule.replace('validate', '').toLowerCase();
        const fn = RULES[ruleName];
        if (fn) {
          const result = fn(val, param);
          if (result !== true) { error = result; break; }
        }
      }
    }
    if (field.required && val.trim() === '') error = 'Ce champ est obligatoire';
    if (field.type === 'email' && val && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) error = 'Email invalide';
    showError(field, error);
    return !error;
  }

  function showError(field, msg) {
    let errEl = field.parentElement.querySelector('.field-error');
    if (msg) {
      field.classList.add('is-invalid');
      field.classList.remove('is-valid');
      if (!errEl) {
        errEl = document.createElement('p');
        errEl.className = 'field-error form-error';
        field.parentElement.appendChild(errEl);
      }
      errEl.textContent = msg;
    } else {
      field.classList.remove('is-invalid');
      field.classList.add('is-valid');
      errEl?.remove();
    }
  }

  /* Wire all forms with class "js-validate" */
  document.querySelectorAll('form.js-validate, form#contactForm, form#registerForm').forEach(form => {
    const fields = form.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([name=csrf_token]), textarea, select');

    fields.forEach(field => {
      field.addEventListener('blur', () => validate(field));
      field.addEventListener('input', () => {
        if (field.classList.contains('is-invalid')) validate(field);
      });
    });

    form.addEventListener('submit', (e) => {
      let valid = true;
      fields.forEach(field => { if (!validate(field)) valid = false; });
      if (!valid) {
        e.preventDefault();
        const firstInvalid = form.querySelector('.is-invalid');
        firstInvalid?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstInvalid?.focus();
      }
    });
  });

  /* Password strength indicator */
  const pwdField = document.getElementById('password') || document.querySelector('input[type=password][data-strength]');
  if (pwdField) {
    const bar = document.createElement('div');
    bar.style.cssText = 'height:3px;margin-top:6px;border-radius:2px;background:var(--border-dark);overflow:hidden;';
    const fill = document.createElement('div');
    fill.style.cssText = 'height:100%;transition:width 0.3s,background 0.3s;width:0;';
    bar.appendChild(fill);
    pwdField.parentElement.appendChild(bar);

    pwdField.addEventListener('input', () => {
      const v = pwdField.value;
      let score = 0;
      if (v.length >= 8) score++;
      if (/[A-Z]/.test(v)) score++;
      if (/[0-9]/.test(v)) score++;
      if (/[^A-Za-z0-9]/.test(v)) score++;
      const colors = ['#c0392b','#e67e22','#f1c40f','#27ae60'];
      fill.style.width = (score * 25) + '%';
      fill.style.background = colors[score - 1] || '#c0392b';
    });
  }
})();
