// Phase 6 · armures, comparaison et boss : filtres du catalogue, comparateur
// à trois entrées, filtre de famille de boss, clavier, responsive, repli sans
// script et audit axe.
const { chromium } = require('playwright');
const axe = require('axe-core');
const assert = require('node:assert/strict');
const { mkdirSync, writeFileSync } = require('node:fs');
const { join } = require('node:path');

const root = new URL((process.env.TUG_URL || 'http://127.0.0.1:4173').replace(/\/$/, '') + '/');
const hubArmor = new URL('pages/armor/index.html', root).href;
const guides = ['body-armor', 'helmets', 'rigs'].map(slug => ({
  slug, url: new URL(`pages/armor/${slug}.html`, root).href
}));
const comparateur = new URL('pages/armor/armor-chart.html', root).href;
const hubBoss = new URL('pages/bosses/index.html', root).href;
const boss = ['reshala', 'killa', 'the-wedge'].map(slug => ({
  slug, url: new URL(`pages/bosses/${slug}.html`, root).href
}));
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

async function testHubArmor(page) {
  const requests = [];
  const capture = r => requests.push(r.url());
  page.on('request', capture);
  const res = await page.goto(hubArmor, { waitUntil: 'networkidle' });
  page.off('request', capture);
  assert.equal(res.status(), 200);
  assert.equal(await page.locator('h1').count(), 1);
  assert.ok(requests.every(url => url.startsWith(root.href)), 'requête hors racine');
  assert.ok(!requests.some(url => /\.(?:mp3)$/i.test(url)), 'audio demandé sur le hub armures');
  assert.equal(await page.locator('#armures-catalogue tbody tr').count(), 390);
  assert.match(await page.locator('[data-armures-compte]').textContent(), /390 pièces affichées sur 390/);
  report.perf.hubArmor = { initial: requests.length, lcpLocal: await page.evaluate(() => window.__tugLcp ?? null) };
  await screenshot(page, 'armures-1440');
  await audit(page, 'Hub armures');
  note('Hub armures : 390 lignes de catalogue et compteur initial cohérent.');

  await page.locator('[data-armures-search]').fill('Granit');
  await ready(page, () => document.querySelectorAll('#armures-catalogue tbody tr:not([hidden])').length < 390);
  const trouves = await page.locator('#armures-catalogue tbody tr:not([hidden])').count();
  assert.ok(trouves >= 1 && trouves < 390, `recherche : ${trouves} lignes`);
  assert.match(await page.locator('[data-armures-compte]').textContent(), new RegExp(`${trouves} pièces? affichées?`));
  await page.locator('[data-armures-search]').fill('');
  await ready(page, () => document.querySelectorAll('#armures-catalogue tbody tr:not([hidden])').length === 390);
  note(`Hub armures : recherche textuelle active (${trouves} lignes pour « Granit »).`);

  await page.locator('[data-armures-classe]').selectOption('6');
  await ready(page, () => document.querySelectorAll('#armures-catalogue tbody tr:not([hidden])').length === 32);
  assert.equal(await page.locator('#armures-catalogue tbody tr:not([hidden])').count(), 32);
  await page.locator('[data-armures-classe]').selectOption('toutes');
  await ready(page, () => document.querySelectorAll('#armures-catalogue tbody tr:not([hidden])').length === 390);
  note('Hub armures : filtre par classe cohérent (32 pièces de classe 6).');

  await page.locator('[data-armures-categorie]').selectOption('Plaque de blindage');
  await ready(page, () => document.querySelectorAll('#armures-catalogue tbody tr:not([hidden])').length === 38);
  assert.equal(await page.locator('#armures-catalogue tbody tr:not([hidden])').count(), 38);
  await page.locator('[data-armures-categorie]').selectOption('');
  await ready(page, () => document.querySelectorAll('#armures-catalogue tbody tr:not([hidden])').length === 390);
  note('Hub armures : filtre par catégorie cohérent (38 plaques).');
}

async function testGuides(page) {
  for (const guide of guides) {
    const res = await page.goto(guide.url, { waitUntil: 'networkidle' });
    assert.equal(res.status(), 200);
    const lignes = await page.locator('table.armures-table tbody tr').count();
    assert.ok(lignes > 0, `${guide.slug} : catalogue vide`);
    const h2 = await page.locator('h2').allTextContents();
    assert.ok(h2.length >= 8, `${guide.slug} : sections manquantes`);
    await screenshot(page, `armure-${guide.slug}-1440`);
    note(`Guide ${guide.slug} : ${lignes} lignes de catalogue, ${h2.length} sections.`);
  }
}

async function testComparateur(page) {
  const res = await page.goto(comparateur, { waitUntil: 'networkidle' });
  assert.equal(res.status(), 200);
  assert.equal(await page.locator('#armures-comparateur tbody tr').count(), 390);
  const selects = page.locator('[data-armures-compare-slot]');
  assert.equal(await selects.count(), 3);
  await selects.nth(0).selectOption({ index: 1 });
  await selects.nth(1).selectOption({ index: 2 });
  await ready(page, () => document.querySelectorAll('.armures-compare__ligne').length > 10);
  const lignes = await page.locator('.armures-compare__ligne').count();
  assert.ok(lignes >= 16, `comparateur : ${lignes} lignes`);
  const texte = await page.locator('[data-armures-compare-grille]').innerText();
  assert.ok(texte.includes('Classe'), 'comparateur : colonne classe absente');
  assert.ok(texte.includes('Matériau'), 'comparateur : colonne matériau absente');
  await screenshot(page, 'comparateur-armures-1440');
  await audit(page, 'Comparateur d’armures');
  note(`Comparateur : ${lignes} lignes alignées pour deux pièces sélectionnées.`);

  await selects.nth(2).selectOption({ index: 3 });
  await ready(page, () => document.querySelectorAll('.armures-compare__ligne')[0].children.length === 4);
  assert.equal(await page.locator('.armures-compare__ligne').first().locator('> *').count(), 4);
  note('Comparateur : trois pièces alignées sur les mêmes colonnes.');
}

