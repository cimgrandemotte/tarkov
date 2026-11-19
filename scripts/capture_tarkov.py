#!/usr/bin/env python3
"""Capture compacte et datée des exports publics Tarkov.dev ; aucune clé requise.

L'export est un jeu de données de recherche, pas le catalogue de production.
Les modes et les valeurs absentes sont conservés. Les listes de compatibilité
volumineuses (slots d'arme et grilles) seront importées au besoin à la phase 5.
"""

import argparse
import hashlib
import json
import re
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = 'https://json.tarkov.dev'
MODES = ('regular', 'pve', 'pvp-season')
FILENAMES = ('items', 'weapons', 'ammo', 'armor', 'maps-overview')
MAX_BYTES = 40 * 1024 * 1024
DEFENSIVE_TYPES = {'armor', 'helmet', 'rig', 'armorPlate'}
DEFENSIVE_PROPERTIES = {
    'ItemPropertiesArmor', 'ItemPropertiesArmorAttachment', 'ItemPropertiesChestRig',
    'ItemPropertiesHelmet',
}
TRADE_AND_PRICE = (
    'buyFromTrader', 'sellToTrader', 'lastLowPrice', 'avg24hPrice', 'low24hPrice',
    'high24hPrice', 'lastOfferCount', 'lastScan', 'minLevelForFlea',
)
TOKEN = re.compile(r'^[0-9a-f]{24}\s+(?:name|shortname|description)$', re.I)


def json_bytes(doc):
    return (json.dumps(doc, ensure_ascii=False, separators=(',', ':'), allow_nan=False) + '\n').encode()


def digest(content):
    return hashlib.sha256(content).hexdigest()


def load_source(endpoint_path, cache=None):
    url = f'{ENDPOINT}/{endpoint_path}'
    if cache:
        stem = endpoint_path.replace('/', '-')
        raw = (cache / f'{stem}.json').read_bytes()
        saved = json.loads((cache / f'{stem}.meta.json').read_text())
        if digest(raw) != saved['sha256'] or len(raw) != saved['size']:
            raise ValueError(f'Empreinte du cache incohérente : {url}')
        headers = saved
    else:
        request = Request(url, headers={'Accept': 'application/json', 'User-Agent': 'TarkovUltimateGuide/0.1'})
        with urlopen(request, timeout=25) as response:
            raw = response.read(MAX_BYTES + 1)
            headers = response.headers
    if len(raw) > MAX_BYTES:
        raise ValueError(f'Export supérieur au seuil de sécurité : {url}')
    doc = json.loads(raw)
    if not isinstance(doc, dict) or not doc.get('data'):
        raise ValueError(f'Export inattendu ou vide : {url}')
    provenance = {
        'url': url,
        'dateServeurHttp': headers.get('Date'),
        'derniereModificationHttp': headers.get('Last-Modified'),
        'etag': headers.get('ETag'),
        'octetsSource': len(raw),
        'sha256Source': digest(raw),
    }
    return doc['data'], provenance


def records(container):
    """L'amont distribue des objets indexés ou des listes selon mode/endpoint."""
    if isinstance(container, dict):
        return list(container.values())
    if isinstance(container, list):
        return container
    raise TypeError(f'Collection inattendue : {type(container)}')


def select(row, keys):
    return {key: row[key] for key in keys if key in row}


def label(value, dictionary):
    if not isinstance(value, str) or not value:
        return None
    return dictionary.get(value, None if TOKEN.match(value) else value)


def make_catalogue(mode, raw, english, french):
    names = {}
    weapon_rows, ammo_rows, armor_rows = [], [], []
    tags, weapon_groups, ammo_groups, armor_groups = Counter(), Counter(), Counter(), Counter()
    source_records = records(raw['items'])
    for item in sorted(source_records, key=lambda entry: entry['id']):
        item_id = item['id']
        if item_id in names or not item_id:
            raise ValueError(f'Identifiant d’objet dupliqué ou vide : {item_id!r}')
        values = item.get('properties') or {}
        kind = values.get('propertiesType')
        types = set(item['types'])
        tags.update(types)
        en_name, fr_name = label(item.get('name'), english), label(item.get('name'), french)
        if not en_name and not fr_name:
            raise ValueError(f'Nom non résolu : {item_id}')
        names[item_id] = {
            'name': en_name,
            'nameFr': fr_name,
            'shortName': label(item.get('shortName'), english),
            'shortNameFr': label(item.get('shortName'), french),
            **select(item, ('normalizedName', 'types', 'categories', 'handbookCategories', 'width', 'height',
                            'weight', 'basePrice', 'updated', 'wikiLink')),
        }
        if kind in {'ItemPropertiesWeapon', 'ItemPropertiesMelee', 'ItemPropertiesPreset'} or 'grenade' in types:
            variant = {
                'ItemPropertiesWeapon': 'arme-a-feu-source', 'ItemPropertiesMelee': 'melee',
                'ItemPropertiesPreset': 'preset',
            }.get(kind, 'grenade-lancee')
            weapon_groups[variant] += 1
            weapon_rows.append({
                'id': item_id, 'groupe': variant,
                'properties': {key: value for key, value in values.items() if key not in {'slots', 'grids'}},
                **select(item, TRADE_AND_PRICE),
            })
        if 'ammo' in types or kind == 'ItemPropertiesAmmo':
            ammo_groups[kind or 'sans-profil'] += 1
            ammo_rows.append({'id': item_id, 'properties': item.get('properties'), **select(item, TRADE_AND_PRICE)})
        if types & DEFENSIVE_TYPES or kind in DEFENSIVE_PROPERTIES or (
            kind == 'ItemPropertiesGlasses' and (values.get('class') or 0) > 0
        ):
            armor_groups[kind or 'sans-profil'] += 1
            armor_rows.append({
                'id': item_id,
                'properties': {k: v for k, v in values.items() if k != 'grids'} if values else item.get('properties'),
                **select(item, TRADE_AND_PRICE),
            })
    if not all(len(value) > 0 for value in (names, weapon_rows, ammo_rows, armor_rows)):
        raise ValueError(f'Sous-catalogue vide pour {mode}')
    categories = {}
    for field in ('itemCategories', 'handbookCategories'):
        categories[field] = {
            row['id']: {
                **select(row, ('normalizedName', 'parent', 'children')),
                'name': label(row.get('name'), english), 'nameFr': label(row.get('name'), french),
            }
            for row in records(raw[field])
        }
    payloads = {
        'items': {'items': names, **categories},
        'weapons': {'rows': weapon_rows},
        'ammo': {'rows': ammo_rows},
        'armor': {'rows': armor_rows, 'armorMaterials': raw['armorMaterials']},
    }
    counts = {
        'items': len(names), 'tagsSource': dict(sorted(tags.items())),
        'lignesArmesEtVariantes': len(weapon_rows), 'groupesArmes': dict(sorted(weapon_groups.items())),
        'lignesAmmo': len(ammo_rows), 'profilsAmmo': dict(sorted(ammo_groups.items())),
        'lignesProtectionEtRigs': len(armor_rows), 'groupesProtection': dict(sorted(armor_groups.items())),
        'nomsFrManquants': sum(value['nameFr'] is None for value in names.values()),
    }
    assert len(names) == len(source_records)
    return payloads, counts


