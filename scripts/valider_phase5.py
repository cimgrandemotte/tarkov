#!/usr/bin/env python3
"""Contrôles statiques de la phase 5 : arsenal, dix familles, balistique et tableau.

Vérifie le HTML produit, les liens, les ancres, les tableaux, les médias,
le JSON-LD, la cohérence avec js/data/weapons.json, js/data/ammo.json et
js/data/weapon-pieces.json, l'index de recherche, le budget média et la
reproductibilité du rendu.
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

HUB_ARMES = 'pages/weapons/index.html'
HUB_AMMO = 'pages/ammo/index.html'
OUTIL = 'pages/ammo/ammo-chart.html'
FAMILLES = ['assault-rifles', 'smgs', 'shotguns', 'sniper-rifles', 'dmrs', 'lmgs',
            'pistols', 'melee', 'grenade-launchers', 'weapon-mods']
PAGES = [HUB_ARMES, *[f'pages/weapons/{slug}.html' for slug in FAMILLES], HUB_AMMO, OUTIL]
STATIC_REPORT = 'docs/validation-phase-5-statique.json'
SECTIONS = {
    HUB_ARMES: {'perimetre', 'familles', 'catalogue', 'comparateur', 'selections', 'sources'},
    HUB_AMMO: {'reperes', 'regle', 'statistiques', 'classes', 'calibres', 'achats', 'sources'},
    OUTIL: {'reperes', 'nuage', 'tableau', 'method', 'sources'},
}
SECTIONS_FAMILLE = {'reperes', 'catalogue', 'presets', 'acquisition', 'conduite', 'sources'}
EFFECTIFS = {'assault-rifles': 63, 'smgs': 23, 'shotguns': 16, 'sniper-rifles': 10, 'dmrs': 11,
             'lmgs': 8, 'pistols': 31, 'melee': 27, 'grenade-launchers': 10, 'weapon-mods': 0}


def sections_de(route):
    if route in SECTIONS:
        return SECTIONS[route]
    return SECTIONS_FAMILLE


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
    tables = re.findall(r'<table class="armes-table"[^>]*>(.*?)</table>', html, re.S)
    # La famille de mêlée n'a ni preset ni vente en magasin : deux tableaux y sont volontairement vides.
    minimum = {'pages/weapons/index.html': 5, 'pages/ammo/ammo-chart.html': 1,
               'pages/weapons/melee.html': 1}.get(route, 2)
    assert len(tables) >= minimum, (route, len(tables))
    for table in tables:
        assert '<caption>' in table, route
        assert '<th scope="col">' in table, route
    wraps = re.findall(r'<div class="table-wrap"([^>]*)>', html)
    assert wraps and all('tabindex="0"' in w and 'role="group"' in w for w in wraps), route
    # Sections focusables pour les ancres du sommaire.
    for section in sections_de(route):
        assert f'id="{section}" tabindex="-1"' in html, (route, section)
    # Données structurées et métadonnées.
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])
    meta = {a.get('name', a.get('property')): a.get('content') for tag, a in tags if tag == 'meta'}
    assert ld['@type'] in ('Article', 'CollectionPage') and ld['inLanguage'] == 'fr-FR'
    assert 120 <= len(ld['description']) <= 170, len(ld['description'])
    assert ld['description'] == meta['description'] == meta['og:description'] == meta['twitter:description']
    assert meta['og:locale'] == 'fr_FR' and not meta.get('robots')
    assert meta['og:image'].endswith('.jpg') and meta['og:image:width'] and meta['og:image:height']
    seen.update(assets)
    return {'referencesLocales': local, 'sourcesExternes': len(outbound), 'images': assets,
            'tableaux': len(tables), 'sections': len(sections_de(route))}


def main(final, dest):
    book = read('docs/pages.json')
    sources = read('docs/sources.json')['sources']
    assets = inventory()
    planned = {p['route']: p for p in book['pages']}
    pubs = {route for route, p in planned.items() if p['etat'] in PUBLISHED}
    assert book['total'] == len(planned) == len(book['pages']) == 86
    # Contrôle cumulative : le compteur du plan reflète toutes les routes
    # publiées à ce stade, et les 13 routes de la phase 5 sont dedans.
    assert book['publiees'] == len(pubs)
    assert set(PAGES) <= pubs, 'les 13 routes de la phase 5 doivent être publiées'
    assert all(set(p['sourcesDeDepart']) <= sources.keys() for p in planned.values())
    # Contrôle cumulatif : tout HTML sur disque est une route planifiée ;
    # les routes publiées et les routes rendues mais pas encore publiées
    # sont admises tant que la phase correspondante n'est pas close.
    assert set(assets['html']) <= {'atelier/index.html', *planned}
    assert set(assets['html']) - {'atelier/index.html', *pubs} <= set(planned)
    assert len(assets['jpg']) >= 54 and len(assets['mp3']) == 8
    ignores = {'node_modules', '.git', '.cache', '.venv', '__pycache__'}
    forbidden = {'.jpeg', '.png', '.svg', '.webp', '.gif', '.zip', '.pdf', '.wav', '.ogg', '.aac', '.flac', '.m4a'}
    intrus = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and p.suffix.lower() in forbidden and not ignores.intersection(p.relative_to(ROOT).parts)]
    assert not intrus, intrus

    # Les fragments et le manifeste sont la source reproductible.
    manifeste = read('templates/armes-phase-5.json')
    assert len(manifeste['families']) == 10 and manifeste['hub']['route'] == HUB_ARMES
    assert len(list((ROOT / 'templates/armes').glob('*.html.part'))) == 13
    for fragment in sorted((ROOT / 'templates/armes').glob('*.html.part')):
        assert fragment.read_text(encoding='utf-8').strip(), fragment.name

    seen = {}
    allowed = {'atelier/index.html', *pubs}
    urls = sorted({urldefrag(s['url'])[0] for s in sources.values()})
    refs = {route: check_html(route, allowed, urls, seen) for route in PAGES}
    for route in PAGES:
        assert sorted(refs[route]['images']) == sorted(planned[route]['mediasEffectifs']), route
    # Les 13 JPG de la phase 5 sont tous référencés, chacun au moins une fois.
    medias_p5 = sorted({m for route in PAGES for m in refs[route]['images']})
    assert len(medias_p5) == 410, medias_p5
    assert all(m.startswith(('images/weapons/', 'images/items/')) for m in medias_p5)
    assert all(0 < seen[m]['octets'] < 600000 for m in medias_p5)

    # Cohérence avec les données de jeu.
    armes = read('js/data/weapons.json')['armes']
    munitions = read('js/data/ammo.json')
    pieces = read('js/data/weapon-pieces.json')['pieces']
    assert len(armes) == 199 and len(munitions['munitions']) == 200 and len(pieces) == 2283
    assert len(munitions['calibres']) == 31 and len(munitions['grenades']) == 7
    assert sum(len(a['presets']) for a in armes) == 401
    familles = Counter(a['famille'] for a in armes)
    assert len(familles) == 9
    for slug, effectif in EFFECTIFS.items():
        route = f'pages/weapons/{slug}.html'
        html = (ROOT / route).read_text(encoding='utf-8')
        if slug == 'weapon-mods':
            tables = re.findall(r'<table class="armes-table"[^>]*>(.*?)</table>', html, re.S)
            assert len(tables) == 2, slug
            assert tables[0].count('<tr') == 24, slug          # vingt-trois emplacements et l'en-tête
            assert tables[1].count('<tr') == 121, slug         # cent vingt pièces et l'en-tête
            continue
        assert len(familles) and effectif > 0
        bloc = re.search(r'<table class="armes-table"[^>]*>(.*?)</table>', html, re.S)
        lignes = bloc.group(1).count('<tr')
        assert lignes - 1 == effectif, (slug, lignes, effectif)

    # Hub arsenal : catalogue complet, familles, comparateur.
    hub_html = (ROOT / HUB_ARMES).read_text(encoding='utf-8')
    assert hub_html.count('data-armes-card') == 10
    assert 'data-armes-compare-a' in hub_html and 'data-armes-compare-c' in hub_html
    catalogue = json.loads(re.search(r'id="armes-donnees">(.*?)</script>', hub_html, re.S)[1])
    assert len(catalogue) == 199
    assert {row['id'] for row in catalogue} == {a['id'] for a in armes}
    for row in catalogue:
        source = next(a for a in armes if a['id'] == row['id'])
        assert row['nom'] == source['nom'] and row['calibre'] == source['calibre']
        assert row['nbPresets'] == len(source['presets'])

    # Tableau balistique : deux cents lignes et le même jeu de cartouches.
    outil_html = (ROOT / OUTIL).read_text(encoding='utf-8')
    assert outil_html.count('data-nom=') == 200
    assert 'id="armes-nuage"' in outil_html
    donnees = json.loads(re.search(r'id="munitions-donnees">(.*?)</script>', outil_html, re.S)[1])
    assert len(donnees) == 200
    assert {row['id'] for row in donnees} == {m['id'] for m in munitions['munitions']}

    # Hub munitions : classes, calibres, achats et grenades.
    ammo_html = (ROOT / HUB_AMMO).read_text(encoding='utf-8')
    assert 'data-calibre=' in ammo_html and '26 x 75 mm' in ammo_html
    assert sum(1 for m in munitions['munitions'] if m['disponibleChezMarchand']) == 154
    assert sum(1 for m in munitions['munitions'] if not m['disponibleChezMarchand']) == 46

    # Index de recherche.
    index = read('js/data/search-index.json')
    entries = index['entrees']
    tally = Counter(row['etat'] for row in entries)
    # Contrôle cumulative : le compteur de l'index reflète toutes les routes
    # publiées à ce stade, et les 13 routes de la phase 5 sont indexées.
    assert index['routesPlanifiees'] == 86 and index['routesPubliees'] == len(pubs)
    assert tally['publiee'] == len(pubs) and tally['planifiee'] == 86 - len(pubs)
    assert tally['accueil'] == 6 and tally['atelier'] == 8 and tally['dossier'] == 19, tally
    for row in entries:
        if row['etat'] == 'planifiee':
            assert row['url'] is None, row
            continue
        target = check_link(row['url'], HOME)
        assert target.relative_to(ROOT).as_posix() in allowed, row
    assert sum(row['etat'] == 'publiee' and row['url'] in PAGES for row in entries) == 13

    # Accueil : lien vers l'arsenal et compteurs à jour.
    home = HOME.read_text(encoding='utf-8')
    assert 'href="./pages/weapons/index.html"' in home
    assert re.search(r'data-count="published">' + str(len(pubs)) + '<', home)
    assert re.search(r'data-count="planned">86<', home)

    # Reproductibilité du rendu.
    renderers = []
    for script in ('rendre_armes.py', 'rendre_cartes.py', 'rendre_dossiers.py', 'rendre_accueil.py'):
        run = subprocess.run([sys.executable, 'scripts/' + script, '--check'], capture_output=True, text=True, check=True, cwd=ROOT)
        renderers.extend(run.stdout.strip().splitlines())

    counts = {'pagesPlanifiees': 86, 'pagesGenerees': len(pubs), 'pagesHtmlTechniques': 1,
              'imagesCreees': len(assets['jpg']), 'audiosCrees': len(assets['mp3'])}
    if final:
        w = read('workflow.json')
        m = read('state_machine.json')['instantane']
        assert w['statut'] == m['etat'] in ('ATTENTE_CONTINUE', 'ATTENTE_LOT')
        assert w['phaseCourante'] == m['phase']
        # La phase 5 est close et dans la liste des phases terminees ;
        # la phase la plus récemment close peut être une phase ultérieure.
        assert 'PHASE_5' in m['phasesTerminees']
        assert m['dernierePhaseTerminee'] in m['phasesTerminees']
        assert w['compteurs'] == m['compteurs'] == counts
        # Contrôle cumulative : les six phases jusqu'à P5 sont closes, et les
        # listes workflow et machine à états concordent. Des phases ultérieures
        # peuvent s'y ajouter.
        assert w['phasesTerminees'] == m['phasesTerminees']
        assert w['phasesTerminees'][:6] == ['PHASE_0', 'PHASE_1', 'PHASE_2', 'PHASE_3', 'PHASE_4', 'PHASE_5']
        # La phase 5 est close : la phase courante est la phase suivante en cours.
        assert w['prochainePhase'] == m['prochainePhase']
        assert w['phaseCourante'] == m['phase']
        phase = {p['id']: p for p in w['phases']}
        assert phase['PHASE_5']['statut'] == 'TERMINEE'
        assert phase['PHASE_5']['lotMedia'] == {'imagesJpg': 381, 'audiosMp3': 0}
        assert phase['PHASE_5']['pagesPubliees'] == 13
        assert set(w['livrables']['pages']) == pubs
        assert sorted(w['livrables']['imagesJpg']) == assets['jpg']
        assert sorted(w['livrables']['audiosMp3']) == assets['mp3']
        for category, files in w['livrables'].items():
            attendus = [path for path in files if path != (dest or STATIC_REPORT)]
            assert len(files) == len(set(files)), category
            assert all((ROOT / path).is_file() for path in attendus), (category, [p for p in attendus if not (ROOT / p).is_file()])
    out = {'statut': 'OK', 'controleCloture': final, 'compteurs': counts,
           'routes': {route: {k: v for k, v in refs[route].items() if k != 'images'} for route in PAGES},
           'mediasPhase5': {m: seen[m] for m in medias_p5},
           'index': dict(tally), 'sourcesRegistre': len(sources),
           'donneesJeu': {'armes': len(armes), 'pieces': len(pieces),
                          'munitions': len(munitions['munitions']), 'calibres': len(munitions['calibres']),
                          'grenades': len(munitions['grenades']), 'presets': sum(len(a['presets']) for a in armes),
                          'familles': len(familles)},
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
