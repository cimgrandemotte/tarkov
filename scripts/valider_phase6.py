#!/usr/bin/env python3
"""Contrôles statiques de la phase 6 : armures, comparaison et boss.

Vérifie le HTML produit, les liens, les ancres, les tableaux, les médias,
le JSON-LD, la cohérence avec js/data/armor.json et js/data/bosses.json,
l'index de recherche, le budget média et la reproductibilité du rendu.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
import re
import subprocess
import sys
from urllib.parse import urldefrag, urlsplit

from PIL import Image
from valider_phase2 import ROOT, HOME, PUBLISHED, check_link, inventory, parse, read

HUB_ARMOR = 'pages/armor/index.html'
GUIDES = ['body-armor', 'helmets', 'rigs']
OUTIL = 'pages/armor/armor-chart.html'
HUB_BOSS = 'pages/bosses/index.html'
BOSSES = ['reshala', 'killa', 'shturman', 'glukhar', 'sanitar', 'tagilla', 'kaban',
          'kollontay', 'zryachiy', 'partisan', 'cultist-priest', 'the-goons',
          'shadow-of-tagilla', 'the-wedge']
PAGES = [HUB_ARMOR, *[f'pages/armor/{slug}.html' for slug in GUIDES], OUTIL,
         HUB_BOSS, *[f'pages/bosses/{slug}.html' for slug in BOSSES]]
STATIC_REPORT = 'docs/validation-phase-6-statique.json'
SECTIONS_ARMOR = {'reperes', 'modele', 'materiaux', 'classes', 'catalogue', 'plaques',
                   'conduite', 'sources'}
SECTIONS_BOSS = {'reperes', 'pv', 'apparitions', 'escortes', 'equipement', 'butin',
                 'communaute', 'sources'}
# Le hub est une page agrégée ; les fiches individuelles portent les sections de données.
SECTIONS_HUB_BOSS = {'reperes', 'grille', 'matrice', 'pv', 'horsfiche', 'suivis', 'conduite', 'sources'}
EFFECTIFS = {'body-armor': 87, 'helmets': 119, 'rigs': 105}
PV_BOSS = {'reshala': 752, 'killa': 890, 'shturman': 812, 'glukhar': 1010, 'sanitar': 1270,
           'tagilla': 1220, 'kaban': 1300, 'kollontay': 1055, 'zryachiy': 1655,
           'partisan': 950, 'cultist-priest': 850, 'the-goons': 1120,
           'shadow-of-tagilla': 1305, 'the-wedge': 750}
APPARITIONS_BOSS = {'reshala': 6, 'killa': 6, 'shturman': 3, 'glukhar': 6, 'sanitar': 6,
                    'tagilla': 3, 'kaban': 3, 'kollontay': 3, 'zryachiy': 3,
                    'partisan': 12, 'cultist-priest': 15, 'the-goons': 15,
                    'shadow-of-tagilla': 3, 'the-wedge': 5}


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
    tables = re.findall(r'<table class="armures-table"[^>]*>(.*?)</table>', html, re.S)
    assert len(tables) >= 2, (route, len(tables))
    for table in tables:
        assert '<caption>' in table, route
        assert '<th scope="col">' in table, route
    wraps = re.findall(r'<div class="table-wrap"([^>]*)>', html)
    assert wraps and all('tabindex="0"' in w and 'role="group"' in w for w in wraps), route
    sections = SECTIONS_ARMOR if '/armor/' in route else (SECTIONS_HUB_BOSS if route == HUB_BOSS else SECTIONS_BOSS)
    for section in sections:
        assert f'id="{section}" tabindex="-1"' in html, (route, section)
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])
    meta = {a.get('name', a.get('property')): a.get('content') for tag, a in tags if tag == 'meta'}
    assert ld['@type'] in ('Article', 'CollectionPage') and ld['inLanguage'] == 'fr-FR'
    assert 120 <= len(ld['description']) <= 170, len(ld['description'])
    assert ld['description'] == meta['description'] == meta['og:description'] == meta['twitter:description']
    assert meta['og:locale'] == 'fr_FR' and not meta.get('robots')
    assert meta['og:image'].endswith('.jpg') and meta['og:image:width'] and meta['og:image:height']
    seen.update(assets)
    return {'referencesLocales': local, 'sourcesExternes': len(outbound), 'images': assets,
            'tableaux': len(tables), 'sections': len(sections)}


def main(final, dest):
    book = read('docs/pages.json')
    sources = read('docs/sources.json')['sources']
    assets = inventory()
    planned = {p['route']: p for p in book['pages']}
    pubs = {route for route, p in planned.items() if p['etat'] in PUBLISHED}
    assert book['total'] == len(planned) == len(book['pages']) == 86
    # En mode non final, la phase est encore en cours : les routes P6 sont rendues
    # sur disque mais pas encore publiées. La règle durable est que tout HTML
    # existant correspond à une route planifiée.
    phase_en_cours = 'PHASE_6'
    rendu_p6 = {route for route in PAGES if route not in pubs}
    attendu_html = {'atelier/index.html', *pubs, *rendu_p6}
    assert all(set(p['sourcesDeDepart']) <= sources.keys() for p in planned.values())
    assert set(assets['html']) <= attendu_html, sorted(set(assets['html']) - attendu_html)
    if final:
        assert book['publiees'] == len(pubs) == 51, book['publiees']
        assert set(PAGES) <= pubs, 'les 20 routes de la phase 6 doivent être publiées'
        assert set(assets['html']) == {'atelier/index.html', *pubs}
    else:
        assert book['publiees'] == len(pubs)
    assert set(PAGES) <= attendu_html, 'les 20 routes de la phase 6 doivent exister'
    ignores = {'node_modules', '.git', '.cache', '.venv', '__pycache__'}
    forbidden = {'.jpeg', '.png', '.svg', '.webp', '.gif', '.zip', '.pdf', '.wav', '.ogg', '.aac', '.flac', '.m4a'}
    intrus = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and p.suffix.lower() in forbidden and not ignores.intersection(p.relative_to(ROOT).parts)]
    assert not intrus, intrus

    manifeste = read('templates/armures-phase-6.json')
    assert len(manifeste['bosses']) == 14
    assert len(list((ROOT / 'templates/armures').glob('*.html.part'))) == 5
    for fragment in sorted((ROOT / 'templates/armures').glob('*.html.part')):
        assert fragment.read_text(encoding='utf-8').strip(), fragment.name

    seen = {}
    allowed = {'atelier/index.html', *pubs, *rendu_p6}
    urls = sorted({urldefrag(s['url'])[0] for s in sources.values()})
    refs = {route: check_html(route, allowed, urls, seen) for route in PAGES}
    for route in PAGES:
        medias_declarees = planned[route].get('mediasEffectifs')
        if medias_declarees is None:
            # Route rendue mais pas encore publiée : les médias cités dans le HTML
            # sont le média réel ; le plan n'a pas encore son inventaire déclamé.
            continue
        assert sorted(refs[route]['images']) == sorted(medias_declarees), route
    medias_p6 = sorted({m for route in PAGES for m in refs[route]['images']})
    assert all(m.startswith(('images/armor/', 'images/bosses/', 'images/items/')) for m in medias_p6)
    assert all(0 < seen[m]['octets'] < 600000 for m in medias_p6)
    assert len(medias_p6) == len(set(medias_p6))
    if final:
        assert len(medias_p6) == 408, medias_p6

    armor = read('js/data/armor.json')
    bosses = read('js/data/bosses.json')
    pieces = armor['pieces']
    assert len(pieces) == 390 and len(armor['materiaux']) == 8 and len(armor['plaques']) == 38
    par_categorie = Counter(p['categorie'] for p in pieces)
    assert par_categorie == {'Gilet tactique': 105, 'Gilet pare-balles': 49, 'Casque': 93,
                              'Masque': 20, 'Plaque de blindage': 38, 'Accessoire blindé': 79,
                              'Protection oculaire': 6}, par_categorie
    assert armor['statistiques']['avecPlaques'] == 97
    assert len(bosses['fiches']) == 14 and bosses['statistiques']['mobsExport'] == 48
    assert bosses['statistiques']['horsFiche'] == 18 and bosses['statistiques']['apparitions'] == 89
    par_slug = {f['slug']: f for f in bosses['fiches']}
    for slug in BOSSES:
        assert par_slug[slug]['pvTotal'] == PV_BOSS[slug], slug
        assert len(par_slug[slug]['apparitions']) == APPARITIONS_BOSS[slug], slug

    # Catalogue d'armure : trois cent quatre-vingt-dix lignes, une par pièce.
    hub_html = (ROOT / HUB_ARMOR).read_text(encoding='utf-8')
    assert hub_html.count('data-nom=') == 390
    for categorie, effectif in par_categorie.items():
        assert effectif > 0, categorie
    # Le comparateur embarque les mêmes pièces que le catalogue.
    outil_html = (ROOT / OUTIL).read_text(encoding='utf-8')
    donnees = json.loads(re.search(r'<script type="application/json" data-armures-json>(.*?)</script>',
                                   outil_html, re.S)[1])
    assert len(donnees) == 390
    assert {row['id'] for row in donnees} == {p['id'] for p in pieces}
    assert outil_html.count('data-nom=') == 390
    assert 'data-armures-compare-slot="1"' in outil_html
    assert 'data-armures-compare-slot="3"' in outil_html
    # Les guides de phase 6 ne montrent que leur catégorie.
    for slug, effectif in EFFECTIFS.items():
        html = (ROOT / f'pages/armor/{slug}.html').read_text(encoding='utf-8')
        tables = re.findall(r'<table class="armures-table"[^>]*>.*?</table>', html, re.S)
        lignes = max(bloc.count('<tr') for bloc in tables)
        assert lignes - 1 == effectif, (slug, lignes, effectif)

    # Hub boss : quatorze cartes, matrice et hors-fiche.
    boss_html = (ROOT / HUB_BOSS).read_text(encoding='utf-8')
    assert boss_html.count('data-boss-card') == 14
    assert boss_html.count('data-boss-famille') == 6
    assert boss_html.count('data-nom=') == 18
    # Chaque fiche de boss donne son total de points de vie et ses apparitions.
    for slug in BOSSES:
        html = (ROOT / f'pages/bosses/{slug}.html').read_text(encoding='utf-8')
        # Le formatage peut utiliser l'espace millier : on normalise avant de chercher.
        assert f'{PV_BOSS[slug]} PV' in html.replace('\u00a0', ' ') or f'{PV_BOSS[slug]}' in html.replace(' ', ''), slug
        assert 'id="communaute"' in html and 'id="sources"' in html, slug
        assert html.count('<li>') >= 3, slug
        # Les avis communautaires sont séparés des chiffres : ils occupent une section dédiée.
        assert re.search(r'id="communaute".*?id="sources"', html, re.S), slug

    # Index de recherche.
    index = read('js/data/search-index.json')
    entries = index['entrees']
    tally = Counter(row['etat'] for row in entries)
    assert index['routesPlanifiees'] == 86
    if final:
        assert index['routesPubliees'] == 51
        assert tally['publiee'] == 51 and tally['planifiee'] == 35
    else:
        assert index['routesPubliees'] == len(pubs), index['routesPubliees']
        assert tally['publiee'] == len(pubs)
    for row in entries:
        if row['etat'] == 'planifiee':
            assert row['url'] is None, row
            continue
        target = check_link(row['url'], HOME)
        assert target.relative_to(ROOT).as_posix() in allowed, row
    if final:
        assert sum(row['etat'] == 'publiee' and row['url'] in PAGES for row in entries) == 20
    else:
        assert sum(row['etat'] == 'publiee' and row['url'] in PAGES for row in entries) == 0

    # Accueil : liens et compteurs à jour.
    home = HOME.read_text(encoding='utf-8')
    assert re.search(r'data-count="published">' + str(len(pubs)) + '<', home)
    assert re.search(r'data-count="planned">86<', home)
    if final:
        # Les sauts de lecture vers les hubs armures et boss s'ajoutent à l'accueil
        # une fois les routes publiées.
        assert 'href="./pages/armor/index.html"' in home
        assert 'href="./pages/bosses/index.html"' in home

    # Reproductibilité du rendu.
    renderers = []
    for script in ('rendre_armures.py', 'rendre_armes.py', 'rendre_cartes.py',
                   'rendre_dossiers.py', 'rendre_accueil.py'):
        run = subprocess.run([sys.executable, 'scripts/' + script, '--check'], capture_output=True,
                             text=True, check=True, cwd=ROOT)
        renderers.extend(run.stdout.strip().splitlines())

    counts = {'pagesPlanifiees': 86, 'pagesGenerees': len(pubs), 'pagesHtmlTechniques': 1,
              'imagesCreees': len(assets['jpg']), 'audiosCrees': len(assets['mp3'])}
    if final:
        w = read('workflow.json')
        m = read('state_machine.json')['instantane']
        assert w['statut'] == m['etat'] == 'ATTENTE_CONTINUE'
        assert w['phaseCourante'] == m['phase'] == 'PHASE_6' and m['dernierePhaseTerminee'] == 'PHASE_6'
        assert w['compteurs'] == m['compteurs'] == counts
        assert w['phasesTerminees'] == m['phasesTerminees'] == ['PHASE_0', 'PHASE_1', 'PHASE_2',
                                                               'PHASE_3', 'PHASE_4', 'PHASE_5', 'PHASE_6']
        phase = {p['id']: p for p in w['phases']}
        assert phase['PHASE_6']['statut'] == 'TERMINEE'
        assert phase['PHASE_6']['lotMedia'] == {'imagesJpg': 402, 'audiosMp3': 0}
        assert phase['PHASE_6']['pagesPubliees'] == 20
        for category, files in w['livrables'].items():
            attendus = [path for path in files if path != (dest or STATIC_REPORT)]
            assert len(files) == len(set(files)), category
            assert all((ROOT / path).is_file() for path in attendus), category
    out = {'statut': 'OK', 'controleCloture': final,
           'publication': {'publiees': len(pubs), 'routesPhase6NonPubliees': sorted(rendu_p6)},
           'compteurs': counts,
           'routes': {route: {k: v for k, v in refs[route].items() if k != 'images'} for route in PAGES},
           'mediasPhase6': {m: seen[m] for m in medias_p6},
           'index': dict(tally), 'sourcesRegistre': len(sources),
           'donneesJeu': {'piecesArmure': len(pieces), 'materiaux': len(armor['materiaux']),
                          'plaques': len(armor['plaques']), 'piecesAvecPlaques': armor['statistiques']['avecPlaques'],
                          'fichesBoss': len(bosses['fiches']), 'mobsExport': bosses['statistiques']['mobsExport'],
                          'horsFiche': bosses['statistiques']['horsFiche'],
                          'apparitions': bosses['statistiques']['apparitions']},
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
