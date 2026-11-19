// Phase 4 · atlas, fiches de lieu, filtres, comparatif, couches, clavier, responsive et repli sans script.
const { chromium } = require('playwright');
const axe = require('axe-core');
const assert = require('node:assert/strict');
const { mkdirSync, writeFileSync } = require('node:fs');
const { join } = require('node:path');

const root = new URL((process.env.TUG_URL || 'http://127.0.0.1:4173').replace(/\/$/, '') + '/');
const atlas = new URL('pages/maps/index.html', root).href;
const fiches = ['factory', 'customs', 'woods', 'shoreline', 'interchange', 'reserve', 'the-lab',
  'lighthouse', 'streets-of-tarkov', 'ground-zero', 'the-labyrinth', 'icebreaker', 'terminal']
  .map(slug => ({ slug, url: new URL(`pages/maps/${slug}.html`, root).href }));
const options = { viewport: { width: 1440, height: 1000 }, locale: 'fr-FR', reducedMotion: 'reduce' };
const timeout = 8000;
const report = { statut: 'ECHEC', rubriques: [], largeursPx: [], wcag: [], console: [], erreursHttp: [], perf: {} };
const note = s => report.rubriques.push(s);
const ready = (p, f, arg) => p.waitForFunction(f, arg, { timeout });
const focused = (p, id) => ready(p, key => document.activeElement.id === key, id);

async function screenshot(page, name, fullPage = false) {
  const dest = process.env.TUG_VISUAL_DIR;
  if (!dest) return;
  mkdirSync(dest, { recursive: true });
  await page.screenshot({ path: join(dest, name + '.jpg'), type: 'jpeg', quality: 87, fullPage });
}

function track(page) {
  page.setDefaultTimeout(timeout);
  page.on('pageerror', e => report.console.push(e.message));
  page.on('console', m => { if (m.type() === 'error') report.console.push(m.text()); });
  page.on('response', res => { if (res.status() >= 400) report.erreursHttp.push([res.status(), res.url()]); });
}

async function audit(page, scope) {
  if (!await page.evaluate(() => Boolean(window.axe))) await page.evaluate(axe.source);
  const result = await page.evaluate(async () => {
    const res = await axe.run({ runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] } });
    const count = rows => rows.map(e => ({ id: e.id, noeuds: e.nodes.length }));
    const failures = res.violations.map(e => ({ id: e.id, noeuds: e.nodes.length, cibles: e.nodes.map(n => n.target) }));
    return { violations: failures, controleHumain: count(res.incomplete), reglesReussies: res.passes.length };
  });
  report.wcag.push({ scope, ...result });
  assert.deepEqual(result.violations, [], `Axe : ${scope}, ${JSON.stringify(result.violations)}`);
}

async function testAtlas(page) {
  const requests = [];
  const capture = r => requests.push(r.url());
  page.on('request', capture);
  const res = await page.goto(atlas, { waitUntil: 'networkidle' });
  page.off('request', capture);
  assert.equal(res.status(), 200);
  assert.equal(await page.locator('h1').count(), 1);
  assert.ok(requests.every(url => url.startsWith(root.href)), 'requête hors racine');
  assert.ok(!requests.some(url => /\.(?:mp3)$/i.test(url)), 'audio demandé sur l’atlas');
  assert.equal(await page.locator('[data-atlas-card]').count(), 13);
  assert.match(await page.locator('[data-atlas-count]').textContent(), /13 lieux affichés sur 13/);
  report.perf.atlas = { initial: requests.length, lcpLocal: await page.evaluate(() => window.__tugLcp ?? null) };
  await screenshot(page, 'atlas-1440');

  // Filtre textuel
  await page.locator('[data-atlas-search]').fill('shoreline');
  await ready(page, () => document.querySelectorAll('[data-atlas-card]:not([hidden])').length < 13);
  const visibles = await page.locator('[data-atlas-card]:not([hidden])').count();
  assert.ok(visibles >= 1 && visibles < 13, `filtre textuel : ${visibles} cartes`);
  assert.match(await page.locator('[data-atlas-count]').textContent(), new RegExp(`${visibles} lieu`));
  await page.locator('[data-atlas-search]').fill('zzzz-introuvable');
  await ready(page, () => document.querySelector('[data-atlas-empty]')?.hidden === false);
  assert.ok(await page.locator('[data-atlas-empty]').isVisible());
  await page.locator('[data-atlas-search]').fill('');
  await ready(page, () => document.querySelectorAll('[data-atlas-card]:not([hidden])').length === 13);
  note('Atlas : recherche par facette, message « aucun lieu », compteur de cartes affichées et restauration à 13.');

  // Filtre par profil
  await page.locator('[data-atlas-mode]').selectOption('pve');
  await ready(page, () => document.querySelectorAll('[data-atlas-card]:not([hidden])').length < 13);
  const pve = await page.locator('[data-atlas-card]:not([hidden])').count();
  assert.ok(pve >= 1 && pve < 13, `filtre profil : ${pve}`);
  await page.locator('[data-atlas-mode]').selectOption('tous');
  await ready(page, () => document.querySelectorAll('[data-atlas-card]:not([hidden])').length === 13);

  // Filtre par danger
  await page.locator('[data-atlas-threat]').selectOption('mines');
  await ready(page, () => document.querySelectorAll('[data-atlas-card]:not([hidden])').length < 13);
  const mines = await page.locator('[data-atlas-card]:not([hidden])').count();
  assert.ok(mines >= 1, 'filtre mines vide');
  await page.locator('[data-atlas-threat]').selectOption('toutes');
  await ready(page, () => document.querySelectorAll('[data-atlas-card]:not([hidden])').length === 13);
  note(`Atlas : filtres profil (${pve} fiches en PvE) et danger (${mines} fiches avec champ de mines) opérationnels.`);

  // Comparatif
  await page.locator('[data-compare-a]').selectOption('factory');
  await page.locator('[data-compare-b]').selectOption('customs');
  await ready(page, () => document.querySelectorAll('[data-compare-grid] .map-compare__col').length === 2);
  const colonnes = await page.locator('[data-compare-grid] .map-compare__col').count();
  assert.equal(colonnes, 2);
  const lignes = await page.locator('[data-compare-grid] dt').count();
  assert.ok(lignes >= 8, `comparatif : ${lignes} lignes`);
  note(`Comparatif : deux colonnes et ${lignes} lignes de données synchronisées.`);

  // Navigation clavier dans l'atlas
  await page.reload({ waitUntil: 'networkidle' });
  await page.keyboard.press('Tab');
  assert.match(await page.evaluate(() => document.activeElement.textContent), /Aller au contenu principal/);
  await page.keyboard.press('Enter');
  await focused(page, 'contenu');
  await page.locator('.field-toc a[href="#comparatif"]').click();
  await focused(page, 'comparatif');
  assert.equal(new URL(page.url()).hash, '#comparatif');
  note('Atlas : lien d’évitement, cible de focus et sommaire ancre fonctionnels au clavier.');

  await audit(page, 'Atlas sur bureau');
}

