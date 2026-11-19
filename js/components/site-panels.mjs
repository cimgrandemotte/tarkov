import { preferences, focusToHash } from './ui.mjs';

// Disclosures de navigation ordinaires : conserver le modèle clavier des liens HTML.
export function initSitePanels() {
  const panels = [...document.querySelectorAll('details[data-site-panel]')];
  if (panels.length === 0) return;
  const close = panel => { panel.open = false; };
  function openTarget(hash) {
    if (!hash?.startsWith('#')) return;
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    const details = target.matches('details[data-user-expand]') ? target : target.querySelector('details[data-user-expand]');
    if (details) details.open = true;
  }
  for (const panel of panels) panel.addEventListener('toggle', () => {
    if (!panel.open) return;
    panels.filter(other => other !== panel && other.open).forEach(close);
  });
  document.addEventListener('pointerdown', event => {
    if (!(event.target instanceof Node)) return;
    panels.filter(panel => panel.open && !panel.contains(event.target)).forEach(close);
  });
  document.addEventListener('focusin', event => {
    panels.filter(panel => panel.open && !panel.contains(event.target)).forEach(close);
  });
  document.addEventListener('click', event => {
    if (!(event.target instanceof Element) || event.defaultPrevented || event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest('a[href]');
    if (!link) return;
    const hash = link.getAttribute('href');
    if (hash.startsWith('#') && (link.hasAttribute('data-expand-target') || link.closest('[data-site-panel]'))) {
      openTarget(hash);
      const panel = link.closest('details[data-site-panel]');
      if (panel) close(panel);
      if (focusToHash(hash)) {
        event.preventDefault();
        if (location.hash !== hash) {
          try { history.pushState(null, '', hash); dispatchEvent(new Event('hashchange')); } catch { /* frame à navigation restreinte */ }
        }
      }
    } else if (link.closest('[data-site-panel]')) {
      close(link.closest('[data-site-panel]'));
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || event.isComposing || document.querySelector('dialog[open]')) return;
    const active = panels.find(panel => panel.open);
    if (!active) return;
    close(active);
    active.querySelector('summary')?.focus({ preventScroll: true });
    event.preventDefault();
  });
  addEventListener('hashchange', () => openTarget(location.hash));
  if (location.hash) openTarget(location.hash);
}

export function initChecklist(form) {
  const boxes = [...form.querySelectorAll('input[type="checkbox"][name]')];
  const status = form.querySelector('[data-checklist-status]');
  const reset = form.querySelector('[data-checklist-reset]');
  const progress = form.querySelector('[data-checklist-progress]');
  const note = form.querySelector('[data-checklist-note]');
  if (boxes.length === 0 || !status || !reset) return;
  const key = `checklist:${form.dataset.checklist}`;
  try {
    const stored = JSON.parse(preferences(key) ?? '[]');
    if (Array.isArray(stored)) boxes.forEach(box => { box.checked = stored.includes(box.name); });
  } catch { /* ancienne version des préférences */ }
  function render(save = false) {
    const completed = boxes.filter(box => box.checked);
    status.textContent = `${completed.length} sur ${boxes.length} vérifiés`;
    reset.disabled = !completed.length;
    if (progress) { progress.value = completed.length; progress.hidden = false; }
    if (save) {
      const saved = preferences(key, JSON.stringify(completed.map(box => box.name)));
      if (note && saved === null) note.textContent = 'Stockage indisponible : les cases restent utilisables sur cette page.';
    }
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('change', () => render(true));
  reset.addEventListener('click', () => {
    boxes.forEach(box => { box.checked = false; });
    boxes[0].focus({ preventScroll: true });
    render(true);
  });
  reset.hidden = false;
  status.hidden = false;
  render();
}
