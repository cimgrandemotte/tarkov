// Phase 3 · parcours, navigation, persistance, responsive et repli natif.
const { chromium } = require('playwright');
const axe = require('axe-core');
const assert = require('node:assert/strict');
const { mkdirSync, writeFileSync } = require('node:fs');
const { join } = require('node:path');
const root = new URL((process.env.TUG_URL || 'http://127.0.0.1:4173').replace(/\/$/,'') + '/');
const guide = new URL('pages/getting-started.html',root).href;
const lore = new URL('pages/lore/index.html',root).href;
const loreDirectory = new URL('pages/lore/',root).href;
const options = {viewport:{width:1440,height:1000},locale:'fr-FR',reducedMotion:'reduce'};
const timeout = 8000;
const report = {statut:'ECHEC',rubriques:[],largeursPx:[],wcag:[],console:[],erreursHttp:[],perf:{}};
const note = s=>report.rubriques.push(s);
const ready = (p, f, arg) => p.waitForFunction(f,arg,{timeout});
const focused = (p,id) => ready(p,key=>document.activeElement.id===key,id);
const open = (p, selector, value) => ready(p,({selector,value})=>document.querySelector(selector).open===value,{selector,value});
const visible = (p,selector) => p.locator(`${selector}:visible`).count();
const waitSearch = p => ready(p,()=>document.querySelector('[data-search-status]').textContent.includes('Suggestions'));

async function screenshot(page, name, fullPage=false) {
  const dest = process.env.TUG_VISUAL_DIR;
  if (!dest) return;
  mkdirSync(dest,{recursive:true});
  await page.screenshot({path:join(dest,name+'.jpg'),type:'jpeg',quality:87,fullPage});
}

function track(page) {
  page.setDefaultTimeout(timeout);
  page.on('pageerror', e=>report.console.push(e.message));
  page.on('console', m=>{ if(m.type()==='error') report.console.push(m.text()); });
  page.on('response', res=>{ if(res.status()>=400) report.erreursHttp.push([res.status(),res.url()]); });
}

async function audit(page, scope) {
  if (!await page.evaluate(() => Boolean(window.axe))) await page.evaluate(axe.source);
  const result = await page.evaluate(async () => {
    const res = await axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}});
    const count = rows => rows.map(e=>({id:e.id,noeuds:e.nodes.length}));
    const failures = res.violations.map(e=>({id:e.id,noeuds:e.nodes.length,cibles:e.nodes.map(node=>node.target)}));
    return {violations:failures,controleHumain:count(res.incomplete),reglesReussies:res.passes.length};
  });
  report.wcag.push({scope,...result});
  assert.deepEqual(result.violations,[],`Axe : ${scope}, ${JSON.stringify(result.violations)}`);
}

async function testLanding(page,url,route,count) {
  const requests = [];
  const capture = request => requests.push(request.url());
  page.on('request',capture);
  const res = await page.goto(url,{waitUntil:'networkidle'});
  page.off('request',capture);
  assert.equal(res.status(),200);
  assert.equal(await page.locator('h1').count(),1);
  await ready(page,()=>{const i=document.querySelector('.field-hero__image'); return i.complete && i.naturalWidth===1376;});
  assert.equal(await page.locator('img[loading="lazy"]').count(),count-1);
  assert.ok(requests.every(url=>url.startsWith(root.href)));
  assert.ok(!requests.some(url=>/(?:\.mp3|search-index\.json|fuse\.min\.mjs|howler\.core\.min\.js)$/i.test(url)));
  report.perf[route] = {initial:requests.length, audio:0, index:0, tiers:0,lcpLocal:await page.evaluate(()=>window.__tugLcp ?? null)};
  await screenshot(page,`${route}-1440`);
  for (const img of await page.locator('main img').all()) {
    await img.scrollIntoViewIfNeeded();
    await img.evaluate(async el=>{ await el.decode(); if (!el.naturalWidth) throw new Error(el.src); });
  }
  await page.evaluate(()=>window.scrollTo(0,0));
  await screenshot(page,`${route}-complet`,true);
}