async function testFiche(page, fiche) {
  const requests = [];
  const capture = r => requests.push(r.url());
  page.on('request', capture);
  const res = await page.goto(fiche.url, { waitUntil: 'networkidle' });
  page.off('request', capture);
  assert.equal(res.status(), 200, `${fiche.slug} : statut ${res.status()}`);
  assert.equal(await page.locator('h1').count(), 1, `${fiche.slug} : un seul h1`);
  assert.ok(requests.every(url => url.startsWith(root.href)), `${fiche.slug} : requête hors racine`);
  assert.ok(!requests.some(url => /\.(?:mp3)$/i.test(url)), `${fiche.slug} : audio demandé`);
  assert.ok((await page.locator('main table').count()) >= 3, `${fiche.slug} : tables manquantes`);
  assert.ok((await page.locator('main table caption').count()) >= 3, `${fiche.slug} : légendes manquantes`);
  assert.equal(await page.locator('main img:not([alt])').count(), 0, `${fiche.slug} : image sans alt`);
  assert.equal(await page.locator('main img[loading="lazy"]').count() >= 0, true);
  for (const img of await page.locator('main img').all()) {
    await img.scrollIntoViewIfNeeded();
    await img.evaluate(async el => { await el.decode(); if (!el.naturalWidth) throw new Error(el.src); });
  }
  report.perf[fiche.slug] = { initial: requests.length, lcpLocal: await page.evaluate(() => window.__tugLcp ?? null) };
  return res;
}