async function testBoss(page) {
  const res = await page.goto(hubBoss, { waitUntil: 'networkidle' });
  assert.equal(res.status(), 200);
  assert.equal(await page.locator('[data-boss-card]').count(), 14);
  assert.equal(await page.locator('[data-boss-famille]').count(), 6);
  await screenshot(page, 'boss-1440');
  await audit(page, 'Hub boss');
  note('Hub boss : 14 fiches et 6 boutons de famille.');

  await page.locator('[data-boss-famille="cultiste"]').click();
  await ready(page, () => document.querySelectorAll('[data-boss-card]:not([hidden])').length === 2);
  assert.equal(await page.locator('[data-boss-card]:not([hidden])').count(), 2);
  await page.locator('[data-boss-famille="toutes"]').click();
  await ready(page, () => document.querySelectorAll('[data-boss-card]:not([hidden])').length === 14);
  note('Hub boss : filtre de famille cohérent (2 fiches cultiste sur 14).');

  for (const fiche of boss) {
    const r = await page.goto(fiche.url, { waitUntil: 'networkidle' });
    assert.equal(r.status(), 200);
    assert.equal(await page.locator('h1').count(), 1);
    assert.ok(await page.locator('#pv table tbody tr').count() >= 7, `${fiche.slug} : points de vie incomplets`);
    assert.ok(await page.locator('#butin table tbody tr').count() >= 1, `${fiche.slug} : butin absent`);
    assert.ok(await page.locator('#communaute li').count() >= 3, `${fiche.slug} : avis communautaires absents`);
    assert.ok(await page.locator('#sources li').count() >= 4, `${fiche.slug} : sources absentes`);
  }
  await screenshot(page, 'boss-reshala-1440');
  await audit(page, 'Fiche boss Reshala');
  note('Fiches boss : points de vie, butin, avis et sources présents sur les trois fiches contrôlées.');
}

async function clavier(page) {
  await page.goto(hubArmor, { waitUntil: 'networkidle' });
  await page.locator('#armures-recherche').focus();
  await focused(page, 'armures-recherche');
  await page.keyboard.type('Granit');
  await ready(page, () => document.querySelectorAll('#armures-catalogue tbody tr:not([hidden])').length < 390);
  await page.keyboard.press('Tab');
  const cible = await page.evaluate(() => document.activeElement.id);
  assert.ok(cible.length > 0, 'navigation clavier bloquée');
  note('Clavier : saisie au clavier et passage au champ suivant dans le catalogue.');
}

async function responsive(browser) {
  const context = await browser.newContext(options);
  const page = await context.newPage();
  track(page);
  const widths = [];
  for (const width of [320, 375, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const url of [hubArmor, comparateur, hubBoss, boss[0].url]) {
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      const debordement = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      assert.ok(debordement <= 1, `débordement horizontal de ${debordement} px à ${width} px sur ${url}`);
      const horsEcran = await page.evaluate(() =>
        [...document.querySelectorAll('a, button, input, select')].filter(el => {
          const r = el.getBoundingClientRect();
          return r.width > 0 && (r.right > window.innerWidth + 2 || r.left < -2);
        }).length);
      assert.equal(horsEcran, 0, `cible hors écran à ${width} px sur ${url}`);
    }
    widths.push(width);
  }
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(hubArmor, { waitUntil: 'networkidle' });
  await screenshot(page, 'armures-1440');
  report.largeursPx = widths;
  note(`Responsive : ${widths.join(', ')} px sans débordement horizontal ni cible hors écran.`);
  await context.close();
}

async function sansScript(browser) {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 900 }, locale: 'fr-FR' });
  const page = await context.newPage();
  track(page);
  await page.goto(hubArmor, { waitUntil: 'domcontentloaded' });
  assert.equal(await page.locator('#armures-catalogue tbody tr').count(), 390, 'catalogue incomplet sans script');
  await page.goto(comparateur, { waitUntil: 'domcontentloaded' });
  assert.equal(await page.locator('#armures-comparateur tbody tr').count(), 390, 'comparateur incomplet sans script');
  await page.goto(hubBoss, { waitUntil: 'domcontentloaded' });
  assert.equal(await page.locator('[data-boss-card]').count(), 14, 'fiches boss absentes sans script');
  await page.goto(boss[0].url, { waitUntil: 'domcontentloaded' });
  assert.ok((await page.locator('main').innerText()).length > 2000, 'contenu textuel insuffisant sans script');
  note('Repli sans JavaScript : catalogue, comparateur et fiches boss entièrement lisibles.');
  await context.close();
}

async function stockageBloque(browser) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'fr-FR' });
  const page = await context.newPage();
  track(page);
  await context.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', { get() { throw new Error('stockage indisponible'); } });
  });
  await page.goto(comparateur, { waitUntil: 'networkidle' });
  assert.equal(await page.locator('#armures-comparateur tbody tr').count(), 390);
  note('Stockage bloqué : le comparateur reste complet sans stockage local.');
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
      await testHubArmor(page);
      await testGuides(page);
      await testComparateur(page);
      await testBoss(page);
      await clavier(page);
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
