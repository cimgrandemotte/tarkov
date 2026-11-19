#!/usr/bin/env python3
"""Contrôles statiques de l’accueil au point d’arrêt de la phase 2."""
import argparse
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess
import sys
from urllib.parse import urldefrag, unquote, urlsplit

from mutagen.mp3 import MP3
from PIL import Image
from valider_phase1 import Page, contrast

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / 'index.html'
WORKSHOP = ROOT / 'atelier/index.html'
PUBLISHED = {'PUBLIEE', 'PUBLIÉE'}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def parse(file):
    text = file.read_text(encoding='utf-8')
    parser = Page()
    parser.feed(text)
    assert len({a['id'] for _, a in parser.tags if 'id' in a}) == sum('id' in a for _, a in parser.tags), file
    return text, parser.tags


def check_link(ref, from_file):
    target = urlsplit(ref)
    if target.scheme:
        assert target.scheme == 'https' and target.hostname, ref
        return None
    assert not target.netloc and not target.path.startswith('/'), ref
    route = (from_file.parent / unquote(target.path)).resolve() if target.path else from_file
    if route.is_dir():
        route = route / 'index.html'
    assert route.is_relative_to(ROOT) and route.is_file(), ref
    if target.fragment and route.suffix == '.html':
        _, tags = parse(route)
        assert any(attr.get('id') == unquote(target.fragment) for _, attr in tags), ref
    return route


def inventory():
    """Inventaire des livrables du guide : les dépendances installées sont exclues."""
    ignores = {'node_modules', '.git', '.cache', '.venv', '__pycache__'}
    found = {}
    for ext in ('html','jpg','mp3'):
        found[ext] = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob(f'*.{ext}')
                            if p.is_file() and not ignores.intersection(p.relative_to(ROOT).parts))
    return found