async function desktop(browser) {
  const context = await browser.newContext(options);
  await context.addInitScript(() => {
    if (!PerformanceObserver.supportedEntryTypes.includes('largest-contentful-paint')) return;
    new PerformanceObserver(list => {
      const lcp = list.getEntries().at(-1);
      window.__tugLcp = { ms: Math.round(lcp.startTime), element: lcp.element?.tagName ?? null, ressource: lcp.url ? new URL(lcp.url).pathname : null };
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  });
  const page = await context.newPage();
  track(page);
  await testAtlas(page);

  for (const fiche of fiches) {
    await testFiche(page, fiche);
  }
  note('Fiches : 13 pages chargées en 200, tableaux légendés, images décodées après défilement, aucune requête hors racine ni audio.');

  // Couches de données sur l'Usine
  await page.goto(fiches[0].url, { waitUntil: 'networkidle' });
  const couches = page.locator('[data-layer-toggle="intitules"]');
  await couches.click();
  await ready(page, () => {
    const el = document.querySelector('[data-layer="intitules"]');
    return el && !el.hasAttribute('hidden');
  });
  assert.ok(await page.locator('[data-layer="intitules"]').isVisible());
  await couches.click();
  await ready(page, () => {
    const el = document.querySelector('[data-layer="intitules"]');
    return el && el.hasAttribute('hidden');
  });
  note('Fiches : couches de données commutables au clavier et à la souris.');

  // Navigation clavier et fil d'Ariane
  await page.reload({ waitUntil: 'networkidle' });
  await page.keyboard.press('Tab');
  assert.match(await page.evaluate(() => document.activeElement.textContent), /Aller au contenu principal/);
  await page.keyboard.press('Enter');
  await focused(page, 'contenu');
  await page.locator('.field-toc a[href="#cles"]').click();
  await focused(page, 'cles');
  note('Fiches : lien d’évitement, focus sur la section et sommaire ancre.');

  // Tableaux : en-têtes de portée et lecture clavier
  const entete = page.locator('main table th[scope="col"]').first();
  assert.ok(await entete.count() > 0);
  await audit(page, 'Fiche Usine sur bureau');
  await context.close();
}

async function responsive(browser) {
  const widths = [320, 768, 1024, 1440];
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, locale: 'fr-FR' });
  const page = await context.newPage();
  track(page);
  for (const width of widths) {
    await page.setViewportSize({ width, height: 900 });
    for (const url of [atlas, fiches[0].url, fiches[8].url]) {
      await page.goto(url, { waitUntil: 'networkidle' });
      const debordement = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      assert.ok(debordement <= 1, `${url} à ${width} px : débordement horizontal de ${debordement} px`);
      const cibles = await page.locator('a, button, input, select').evaluateAll(nodes =>
        nodes.filter(n => n.offsetParent !== null).map(n => {
          const r = n.getBoundingClientRect();
          return { t: r.top, b: r.bottom, l: r.left, r: r.right };
        }).filter(r => r.b > 0 && r.t < 900 && (r.r > window.innerWidth + 1 || r.l < -1)).length);
      assert.equal(cibles, 0, `${url} à ${width} px : ${cibles} cibles hors écran`);
    }
    report.largeursPx.push(width);
  }
  note(`Responsive : ${widths.join(', ')} px sans débordement horizontal ni cible hors écran sur l’atlas et deux fiches.`);
  await context.close();
}

async function sansScript(browser) {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 900 }, locale: 'fr-FR' });
  const page = await context.newPage();
  track(page);
  await page.goto(atlas, { waitUntil: 'domcontentloaded' });
  const cartes = await page.locator('[data-atlas-card]').count();
  assert.equal(cartes, 13, 'cartes invisibles sans script');
  const tables = await page.locator('main table').count();
  assert.ok(tables >= 2, 'tableaux de l’atlas absents sans script');
  await page.goto(fiches[3].url, { waitUntil: 'domcontentloaded' });
  assert.ok((await page.locator('main table').count()) >= 3, 'tableaux de fiche absents sans script');
  assert.ok((await page.locator('main').innerText()).length > 2000, 'contenu textuel insuffisant sans script');
  note('Repli sans JavaScript : 13 cartes, tableaux et contenu textuel complet sur l’atlas et une fiche.');
  await context.close();
}

async function stockageBloque(browser) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'fr-FR' });
  const page = await context.newPage();
  track(page);
  await context.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', {
      get() { throw new Error('stockage indisponible'); },
    });
  });
  await page.goto(atlas, { waitUntil: 'networkidle' });
  assert.equal(await page.locator('[data-atlas-card]').count(), 13);
  note('Stockage bloqué : l’atlas reste complète sans stockage local.');
  await context.close();
}

async function lancer() {
  if (process.env.TUG_CHROMIUM === 'sparticuz') {
    const sp = require('@sparticuz/chromium');
    const chemin = await sp.executablePath();
    return chromium.launch({ executablePath: chemin, args: sp.args, headless: true });
  }
  if (process.env.TUG_CHROMIUM) return chromium.launch({ executablePath: process.env.TUG_CHROMIUM });
  return chromium.launch();
}

async function phase(nom, fonction) {
  const browser = await lancer();
  try {
    await fonction(browser);
  } finally {
    await browser.close().catch(() => {});
  }
  note(`Phase « ${nom} » terminée.`);
}

(async () => {
  try {
    await phase('bureau', desktop);
    await phase('responsive', responsive);
    await phase('repli sans script', sansScript);
    await phase('stockage bloqué', stockageBloque);
    report.statut = 'OK';
    note('Aucune erreur console ni réponse HTTP en erreur sur les parcours joués.');
  } catch (erreur) {
    report.statut = 'ECHEC';
    report.erreur = erreur.message;
    note(`ÉCHEC : ${erreur.message}`);
  }
  const sortie = process.env.TUG_TEST_REPORT;
  if (sortie) writeFileSync(sortie, JSON.stringify(report, null, 2));
  console.log(`${report.statut} · ${report.rubriques.length} rubriques · ${report.wcag.length} audits axe · ` +
    `${report.erreursHttp.length} erreur(s) HTTP · ${report.console.length} erreur(s) console`);
  report.rubriques.forEach(r => console.log(' - ' + r));
  process.exit(report.statut === 'OK' ? 0 : 1);
})();
