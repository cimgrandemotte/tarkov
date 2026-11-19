#!/usr/bin/env python3
"""Vérifie les pages publiées de P3, les liens, les inventaires et le point d’arrêt."""
import argparse
from collections import Counter
from hashlib import sha256
import json
import re
import subprocess
import sys
from urllib.parse import urldefrag, urlsplit

from PIL import Image
from valider_phase2 import ROOT, HOME, WORKSHOP, PUBLISHED, check_link, inventory, parse, read

PAGES = ('pages/getting-started.html', 'pages/lore/index.html')
STATIC_REPORT = 'docs/validation-phase-3-statique.json'
BROWSER_REPORTS = ['docs/validation-phase-3-navigateur.json', 'docs/validation-phase-3-accueil.json', 'docs/validation-phase-3-atelier.json']


def check_html(route, allowed, allowed_urls, seen):
    file = ROOT / route
    html, tags = parse(file)
    ids = {att['id'] for _, att in tags if 'id' in att}
    assert sum(tag == 'h1' for tag, _ in tags) == 1 and any(tag == 'html' and a.get('lang') == 'fr' for tag, a in tags), route
    assert 'usemap=' not in html and not re.search(r'<(?:svg|iframe|embed)\b', html), route
    local, assets, outbound = 0, {}, set()
    for tag, attr in tags:
        for key in ('aria-labelledby','aria-describedby','aria-controls','for','data-dialog-open'):
            if key in attr:
                assert set(attr[key].split()) <= ids, (route, key, attr)
        for key in ('href','src'):
            if key not in attr:
                continue
            dest = check_link(attr[key], file)
            local += dest is not None
            if tag == 'a' and dest is None:
                uri = urldefrag(attr[key])[0]
                assert uri in allowed_urls, (route, attr[key])
                outbound.add(uri)
            elif tag == 'a' and dest.suffix == '.html':
                assert dest.relative_to(ROOT).as_posix() in allowed, attr[key]
        if tag == 'img':
            img = check_link(attr['src'], file)
            assert img.suffix == '.jpg' and attr['alt'].strip(), attr
            assert attr.get('loading') == 'lazy' or attr.get('fetchpriority') == 'high', attr
            with Image.open(img) as source:
                assert source.format == 'JPEG' and source.size == (int(attr['width']), int(attr['height'])), img
                source.verify()
            assets[img.relative_to(ROOT).as_posix()] = {'px':[int(attr['width']),int(attr['height'])], 'octets':img.stat().st_size, 'sha256':sha256(img.read_bytes()).hexdigest()}
        if route in PAGES:
            assert tag not in ('audio','video'), route
    if route in PAGES:
        assert sum(tag == 'link' and a.get('as') == 'image' and a.get('rel') == 'preload' for tag, a in tags) == 1
        assert sum(tag == 'img' and a.get('fetchpriority') == 'high' for tag, a in tags) == 1
        ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[1])
        meta = {a.get('name',a.get('property')):a.get('content') for tag,a in tags if tag == 'meta'}
        assert ld['@type'] == 'Article' and ld['inLanguage'] == 'fr-FR' and 150 <= len(ld['description']) <= 160
        assert ld['description'] == meta['description'] == meta['og:description'] == meta['twitter:description']
        assert meta['og:locale'] == 'fr_FR' and not meta.get('robots')
        if route==PAGES[0]:
            assert sorted(int(a['data-raid-step']) for tag, a in tags if tag == 'li' and 'data-raid-step' in a) == list(range(1,11))
            assert sum(tag=='details' and 'data-faq' in a and 'open' not in a for tag,a in tags) == 24
            assert Counter(a['type'] for tag,a in tags if tag=='input')['checkbox'] == 16
            assert sum('data-checklist' in a for tag,a in tags if tag=='form') == 2
            assert sum('data-bind' in a for _,a in tags) == 12
        else:
            assert sum(tag == 'details' and 'data-spoiler' in a and 'open' not in a for tag,a in tags) == 3
            assert sum(tag=='button' and 'data-tab' in a for tag,a in tags) == 2
            assert sum(tag=='details' and 'chronicle__event' in a.get('class','') for tag,a in tags) == 8
            assert sum(tag=='a' and a.get('href') in ('#zone-economique','#ville-tarkov','#port-tarkov','#blocus') for tag,a in tags) == 4
    seen.update(assets)
    return {'referencesLocales':local,'sourcesExternes':len(outbound),'images': assets}


