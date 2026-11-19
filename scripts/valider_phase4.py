#!/usr/bin/env python3
"""Contrôles statiques de la phase 4 : atlas et treize fiches de lieu.

Vérifie le HTML produit, les liens, les ancres, les tableaux, les médias,
le JSON-LD, la cohérence avec js/data/maps.json, l'index de recherche,
le budget média et la reproductibilité du rendu.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
import re
import subprocess
import sys
from urllib.parse import urldefrag, urlsplit

from html import escape

from PIL import Image
from valider_phase2 import ROOT, HOME, WORKSHOP, PUBLISHED, check_link, inventory, parse, read

ATLAS = 'pages/maps/index.html'
LIEUX = ['factory', 'customs', 'woods', 'shoreline', 'interchange', 'reserve', 'the-lab',
         'lighthouse', 'streets-of-tarkov', 'ground-zero', 'the-labyrinth', 'icebreaker', 'terminal']
PAGES = [ATLAS, *[f'pages/maps/{slug}.html' for slug in LIEUX]]
STATIC_REPORT = 'docs/validation-phase-4-statique.json'
BROWSER_REPORTS = ['docs/validation-phase-4-navigateur.json', 'docs/validation-phase-4-accueil.json']
SECTIONS = {'reperes', 'sorties', 'rencontres', 'terrain', 'cles', 'conduite', 'sources'}
SECTIONS_ATLAS = {'repere', 'lieux', 'comparatif', 'transits', 'variantes', 'sources'}
DUREES = {'factory': 20, 'customs': 35, 'woods': 35, 'shoreline': 45, 'interchange': 40,
          'reserve': 40, 'the-lab': 30, 'lighthouse': 40, 'streets-of-tarkov': 40,
          'ground-zero': 30, 'the-labyrinth': 30, 'icebreaker': 50, 'terminal': 50}


def check_html(route, allowed, allowed_urls, seen):
    file = ROOT / route
    html, tags = parse(file)
    ids = {att['id'] for _, att in tags if 'id' in att}
    assert sum(tag == 'h1' for tag, _ in tags) == 1, route
    assert any(tag == 'html' and a.get('lang') == 'fr' for tag, a in tags), route
    assert 'usemap=' not in html and not re.search(r'<(?:svg|iframe|embed)\b', html), route
    assert not re.search(r'<audio\b|<video\b', html), route
    local, assets, outbound = 0, {}, set()
    for tag, attr in tags:
        for key in ('aria-labelledby', 'aria-describedby', 'aria-controls', 'for', 'data-dialog-open'):
            if key in attr:
                assert set(attr[key].split()) <= ids, (route, key, attr)
        for key in ('href', 'src'):
            if key not in attr:
                continue
            dest = check_link(attr[key], file)
            local += dest is not None
            if tag == 'a' and dest is None:
                uri = urldefrag(attr[key])[0]
                assert uri in allowed_urls, (route, attr[key])
                outbound.add(uri)
            elif tag == 'a' and dest.suffix == '.html':
                assert dest.relative_to(ROOT).as_posix() in allowed, (route, attr[key])
        if tag == 'img':
            img = check_link(attr['src'], file)
            assert img.suffix == '.jpg' and attr['alt'].strip(), attr
            assert attr.get('loading') == 'lazy' or attr.get('fetchpriority') == 'high', attr
            with Image.open(img) as source:
                assert source.format == 'JPEG' and source.size == (int(attr['width']), int(attr['height'])), img
                source.verify()
            assets[img.relative_to(ROOT).as_posix()] = {'px': [int(attr['width']), int(attr['height'])],
                                                        'octets': img.stat().st_size,
                                                        'sha256': sha256(img.read_bytes()).hexdigest()}
    # Tables : légende, en-têtes de portée, conteneur focusable.
    tables = re.findall(r'<table class="map-table">(.*?)</table>', html, re.S)
    minimum = 2 if route == ATLAS else 4
    assert len(tables) >= minimum, (route, len(tables))
    for table in tables:
        assert '<caption>' in table, route
        assert '<th scope="col">' in table, route
    wraps = re.findall(r'<div class="table-wrap"([^>]*)>', html)
    assert wraps and all('tabindex="0"' in w and 'role="group"' in w for w in wraps), route
    # Sections focusables pour les ancres du sommaire.
    for section in (SECTIONS_ATLAS if route == ATLAS else SECTIONS):
        assert f'id="{section}" tabindex="-1"' in html, (route, section)
    # Données structurées et métadonnées.
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])
    meta = {a.get('name', a.get('property')): a.get('content') for tag, a in tags if tag == 'meta'}
    assert ld['@type'] in ('Article', 'CollectionPage') and ld['inLanguage'] == 'fr-FR'
    assert 145 <= len(ld['description']) <= 165
    assert ld['description'] == meta['description'] == meta['og:description'] == meta['twitter:description']
    assert meta['og:locale'] == 'fr_FR' and not meta.get('robots')
    assert meta['og:image'].endswith('.jpg') and meta['og:image:width'] and meta['og:image:height']
    seen.update(assets)
    return {'referencesLocales': local, 'sourcesExternes': len(outbound), 'images': assets,
            'tableaux': len(tables), 'sections': len(SECTIONS_ATLAS if route == ATLAS else SECTIONS)}


def main(final, dest):
    book = read('docs/pages.json')
    sources = read('docs/sources.json')['sources']
    assets = inventory()
    planned = {p['route']: p for p in book['pages']}
    pubs = {route for route, p in planned.items() if p['etat'] in PUBLISHED}
    assert book['total'] == len(planned) == len(book['pages']) == 86
    assert book['publiees'] == len(pubs) >= 17
    assert set(PAGES) <= pubs, 'les 14 routes de la phase 4 doivent être publiées'
    assert all(set(p['sourcesDeDepart']) <= sources.keys() for p in planned.values())
    # Contrôle cumulatif : tout HTML sur disque est une route planifiée ;
    # les routes publiées et les routes rendues mais pas encore publiées
    # sont admises tant que la phase correspondante n'est pas close.
    assert set(assets['html']) <= {'atelier/index.html', *planned}
    assert set(assets['html']) - {'atelier/index.html', *pubs} <= set(planned)
    assert len(assets['jpg']) >= 41 and len(assets['mp3']) == 8
    ignores = {'node_modules', '.git', '.cache', '.venv', '__pycache__'}
    forbidden = {'.jpeg', '.png', '.svg', '.webp', '.gif', '.zip', '.pdf', '.wav', '.ogg', '.aac', '.flac', '.m4a'}
    intrus = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and p.suffix.lower() in forbidden and not ignores.intersection(p.relative_to(ROOT).parts)]
    assert not intrus, intrus

    # Les fragments et le manifeste sont la source reproductible.
    manifeste = read('templates/cartes-phase-4.json')
    assert len(manifeste['fiches']) == 13 and manifeste['hub']['route'] == ATLAS
    for fragment in sorted((ROOT / 'templates/cartes').glob('*.html.part')):
        assert fragment.read_text(encoding='utf-8').strip(), fragment.name

    seen = {}
    allowed = {'atelier/index.html', *pubs}
    urls = sorted({urldefrag(s['url'])[0] for s in sources.values()})
    refs = {route: check_html(route, allowed, urls, seen) for route in PAGES}
    for route in PAGES:
        assert sorted(refs[route]['images']) == sorted(planned[route]['mediasEffectifs']), route
    # Les 20 JPG de la phase 4 sont tous référencés, chacun au moins une fois.
    medias_p4 = sorted({m for route in PAGES for m in refs[route]['images']})
    assert len(medias_p4) == 42, medias_p4
    assert all(m.startswith('images/maps/') for m in medias_p4)
    assert all(0 < seen[m]['octets'] < 600000 for m in medias_p4)

    # Cohérence avec les données de jeu.
    donnees = {lieu['slug']: lieu for lieu in read('js/data/maps.json')['lieux']}
    assert len(donnees) == 13
    total_sorties = sum(len(lieu['sorties']) for lieu in donnees.values())
    total_transits = sum(len(lieu['transits']) for lieu in donnees.values())
    total_boss = sum(len(lieu['boss']) for lieu in donnees.values())
    total_cles = sum(len(lieu.get('clesWiki') or []) for lieu in donnees.values())
    assert total_sorties == 119 and total_transits == 29 and total_boss == 48 and total_cles == 230
    for slug in LIEUX:
        assert slug in donnees and donnees[slug]['dureeMinutes'] == DUREES[slug], slug
        route = f'pages/maps/{slug}.html'
        html = (ROOT / route).read_text(encoding='utf-8')
        for sortie in donnees[slug]['sorties']:
            assert escape(sortie['nom']) in html, (slug, sortie['nom'])
            if sortie.get('libelleJeu'):
                assert escape(sortie['libelleJeu']) in html, (slug, sortie['libelleJeu'])
    assert sum(len(lieu.get('variantes') or []) for lieu in donnees.values()) == 6

    # Atlas : grille complète, comparatif et transits.
    atlas_html = (ROOT / ATLAS).read_text(encoding='utf-8')
    assert atlas_html.count('data-atlas-card') == 13
    assert 'data-compare-data' in atlas_html and 'data-compare-grid' in atlas_html
    comparatif = json.loads(re.search(r'<script type="application/json" data-compare-data>(.*?)</script>', atlas_html, re.S)[1])
    assert len(comparatif) == 13
    assert {row['slug'] for row in comparatif} == set(donnees)
    for row in comparatif:
        assert row['sortiesPmc'] + row['sortiesScav'] + row['sortiesPartagees'] == len(donnees[row['slug']]['sorties'])

    # Index de recherche.
    index = read('js/data/search-index.json')
    entries = index['entrees']
    tally = Counter(row['etat'] for row in entries)
    assert index['routesPlanifiees'] == 86 and index['routesPubliees'] == len(pubs)
    assert tally['publiee'] == len(pubs) and tally['planifiee'] == 86 - len(pubs)
    assert tally['accueil'] == 6 and tally['atelier'] == 8
    assert tally['dossier'] == 19, tally
    for row in entries:
        if row['etat'] == 'planifiee':
            assert row['url'] is None, row
            continue
        target = check_link(row['url'], HOME)
        assert target.relative_to(ROOT).as_posix() in allowed, row
    assert sum(row['etat'] == 'publiee' and row['url'] in PAGES for row in entries) == 14

    # Accueil : lien vers l'atlas et compteurs à jour.
    home = HOME.read_text(encoding='utf-8')
    assert 'href="./pages/maps/index.html"' in home
    assert re.search(r'data-count="published">%d<' % len(pubs), home)
    assert re.search(r'data-count="planned">86<', home)

    # Reproductibilité du rendu.
    renderers = []
    for script in ('rendre_cartes.py', 'rendre_dossiers.py', 'rendre_accueil.py'):
        run = subprocess.run([sys.executable, 'scripts/' + script, '--check'], capture_output=True, text=True, check=True, cwd=ROOT)
        renderers.extend(run.stdout.strip().splitlines())

    counts = {'pagesPlanifiees': 86, 'pagesGenerees': len(pubs), 'pagesHtmlTechniques': 1,
              'imagesCreees': len(assets['jpg']), 'audiosCrees': len(assets['mp3'])}
    if final:
        w = read('workflow.json')
        m = read('state_machine.json')['instantane']
        assert w['statut'] == m['etat'] in ('ATTENTE_CONTINUE', 'ATTENTE_LOT')
        assert w['compteurs'] == m['compteurs'] == counts
        assert 'PHASE_4' in w['phasesTerminees'] == m['phasesTerminees']
        assert m['dernierePhaseTerminee'] in m['phasesTerminees']
        phase = {p['id']: p for p in w['phases']}
        assert phase['PHASE_4']['statut'] == 'TERMINEE'
        assert phase['PHASE_4']['lotMedia'] == {'imagesJpg': 42, 'audiosMp3': 0}
        assert phase['PHASE_4']['pagesPubliees'] == 14
        assert all(read(report)['statut'] == 'OK' for report in BROWSER_REPORTS)
        assert set(w['livrables']['pages']) == pubs
        assert sorted(w['livrables']['imagesJpg']) == assets['jpg']
        assert sorted(w['livrables']['audiosMp3']) == assets['mp3']
        for category, files in w['livrables'].items():
            # Le rapport statique de cette phase est produit par ce contrôle : il peut manquer au premier passage.
            attendus = [path for path in files if path != (dest or STATIC_REPORT)]
            assert len(files) == len(set(files)), category
            assert all((ROOT / path).is_file() for path in attendus), (category, [p for p in attendus if not (ROOT / p).is_file()])
    out = {'statut': 'OK', 'controleCloture': final, 'compteurs': counts,
           'routes': {route: {k: v for k, v in refs[route].items() if k != 'images'} for route in PAGES},
           'mediasPhase4': {m: seen[m] for m in medias_p4},
           'index': dict(tally), 'sourcesRegistre': len(sources),
           'donneesJeu': {'sorties': total_sorties, 'transits': total_transits,
                          'rencontres': total_boss, 'cles': total_cles, 'variantes': 6},
           'reproductibilite': renderers}
    data = json.dumps(out, ensure_ascii=False, indent=2) + '\n'
    if dest:
        (ROOT / dest).write_text(data, encoding='utf-8')
    print(data, end='')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--final', action='store_true', help='contrôler aussi les compteurs, les rapports et l’état de clôture')
    cli.add_argument('--out', help='chemin du rapport JSON')
    args = cli.parse_args()
    main(args.final, args.out)
