#!/usr/bin/env python3
"""Contrôles statiques reproductibles de l’atelier livré en phase 1."""
from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from mutagen.mp3 import MP3
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / 'atelier/index.html'


def read(file):
    return json.loads((ROOT / file).read_text(encoding='utf-8'))


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def check_local(value, ids):
    if not value:
        return None
    url = urlsplit(value)
    if url.scheme:
        assert url.scheme == 'https' and url.netloc, value
        return None
    assert not url.netloc and not url.path.startswith('/'), value
    name = unquote(url.path)
    target = (HTML.parent / name).resolve() if name else HTML
    if target.is_dir():
        target /= 'index.html'
    assert target.is_relative_to(ROOT) and target.is_file(), value
    if target == HTML and url.fragment:
        assert unquote(url.fragment) in ids, value
    return target.relative_to(ROOT).as_posix()


def contrast(fg, bg):
    def lumi(c):
        x = [int(c[i:i+2], 16) / 255 for i in (0,2,4)]
        return sum((v / 12.92 if v <= .04045 else ((v+.055) / 1.055) ** 2.4) * k for v, k in zip(x, (.2126,.7152,.0722)))
    a, b = sorted((lumi(fg), lumi(bg)))
    return round((b + .05) / (a + .05), 2)


def main():
    parser = Page()
    parser.feed(HTML.read_text(encoding='utf-8'))
    tags = parser.tags
    ids = [attr['id'] for _, attr in tags if 'id' in attr]
    assert len(set(ids)) == len(ids)
    assert sum(tag == 'h1' for tag, _ in tags) == 1
    routes = read('docs/pages.json')['pages']
    assert len({row['route'] for row in routes}) == len(routes) == 86
    # Audit historique de la phase 1 : aucune route ne pouvait exister sur le disque.
    # La règle durable est qu'aucune route non publiée ne doit avoir de fichier.
    publiees_routes = {row['route'] for row in routes if row['etat'] in ('PUBLIEE', 'PUBLIÉE')}
    book_files = [row['route'] for row in routes if (ROOT / row['route']).exists()]
    # Règle durable : une route non publiée ne doit pas laisser de fichier, sauf
    # si elle appartient à la phase en cours de production, où le fichier est
    # rendu avant la publication.
    phase_en_cours = read('workflow.json')['phaseCourante']
    rendu_non_publie = {row['route'] for row in routes
                        if row['phase'] == phase_en_cours and row['route'] not in publiees_routes}
    assert not [route for route in book_files
                if route not in publiees_routes and route not in rendu_non_publie], book_files
    index = read('js/data/search-index.json')
    counts = Counter(item['etat'] for item in index['entrees'])
    publiees = [row for row in routes if row['etat'] in ('PUBLIEE', 'PUBLIÉE')]
    assert counts['atelier'] == 8, counts
    assert counts['planifiee'] == 86 - len(publiees), counts
    assert index['routesPubliees'] == len(publiees) and index['routesPlanifiees'] == 86
    for row in index['entrees']:
        if row['etat'] == 'planifiee':
            assert row['url'] is None
        elif row['etat'] == 'publiee':
            assert row['url'] in {page['route'] for page in publiees}, row
        elif row['etat'] == 'dossier':
            url = urlsplit(row['url'])
            cible = (ROOT / url.path)
            assert cible.is_file(), row
            page = Page()
            page.feed(cible.read_text(encoding='utf-8'))
            ids_page = {attr['id'] for _, attr in page.tags if 'id' in attr}
            assert url.fragment in ids_page, row
        elif row['etat'] == 'atelier':
            url = urlsplit(row['url'])
            assert url.path == 'atelier/' and url.fragment in ids and (ROOT / url.path / 'index.html').is_file()
        else:
            url = urlsplit(row['url'])
            accueil = Page()
            accueil.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
            ids_accueil = {attr['id'] for _, attr in accueil.tags if 'id' in attr}
            assert url.path in ('', './') and url.fragment in ids_accueil, row
    checked_refs = []
    externals = set()
    for tag, attr in tags:
        for key in ('aria-labelledby','aria-describedby','aria-controls','for','data-dialog-open'):
            if key in attr:
                assert all(item in ids for item in attr[key].split()), (tag,key,attr)
        for key in ('href','src'):
            if attr.get(key, '').startswith('https://'):
                externals.add(attr[key]); continue
            found = check_local(attr.get(key), ids)
            if found: checked_refs.append(found)
        if tag == 'img':
            file = check_local(attr['src'], ids)
            assert file.endswith('.jpg') and attr.get('alt') and attr.get('height') and attr.get('width'), attr
            assert attr.get('loading') == 'lazy' or attr.get('fetchpriority') == 'high', attr
    meta = {a.get('name',a.get('property')):a.get('content') for t,a in tags if t=='meta'}
    assert 150 <= len(meta['description']) <= 160
    assert meta['keywords'] and meta['og:title'] and meta['twitter:card'] and meta['robots'].startswith('noindex')
    for image in ('og:image','twitter:image'):
        assert check_local(meta[image], ids).endswith('.jpg')
    for title in ('og:title', 'twitter:title'):
        assert 'Atelier' in meta[title]
    text = HTML.read_text()
    assert json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)[1])['@type']=='WebPage'
    refs_css = 0
    for css in (ROOT / 'css').rglob('*.css'):
        for data in re.findall(r"url\(['\"]?([^)'\"]+)['\"]?\)", css.read_text()):
            file = (css.parent / data).resolve()
            assert file.is_relative_to(ROOT) and file.is_file(), (css, data)
            refs_css += 1
    ignores = {'node_modules', '.git', '.cache', '.venv', '__pycache__'}
    forbidden = [f.relative_to(ROOT).as_posix() for f in ROOT.rglob('*') if f.suffix.lower() in
                 ('.png','.jpeg','.svg','.webp','.gif','.wav','.ogg','.flac','.aac','.m4a','.zip','.pdf')
                 and not ignores.intersection(f.relative_to(ROOT).parts)]
    assert not forbidden, forbidden
    images = {}
    for f in sorted((ROOT / 'images').rglob('*.jpg')):
        relative = f.relative_to(ROOT).as_posix()
        # Les thumbnails d'objets (images/items/) sont des images reelles du wiki,
        # pas des visuels generes du site : ils ne sont pas soumis a la taille minimale.
        objet = relative.startswith('images/items/')
        with Image.open(f) as im:
            w,h = im.size
            # Les visuels de l'atelier respectent le format de reference ; les phases suivantes
            # ont ajoute des formats de bandeau (1584 x 672) et des visuels plus larges.
            atelier = relative.startswith('images/ui/')
            assert im.format == 'JPEG' and (objet or (w >= 1280 and (h >= 720 or not atelier))), (f,w,h)
            assert f.stat().st_size < 600000, (f, f.stat().st_size)
            im.verify()
        images[relative] = {'largeur':w,'hauteur':h,'octets':f.stat().st_size,'sha256':sha256(f.read_bytes()).hexdigest()}
    assert len(images)>=4 and sum(t=='img' for t,_ in tags)==4
    audio = {}
    for clip in read('audio/catalogue.json')['clips']:
        f = ROOT / clip['fichier']
        info = MP3(f).info
        assert clip['sha256'] == sha256(f.read_bytes()).hexdigest()
        assert info.channels == 2 and info.sample_rate == 44100 and info.bitrate == 160000
        assert abs(info.length - clip['secondesPcm']) < .09
        audio[clip['fichier']] = {'secondesMp3':round(info.length,3),'boucle':clip['boucle'],'octets':f.stat().st_size}
    # Le catalogue audio couvre tous les MP3 du depot ; le compte exact a evolue avec les phases suivantes.
    assert len(audio) >= 7 and sum(a['boucle'] for a in audio.values()) >= 4
    assert set(audio)=={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*.mp3')}
    for f, rec in read('docs/dependances.json').items():
        assert rec['sha256'] == sha256((ROOT / f).read_bytes()).hexdigest(), f
    palette = {
        'texte principal / fond':('f1efe7','0b0d0b',4.5), 'texte secondaire / carte':('b9bdb3','161a15',4.5),
        'or / carte':('c8aa6e','161a15',4.5),'texte / bouton or':('14140e','c8aa6e',4.5),
        'contours commandes / surface':('6e7667','1c211a',3.0),'focus / surface':('efcf95','1c211a',3.0),
        'valeur en écart / cellule':('efcf95','292319',4.5),'vert / badge':('9fbe98','182216',4.5),
        'identifiant hero / fond badge au maximum':('e2e2d5','252c27',4.5),
    }
    ratios = {key:contrast(a,b) for key,(a,b,_) in palette.items()}
    assert all(ratios[key]>=minimum for key, (_,_,minimum) in palette.items()), ratios
    report = {'statut':'OK','referenceUtc':'2026-11-18','atelier':'atelier/index.html','routesPlanifiees':len(routes),
              'routesEditorialesPubliees':len(book_files),'index':dict(counts),'attributsLocauxResolus':len(checked_refs),
              'urlsExternesSyntaxeVerifiee':len(externals),'referencesCssResolues':refs_css,'longueurDescription':len(meta['description']),
              'dependenciesLocalesVerifiees':len(read('docs/dependances.json')),
              'contrastesPalette':ratios,'images':images,'audios':audio}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__=='__main__':
    main()
