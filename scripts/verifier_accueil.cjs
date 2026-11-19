// Vérifications de la phase 2 : lancer scripts/servir.py puis ce scénario Playwright.
const { chromium } = require('playwright');
const axe = require('axe-core');
const assert = require('node:assert/strict');
const { mkdirSync, readFileSync, writeFileSync } = require('node:fs');
const { join } = require('node:path');

const root = new URL((process.env.TUG_URL || 'http://127.0.0.1:4173').replace(/\/$/, '') + '/');
const home = root.href;
const atelier = new URL('atelier/', root).href;
const timeout = 7000;
const book = JSON.parse(readFileSync(join(__dirname,'../docs/pages.json'),'utf8'));
const p3 = book.pages.filter(p=>p.phase==='PHASE_3' && p.etat==='PUBLIEE').length;
const p4 = book.pages.filter(p=>p.phase==='PHASE_4' && p.etat==='PUBLIEE').length;
const report = { statut:'ECHEC', rubriques:[], largeursPx:[], wcag:[], console:[], requetesInitiales:{}, medias:{} };
const notes = report.rubriques;
const shotDir = process.env.TUG_VISUAL_DIR;
const wait = (page, predicate, parameter) => page.waitForFunction(predicate, parameter, {timeout});
const active = (page, id) => wait(page, target => document.activeElement.id === target, id);
const open = (page, query, value) => wait(page, ({query,value}) => document.querySelector(query).open === value, {query,value});
const count = (page, query) => page.locator(query).count();

async function snapshot(page, filename, fullPage=false) {
  if (!shotDir) return;
  mkdirSync(shotDir,{recursive:true});
  await page.screenshot({path:join(shotDir, filename+'.jpg'),type:'jpeg',quality:87,fullPage});
}

async function audit(page, scope) {
  if (!await page.evaluate(() => Boolean(window.axe))) await page.evaluate(axe.source);
  const result = await page.evaluate(async () => {
    const a = await axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}});
    const narrow = rows => rows.map(e=>({id:e.id,noeuds:e.nodes.length}));
    return {violations:narrow(a.violations),controleHumain:narrow(a.incomplete),reglesReussies:a.passes.length};
  });
  report.wcag.push({scope,...result});
  assert.deepEqual(result.violations, [], `Violations axe · ${scope}: ${JSON.stringify(result.violations)}`);
}

