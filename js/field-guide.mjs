import { preferences } from './components/ui.mjs';

// Mémo d'interface uniquement : ne capte ni ne modifie une touche du jeu.
function initKeyGuide(form) {
  const picker = form.elements.disposition;
  const controls = form.querySelector('[data-keys-controls]');
  const rows = [...form.querySelectorAll('[data-bind]')];
  const feedback = form.querySelector('[data-keys-status]');
  const note = form.querySelector('#keys-note');
  const instructions = form.querySelector('[data-keys-instruction]');
  const reset = form.querySelector('[data-keys-reset]');
  if (!picker || !controls || !feedback || !note || !instructions || !reset || rows.length === 0) return;
  const key = 'guide:touches-v1';
  const modes = ['qwerty', 'azerty', 'custom'];
  const messages = {
    qwerty: 'Touches QWERTY par défaut. Ce tableau ne modifie pas le jeu.',
    azerty: 'AZERTY proposé, pas un préréglage officiel. Vérifie Z, Q et la rangée de chiffres dans le menu du jeu.',
    custom: 'Aide-mémoire personnel. Aucun changement dans le jeu.',
  };
  let data = Object.create(null);
  const clean = value => typeof value === 'string' ? value.trim().slice(0, 32) : '';
  try {
    const saved = JSON.parse(preferences(key) ?? '{}');
    picker.value = modes.includes(saved?.mode) ? saved.mode : 'qwerty';
    for (const row of rows) {
      const value = clean(saved?.keys?.[row.dataset.bind]);
      if (value) data[row.dataset.bind] = value;
    }
  } catch { picker.value = 'qwerty'; }
  function persist(message = 'Enregistré dans ce navigateur.') {
    const saved = preferences(key, JSON.stringify({ mode: picker.value, keys: data }));
    feedback.textContent = saved === null ? 'Stockage indisponible. Changements valables sur cette page seulement.' : message;
  }
  function paint() {
    const custom = picker.value === 'custom';
    note.textContent = messages[picker.value];
    instructions.hidden = !custom;
    for (const row of rows) {
      const value = row.querySelector('[data-key-value]');
      const input = row.querySelector('input');
      if (!input || !value) continue;
      value.hidden = custom;
      input.hidden = input.disabled = !custom;
      value.textContent = row.dataset[picker.value] ?? row.dataset.qwerty;
      if (custom) input.value = data[row.dataset.bind] || row.dataset.qwerty;
    }
  }
  form.addEventListener('submit', event => event.preventDefault());
  picker.addEventListener('change', () => { paint(); persist(); });
  form.addEventListener('input', event => {
    const row = event.target.closest('input')?.closest('[data-bind]');
    if (!row || picker.value !== 'custom' || event.isComposing) return;
    const name = row.dataset.bind;
    const value = clean(event.target.value);
    if (value) data[name] = value;
    else delete data[name];
    persist();
  });
  form.addEventListener('change', event => {
    const row = event.target.closest('input')?.closest('[data-bind]');
    if (!row || picker.value !== 'custom') return;
    const value = clean(event.target.value);
    if (value) data[row.dataset.bind] = value;
    else delete data[row.dataset.bind];
    event.target.value = value || row.dataset.qwerty;
    persist();
  });
  reset.addEventListener('click', () => {
    data = Object.create(null);
    picker.value = 'qwerty';
    paint();
    persist('Commandes remises aux valeurs par défaut.');
    picker.focus({ preventScroll: true });
  });
  controls.hidden = form.querySelector('[data-keys-foot]').hidden = false;
  paint();
}

function initSpoilers(group) {
  const panes = [...group.querySelectorAll('details[data-spoiler]')];
  const actions = group.querySelector('[data-spoiler-actions]');
  const close = group.querySelector('[data-spoiler-close]');
  if (!panes.length || !actions || !close) return;
  const sync = () => { close.disabled = !panes.some(p => p.open); };
  const shut = () => {
    const firstOpen = panes.find(p => p.open);
    if (!firstOpen) return;
    panes.forEach(p => { p.open = false; });
    sync();
    if (document.activeElement === close || document.activeElement === document.body) firstOpen.querySelector('summary')?.focus();
  };
  // Ne pas restaurer un spoiler laissé ouvert à la revisite, même avec le cache arrière.
  addEventListener('pageshow', event => { if (event.persisted) shut(); });
  panes.forEach(p => p.addEventListener('toggle', sync));
  close.addEventListener('click', shut);
  actions.hidden = false;
  sync();
}

function initOutline() {
  const links = [...document.querySelectorAll('.field-toc a, .field-toc-mobile a')];
  if (links.length === 0) return;
  const sections = [...document.querySelectorAll('.field-notes > .field-section')];
  const desktop = matchMedia('(min-width: 56.001rem)');
  let frame = null;
  const set = hash => {
    for (const link of links) {
      if (link.hash === hash) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  };
  function update() {
    const target = document.getElementById(location.hash.slice(1))?.closest('.field-section');
    set(target ? `#${target.id}` : links[0].hash);
  }
  function follow() {
    if (!desktop.matches || frame !== null || sections.length === 0) return;
    frame = requestAnimationFrame(() => {
      frame = null;
      const line = document.querySelector('.commandbar').getBoundingClientRect().bottom + 54;
      const seen = sections.filter(section => section.getBoundingClientRect().top <= line);
      set(`#${(seen.at(-1) ?? sections[0]).id}`);
    });
  }
  const mobile = document.querySelector('.field-toc-mobile');
  mobile?.addEventListener('click', event => {
    if (!event.target.closest('a') || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button) return;
    // La fermeture avant le report de focus évite de décaler la section visée.
    mobile.open = false;
  });
  addEventListener('hashchange', update);
  addEventListener('scroll', follow, { passive: true });
  desktop.addEventListener('change', event => { if (event.matches) follow(); else update(); });
  update();
}

document.querySelectorAll('[data-keyboard-guide]').forEach(initKeyGuide);
document.querySelectorAll('[data-spoiler-group]').forEach(initSpoilers);
initOutline();
