import { focusToHash } from './ui.mjs';

const rootUrl = new URL('../../', import.meta.url);
const indexUrl = new URL('js/data/search-index.json', rootUrl);
const normalize = str => String(str).normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().trim();
const limit = 9;

function loadIndex() {
  return Promise.all([
    import('../vendor/fuse.min.mjs'),
    fetch(indexUrl, { credentials: 'same-origin' }).then(res => {
      if (!res.ok) throw new Error('Index indisponible');
      return res.json();
    }),
  ]).then(([{ default: Fuse }, index]) => {
    if (index.schemaVersion !== 1 || !Array.isArray(index.entrees)) throw new Error('Schéma de l’index');
    return { index, fuzzy: new Fuse(index.entrees, {
      ignoreDiacritics: true, ignoreLocation: true, includeScore: true, threshold: .33, minMatchCharLength: 2,
      keys: [{ name: 'titre', weight: .60 }, { name: 'termes', weight: .33 }, { name: 'description', weight: .07 }],
    }) };
  });
}

function destination(row) {
  if (!row.url || row.etat === 'planifiee') return null;
  const next = new URL(row.url, rootUrl);
  return next.origin === rootUrl.origin && next.pathname.startsWith(rootUrl.pathname) ? next : null;
}

function makeResult(row, onNavigate) {
  const li = document.createElement('li');
  const url = destination(row);
  const hit = document.createElement(url ? 'a' : 'div');
  const body = document.createElement('div');
  const title = document.createElement('span');
  const desc = document.createElement('span');
  const meta = document.createElement('span');
  hit.className = 'search-hit';
  title.className = 'search-hit__title';
  desc.className = 'search-hit__desc';
  meta.className = 'search-hit__meta';
  title.textContent = row.titre;
  desc.textContent = row.description;
  meta.textContent = row.etat === 'atelier' ? 'Atelier' : row.etat === 'publiee' ? 'Publié' : row.etat === 'accueil' ? 'Repère · Accueil' : row.etat === 'dossier' ? 'Repère · Guide' : `À venir · Phase ${row.phase}`;
  if (url) {
    hit.href = url.href;
    const indexAsDirectory = path => path.replace(/\/index\.html$/, '/');
    const here = indexAsDirectory(location.pathname) === indexAsDirectory(url.pathname);
    if (here && url.hash) hit.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || !document.getElementById(url.hash.slice(1))) return;
      event.preventDefault();
      onNavigate(url.hash);
    });
  }
  body.append(title, desc);
  hit.append(body, meta);
  li.append(hit);
  return li;
}

export function initSearch(dialog, driver) {
  if (!dialog || !driver) return;
  const form = dialog.querySelector('form[role="search"]');
  const input = form.elements.requete;
  const scope = form.elements.portee;
  const count = dialog.querySelector('[data-search-status]');
  const results = dialog.querySelector('[data-search-results]');
  const retry = dialog.querySelector('[data-search-retry]');
  let data;
  let pending;
  let timer = 0;
  function navigate(hash) {
    driver.dismiss('navigate');
    if (location.hash !== hash) {
      try { history.pushState(null, '', hash); dispatchEvent(new Event('hashchange')); } catch { /* frame restreint */ }
    }
    focusToHash(hash);
  }
  function paint(rows) { results.replaceChildren(...rows.map(row => makeResult(row, navigate))); }
  function show() {
    if (!dialog.open || !data) return;
    const text = input.value.trim();
    const accepts = row => scope.value === 'all' || row.etat === scope.value || (scope.value === 'accueil' && row.url === 'index.html');
    if (text.length < 2) {
      const basics = data.index.entrees.filter(accepts).filter(row => scope.value !== 'all' || row.etat !== 'planifiee');
      if (scope.value === 'all' && /\/atelier\/(?:index\.html)?$/.test(location.pathname)) {
        basics.sort((a,b) => Number(b.etat === 'atelier') - Number(a.etat === 'atelier'));
      }
      count.textContent = text.length ? 'Saisissez au moins deux caractères.' : 'Suggestions · Essayez « extraction », « quêtes » ou « comparateur ».';
      paint(basics.slice(0, 5));
      return;
    }
    const plain = normalize(text);
    // Un préfixe dans le titre doit passer devant une correspondance approximative dans une description.
    const exactness = row => {
      const title = normalize(row.titre);
      if (title === plain) return 0;
      if (title.startsWith(plain)) return 1;
      if (title.includes(plain) || row.termes.some(term => normalize(term) === plain)) return 2;
      return 3;
    };
    const matches = data.fuzzy.search(text).filter(hit => accepts(hit.item)).sort((a, b) =>
      exactness(a.item) - exactness(b.item) || a.score - b.score);
    const strong = matches.filter(hit => exactness(hit.item) < 3 || hit.score <= .88);
    const hits = strong.length ? strong : matches;
    const length = hits.length;
    count.textContent = length ? `${length} résultat${length > 1 ? 's' : ''}${length > limit ? ` · ${limit} affichés` : ''}.` : 'Aucun résultat. Essayez un mot plus court ou élargissez la portée.';
    paint(hits.slice(0, limit).map(hit => hit.item));
  }
  function ensure() {
    if (data) { show(); return; }
    if (pending) return;
    retry.hidden = true;
    count.textContent = 'Chargement de l’index…';
    results.replaceChildren();
    pending = loadIndex().then(value => { data = value; show(); }).catch(() => {
      count.textContent = 'L’index local n’a pas pu être chargé. Réessayez ou utilisez la navigation.';
      retry.hidden = false;
    }).finally(() => { pending = undefined; });
  }
  // L'index et Fuse ne coûtent rien au premier affichage.
  if ('MutationObserver' in globalThis) new MutationObserver(() => { if (dialog.open) ensure(); }).observe(dialog, { attributes: true, attributeFilter: ['open'] });
  input.addEventListener('input', event => {
    if (event.isComposing) return;
    clearTimeout(timer);
    timer = setTimeout(show, 90);
  });
  input.addEventListener('compositionend', show);
  scope.addEventListener('change', show);
  retry.addEventListener('click', ensure);
  form.addEventListener('submit', event => {
    event.preventDefault();
    show();
    results.querySelector('a')?.focus();
  });
  input.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown' && results.querySelector('a')) {
      event.preventDefault();
      results.querySelector('a').focus();
    }
  });
  document.addEventListener('keydown', event => {
    if (!event.isComposing && !event.altKey && !event.repeat && (event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      if (dialog.open) { event.preventDefault(); input.focus(); }
      else if (driver.open(document.activeElement)) event.preventDefault();
    }
  });
}
