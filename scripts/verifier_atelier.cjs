// Contrôles reproductibles : Playwright, axe-core et un serveur de prévisualisation lancé.
const { chromium } = require('playwright');
const axe = require('axe-core');
const assert = require('node:assert/strict');
const { writeFileSync } = require('node:fs');

const origin = (process.env.TUG_URL || 'http://127.0.0.1:4173').replace(/\/$/, '');
const workshop = `${origin}/atelier/`;
const timeout = 6000;
const checked = [];
const report = { statut: 'ECHEC', rubriques: checked, wcag: [], largeursPx: [], console: [], medias: {} };

async function condition(page, predicate, value) {
  await page.waitForFunction(predicate, value, { timeout });
}

async function audit(page, scope) {
  if (!(await page.evaluate(() => Boolean(window.axe)))) await page.evaluate(axe.source);
  const { violations, incomplete, passes } = await page.evaluate(async () => {
    const data = await axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}});
    const slim = findings => findings.map(x => ({id:x.id,noeuds:x.nodes.length}));
    return {violations:slim(data.violations),incomplete:slim(data.incomplete),passes: data.passes.length};
  });
  report.wcag.push({ scope, violations, controleHumain: incomplete, reglesReussies: passes });
  assert.equal(violations.length, 0, JSON.stringify(violations));
}