async function desktop(browser) {
  const context = await browser.newContext(options);
  await context.addInitScript(() => {
    if (!PerformanceObserver.supportedEntryTypes.includes('largest-contentful-paint')) return;
    new PerformanceObserver(list => {
      const lcp=list.getEntries().at(-1);
      window.__tugLcp={ms:Math.round(lcp.startTime),element:lcp.element?.tagName ?? null,ressource:lcp.url?new URL(lcp.url).pathname:null};
    }).observe({type:'largest-contentful-paint',buffered:true});
  });
  const page=await context.newPage(); track(page);
  await testLanding(page,guide,'guide-phase3',5);
  await audit(page,'Guide sur bureau');
  await page.reload();
  await page.keyboard.press('Tab');
  assert.match(await page.evaluate(()=>document.activeElement.textContent),/Aller au contenu principal/);
  await page.keyboard.press('Enter');
  await focused(page,'contenu');
  await page.getByRole('link',{name:'Suivre les 10 étapes'}).click();
  await focused(page,'parcours');
  assert.equal(new URL(page.url()).hash,'#parcours');
  const route = page.locator('[data-checklist="guide-parcours-v1"]');
  const kit = page.locator('[data-checklist="guide-kit-v1"]');
  const status = form=>form.locator('[data-checklist-status]');
  assert.equal(await route.locator('[data-raid-step]').count(),10);
  assert.equal(await route.locator('input:checked').count(),0);
  await route.locator('#etape-1').focus(); await page.keyboard.press('Space');
  await route.locator('#etape-5').check();
  await kit.locator('[name="soins"]').check();
  assert.match(await status(route).innerText(),/2 sur 10/);
  assert.match(await status(kit).innerText(),/1 sur 6/);
  assert.equal(await route.locator('progress').evaluate(el=>el.value),2);
  await page.reload();
  assert.equal(await route.locator('input:checked').count(),2);
  assert.equal(await kit.locator('input:checked').count(),1);
  await route.getByRole('button',{name:'Réinitialiser les étapes'}).click();
  await focused(page,'etape-1');
  assert.equal(await route.locator('progress').evaluate(el=>el.value),0);
  assert.equal(await kit.locator('input:checked').count(),1);
  await kit.getByRole('button',{name:'Réinitialiser ce kit'}).click();
  assert.equal(await kit.locator('input:checked').count(),0);
  note('Parcours : dix étapes, raccourcis d’évitement et d’ancre, deux checklists indépendantes restaurées et réinitialisées, avec retour du focus et compteur.')

  await page.locator('.field-toc a[href="#touches"]').click();
  await focused(page,'touches');
  const board = page.locator('[data-keyboard-guide]');
  const combo = board.getByLabel('Disposition');
  const movement = board.locator('[data-bind="move"] kbd');
  assert.equal(await combo.inputValue(),'qwerty');
  assert.equal(await movement.innerText(),'W · A · S · D');
  await combo.selectOption('azerty');
  assert.equal(await movement.innerText(),'Z · Q · S · D');
  await page.reload();
  assert.equal(await combo.inputValue(),'azerty');
  await combo.selectOption('custom');
  assert.equal(await visible(page,'.keys-row input'),12);
  const exits = board.getByRole('textbox',{name:'Lister les extractions'});
  await exits.fill('B × 2');
  await board.getByRole('textbox',{name:'Interagir'}).fill('Souris 5');
  assert.equal(await exits.inputValue(),'B × 2');
  await audit(page,'Guide, commandes personnalisées');
  await page.reload();
  assert.equal(await exits.inputValue(),'B × 2');
  await combo.selectOption('azerty');
  assert.equal(await visible(page,'.keys-row input'),0);
  await combo.selectOption('custom');
  assert.equal(await exits.inputValue(),'B × 2');
  await board.getByRole('button',{name:'Réinitialiser les commandes'}).click();
  await focused(page,'profil-clavier');
  assert.equal(await combo.inputValue(),'qwerty');
  await combo.selectOption('custom');
  assert.equal(await exits.inputValue(),'O × 2');
  const faq = page.locator('[data-faq]');
  assert.equal(await faq.count(),24);
  await faq.first().locator('summary').focus(); await page.keyboard.press('Enter');
  await open(page,'[data-faq]',true);
  assert.ok(await faq.first().locator('p').isVisible());
  note('Commandes : trois dispositions, 12 actions, édition et restauration locales, reset clavier. FAQ : 24 volets natifs, dont ouverture par Entrée.')

  const trigger=page.getByRole('button',{name:'Rechercher Ctrl K dans le guide'});
  const query=page.locator('#search-query');
  const scope=page.locator('#search-scope');
  await trigger.focus(); await page.keyboard.press('Control+K'); await focused(page,'search-query');
  await waitSearch(page);
  await scope.selectOption('dossier');
  await query.fill('sante');
  const hit=page.getByRole('link',{name:/Santé du personnage et soins/});
  await hit.waitFor();
  assert.ok((await hit.getAttribute('href')).endsWith('getting-started.html#sante'));
  await hit.focus(); await page.keyboard.press('Enter');
  await open(page,'#search-dialog',false);
  await focused(page,'sante');
  assert.equal(new URL(page.url()).hash,'#sante');
  await page.locator('.mega-nav summary').focus(); await page.keyboard.press('Enter');
  await open(page,'.mega-nav',true);
  await audit(page,'Guide, méga-menu ouvert');
  await page.keyboard.press('Escape'); await open(page,'.mega-nav',false);
  assert.ok(await page.locator('.mega-nav summary').evaluate(s=>document.activeElement===s));

  await testLanding(page,lore,'lore-phase3',4);
  await audit(page,'Lore sur bureau, révélations fermées');
  const pins = page.locator('.region-plate a.plate-index');
  assert.equal(await pins.count(),4);
  await pins.nth(2).focus(); await page.keyboard.press('Enter');
  await focused(page,'port-tarkov');
  assert.equal(new URL(page.url()).hash,'#port-tarkov');
  await page.getByRole('link',{name:'Explorer la chronologie'}).click();
  await focused(page,'chronologie');
  const tabs = page.getByRole('tablist',{name:'Sélectionner le fil chronologique'});
  const fiction = tabs.getByRole('tab',{name:'Dans l’univers'});
  const real = tabs.getByRole('tab',{name:'Dates de publication'});
  await fiction.focus(); await page.keyboard.press('ArrowRight');
  assert.equal(await real.getAttribute('aria-selected'),'true');
  assert.equal(await visible(page,'.chronicle__panel'),1);
  const release = page.locator('#temps-reel details').nth(1);
  await release.locator('summary').focus(); await page.keyboard.press('Space');
  assert.match(await release.locator('p').innerText(),/date est confirmée/);
  await real.focus(); await page.keyboard.press('Home');
  assert.equal(await fiction.getAttribute('aria-selected'),'true');
  await page.keyboard.press('End');
  assert.equal(await real.getAttribute('aria-selected'),'true');
  await screenshot(page,'lore-phase3-chronologie');
  const spoilers = page.locator('[data-spoiler]');
  assert.equal(await spoilers.count(),3);
  assert.equal(await page.locator('[data-spoiler][open]').count(),0);
  assert.equal(await visible(page,'[data-spoiler-content]'),0);
  await spoilers.nth(0).locator('summary').click();
  await spoilers.nth(1).locator('summary').focus(); await page.keyboard.press('Enter');
  assert.ok(await page.getByText('Savior',{exact:true}).isVisible());
  await audit(page,'Lore, un onglet et deux révélations ouvertes');
  await page.getByRole('button',{name:'Refermer toutes les révélations'}).click();
  assert.equal(await page.locator('[data-spoiler][open]').count(),0);
  assert.ok(await spoilers.first().locator('summary').evaluate(s=>document.activeElement===s));
  await spoilers.first().locator('summary').click(); await page.reload();
  assert.equal(await page.locator('[data-spoiler][open]').count(),0);
  const contrast = page.getByRole('button',{name:'Contraste renforcé'});
  await contrast.click();
  assert.equal(await page.locator('html').getAttribute('data-theme'),'contrast');
  await audit(page,'Lore, contraste renforcé');
  await contrast.click();
  note('Lore : quatre repères de carte accessibles, onglets au clavier, jalons ouvrables. Trois volets sans révélation au chargement, remise à zéro et fermeture groupée.')

  await page.goto(loreDirectory);
  await trigger.click(); await waitSearch(page);
  await scope.selectOption('dossier'); await query.fill('chronologie de norvinsk');
  await page.getByRole('link',{name:/Chronologie de Norvinsk/}).click();
  await focused(page,'chronologie');
  assert.equal(page.url(),loreDirectory+'#chronologie');
  assert.equal(await page.locator('[data-spoiler][open]').count(),0);
  await page.goto(root.href);
  assert.equal(await page.locator('[data-count="published"]').textContent(),'03');
  await page.getByRole('link',{name:'Préparer mon premier raid',exact:true}).click();
  await page.waitForURL(guide);
  await page.locator('.commandbar__nav-link').filter({hasText:/^Norvinsk$/}).click();
  await page.waitForURL(lore);
  await page.getByRole('button',{name:'Rechercher Ctrl K dans le guide'}).click(); await waitSearch(page);
  await scope.selectOption('publiee'); await query.fill('Tarkov');
  await page.getByRole('link',{name:/Premiers pas dans Tarkov/}).click();
  await page.waitForURL(guide);
  await page.goto(root.href);
  await page.getByRole('link',{name:/Comprendre Norvinsk/}).click();
  await page.waitForURL(lore);
  note('Accueil, méga-menu et recherche : accès aux deux routes, repères focusables, alias /pages/lore/ et portée Pages publiées. Pas de spoiler ouvert par un lien de recherche.')
  await context.close();
}

