#!/usr/bin/env python3
"""Régénère les dérivés publics (recherche et échantillon atelier), sans réseau."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def write(path, data, module=False):
    text = json.dumps(data, ensure_ascii=False, indent=2 if not module else None)
    (ROOT / path).write_text(('/* Produit par scripts/generer_socle.py. */\nexport default ' if module else '') + text + (';\n' if module else '\n'), encoding='utf-8')


def main():
    book = read('docs/pages.json')['pages']
    sections = read('js/data/sections-atelier.json')
    groups = {'regular': 'PvP Zone', 'pve': 'PvE Zone', 'pvp-season': 'Seasonal'}
    sample = {'dateUtc': '2026-11-18', 'libelles': groups, 'source': 'https://json.tarkov.dev/endpoints', 'cartes': []}
    allowed = {'customs': 'plein-air', 'factory': 'interieur', 'woods': 'plein-air', 'icebreaker': 'scenario', 'ground-zero': 'plein-air', 'interchange': 'interieur'}
    maps = {mode: {row['normalizedName']: row for row in read(f'recherche/tarkov-dev/{mode}/maps-overview.json')['rows']} for mode in groups}
    for slug, family in allowed.items():
        rows = {mode: maps[mode][slug] for mode in groups if slug in maps[mode]}
        if not rows:
            continue
        base = next(iter(rows.values()))
        sample['cartes'].append({'id': slug, 'nom': base['name'], 'nomFr': base['nameFr'], 'famille': family, 'modes': {
            mode: {'duree': row['raidDuration'], 'extracts': row['tailleDesListesSource']['extracts'],
                   'transits': row['tailleDesListesSource']['transits']} for mode, row in rows.items()}})
    write('js/data/maps-sample.mjs', sample, module=True)

    curated = {
        'getting-started': ['débutant', 'guide débutant', 'raid', 'commencer', 'nouveau', 'pve', 'paramètres'],
        'lore': ['Norvinsk', 'lore', 'histoire', 'TerraGroup', 'univers', 'chronologie', 'Contract Wars'],
        'spt-tushonka': ['spt', 'sp-tushonka', 'solo', 'single player', 'sp tarkov', 'mods', 'Fika'],
        'ammo': ['ballistique', 'munitions', 'calibre', 'pénétration', 'dégâts', 'tableau'],
        'maps': ['cartes', 'atlas', 'extract', 'extraction', 'lieux', 'raid'],
        'patch-notes': ['changelog', 'historique', '1.3.0.0', '1.3.0.2', 'patchs', 'mises à jour', 'unity'],
        'quests': ['quêtes', 'tasks', 'objectifs', 'Kappa', 'tracker'],
        'hideout': ['planque', 'abri', 'craft', 'fabrication', 'stations'],
        'traders': ['marchands', 'traders', 'réputation', 'loyalty level', 'barter'],
        'events': ['événements', 'blackout', 'halloween', 'kord breach', 'full speed ahead', 'duckov', 'wild wild woods', 'tarkov city'],
    }
    entries = [{'titre': s['titre'], 'description': s['description'], 'termes': s['termes'], 'etat': 'atelier',
                'url': f'atelier/#{s["id"]}'} for s in sections]
    home = next((page for page in book if page['route'] == 'index.html' and page['etat'] in ('PUBLIEE', 'PUBLIÉE')), None)
    home_sections = ROOT / 'js/data/sections-accueil.json'
    if home and home_sections.is_file():
        repere = read('js/data/sections-accueil.json')
        entries = [{'titre': r['titre'], 'description': r['description'], 'termes': r['termes'], 'etat': 'accueil',
                    'url': f'./#{r["id"]}'} for r in repere] + entries
    for page in book:
        route = page['route']
        slug = route.removesuffix('.html').removesuffix('/index').split('/')[-1]
        group = route.split('/')[1] if route.count('/') == 2 else slug
        terms = [part.replace('-', ' ') for part in (group, slug) if re.fullmatch(r'[\w-]+', part)]
        terms += curated.get(slug, [])
        for c in sample['cartes']:
            if c['id'] == slug:
                terms.extend((c['nom'], c['nomFr']))
        is_published = page['etat'] in ('PUBLIEE', 'PUBLIÉE')
        if is_published and not (ROOT / route).is_file():
            raise ValueError(f'Manifeste publié sans fichier : {route}')
        entries.append({'titre': page['titre'], 'description': page['angleEditorial'], 'termes': list(dict.fromkeys(terms)),
                        'etat': 'publiee' if is_published else 'planifiee',
                        'phase': int(page['phase'].split('_')[1]), 'url': route if is_published else None})
    published = {e['url']: e for e in entries if e['etat'] == 'publiee'}
    dossiers = ROOT / 'js/data/sections-dossiers.json'
    if dossiers.is_file():
        for section in read('js/data/sections-dossiers.json'):
            route = section['route']
            if route not in published:
                continue
            anchor = section['id']
            if not re.fullmatch(r'[a-z0-9-]+', anchor) or not re.search(r'id="' + re.escape(anchor) + r'"', (ROOT / route).read_text(encoding='utf-8')):
                raise ValueError(f'Repère de dossier sans section : {route}#{anchor}')
            entries.append({'titre':section['titre'], 'description':section['description'], 'termes':section['termes'],
                            'etat':'dossier', 'url':f'{route}#{anchor}', 'phase':published[route]['phase']})
    write('js/data/search-index.json', {'schemaVersion': 1, 'routesPlanifiees': len(book),
                                      'routesPubliees': sum(e['etat'] == 'publiee' for e in entries), 'entrees': entries})
    anchors = sum(entry['etat'] == 'accueil' for entry in entries)
    repere_count = sum(entry['etat'] == 'dossier' for entry in entries)
    print(f'{len(entries)} entrées indexées ({len(book)} routes, {anchors} repères accueil, {len(sections)} atelier, {repere_count} guides), '
          f'{len(sample["cartes"])} cartes de démonstration.')


if __name__ == '__main__':
    main()