async function run() {
  let options = {headless:true};
  if (process.env.TUG_CHROMIUM === 'sparticuz') {
    const sp = require('@sparticuz/chromium');
    options = {...options,executablePath:await sp.executablePath(),
      args:sp.args.filter(flag=>!['--disable-web-security','--allow-running-insecure-content','--single-process'].includes(flag))};
  } else if (process.env.TUG_CHROMIUM) options.executablePath = process.env.TUG_CHROMIUM;
  const browser = await chromium.launch(options);
  report.chromium = browser.version();
  try {
    const context = await browser.newContext({viewport:{width:1440,height:970},locale:'fr-FR',reducedMotion:'reduce'});
    await context.addInitScript(() => {
      if (!PerformanceObserver.supportedEntryTypes.includes('largest-contentful-paint')) return;
      new PerformanceObserver(list => {
        const e = list.getEntries().at(-1);
        window.__tugLcp = {ms:Math.round(e.startTime),element:e.element?.tagName || null,ressource:e.url ? new URL(e.url).pathname : null};
      }).observe({type:'largest-contentful-paint', buffered:true});
    });
    const page = await context.newPage();
    page.setDefaultTimeout(timeout);
    const requests = [], responseErrors = [];
    page.on('request', req=>requests.push(req.url()));
    page.on('response', res=>{if (res.status()>=400) responseErrors.push([res.status(),res.url()]);});
    page.on('pageerror', e=>report.console.push(e.message));
    page.on('console', m=>{if(m.type()==='error') report.console.push(m.text());});
    const media = () => requests.filter(path=>new URL(path).pathname.endsWith('.mp3'));
    const lazy = path => /(?:search-index\.json|fuse\.min\.mjs|howler\.core\.min\.js|tables\.mjs|maps-sample\.mjs)(?:\?|$)/.test(path);
    const response = await page.goto(home,{waitUntil:'networkidle'});
    assert.equal(response.status(),200);
    assert.equal(response.request().redirectedFrom(),null);
    assert.equal(page.url(), home);
    assert.equal(await page.title(),'Tarkov Ultimate Guide — Guide FR d’Escape from Tarkov');
    assert.match(await page.locator('h1').innerText(),/TARKOV\s+ULTIMATE GUIDE/);
    assert.equal(await page.locator('[data-count="published"]').textContent(),String(book.publiees).padStart(2,'0'));
    assert.equal(await page.locator('[data-count="planned"]').textContent(),'86');
    assert.equal(await page.locator('[data-count="items"]').textContent(),'5\u202f498');
    assert.equal(await page.locator('[data-count="modes"]').textContent(),'03');
    assert.equal(await page.locator('audio').getAttribute('src'),null);
    assert.deepEqual(media(),[]);
    assert.deepEqual(requests.filter(lazy),[]);
    assert.equal(await page.locator('[data-hero-motion]').getAttribute('data-motion-active'),'false');
    const heroImage = page.locator('.hero-home__image');
    await wait(page, () => { const i = document.querySelector('.hero-home__image'); return i.complete && i.naturalWidth === 1376; });
    assert.equal(await heroImage.getAttribute('fetchpriority'),'high');
    assert.equal(await count(page,'main img[loading="lazy"]'),7);
    report.requetesInitiales = {total:requests.length,mp3:media().length,rechercheOuOutils:requests.filter(lazy).length,externes:requests.filter(r=>!r.startsWith(home)).length};
    report.lcpLocal = await page.evaluate(() => window.__tugLcp ?? null);
    await snapshot(page,'accueil-phase2-1440');
    notes.push(`Accueil 200 sans redirection ; compteurs ${book.publiees}/86 · 5 498/3 ; hero JPG prioritaire et 7 images différées. Aucun MP3, index Fuse ou code atelier au premier affichage.`);
    await audit(page,'accueil bureau, état de base');

    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.textContent.trim()),'Aller au contenu principal');
    await page.keyboard.press('Enter');
    await active(page,'contenu');
    const menu = page.locator('.mega-nav');
    const menuSummary = menu.locator('summary');
    const summarySelector = '.mega-nav > summary';
    await menuSummary.focus();
    await page.keyboard.press('Enter');
    await open(page,'.mega-nav',true);
    assert.equal(await menu.locator('a:visible').count(),11+p3);
    await audit(page,'méga-menu ouvert');
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.textContent),'Brief de premier raid');
    await page.keyboard.press('Escape');
    await open(page,'.mega-nav',false);
    assert.ok(await menuSummary.evaluate(el=>el===document.activeElement));
    await page.keyboard.press('Space');
    await open(page,'.mega-nav',true);
    const modes = page.locator('.commandbar__nav-link[href="#modes"]');
    await modes.focus();
    await open(page,'.mega-nav',false);
    await menuSummary.click();
    await open(page,'.mega-nav',true);
    // Bord de la scène, hors du panneau et de tout lien.
    const beforeAside = page.url();
    await page.mouse.click(4, 150);
    await open(page,'.mega-nav',false);
    assert.equal(page.url(),beforeAside);
    await page.locator(summarySelector).click();
    await menu.getByRole('link',{name:'Cartes & extractions',exact:true}).click();
    await open(page,'.mega-nav',false);
    await open(page,'#dossier-cartes details',true);
    await active(page,'dossier-cartes');
    assert.equal(new URL(page.url()).hash,'#dossier-cartes');
    // La vignette publiée renvoie vers l'atlas des treize lieux.
    assert.equal(await page.locator('#dossier-cartes a[href="./pages/maps/index.html"]').count(),1);
    await page.locator('#dossier-cartes summary').click();
    await open(page,'#dossier-cartes details',false);
    notes.push('Évitement clavier, menu Tab/Échap, retour du focus, fermeture en sortant et accès aux aperçus sans lien absent.');

    const search = page.getByRole('button',{name:'Rechercher Ctrl K dans le guide'});
    const dialog = page.locator('#search-dialog');
    const input = page.locator('#search-query');
    const scope = page.locator('#search-scope');
    await search.focus();
    await page.keyboard.press('Control+K');
    await active(page,'search-query');
    await wait(page,()=>document.querySelector('[data-search-status]').textContent.includes('Suggestions'));
    assert.ok(requests.some(r=>r.endsWith('search-index.json')) && requests.some(r=>r.endsWith('fuse.min.mjs')));
    await input.fill('munitons');
    await wait(page,()=>document.querySelector('[data-search-results] li:first-child .search-hit__title')?.textContent.startsWith('Munitions'));
    assert.equal(await dialog.locator('[data-search-results] li').first().locator('a').count(),0);
    assert.match(await dialog.locator('[data-search-results] li').first().textContent(),/À venir/);
    await input.fill('quetes');
    await wait(page,()=>document.querySelector('[data-search-results] li:first-child .search-hit__title')?.textContent.toLowerCase().includes('quêtes'));
    await input.fill('zzxxzxzz');
    await wait(page,()=>document.querySelector('[data-search-status]').textContent.includes('Aucun résultat'));
    await page.keyboard.press('Escape');
    await open(page,'#search-dialog',false);
    await wait(page,()=>document.activeElement?.dataset.dialogOpen === 'search-dialog');
    await search.click();
    await scope.selectOption('accueil');
    await input.fill('premier raid');
    const guide = dialog.getByRole('link',{name:/Préparer son premier raid/});
    await guide.waitFor();
    await audit(page,'dialogue de recherche');
    await input.focus(); await page.keyboard.press('ArrowDown');
    assert.ok(await guide.evaluate(a=>a===document.activeElement));
    await page.keyboard.press('Enter');
    await open(page,'#search-dialog',false);
    await active(page,'premiers-pas');
    assert.equal(new URL(page.url()).hash,'#premiers-pas');
    notes.push('Recherche différée : Ctrl+K, faute, accents, résultat « À venir » sans href, portée accueil, zéro résultat, flèche et entrée, Échap et restitution.');

    const checks = page.getByRole('form',{name:'Checklist personnelle avant le raid'});
    const status = checks.getByRole('status');
    const first = checks.getByRole('checkbox',{name:/Choisir mon mode/});
    const second = checks.getByRole('checkbox',{name:/Repérer un extract/});
    await first.focus(); await page.keyboard.press('Space');
    await second.check();
    assert.match(await status.innerText(),/2 sur 3/);
    await page.reload({waitUntil:'networkidle'});
    assert.ok(await first.isChecked() && await second.isChecked());
    await checks.getByRole('button',{name:'Réinitialiser la checklist'}).click();
    assert.match(await status.innerText(),/0 sur 3/);
    assert.ok(await first.evaluate(ch=>ch===document.activeElement));
    const modesList = page.getByRole('tablist',{name:'Modes de jeu de Tarkov'});
    await modesList.getByRole('tab',{name:'PvP Zone'}).focus();
    await page.keyboard.press('ArrowRight');
    assert.match(await page.getByRole('tabpanel').innerText(),/PvE Zone/);
    await page.keyboard.press('End');
    assert.match(await page.getByRole('tabpanel').innerText(),/0\.16\.9\.5\.40743/);
    await page.keyboard.press('Home');
    assert.equal(await modesList.getByRole('tab',{name:'PvP Zone'}).getAttribute('aria-selected'),'true');
    assert.equal(await page.getByRole('tabpanel').count(),1);
    notes.push('Checklist au clavier, compteur live, mémoire locale et reset ; cinq onglets parcourus par flèches/Home/End.');

    const radio = page.locator('.compact-audio');
    const audio = radio.locator('audio');
    const audioToggle = radio.locator('[data-audio-toggle]');
    await radio.locator('summary').click();
    await open(page,'.compact-audio',true);
    const intro = radio.getByRole('button',{name:/Signal de Norvinsk/});
    await intro.click();
    assert.equal(await intro.getAttribute('aria-pressed'),'true');
    assert.deepEqual(media(),[]);
    await audioToggle.focus(); await page.keyboard.press('Enter');
    await wait(page,()=>{const a=document.querySelector('audio');return !a.paused && a.currentTime>.1});
    assert.equal(await radio.getAttribute('data-audio-state'),'playing');
    assert.ok(await audio.evaluate(a=>a.duration>30 && a.duration<30.1 && a.loop===false));
    await audio.evaluate(a=>{a.currentTime=a.duration-.18});
    await wait(page,()=>document.querySelector('audio').ended && document.querySelector('.compact-audio').dataset.audioState==='ready');
    assert.match(await radio.getByRole('status').innerText(),/Écoute terminée/);
    await audioToggle.click();
    await wait(page,()=>document.querySelector('.compact-audio').dataset.audioState==='playing');
    await audioToggle.click();
    assert.equal(await radio.getAttribute('data-audio-state'),'paused');
    assert.ok(await audio.evaluate(a=>a.paused));
    await radio.getByRole('slider',{name:'Volume de l’ambiance'}).focus();
    await page.keyboard.press('Home');
    assert.equal(await audio.evaluate(a=>a.volume),0);
    const before = media().length;
    await page.reload({waitUntil:'networkidle'});
    await radio.locator('summary').click();
    assert.equal(await intro.getAttribute('aria-pressed'),'true');
    assert.equal(await audio.getAttribute('src'),null);
    assert.ok(await audio.evaluate(a=>a.paused && a.volume===0));
    assert.equal(media().length,before);
    await page.keyboard.press('Escape');
    await open(page,'.compact-audio',false);
    assert.ok(await radio.locator('summary').evaluate(el=>el === document.activeElement));
    const range = await context.request.get(new URL('audio/themes/intro_norvinsk.mp3',root).href,{headers:{Range:'bytes=0-8191'}});
    assert.equal(range.status(),206);
    assert.match(range.headers()['content-range'],/^bytes 0-8191\/600816$/);
    assert.equal((await range.body()).length,8192);
    report.medias = {requetesObservees:[...new Set(media().map(p=>new URL(p).pathname.split('/').at(-1)))],pause:true,finNonBouclee:true,rechargementSilencieux:true,range:206};
    notes.push('Radio : piste sélectionnable sans requête ; lancement clavier, fin non bouclée, reprise, pause, volume, préférences et rechargement muet. Requête Range MP3 206.');

    const contrast = page.getByRole('button',{name:'Contraste renforcé'});
    await contrast.click();
    assert.equal(await page.locator('html').getAttribute('data-theme'),'contrast');
    assert.equal(await contrast.getAttribute('aria-pressed'),'true');
    await audit(page,'accueil, contraste renforcé');
    await contrast.click();
    await page.emulateMedia({reducedMotion:'no-preference'});
    await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
    await wait(page,()=>document.querySelector('[data-hero-motion]').dataset.motionActive==='true');
    await page.evaluate(()=>scrollTo({top:document.body.scrollHeight,behavior:'instant'}));
    await wait(page,()=>document.querySelector('[data-hero-motion]').dataset.motionActive==='false');
    await page.getByRole('button',{name:'Réduire les animations'}).click();
    assert.equal(await page.locator('html').getAttribute('data-motion'),'off');
    await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
    await wait(page,()=>document.querySelector('[data-hero-motion]').dataset.motionActive==='false');
    notes.push('Contraste renforcé, mouvement système respecté, animation effective seulement à l’écran et réduction manuelle persistante.');

    for (const width of [320,390,600,768,991,1024,1440]) {
      await page.setViewportSize({width,height:844});
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth===document.documentElement.clientWidth), `Débordement accueil à ${width}px`);
      await menuSummary.click();
      await open(page,'.mega-nav',true);
      const hitbox = await page.locator('.mega-nav__panel').boundingBox();
      assert.ok(hitbox.x >= 0 && hitbox.x + hitbox.width <= width && hitbox.y + hitbox.height <= 844, `${width}px ${JSON.stringify(hitbox)}`);
      await page.keyboard.press('Escape');
      await open(page,'.mega-nav',false);
      report.largeursPx.push(width);
    }
    await search.click();
    await scope.selectOption('atelier');
    await input.fill('comparateur');
    await dialog.getByRole('link',{name:/Comparateur de cartes/}).click();
    await page.waitForURL(atelier+'#comparateur');
    assert.match(await page.locator('h1').innerText(),/Atelier/);
    await page.locator('.workshop-footer').getByRole('link',{name:'Accueil du guide'}).click();
    await page.waitForURL(home);
    assert.equal(await page.locator('h1').getAttribute('id'),'titre-accueil');
    assert.deepEqual(responseErrors,[]);
    assert.deepEqual(requests.filter(q=>!q.startsWith(home)),[]);
    assert.deepEqual(report.console,[]);
    notes.push('Sans débordement page ou panneau de 320 à 1440 px. Recherche vers le comparateur réel et retour accueil, aucune requête externe automatique ni erreur console.');
    for (const image of await page.locator('main img[loading="lazy"]').all()) {
      await image.scrollIntoViewIfNeeded();
      await image.evaluate(async img => {
        await img.decode();
        if (img.naturalWidth !== 1376) throw new Error(`JPG non décodé : ${img.src}`);
      });
    }
    assert.deepEqual(responseErrors,[]);
    notes.push('Les huit JPG, dont les sept différés, décodent après défilement.');
    await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
    await snapshot(page,'accueil-phase2-complet',true);
    await context.close();

    const devices = await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true,reducedMotion:'reduce'});
    const mobile = await devices.newPage();
    await mobile.goto(home,{waitUntil:'networkidle'});
    await snapshot(mobile,'accueil-phase2-mobile');
    const mobileMenu = mobile.locator(summarySelector);
    await mobileMenu.tap();
    await open(mobile,'.mega-nav',true);
    await mobile.locator('.mega-nav').getByRole('link',{name:'Hideout & économie',exact:true}).tap();
    await open(mobile,'.mega-nav',false);
    await open(mobile,'#dossier-hideout details',true);
    assert.equal(new URL(mobile.url()).hash,'#dossier-hideout');
    await mobile.getByRole('button',{name:'Rechercher Ctrl K dans le guide'}).tap();
    await open(mobile,'#search-dialog',true);
    await mobile.getByRole('button',{name:'Fermer la recherche'}).tap();
    await audit(mobile,'accueil tactile à 390 px');
    await devices.close();

    const nojs = await browser.newContext({viewport:{width:390,height:844},javaScriptEnabled:false});
    const simple = await nojs.newPage();
    await simple.goto(home);
    assert.equal(await simple.locator('.mode-home .tabs__panel:visible').count(),5);
    assert.equal(await simple.locator('.dossier-card summary:visible').count(),6);
    assert.equal(await simple.locator('.news-card:visible').count(),3);
    assert.ok(!await simple.getByRole('button',{name:'Rechercher Ctrl K dans le guide'}).isVisible());
    await simple.locator(summarySelector).click();
    await simple.locator('.mega-nav').getByRole('link',{name:'Brief de premier raid'}).click();
    assert.equal(new URL(simple.url()).hash,'#premiers-pas');
    assert.ok(await simple.getByRole('checkbox',{name:/Choisir mon mode/}).isVisible());
    await simple.getByRole('checkbox',{name:/Choisir mon mode/}).check();
    await simple.locator('#dossier-cartes summary').click();
    assert.ok(await simple.getByRole('link',{name:'Lire : Atlas des cartes'}).isVisible());
    await simple.locator('#programme summary').click();
    assert.ok(await simple.getByText('Phase 3 · Débutant et lore').isVisible());
    await simple.locator('.compact-audio summary').click();
    assert.ok(await simple.getByRole('link',{name:'Écouter Signal de Norvinsk (MP3)'}).isVisible());
    await nojs.close();
    notes.push('Sur mobile tactile et sans JS : menu et sections atteignables ; dossiers, programme, contenu des cinq modes, checklist native et lien MP3 disponibles.');

    const retryPage = await browser.newPage({reducedMotion:'reduce'});
    const searchJson = '**/js/data/search-index.json';
    await retryPage.route(searchJson, route=>route.fulfill({status:503}));
    await retryPage.goto(home);
    await retryPage.getByRole('button',{name:'Rechercher Ctrl K dans le guide'}).click();
    const retry = retryPage.getByRole('button',{name:'Recharger l’index'});
    await retry.waitFor();
    assert.match(await retryPage.locator('[data-search-status]').textContent(),/n’a pas pu/);
    await retryPage.unroute(searchJson);
    await retry.click();
    await wait(retryPage,()=>document.querySelector('[data-search-status]').textContent.includes('Suggestions'));
    await retryPage.close();
    notes.push('Défaillance simulée de l’index : message compréhensible, navigation disponible et rechargement réussi.');
    report.statut = 'OK';
  } finally {
    await browser.close();
  }
}

run().catch(error=>{report.erreur=error.message;console.error(error.stack);process.exitCode=1;}).finally(()=>{
  const out = JSON.stringify(report,null,2)+'\n';
  if (process.env.TUG_TEST_REPORT) writeFileSync(process.env.TUG_TEST_REPORT,out);
  process.stdout.write(out);
});
