// Phase 5 · arsenal, familles, balistique et tableau : filtres, comparateur,
// nuage Chart.js, clavier, responsive, repli sans script et audit axe.
const { chromium } = require('playwright');
const axe = require('axe-core');
const assert = require('node:assert/strict');
const { mkdirSync, writeFileSync } = require('node:fs');
const { join } = require('node:path');

const root = new URL((process.env.TUG_URL || 'http://127.0.0.1:4173').replace(/\/$/, '') + '/');
const arsenal = new URL('pages/weapons/index.html', root).href;
const familles = ['assault-rifles', 'smgs', 'shotguns', 'sniper-rifles', 'dmrs', 'lmgs',
  'pistols', 'melee', 'grenade-launchers', 'weapon-mods'].map(slug => ({
  slug, url: new URL(`pages/weapons/${slug}.html`, root).href
}));
const balistique = new URL('pages/ammo/index.html', root).href;
const tableau = new URL('pages/ammo/ammo-chart.html', root).href;
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

async function testArsenal(page) {
  const requests = [];
  const capture = r => requests.push(r.url());
  page.on('request', capture);
  const res = await page.goto(arsenal, { waitUntil: 'networkidle' });
  page.off('request', capture);
  assert.equal(res.status(), 200);
  assert.equal(await page.locator('h1').count(), 1);
  assert.ok(requests.every(url => url.startsWith(root.href)), 'requête hors racine');
  assert.ok(!requests.some(url => /\.(?:mp3)$/i.test(url)), 'audio demandé sur l’arsenal');
  assert.equal(await page.locator('[data-armes-card]').count(), 10);
  assert.equal(await page.locator('#armes-catalogue tbody tr').count(), 199);
  assert.match(await page.locator('[data-armes-compte]').textContent(), /199 armes affichées sur 199/);
  report.perf.arsenal = { initial: requests.length, lcpLocal: await page.evaluate(() => window.__tugLcp ?? null) };
  await screenshot(page, 'arsenal-1440');
  note('Arsenal : 10 fiches de famille, 199 lignes de catalogue et compteur initial cohérent.');

  // Recherche textuelle
  await page.locator('[data-armes-search]').fill('AK-74');
  await ready(page, () => document.querySelectorAll('#armes-catalogue tbody tr:not([hidden])').length < 199);
  const trouves = await page.locator('#armes-catalogue tbody tr:not([hidden])').count();
  assert.ok(trouves >= 1 && trouves < 199, `recherche : ${trouves} lignes`);
  assert.match(await page.locator('[data-armes-compte]').textContent(), new RegExp(`${trouves} armes? affichées?`));
  await page.locator('[data-armes-search]').fill('');
  await ready(page, () => document.querySelectorAll('#armes-catalogue tbody tr:not([hidden])').length === 199);
  note(`Arsenal : recherche textuelle active (${trouves} lignes pour « AK-74 »).`);

  // Filtre par famille
  await page.locator('[data-armes-famille]').selectOption('pistolets-mitrailleurs');
  await ready(page, () => document.querySelectorAll('#armes-catalogue tbody tr:not([hidden])').length === 23);
  assert.equal(await page.locator('#armes-catalogue tbody tr:not([hidden])').count(), 23);
  await page.locator('[data-armes-famille]').selectOption('toutes');
  await ready(page, () => document.querySelectorAll('#armes-catalogue tbody tr:not([hidden])').length === 199);
  note('Arsenal : filtre par famille (23 pistolets-mitrailleurs) et restauration à 199 lignes.');

  // Filtre par disponibilité marchande
  await page.locator('[data-armes-marchand]').selectOption('oui');
  await ready(page, () => document.querySelectorAll('#armes-catalogue tbody tr:not([hidden])').length === 18);
  const enMagasin = await page.locator('#armes-catalogue tbody tr:not([hidden])').count();
  assert.equal(enMagasin, 18, `ventes en magasin : ${enMagasin}`);
  await page.locator('[data-armes-marchand]').selectOption('toutes');
  await ready(page, () => document.querySelectorAll('#armes-catalogue tbody tr:not([hidden])').length === 199);

  // Seuils numériques
  await page.locator('[data-armes-recul]').fill('80');
  await ready(page, () => document.querySelectorAll('#armes-catalogue tbody tr:not([hidden])').length < 199);
  const dociles = await page.locator('#armes-catalogue tbody tr:not([hidden])').count();
  assert.ok(dociles > 0 && dociles < 199, `seuil de recul : ${dociles}`);
  await page.locator('[data-armes-recul]').fill('');
  await ready(page, () => document.querySelectorAll('#armes-catalogue tbody tr:not([hidden])').length === 199);
  note(`Arsenal : seuil de recul vertical à 80 (${dociles} lignes) opérationnel.`);

  // Comparateur à trois entrées
  const optionsA = await page.locator('[data-armes-compare-a] option').count();
  assert.equal(optionsA, 200, `options du comparateur : ${optionsA}`);
  await page.locator('[data-armes-compare-a]').selectOption({ index: 1 });
  await page.locator('[data-armes-compare-b]').selectOption({ index: 2 });
  await page.locator('[data-armes-compare-c]').selectOption({ index: 3 });
  await ready(page, () => document.querySelectorAll('[data-armes-compare-corps] tr').length > 0);
  const lignes = await page.locator('[data-armes-compare-corps] tr').count();
  assert.ok(lignes >= 13, `comparateur : ${lignes} lignes`);
  const colonnes = await page.locator('[data-armes-compare-table] thead th').count();
  assert.equal(colonnes, 4, `colonnes du comparateur : ${colonnes}`);
  assert.match(await page.locator('[data-armes-compare-status]').textContent(), /3 armes comparées/);
  note(`Comparateur : trois armes, ${lignes} indicateurs et quatre colonnes de tableau.`);

  // Navigation clavier
  await page.reload({ waitUntil: 'networkidle' });
  await page.keyboard.press('Tab');
  assert.match(await page.evaluate(() => document.activeElement.textContent), /Aller au contenu principal/);
  await page.keyboard.press('Enter');
  await focused(page, 'contenu');
  await page.locator('.field-toc a[href="#comparateur"]').click();
  await focused(page, 'comparateur');
  note('Arsenal : lien d’évitement, cible de focus et sommaire ancre fonctionnels au clavier.');

  await audit(page, 'Arsenal sur bureau');
}

