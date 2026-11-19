#!/usr/bin/env python3
"""Contrôler les livrables du point d’arrêt de la phase 0."""
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


def validate():
    workflow = read('workflow.json')
    state = read('state_machine.json')['instantane']
    plan = read('docs/pages.json')
    sources = read('docs/sources.json')['sources']
    assert workflow['statut'] == state['etat'] in ('ATTENTE_CONTINUE', 'ATTENTE_LOT')
    assert workflow['phaseCourante'] == state['phase']
    assert workflow['phasesTerminees'] == state['phasesTerminees']
    assert 'PHASE_0' in workflow['phasesTerminees']
    assert workflow['prochainePhase'] == state['prochainePhase']
    assert workflow['compteurs'] == state['compteurs']
    routes = {page['route'] for page in plan['pages']}
    assert len(routes) == plan['total'] == len(plan['pages']) == workflow['compteurs']['pagesPlanifiees']
    assert len(routes) >= workflow['limites']['pagesHtmlObjectifMinimum']
    assert 'pages/maps/terminal.html' in routes
    assert len([path for path in routes if path.startswith('pages/maps/')]) == 14
    by_phase = Counter(page['phase'] for page in plan['pages'])
    assert by_phase == plan['parPhase']
    assert all(entry['pagesPrevues'] == by_phase[entry['id']] for entry in workflow['phases'])
    publiees = {page['route'] for page in plan['pages'] if page['etat'] in ('PUBLIEE', 'PUBLIÉE')}
    for page in plan['pages']:
        path = ROOT / page['route']
        assert path.suffix == '.html' and path.parent.is_dir(), path
        # Une route non publiee ne doit pas exister sur le disque ; une route publiee, si.
        # Un fichier peut exister pour une route rendue et pas encore publiée,
        # à condition qu'elle appartienne à la phase en cours.
        phase_en_cours = workflow['phaseCourante']
        rendu_attendu = page['route'] in publiees or page['phase'] == phase_en_cours
        assert path.exists() == rendu_attendu or path.exists() == (page['route'] in publiees), path
        assert page['sourcesDeDepart'] and set(page['sourcesDeDepart']).issubset(sources)
        assert len(page['illustrationsJpg']) >= (3 if page['gabarit'] == 'carte' else 2)
    assert all((ROOT / path).is_file() for path in workflow['livrables']['donnees'])
    ignores = {'node_modules', '.git', '.cache', '.venv', '__pycache__'}
    for pattern in ('*.jpeg', '*.png', '*.zip', '*.pdf'):
        assert not [path for path in ROOT.rglob(pattern) if path.is_file()
                    and not ignores.intersection(path.relative_to(ROOT).parts)], pattern
    assert workflow['compteurs']['pagesGenerees'] == len(publiees)
    assert workflow['compteurs']['imagesCreees'] == len(list(ROOT.glob('images/**/*.jpg')))
    assert workflow['compteurs']['audiosCrees'] == len(list(ROOT.glob('audio/**/*.mp3')))
    data_root = ROOT / 'recherche/tarkov-dev'
    manifest = read('recherche/tarkov-dev/manifest.json')
    assert manifest['buildEftAtteste'] is None
    for key, entry in manifest['fichiers'].items():
        body = (data_root / key).read_bytes()
        assert len(body) == entry['octets'] and sha256(body).hexdigest() == entry['sha256'], key
    assert all(entry['sha256Source'] and entry['dateServeurHttp'] for entry in manifest['sources'].values())
    counts = {}
    for mode, meta in manifest['modes'].items():
        def payload(name):
            return read(f'recherche/tarkov-dev/{mode}/{name}.json')
        catalogue = payload('items')['items']
        assert len(catalogue) == meta['items']
        assert all(value['name'] and value['nameFr'] for value in catalogue.values())
        for name, key in (('weapons', 'lignesArmesEtVariantes'), ('ammo', 'lignesAmmo'), ('armor', 'lignesProtectionEtRigs')):
            doc = payload(name)
            row_ids = {item['id'] for item in doc['rows']}
            assert len(row_ids) == len(doc['rows']) == meta[key]
            assert doc['mode'] == mode and row_ids.issubset(catalogue), (mode, name)
        atlas = payload('maps-overview')['rows']
        assert len({row['normalizedName'] for row in atlas}) == meta['entreesCartographiquesSource']
        assert {'terminal', 'infected-lab', 'icebreaker'}.issubset({row['normalizedName'] for row in atlas})
        counts[mode] = meta['items']
    spt = read('recherche/versions/sp-tushonka.json')
    eft = read('recherche/versions/eft.json')
    assert spt['releaseStableJouable']['prerelease'] is False
    assert spt['releaseStableJouable']['buildEftRequis'] == '0.16.9.5.40743'
    assert spt['prereleaseNuGet']['version'] == '5.0.0-pre.202611061606'
    assert eft['dernierPatchNumeroteDansCeFlux']['version'] == '1.3.0.0'
    return {'statut': 'OK', 'routesUniques': len(routes), 'sourcesRepertoriees': len(sources),
            'empreintesDeFichiersVerifiees': len(manifest['fichiers']), 'objetsVerifiesParMode': counts,
            'etat': state['etat'], 'prochainePhase': state['prochainePhase']}


if __name__ == '__main__':
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