async function responsive(browser) {
  const context=await browser.newContext({...options,reducedMotion:'reduce',viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1});
  const mobile=await context.newPage(); track(mobile);
  for (const width of [320,390,768,1024,1440]) {
    await mobile.setViewportSize({width,height:844});
    for (const url of [guide,lore]) {
      await mobile.goto(url,{waitUntil:'networkidle'});
      const sizes= await mobile.evaluate(()=>[document.documentElement.clientWidth, document.documentElement.scrollWidth]);
      assert.deepEqual(sizes,[width,width],`${url} à ${width}`);
      if (width===390) await screenshot(mobile,`${url===guide?'guide':'lore'}-phase3-mobile`);
    }
    report.largeursPx.push(width);
  }
  await mobile.setViewportSize({width:390,height:844});
  await mobile.goto(guide);
  const menu = mobile.locator('.mega-nav summary');
  await menu.tap(); await open(mobile,'.mega-nav',true);
  await mobile.locator('.mega-nav').getByRole('link',{name:'Lore de Norvinsk'}).tap();
  await mobile.waitForURL(lore);
  const outline = mobile.locator('.field-toc-mobile');
  await outline.locator('summary').tap(); await open(mobile,'.field-toc-mobile',true);
  await outline.getByRole('link',{name:'Les deux chronologies'}).tap();
  await focused(mobile,'chronologie'); await open(mobile,'.field-toc-mobile',false);
  await mobile.getByRole('tab',{name:'Dates de publication'}).tap();
  await mobile.locator('#temps-reel details').last().locator('summary').tap();
  assert.ok(await mobile.locator('#temps-reel details').last().locator('p').isVisible());
  await audit(mobile,'Lore tactile, onglet des dates');
  await mobile.goto(guide);
  await mobile.locator('label[for="etape-1"]').tap();
  assert.ok(await mobile.locator('#etape-1').isChecked());
  await audit(mobile,'Guide tactile');
  await context.close();
  note('Tactile : menu, sommaire, onglets et cases utilisables. Les deux pages tiennent aux cinq largeurs sans défilement horizontal.')
}