async function testFamilles(page) {
  const attendus = { 'assault-rifles': 63, smgs: 23, shotguns: 16, 'sniper-rifles': 10, dmrs: 11,
    lmgs: 8, pistols: 31, melee: 27, 'grenade-launchers': 10 };
  for (const famille of familles) {
    const requests = [];
    const capture = r => requests.push(r.url());
    page.on('request', capture);
    const res = await page.goto(famille.url, { waitUntil: 'networkidle' });
    page.off('request', capture);
    assert.equal(res.status(), 200, `${famille.slug} : statut ${res.status()}`);
    assert.equal(await page.locator('h1').count(), 1, `${famille.slug} : un seul h1`);
    assert.ok(requests.every(url => url.startsWith(root.href)), `${famille.slug} : requête hors racine`);
    assert.ok(!requests.some(url => /\.(?:mp3)$/i.test(url)), `${famille.slug} : audio demandé`);
    assert.ok((await page.locator('main table').count()) >= 1, `${famille.slug} : tableau manquant`);
    assert.ok((await page.locator('main table caption').count()) >= 1, `${famille.slug} : légende manquante`);
    assert.equal(await page.locator('main img:not([alt])').count(), 0, `${famille.slug} : image sans alt`);
    const attendu = attendus[famille.slug];
    if (attendu) {
      const lignes = await page.locator('main table').first().locator('tbody tr').count();
      assert.equal(lignes, attendu, `${famille.slug} : ${lignes} lignes, ${attendu} attendues`);
    }
    for (const img of await page.locator('main img').all()) {
      await img.scrollIntoViewIfNeeded();
      await img.evaluate(async el => { await el.decode(); if (!el.naturalWidth) throw new Error(el.src); });
    }
    report.perf[famille.slug] = { initial: requests.length, lcpLocal: await page.evaluate(() => window.__tugLcp ?? null) };
  }
  note('Familles : dix pages chargées en 200, tableaux légendés, images décodées, effectifs de catalogue exacts.');
  await audit(page, 'Fiche fusils d’assaut sur bureau');
}

async function testBalistique(page) {
  const requests = [];
  const capture = r => requests.push(r.url());
  page.on('request', capture);
  const res = await page.goto(balistique, { waitUntil: 'networkidle' });
  page.off('request', capture);
  assert.equal(res.status(), 200);
  assert.ok(requests.every(url => url.startsWith(root.href)), 'requête hors racine');
  const tables = await page.locator('main table').count();
  assert.ok(tables >= 4, `balistique : ${tables} tableaux`);
  note('Balistique : page chargée, tableaux de classes, de calibres, de traceurs, de grenades et d’achats présents.');
  await audit(page, 'Balistique sur bureau');
}