def main(final=False):
    text, tags = parse(HOME)
    _, workshop = parse(WORKSHOP)
    index = read('js/data/search-index.json')
    plan = read('docs/pages.json')
    sources = read('docs/sources.json')['sources']
    assert plan['total'] == len(plan['pages']) == len({p['route'] for p in plan['pages']}) == 86
    published = [p for p in plan['pages'] if p['etat'] in PUBLISHED]
    assert plan['publiees'] == len(published) >= 1 and published[0]['route'] == 'index.html'
    assert published[0]['dateDePublication'] == '2026-11-18'
    assert (ROOT / published[0]['rechercheCiblee']).is_file()
    assert all(set(row['sourcesDeDepart']).issubset(sources) for row in plan['pages'])
    assets = inventory()
    # Contrôle cumulatif : tout HTML sur disque est une route planifiée.
    assert set(assets['html']) <= {'atelier/index.html', 'index.html', *(row['route'] for row in plan['pages'])}
    assert len(assets['jpg']) >= 12 and len(assets['mp3']) == 8
    extensions = {'.png','.jpeg','.svg','.webp','.gif','.wav','.ogg','.flac','.aac','.m4a','.zip','.pdf'}
    ignores = {'node_modules', '.git', '.cache', '.venv', '__pycache__'}
    forbidden = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
                 if p.is_file() and p.suffix.lower() in extensions
                 and not ignores.intersection(p.relative_to(ROOT).parts)]
    assert not forbidden, forbidden
    assert index['routesPubliees'] == len(published) and index['routesPlanifiees'] == plan['total']
    entries = Counter(item['etat'] for item in index['entrees'])
    assert entries['publiee'] == len(published) and entries['planifiee'] == plan['total'] - len(published)
    assert entries['atelier'] == 8 and entries['accueil'] == 6
    by_state = {'atelier':WORKSHOP, 'accueil':HOME}
    routes_publiees = {row['route'] for row in published}
    for item in index['entrees']:
        if item['etat'] == 'planifiee':
            assert item['url'] is None, item
        elif item['etat'] == 'publiee':
            cible = check_link(item['url'], HOME)
            assert cible is not None and cible.relative_to(ROOT).as_posix() in routes_publiees, item
        elif item['etat'] == 'dossier':
            cible = check_link(item['url'], HOME)
            assert cible is not None and cible.relative_to(ROOT).as_posix() in routes_publiees, item
        else:
            assert check_link(item['url'], HOME) == by_state[item['etat']], item
    assert {s['id'] for s in read('js/data/sections-accueil.json')} == {urlsplit(i['url']).fragment for i in index['entrees'] if i['etat'] == 'accueil'}
    assert sum(t == 'h1' for t, _ in tags) == 1
    assert any(t == 'html' and a.get('lang') == 'fr' for t, a in tags)
    assert any(t == 'meta' and a.get('name') == 'robots' and 'noindex' in a['content'] for t, a in workshop)
    assert not any(t == 'meta' and a.get('name') == 'robots' and 'noindex' in a['content'] for t, a in tags)
    assert any(t == 'audio' and 'src' not in a and 'autoplay' not in a and a['preload']=='none' for t, a in tags)
    assert sum(t == 'section' and 'mode-home__panel' in a.get('class','') for t, a in tags) == 5
    assert sum(t == 'summary' and 'dossier-card__trigger' in a.get('class','') for t, a in tags) == 6
    assert 'usemap=' not in text and 'role="menu"' not in text
    ids = {a['id'] for _, a in tags if 'id' in a}
    local = 0
    external = set()
    related = {urldefrag(s['url'])[0] for s in sources.values()}
    images = {}
    for tag, attr in tags:
        for key in ('aria-labelledby', 'aria-describedby', 'aria-controls', 'for', 'data-dialog-open'):
            if key in attr:
                assert set(attr[key].split()).issubset(ids), (key, attr)
        for key in ('href', 'src'):
            if key not in attr:
                continue
            f = check_link(attr[key], HOME)
            if f is None:
                if tag == 'a':
                    slug = urldefrag(attr[key])[0]
                    external.add(slug)
                    assert slug in related, attr[key]
            else:
                local += 1
        if tag == 'img':
            f = check_link(attr['src'], HOME)
            assert f.suffix == '.jpg' and attr['alt'].strip() and attr['width'] and attr['height']
            assert attr.get('loading') == 'lazy' or attr.get('fetchpriority') == 'high'
            with Image.open(f) as im:
                assert im.format == 'JPEG' and im.size == (int(attr['width']), int(attr['height'])) == (1376, 768)
                im.verify()
            images[f.relative_to(ROOT).as_posix()] = {'px':[1376,768], 'octets':f.stat().st_size,'sha256':sha256(f.read_bytes()).hexdigest()}
    assert sorted(images) == published[0]['mediasEffectifs']
    assert sum(t=='link' and a.get('rel')=='preload' and a.get('as')=='image' for t,a in tags) == 1
    meta = {a.get('name', a.get('property')):a.get('content') for t, a in tags if t == 'meta'}
    assert 150 <= len(meta['description']) <= 160
    assert meta['keywords'] and meta['og:title'] and meta['og:description'] == meta['description']
    assert meta['og:locale'] == 'fr_FR' and meta['twitter:card'] == 'summary_large_image'
    for key in ('og:image','twitter:image'):
        assert urlsplit(meta[key]).path.endswith('/images/hero/tarkov-night-rain.jpg')
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)[1])
    assert ld['@type'] == 'WebSite' and ld['inLanguage'] == 'fr-FR' and ld['description'] == meta['description']
    time_urls = {attr.get('datetime') for t, attr in tags if t == 'time'}
    for timestamp in ('2026-11-23T15:00:00Z','2026-11-22','2026-12-07','2026-11-18','2026-10-29'):
        assert timestamp in time_urls, timestamp
    assert not any(stamp.startswith(('2026-11-22T','2026-12-07T')) for stamp in time_urls if stamp)
    assert '1.3.0.2.48779' in text and 'déploiement non confirmé' in text
    captured = read('recherche/tarkov-dev/manifest.json')
    nums = dict(re.findall(r'data-count="([a-z]+)">([^<]+)<', text))
    values = {key:int(v.replace('\u202f','')) for key,v in nums.items()}
    assert values['published'] == len(published) and values['planned'] == plan['total']
    assert values['modes'] == len(captured['modes']) and all(values['items'] == profile['items'] for profile in captured['modes'].values())
    assert captured['buildEftAtteste'] is None
    clips = read('audio/catalogue.json')['clips']
    assert len(clips) == len({a['fichier'] for a in clips}) and sorted(a['fichier'] for a in clips) == assets['mp3']
    for entry in clips:
        audio = ROOT / entry['fichier']
        signal = MP3(audio).info
        assert signal.channels == 2 and signal.sample_rate == 44100 and signal.bitrate == 160000
        assert audio.stat().st_size == entry['octets'] and sha256(audio.read_bytes()).hexdigest() == entry['sha256']
        assert abs(signal.length - entry['secondesPcm']) <= .09
    clip = next(clip for clip in clips if clip['type'] == 'theme')
    info = MP3(ROOT / clip['fichier']).info
    assert clip['fichier'] == published[0]['audiosEffectifs'][0] and not clip['boucle'] and 30 < info.length < 30.09
    palette = {'héro · légende':('e2e3d5','21251b'), 'carte · label':('e4c78c','1a1c13'),
               'menu · texte':('f1efe7','151912'), 'compteur · valeur':('efcf95','141813'),
               'compteur · label':('b9bdb3','141813'), 'texte · bouton or':('14140e','c8aa6e')}
    ratios = {key:contrast(*colors) for key, colors in palette.items()}
    assert all(value >= 4.5 for value in ratios.values())
    cmd = subprocess.run([sys.executable, 'scripts/rendre_accueil.py', '--check'], cwd=ROOT, check=True, capture_output=True, text=True)
    if final:
        workflow = read('workflow.json')
        machine = read('state_machine.json')
        state = machine['instantane']
        counts = {'pagesPlanifiees':86,'pagesGenerees':len(published),'pagesHtmlTechniques':1,
                  'imagesCreees':len(assets['jpg']),'audiosCrees':len(assets['mp3'])}
        assert workflow['compteurs'] == state['compteurs'] == counts
        assert workflow['statut'] == state['etat'] in ('ATTENTE_CONTINUE', 'ATTENTE_LOT')
        assert workflow['phaseCourante'] == state['phase']
        assert 'PHASE_2' in workflow['phasesTerminees'] == state['phasesTerminees']
        assert workflow['fuseau'] == machine['fuseau'] == 'UTC'
        assert sorted(workflow['livrables']['pages']) == sorted(row['route'] for row in published)
        assert workflow['livrables']['htmlTechniques'] == ['atelier/index.html']
        for kind, ext in [('imagesJpg','jpg'), ('audiosMp3','mp3')]:
            assert sorted(workflow['livrables'][kind]) == assets[ext]
        for kind, files in workflow['livrables'].items():
            for f in files:
                assert (ROOT / f).is_file(), (kind, f)
        phase = next(phase for phase in workflow['phases'] if phase['id'] == 'PHASE_2')
        assert phase['lotMedia'] == {'imagesJpg':8, 'audiosMp3':1}
        assert all(read(f)['statut'] == 'OK' for f in phase['validations'] if not f.endswith('statique.json'))
    print(json.dumps({'statut':'OK','referenceUtc':'2026-11-18','compteursHtml':values,'publications':assets['html'],
                      'index':dict(entries),'liensCheminsLocauxVerifies':local,'sourcesExternesAnnoncees':len(external),
                      'sourcesRegistre':len(sources),'descriptionCaracteres':len(meta['description']),
                      'images':images,'introMp3':{'secondesMp3':round(info.length,4),'octets':clip['octets'],'boucle':clip['boucle']},
                      'contrastesPalette':ratios,'renduReproductible':cmd.returncode == 0,'etatFinalControle':final},
                     indent=2, ensure_ascii=False))


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--final', action='store_true', help='inclure la cohérence des deux fichiers de suivi à la clôture')
    main(final=cli.parse_args().final)