async function fallbacks(browser) {
  const nojs = await browser.newContext({...options,javaScriptEnabled:false,viewport:{width:390,height:844}});
  const page=await nojs.newPage();
  await page.goto(guide);
  assert.ok(!await page.getByRole('button',{name:'Rechercher Ctrl K dans le guide'}).isVisible());
  assert.equal(await visible(page,'[data-raid-step]'),10);
  await page.locator('#etape-1').check();
  assert.ok(await page.locator('#etape-1').isChecked());
  assert.equal(await visible(page,'[data-key-value]'),12);
  await page.locator('[data-faq]').last().locator('summary').click();
  assert.ok(await page.locator('[data-faq]').last().locator('p').isVisible());
  await page.goto(lore);
  assert.equal(await visible(page,'.chronicle__panel'),2);
  assert.equal(await page.locator('[data-spoiler][open]').count(),0);
  await page.locator('[data-spoiler]').last().locator('summary').click();
  assert.ok(await page.locator('[data-spoiler-content]').last().isVisible());
  await nojs.close();
  const blocked = await browser.newContext(options);
  await blocked.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Stockage désactivé','SecurityError');}}));
  const tmp = await blocked.newPage(); track(tmp);
  await tmp.goto(guide);
  await tmp.locator('#etape-1').check();
  await ready(tmp,()=>document.querySelector('[data-checklist-note]').textContent.includes('Stockage indisponible'));
  await tmp.locator('#profil-clavier').selectOption('custom');
  assert.match(await tmp.locator('[data-keys-status]').textContent(),/Stockage indisponible/);
  await tmp.getByRole('textbox',{name:'Se déplacer'}).fill('Flèches');
  assert.equal(await tmp.getByRole('textbox',{name:'Se déplacer'}).inputValue(),'Flèches');
  await blocked.close();
  note('Sans JavaScript : contenus, QWERTY, FAQ, légendes, chronologies et volets natifs. Sans stockage : cases et modifications utilisables avec un avis local.')
}

async function run() {
  let opts={headless:true};
  if (process.env.TUG_CHROMIUM==='sparticuz') {
    const sp=require('@sparticuz/chromium');
    opts={...opts,executablePath:await sp.executablePath(),args:sp.args.filter(flag=>!['--disable-web-security','--allow-running-insecure-content','--single-process'].includes(flag))};
  } else if (process.env.TUG_CHROMIUM) opts.executablePath=process.env.TUG_CHROMIUM;
  const browser=await chromium.launch(opts);
  report.chromium=browser.version();
  try {
    await desktop(browser);
    await responsive(browser);
    await fallbacks(browser);
    assert.deepEqual(report.console,[]); assert.deepEqual(report.erreursHttp,[]);
    report.statut='OK';
  } finally { await browser.close(); }
}
run().catch(e=>{report.erreur=e.message;console.error(e.stack);process.exitCode=1;}).finally(()=>{
  const output=JSON.stringify(report,null,2)+'\n';
  if (process.env.TUG_TEST_REPORT) writeFileSync(process.env.TUG_TEST_REPORT,output);
  process.stdout.write(output);
});