def main(final, dest):
    book = read('docs/pages.json'); sources = read('docs/sources.json')['sources']; assets = inventory()
    planned = {p['route']: p for p in book['pages']}; pubs = {route for route, p in planned.items() if p['etat'] in PUBLISHED}
    assert book['total'] == len(planned) == len(book['pages']) == 86
    assert book['publiees'] == len(pubs)
    assert {'index.html',*PAGES} <= pubs, 'les pages de la phase 3 doivent rester publiées'
    assert all(set(p['sourcesDeDepart']) <= sources.keys() for p in planned.values())
    # Contrôle cumulatif : tout HTML sur disque est une route planifiée ;
    # les routes rendues mais pas encore publiées sont admises.
    assert set(assets['html']) <= {'atelier/index.html', *planned}
    assert set(assets['html']) - {'atelier/index.html', *pubs} <= set(planned)
    assert len(assets['jpg']) >= 21 and len(assets['mp3']) == 8
    assert all(media in assets['jpg'] for media in sum((planned[r]['mediasEffectifs'] for r in PAGES), []))
    forbidden = {'.jpeg','.png','.svg','.webp','.gif','.zip','.pdf','.wav','.ogg','.aac','.flac','.m4a'}
    ignores = {'node_modules', '.git', '.cache', '.venv', '__pycache__'}
    intrus = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and p.suffix.lower() in forbidden and not ignores.intersection(p.relative_to(ROOT).parts)]
    assert not intrus, intrus
    # Limites et repères du relevé sont associés aux deux pages dans le manifeste.
    for route in PAGES:
        p = planned[route]; assert p['phase'] == 'PHASE_3' and p['dateDePublication'] == '2026-11-18'
        assert p['rechercheCiblee'] == 'docs/veille-phase-3.md' and (ROOT / p['rechercheCiblee']).is_file()
    seen = {}
    allowed = {'atelier/index.html',*pubs}
    urls = sorted({urldefrag(s['url'])[0] for s in sources.values()})
    refs = {route: check_html(route, allowed, urls, seen) for route in ('index.html',*PAGES)}
    assert {route:sorted(refs[route]['images']) for route in ('index.html',*PAGES)} == {route:planned[route]['mediasEffectifs'] for route in ('index.html',*PAGES)}
    new_media = sorted(set(refs[PAGES[0]]['images']) | set(refs[PAGES[1]]['images']))
    assert len(new_media) == 9 and not set(new_media).intersection(refs['index.html']['images'])
    assert all(p.startswith(('images/guide/','images/lore/')) for p in new_media)
    assert all(0 < seen[p]['octets'] < 350000 for p in new_media)
    # Atelier séparé ; seuls les liens de son index entrent dans le contrôle P3.
    _, studio = parse(WORKSHOP)
    assert any(tag=='meta' and attr.get('name')=='robots' and 'noindex' in attr['content'] for tag,attr in studio)
    index = read('js/data/search-index.json'); entries = index['entrees']
    assert index['routesPlanifiees']==86 and index['routesPubliees']==len(pubs)
    tally = Counter(row['etat'] for row in entries)
    assert tally['publiee']==len(pubs) and tally['planifiee']==86-len(pubs), tally
    assert tally['accueil']==6 and tally['atelier']==8 and tally['dossier']>=15, tally
    for row in entries:
        if row['etat']=='planifiee':
            assert row['url'] is None
            continue
        target = check_link(row['url'], HOME)
        assert target.relative_to(ROOT).as_posix() in allowed
        if row['etat']=='dossier':
            route = urlsplit(row['url'])
            assert route.path in PAGES + ('pages/maps/index.html',) and route.fragment
            assert route.fragment not in ('spoilers','temps-fiction','temps-reel')
            assert not any(key in json.dumps(row).lower() for key in ('savior','debtor','fallen','the ticket','kerman'))
    html = HOME.read_text(encoding='utf-8')
    assert all(f'href="./{route}"' in html for route in PAGES)
    assert re.search(r'data-count="published">' + f'{len(pubs):02d}' + '<',html)
    renderers = []
    for script in ('rendre_accueil.py','rendre_dossiers.py'):
        run = subprocess.run([sys.executable,'scripts/'+script,'--check'],capture_output=True,text=True,check=True,cwd=ROOT)
        renderers.extend(run.stdout.strip().splitlines())
    counts = {'pagesPlanifiees':86, 'pagesGenerees':3,'pagesHtmlTechniques':1,'imagesCreees':21,'audiosCrees':8}
    w = read('workflow.json'); m = read('state_machine.json')['instantane']
    if final and w['phaseCourante']=='PHASE_3':
        assert w['statut']==m['etat']=='ATTENTE_CONTINUE' and w['phaseCourante']==m['phase']=='PHASE_3'
        assert w['compteurs']==m['compteurs']==counts and w['phasesTerminees']==m['phasesTerminees']==['PHASE_0','PHASE_1','PHASE_2','PHASE_3']
        assert w['prochainePhase']==m['prochainePhase']=='PHASE_4' and m['prochainEvenementAttendu']=='CONTINUE' and m['dernierePhaseTerminee']=='PHASE_3'
        phase = {p['id']:p for p in w['phases']}
        assert phase['PHASE_3']['statut']=='TERMINEE' and phase['PHASE_4']['statut']=='A_FAIRE'
        assert phase['PHASE_3']['lotMedia'] == {'imagesJpg':len(new_media),'audiosMp3':0} and phase['PHASE_3']['pagesPubliees']==2
        assert phase['PHASE_3']['validations'] == [STATIC_REPORT,*BROWSER_REPORTS]
        assert all(read(report)['statut']=='OK' for report in BROWSER_REPORTS)
        assert set(w['livrables']['pages'])==pubs and w['livrables']['imagesJpg']==assets['jpg'] and w['livrables']['audiosMp3']==assets['mp3']
        for category,files in w['livrables'].items():
            assert len(files)==len(set(files)) and all((ROOT / path).is_file() for path in files), category
    out = {'statut':'OK','controleCloture':final and w['phaseCourante']=='PHASE_3','compteurs':counts,'routes':refs,'index':dict(tally), 'sourcesRegistre':len(sources),
           'budgetPhase3':{'imagesJpg':len(new_media),'audiosMp3':0}, 'reproductibilite':renderers}
    data = json.dumps(out,ensure_ascii=False,indent=2)+'\n'
    if dest:
        (ROOT / dest).write_text(data,encoding='utf-8')
    print(data,end='')


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--final',action='store_true',help='contrôler aussi les compteurs, les rapports et l’état de clôture')
    cli.add_argument('--out',help='chemin du rapport JSON')
    args=cli.parse_args(); main(args.final,args.out)
