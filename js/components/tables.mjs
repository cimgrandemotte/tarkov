import sample from '../data/maps-sample.mjs';

const byId = new Map(sample.cartes.map(card => [card.id, card]));
const modes = sample.libelles;
const plural = n => n > 1 ? 's' : '';

function shareFilter(form, keys, apply) {
  function restore() {
    const q = new URLSearchParams(location.search);
    for (const key of keys) {
      const element = form.elements[key];
      const candidate = q.get(key);
      element.value = Array.from(element.options).some(option => option.value === candidate) ? candidate : element.options[0].value;
    }
    apply();
  }
  form.addEventListener('change', () => {
    const next = new URL(location.href);
    for (const key of keys) {
      const element = form.elements[key];
      if (element.value === element.options[0].value) next.searchParams.delete(key);
      else next.searchParams.set(key, element.value);
    }
    try { history.replaceState(null, '', next.href); } catch { /* sans historique dans certaines iframes */ }
    apply();
  });
  form.addEventListener('submit', event => event.preventDefault());
  addEventListener('popstate', restore);
  form.querySelector('[data-reset]')?.addEventListener('click', () => {
    for (const key of keys) form.elements[key].selectedIndex = 0;
    form.dispatchEvent(new Event('change'));
  });
  restore();
  form.hidden = false;
}

export function initCatalogue(root) {
  const form = root.querySelector('form');
  const rows = [...root.querySelectorAll('[data-family][data-profile]')];
  const count = root.querySelector('[data-filter-count]');
  const empty = root.querySelector('[data-filter-empty]');
  function apply() {
    const { type, profil } = form.elements;
    let n = 0;
    for (const row of rows) {
      row.hidden = Boolean((type.value && row.dataset.family !== type.value) || (profil.value && row.dataset.profile !== profil.value));
      if (!row.hidden) n++;
    }
    count.textContent = `${n} entrée${plural(n)} sur ${rows.length}.`;
    empty.hidden = Boolean(n);
  }
  shareFilter(form, ['type', 'profil'], apply);
}

export function initTierList(root) {
  const form = root.querySelector('form');
  const rows = [...root.querySelectorAll('[data-rank]')];
  const counter = root.querySelector('[data-tier-count]');
  function apply() {
    const rank = form.elements.rang.value;
    rows.forEach(row => { row.hidden = Boolean(rank && row.dataset.rank !== rank); });
    const length = rows.filter(row => !row.hidden).length;
    counter.textContent = `${length} priorité${plural(length)} sur ${rows.length}.`;
  }
  shareFilter(form, ['rang'], apply);
}

const metrics = [
  ['Durée exportée', 'duree', ' min'], ['Entrées d’extract', 'extracts', ''], ['Entrées de transit', 'transits', ''],
];

function tableCell(content, tag = 'td', scope) {
  const element = document.createElement(tag);
  element.textContent = content;
  if (scope) element.scope = scope;
  return element;
}

export function initComparator(root) {
  const form = root.querySelector('form');
  const table = root.querySelector('table');
  const status = root.querySelector('[data-compare-status]');
  const profile = form.elements.comparaison;
  const picks = [form.elements.carteA, form.elements.carteB, form.elements.carteC];
  function apply() {
    const mode = profile.value;
    const used = new Set();
    for (let i = 0; i < picks.length; i++) {
      const select = picks[i];
      if (byId.get(select.value)?.modes[mode] && !used.has(select.value)) used.add(select.value);
      else if (i < 2) {
        const first = sample.cartes.find(card => card.modes[mode] && !used.has(card.id));
        select.value = first?.id ?? '';
        if (first) used.add(first.id);
      } else select.value = '';
    }
    const chosen = picks.map(s => byId.get(s.value)).filter(Boolean);
    picks.forEach(select => {
      const others = picks.filter(other => other !== select).map(other => other.value);
      for (const opt of select.options) opt.disabled = Boolean(opt.value && (!byId.get(opt.value)?.modes[mode] || others.includes(opt.value)));
    });
    const thead = document.createElement('tr');
    thead.append(tableCell('Indicateur', 'th', 'col'), ...chosen.map(card => tableCell(card.nom, 'th', 'col')));
    const body = metrics.map(([label, name, unit]) => {
      const tr = document.createElement('tr');
      const values = chosen.map(card => card.modes[mode]?.[name] ?? null);
      const different = new Set(values.filter(v => v !== null)).size > 1;
      tr.append(tableCell(label, 'th', 'row'));
      for (const value of values) {
        const cell = tableCell(Number.isFinite(value) ? `${value}${unit}` : 'Non renseigné');
        if (different && Number.isFinite(value)) cell.className = 'data-table__diff';
        tr.append(cell);
      }
      return tr;
    });
    table.dataset.columns = String(chosen.length);
    table.tHead.replaceChildren(thead);
    table.tBodies[0].replaceChildren(...body);
    status.textContent = `${chosen.length} lieux sélectionnés · ${modes[mode]}.`;
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('change', apply);
  form.querySelector('[data-compare-reset]').addEventListener('click', () => { form.reset(); apply(); });
  apply();
  form.hidden = false;
}