def make_maps(raw, english, french):
    rows = []
    for entry in records(raw['maps']):
        labels = {
            'name': label(entry.get('name'), english),
            'nameFr': label(entry.get('name'), french),
        }
        rows.append({
            **select(entry, ('id', 'normalizedName', 'nameId', 'raidDuration', 'players', 'minPlayerLevel',
                             'maxPlayerLevel', 'accessKeysMinPlayerLevel', 'accessKeys')),
            **labels,
            'tailleDesListesSource': {key: len(entry[key]) if entry.get(key) is not None else None
                                      for key in ('extracts', 'transits', 'spawns', 'bosses', 'locks', 'hazards')},
        })
    if not rows or len({row['id'] for row in rows}) != len(rows):
        raise ValueError('Liste des cartes vide ou avec des doublons')
    return {'rows': sorted(rows, key=lambda row: row['normalizedName']),
            'note': 'Inventaire des entrées techniques, pas une preuve de disponibilité. Un tableau vide ne prouve pas l’absence en jeu.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'recherche' / 'tarkov-dev')
    parser.add_argument('--cache', type=Path, help='Relire un lot brut interne avec ses métadonnées et ses empreintes')
    args = parser.parse_args()
    endpoint_paths = ['endpoints'] + [f'{mode}/{stem}' for mode in MODES for stem in (
        'items', 'items_en', 'items_fr', 'maps', 'maps_en', 'maps_fr',
    )]
    with ThreadPoolExecutor(max_workers=4) as pool:
        loaded = dict(zip(endpoint_paths, pool.map(lambda path: load_source(path, args.cache), endpoint_paths), strict=True))
    catalogue = loaded['endpoints'][0]
    if not set(MODES) <= set(catalogue['gameModes']) or not {'en', 'fr'} <= set(catalogue['languages']):
        raise ValueError('Modes/langues non supportés dans le catalogue amont')
    results = {'endpoints.json': json_bytes(catalogue)}
    counts_by_mode = {}
    for mode in MODES:
        def payload(key):
            return loaded[f'{mode}/{key}'][0]
        files, counts = make_catalogue(mode, payload('items'), payload('items_en'), payload('items_fr'))
        files['maps-overview'] = make_maps(payload('maps'), payload('maps_en'), payload('maps_fr'))
        counts['entreesCartographiquesSource'] = len(files['maps-overview']['rows'])
        counts_by_mode[mode] = counts
        for name in FILENAMES:
            group = 'maps' if name == 'maps-overview' else 'items'
            inputs = [f'{mode}/{key}' for key in (group, group + '_en', group + '_fr')]
            results[f'{mode}/{name}.json'] = json_bytes({
                'schemaVersion': 1, 'mode': mode, 'sources': inputs, **files[name],
            })
    manifest = {
        'schemaVersion': 1,
        'fournisseur': 'Tarkov.dev / The Hideout (données communautaires)',
        'buildEftAtteste': None,
        'note': ('Instantané daté, non assimilable à un build EFT. Les champs de prix sont des observations historiques, '
                 'pas le prix garanti ni la preuve de disponibilité. Pas de médias ou textes descriptifs redistribués.'),
        'sources': {key: value[1] for key, value in loaded.items()},
        'modes': counts_by_mode,
        'fichiers': {name: {'octets': len(body), 'sha256': digest(body)} for name, body in results.items()},
    }
    results['manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()
    args.out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.capture-', dir=args.out) as tmp:
        for name, body in results.items():
            path = Path(tmp) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        for name in results:
            destination = args.out / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            (Path(tmp) / name).replace(destination)
    for mode, counts in counts_by_mode.items():
        print(f'{mode}: {counts["items"]} objets, {counts["groupesArmes"]}, '
              f'{counts["lignesAmmo"]} munitions, {counts["lignesProtectionEtRigs"]} protections/rigs, '
              f'{counts["entreesCartographiquesSource"]} entrées cartes')
    print(f'{len(results)} fichiers, {sum(len(body) for body in results.values()):,} octets')


if __name__ == '__main__':
    main()