async function run() {
  let options = {headless:true};
  if (process.env.TUG_CHROMIUM === 'sparticuz') {
    const sp = require('@sparticuz/chromium');
    options = { ...options, executablePath: await sp.executablePath(),
      args: sp.args.filter(flag => !['--disable-web-security','--allow-running-insecure-content','--single-process'].includes(flag)) };
  } else if (process.env.TUG_CHROMIUM) options.executablePath = process.env.TUG_CHROMIUM;
  const browser = await chromium.launch(options);
  report.chromium = browser.version();
  try {
    const context = await browser.newContext({viewport:{width:1440,height:900},reducedMotion:'reduce',locale:'fr-FR'});
    const page = await context.newPage();
    page.setDefaultTimeout(timeout);
    const responseErrors = [], nonlocal = [], allMedia = [];
    page.on('pageerror', error => report.console.push(error.message));
    page.on('console', message => { if (message.type()==='error') report.console.push(message.text()); });
    page.on('response', res => { if (res.status() >= 400) responseErrors.push([res.status(), res.url()]); });
    page.on('request', req => {
      if (!req.url().startsWith(origin+'/')) nonlocal.push(req.url());
      if (/\.mp3$/.test(req.url())) allMedia.push(req.url().split('/').at(-1));
    });
    const entry = await page.goto(workshop, {waitUntil:'networkidle'});
    assert.equal(entry.status(), 200);
    assert.equal(new URL(page.url()).pathname, new URL(workshop).pathname);
    assert.equal(await page.locator('h1').innerText(), 'Atelier\ndes fondations.');
    assert.equal(await page.locator('meta[name=robots]').getAttribute('content'), 'noindex, follow');
    assert.equal(allMedia.length, 0);
    assert.equal(await page.locator('audio').getAttribute('src'), null);
    assert.ok(await page.locator('#vue-ensemble [data-hero-motion]').getAttribute('data-motion-active') === 'false');
    checked.push('Atelier hors indexation à sa propre URL, aucun média chargé d’office, mouvement réduit appliqué.');

    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.textContent.trim()), 'Aller au contenu principal');
    await page.keyboard.press('Enter');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'contenu');
    checked.push('Lien d’évitement utilisable au clavier et focus placé sur le contenu principal.');

    const search = page.getByRole('button',{name:'Rechercher Ctrl K dans le guide'});
    await search.focus();
    await page.keyboard.press('Control+K');
    const s = page.locator('#search-query');
    const sd = page.locator('#search-dialog');
    await condition(page, () => document.activeElement?.id === 'search-query');
    await condition(page, () => document.querySelector('[data-search-status]').textContent.includes('Suggestions'));
    await s.fill('munitons');
    await condition(page, () => document.querySelector('[data-search-results] li:first-child')?.textContent.includes('Munitions'));
    assert.equal(await sd.locator('[data-search-results] li').first().locator('a').count(), 0);
    await s.fill('quetes');
    await condition(page, () => document.querySelector('[data-search-results] li:first-child')?.textContent.toLowerCase().includes('quêtes'));
    await s.fill('zzqqzz');
    await condition(page, () => document.querySelector('[data-search-status]').textContent.includes('Aucun résultat'));
    await page.keyboard.press('Escape');
    await sd.waitFor({state:'hidden'});
    await condition(page, () => document.activeElement?.dataset.dialogOpen === 'search-dialog');
    await search.click();
    await s.fill('comparateur');
    await page.locator('#search-scope').selectOption('atelier');
    const hit = sd.getByRole('link', {name:/Comparateur de cartes/});
    await hit.waitFor();
    await audit(page, 'dialogue de recherche');
    await s.focus();
    await page.keyboard.press('ArrowDown');
    assert.match(await page.evaluate(() => document.activeElement.textContent), /Comparateur/);
    await page.keyboard.press('Enter');
    await sd.waitFor({state:'hidden'});
    assert.equal(new URL(page.url()).hash, '#comparateur');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'comparateur');
    checked.push('Ctrl+K, faute « munitons », requête sans accent, zéro résultat, portée, lien réel, Échap et restitution du focus.');

    const modeButton = page.getByRole('button',{name:/Lire la méthode/});
    await modeButton.click();
    const close = page.getByRole('button',{name:'Fermer la méthode'});
    await condition(page, () => document.activeElement.getAttribute('aria-label')==='Fermer la méthode');
    await page.keyboard.press('Tab');
    assert.equal(await close.evaluate(button => button === document.activeElement), true);
    await close.click();
    await page.locator('#method-dialog').waitFor({state:'hidden'});
    await condition(page, () => document.activeElement?.dataset.dialogOpen === 'method-dialog');
    checked.push('Modale secondaire : focus initial, confinement et restitution.');

    const tabs = page.getByRole('tablist',{name:'Mode de jeu'});
    await tabs.getByRole('tab',{name:'PvP Zone'}).focus();
    await page.keyboard.press('ArrowRight');
    assert.equal(await tabs.getByRole('tab',{name:'PvE Zone'}).getAttribute('aria-selected'), 'true');
    assert.equal(await page.getByRole('tabpanel').count(), 1);
    await page.keyboard.press('End');
    assert.match(await page.getByRole('tabpanel').innerText(), /0\.16\.9\.5\.40743/);
    await page.keyboard.press('Home');
    assert.equal(await tabs.getByRole('tab',{name:'PvP Zone'}).getAttribute('aria-selected'), 'true');
    checked.push('Onglets : flèches, Home, End, un panneau actif.');

    const tooltip = page.locator('#tip-extract');
    const help = page.getByRole('button',{name:'Précision sur les entrées d’extract'});
    await help.focus();
    await tooltip.waitFor();
    await page.keyboard.press('Escape');
    await tooltip.waitFor({state:'hidden'});
    await help.hover();
    await tooltip.waitFor();
    const pt = await tooltip.boundingBox();
    await page.mouse.move(pt.x + pt.width - 12, pt.y + 5);
    assert.ok(await tooltip.isVisible());
    await page.keyboard.press('Escape');
    await tooltip.waitFor({state:'hidden'});
    checked.push('Infobulle : focus, survol de la bulle elle-même et fermeture Échap.');

    await page.locator('#filtres select[name=profil]').selectOption('pve');
    assert.equal(await page.locator('#filtres li:visible').count(), 2);
    await page.locator('#filtres select[name=type]').selectOption('scenario');
    assert.equal(await page.locator('#filtres li:visible').count(), 0);
    assert.ok(await page.locator('[data-filter-empty]').isVisible());
    assert.equal(new URL(page.url()).searchParams.get('profil'), 'pve');
    await page.reload({waitUntil:'load'});
    assert.equal(await page.locator('#filtres li:visible').count(), 0);
    await page.getByRole('button',{name:'Effacer les filtres'}).click();
    assert.equal(await page.locator('#filtres li:visible').count(), 6);
    checked.push('Filtres combinés : mode, type, liste vide, restauration après rechargement, remise à zéro.');

    await page.locator('[name=carteC]').selectOption('icebreaker');
    assert.equal(await page.locator('#comparateur thead th').count(), 4);
    assert.match(await page.locator('#comparateur tbody').innerText(), /50 min/);
    await page.locator('[name=comparaison]').selectOption('pvp-season');
    assert.match(await page.locator('[data-compare-status]').innerText(), /3 lieux sélectionnés · Seasonal/);
    assert.ok(await page.locator('[name=carteA] option[value=factory]').evaluate(el => el.disabled));
    assert.ok(await page.locator('#comparateur td.data-table__diff').count() > 0);
    await page.getByRole('button',{name:'Réinitialiser',exact:true}).click();
    assert.equal(await page.locator('#comparateur thead th').count(), 3);
    await page.locator('[name=rang]').selectOption('S');
    assert.equal(await page.locator('.tier-list__item:visible').count(), 2);
    await page.locator('[name=rang]').selectOption('');
    const accordion = page.getByText('Pourquoi trois instantanés ?', {exact:true});
    await accordion.focus();
    await page.keyboard.press('Space');
    assert.ok(await accordion.evaluate(node => node.parentElement.open));
    checked.push('Comparateur à 2 et 3 cartes, profil, doublons neutralisés, remise à zéro, filtre de tier list et accordéon clavier.');
    await audit(page, 'atelier, état de base');

    const play = page.locator('[data-audio-toggle]');
    const audio = page.locator('audio[data-audio-element]');
    const player = page.locator('[data-audio-player]');
    await page.getByRole('button',{name:/Forêt nocturne/}).click();
    assert.equal(allMedia.length, 0);
    assert.equal(await audio.getAttribute('src'), null);
    await play.focus(); await page.keyboard.press('Enter');
    await condition(page, () => !document.querySelector('audio').paused && document.querySelector('audio').currentTime > .1);
    assert.equal(await player.getAttribute('data-audio-state'), 'playing');
    assert.ok(await audio.evaluate(el=>el.loop && el.duration>59 && el.duration<61));
    await audio.evaluate(el=>{ el.currentTime=el.duration-.16; });
    await condition(page, () => {
      const audio = document.querySelector('audio');
      return !audio.seeking && !audio.paused && audio.currentTime < 1;
    });
    for (const [button, label] of [[/Ruines urbaines/,'Ruines urbaines'],[/Pluie sur tôle/,'Pluie sur tôle'],[/Bunker industriel/,'Bunker industriel']]) {
      await page.getByRole('button',{name:button}).click();
      await condition(page, name => document.querySelector('[data-audio-status]').textContent===`En lecture · ${name}`, label);
    }
    assert.ok(allMedia.includes('ambient_rain.mp3') && allMedia.includes('ambient_urban.mp3'));
    await condition(page, () => document.querySelector('[data-audio-status]').textContent==='En lecture · Bunker industriel');
    await page.locator('[data-audio-volume]').focus();
    await page.keyboard.press('End');
    assert.equal(await audio.evaluate(el=>el.volume), 1);
    await page.keyboard.press('Home');
    assert.equal(await audio.evaluate(el=>el.volume), 0);
    await play.click();
    assert.equal(await player.getAttribute('data-audio-state'), 'paused');
    assert.ok(await audio.evaluate(el=>el.paused));
    for (const [href, button] of [['hover','Effleurement'],['click','Clic métallique'],['notification','Signal radio']]) {
      const response = page.waitForResponse(res => res.url().endsWith(`/ui_${href}.mp3`) && res.ok());
      await page.getByRole('button',{name:button,exact:true}).click();
      await response;
      await condition(page, () => [...window.Howler._howls].some(h => h.state()==='loaded'));
    }
    assert.equal(await page.locator('[data-audio-sample-status]').textContent(),'Échantillon : Signal radio.');
    const before = allMedia.length;
    await page.reload({waitUntil:'networkidle'});
    assert.equal(allMedia.length, before);
    assert.equal(await page.locator('[data-audio-track]').innerText(),'Bunker industriel');
    assert.equal(await audio.evaluate(el=>el.volume), 0);
    assert.ok(await audio.evaluate(el=>el.paused && !el.getAttribute('src')));
    report.medias = { requetesObservees:[...new Set(allMedia)].sort(), autoplay:false };
    checked.push('Piste à l’arrêt sans requête, lecture clavier, boucle observée, quatre pistes, volume extrêmes, pause, trois sons UI et rechargement silencieux.');

    const contrast = page.getByRole('button',{name:'Contraste renforcé'});
    await contrast.click();
    assert.equal(await contrast.getAttribute('aria-pressed'), 'true');
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'contrast');
    await audit(page, 'contraste renforcé');
    await contrast.click();
    await page.emulateMedia({reducedMotion:'no-preference'});
    await page.evaluate(() => scrollTo({top:0,behavior:'instant'}));
    await condition(page, () => document.querySelector('[data-hero-motion]').dataset.motionActive==='true');
    const reduce = page.getByRole('button',{name:'Réduire les animations'});
    await reduce.focus(); await page.keyboard.press('Enter');
    assert.equal(await page.locator('html').getAttribute('data-motion'), 'off');
    assert.equal(await page.locator('[data-hero-motion]').getAttribute('data-motion-active'), 'false');
    checked.push('Thème à contraste renforcé, animation effective et arrêt par préférence.');

    for (const w of [320, 390, 768, 1024, 1440]) {
      await page.setViewportSize({width:w,height:850});
      const dimensions = await page.evaluate(() => ({viewport: document.documentElement.clientWidth, contenu: document.documentElement.scrollWidth}));
      assert.equal(dimensions.contenu, dimensions.viewport, `Débordement à ${w} px`);
      report.largeursPx.push(w);
    }
    const devices = await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true,reducedMotion:'reduce'});
    const mobile = await devices.newPage();
    await mobile.goto(workshop);
    const menu = mobile.locator('[data-mobile-menu]');
    await menu.getByText('Menu',{exact:true}).tap();
    assert.equal(await menu.evaluate(el=>el.open), true);
    await menu.getByRole('link',{name:'Modes de jeu'}).tap();
    assert.equal(await menu.evaluate(el=>el.open), false);
    assert.equal(new URL(mobile.url()).hash, '#modes');
    await audit(mobile, 'atelier tactile à 390 px');
    await devices.close();
    checked.push('Mobile tactile : menu interactif, retour à la section choisie, 320–1440 px sans débordement de page.');

    const nojs = await browser.newContext({ javaScriptEnabled:false, viewport:{width:390,height:844} });
    const text = await nojs.newPage();
    await text.goto(workshop);
    assert.equal(await text.locator('.tabs__panel:visible').count(), 5);
    assert.equal(await text.locator('#comparateur tbody tr').count(), 3);
    assert.equal(await text.locator('#filtres li:visible').count(), 6);
    assert.ok(await text.locator('#ambiances noscript a').isVisible());
    await nojs.close();
    checked.push('Sans JavaScript : 5 modes, catalogue, tableau de base, navigation native et lien MP3 restent disponibles.');
    assert.deepEqual(nonlocal, []);
    assert.deepEqual(responseErrors, []);
    assert.deepEqual(report.console, []);
    report.statut = 'OK';
  } finally {
    await browser.close();
  }
}

run().catch(error => { report.erreur = error.message; console.error(error.stack); process.exitCode=1; }).finally(() => {
  const output = JSON.stringify(report, null, 2) + '\n';
  if (process.env.TUG_TEST_REPORT) writeFileSync(process.env.TUG_TEST_REPORT, output);
  process.stdout.write(output);
});