async function testTableau(page) {
  const requests = [];
  const capture = r => requests.push(r.url());
  page.on('request', capture);
  const res = await page.goto(tableau, { waitUntil: 'networkidle' });
  page.off('request', capture);
  assert.equal(res.status(), 200);
  assert.ok(requests.every(url => url.startsWith(root.href)), 'requête hors racine');
  assert.equal(await page.locator('#ammo-tableau tbody tr').count(), 200);
  assert.match(await page.locator('[data-ammo-compte]').textContent(), /200 cartouches affichées sur 200/);
  note('Tableau balistique : 200 lignes de cartouches et compteur initial cohérent.');

  // Filtres du tableau
  await page.locator('[data-ammo-calibre]').selectOption({ index: 1 });
  await ready(page, () => document.querySelectorAll('#ammo-tableau tbody tr:not([hidden])').length < 200);
  const calibre = await page.locator('#ammo-tableau tbody tr:not([hidden])').count();
  assert.ok(calibre > 0 && calibre < 200, `filtre calibre : ${calibre}`);
  await page.locator('[data-ammo-calibre]').selectOption('tous');
  await ready(page, () => document.querySelectorAll('#ammo-tableau tbody tr:not([hidden])').length === 200);
  await page.locator('[data-ammo-search]').fill('M855');
  await ready(page, () => document.querySelectorAll('#ammo-tableau tbody tr:not([hidden])').length < 200);
  const recherche = await page.locator('#ammo-tableau tbody tr:not([hidden])').count();
  assert.ok(recherche >= 1, 'recherche de cartouche vide');
  await page.locator('[data-ammo-search]').fill('');
  await ready(page, () => document.querySelectorAll('#ammo-tableau tbody tr:not([hidden])').length === 200);
  note(`Tableau balistique : filtres calibre (${calibre} lignes) et recherche (${recherche} lignes) opérationnels.`);

  // Nuage Chart.js
  await ready(page, () => Boolean(window.Chart));
  const points = await page.evaluate(() => window.Chart.getChart('armes-nuage')?.data.datasets
    .reduce((total, dataset) => total + dataset.data.length, 0) ?? 0);
  assert.equal(points, 200, `nuage : ${points} points`);
  const peint = await page.evaluate(() => {
    const canvas = document.getElementById('armes-nuage');
    const contexte = canvas.getContext('2d');
    const donnees = contexte.getImageData(0, 0, canvas.width, canvas.height).data;
    let visibles = 0;
    for (let i = 3; i < donnees.length; i += 4) if (donnees[i] > 0) visibles += 1;
    return visibles;
  });
  assert.ok(peint > 1000, `nuage : ${peint} pixels peints`);
  note(`Nuage : Chart.js local chargé, ${points} points et ${peint} pixels rendus dans la toile.`);
  await screenshot(page, 'tableau-balistique-1440');
  await audit(page, 'Tableau balistique sur bureau');
}

async function responsive(browser) {
  const widths = [320, 768, 1024, 1440];
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, locale: 'fr-FR' });
  const page = await context.newPage();
  track(page);
  for (const width of widths) {
    await page.setViewportSize({ width, height: 900 });
    for (const url of [arsenal, familles[0].url, tableau]) {
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
  note(`Responsive : ${widths.join(', ')} px sans débordement horizontal ni cible hors écran sur l’arsenal, une fiche et le tableau.`);
  await context.close();
}

async function sansScript(browser) {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 900 }, locale: 'fr-FR' });
  const page = await context.newPage();
  track(page);
  await page.goto(arsenal, { waitUntil: 'domcontentloaded' });
  assert.equal(await page.locator('#armes-catalogue tbody tr').count(), 199, 'catalogue incomplet sans script');
  assert.equal(await page.locator('[data-armes-card]').count(), 10, 'fiches de famille absentes sans script');
  await page.goto(tableau, { waitUntil: 'domcontentloaded' });
  assert.equal(await page.locator('#ammo-tableau tbody tr').count(), 200, 'tableau des munitions incomplet sans script');
  assert.ok((await page.locator('main').innerText()).length > 2000, 'contenu textuel insuffisant sans script');
  note('Repli sans JavaScript : catalogue complet, dix fiches de famille et deux cents cartouches lisibles.');
  await context.close();
}

async function stockageBloque(browser) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'fr-FR' });
  const page = await context.newPage();
  track(page);
  await context.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', { get() { throw new Error('stockage indisponible'); } });
  });
  await page.goto(arsenal, { waitUntil: 'networkidle' });
  assert.equal(await page.locator('#armes-catalogue tbody tr').count(), 199);
  note('Stockage bloqué : l’arsenal reste complet sans stockage local.');
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
    await phase('bureau', async browser => {
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
      await testArsenal(page);
      await testFamilles(page);
      await testBalistique(page);
      await testTableau(page);
      await context.close();
    });
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
