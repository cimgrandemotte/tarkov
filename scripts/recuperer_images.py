#!/usr/bin/env python3
"""Recuperer les vraies images des objets sur le wiki Fandom Escape from Tarkov.

Chaque objet d'un catalogue (arme, armure, munition, etc.) reçoit sa vraie image
du wiki de reference, telechargee puis convertie en JPEG (le site n'accepte que
du JPG). L'image est stockee dans images/items/{slug}.jpg et un registre JSON
recorde la correspondance objet -> image.

Usage :
    python3 scripts/recuperer_images.py armes       # catalogue des armes
    python3 scripts/recuperer_images.py armures     # catalogue des armures
    python3 scripts/recuperer_images.py munitions   # catalogue des munitions
    python3 scripts/recuperer_images.py --liste     # tous les catalogues
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / 'images' / 'items'
REGISTRE = ROOT / 'docs' / 'images-objets.json'

API = 'https://escapefromtarkov.fandom.com/api.php'
UA = 'TarkovGuide/1.0 (recuperation images reference)'
FONDS = (26, 26, 28)  # fond sombre neutre pour les images a fond transparent


def api(params):
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def slugify(nom):
    """Slug fichier : minuscules, tirets, pas d'accents."""
    import re
    s = nom.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def rechercher_page(nom):
    """Retourne le titre de page wiki le plus pertinent pour un nom d'objet."""
    s = api({'action': 'query', 'list': 'search', 'srsearch': nom,
             'srnamespace': 0, 'srlimit': 3, 'format': 'json'})
    resultats = s.get('query', {}).get('search', [])
    return resultats[0]['title'] if resultats else None


def image_page(titre):
    """Retourne l'URL de la thumbnail d'une page wiki (ou None)."""
    pi = api({'action': 'query', 'titles': titre, 'prop': 'pageimages',
              'pithumbsize': 700, 'redirects': 1, 'format': 'json'})
    pages = pi.get('query', {}).get('pages', {})
    for pg in pages.values():
        th = pg.get('thumbnail')
        if th:
            return th['source']
    return None


def telecharger(url, destination):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    destination.write_bytes(data)
    return data


def convertir_jpg(data, destination, largeur=700):
    from PIL import Image
    im = Image.open(__import__('io').BytesIO(data))
    im = im.convert('RGBA')
    # Mettre le fond si l'image est a fond transparent.
    if im.mode == 'RGBA':
        fond = Image.new('RGBA', im.size, FONDS + (255,))
        fond.paste(im, mask=im.split()[3])
        im = fond.convert('RGB')
    else:
        im = im.convert('RGB')
    # Redimensionner a une largeur constante, hauteur proportionnelle.
    if im.width > largeur:
        ratio = largeur / im.width
        im = im.resize((largeur, int(im.height * ratio)), Image.LANCZOS)
    im.save(destination, 'JPEG', quality=90, optimize=True)


def traiter(catalogue, label):
    """Recuperer les images pour tous les objets d'un catalogue."""
    IMAGES.mkdir(parents=True, exist_ok=True)
    registre = json.loads(REGISTRE.read_text(encoding='utf-8')) if REGISTRE.exists() else {}
    sous = registre.setdefault(label, {})
    objets = catalogue if isinstance(catalogue, list) else list(catalogue.values())
    ok, manquant, erreur = 0, [], 0
    for i, obj in enumerate(objets, 1):
        nom = obj.get('nom') or obj.get('shortName') or obj.get('name')
        if not nom:
            continue
        key = slugify(nom)
        if key in sous and sous[key]:
            continue  # deja recupere
        destination = IMAGES / f'{key}.jpg'
        try:
            titre = rechercher_page(nom)
            if not titre:
                manquant.append(nom)
                continue
            url = image_page(titre)
            if not url:
                manquant.append(nom)
                continue
            data = telecharger(url, destination)
            convertir_jpg(data, destination)
            sous[key] = destination.relative_to(ROOT).as_posix()
            ok += 1
            if ok % 20 == 0:
                REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
                print(f'  [{label}] {ok} images recuperees, {i}/{len(objets)}', flush=True)
        except Exception as exc:  # pas de bris de boucle sur un objet
            erreur += 1
            print(f'  [{label}] {nom} : {exc}', flush=True)
        time.sleep(0.25)  # ménager l'API
    REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'[{label}] OK {ok} · manquant {len(manquant)} · erreur {erreur}')
    if manquant:
        print('  manquants :', ', '.join(manquant[:20]))
    return ok


def charger(nom_fichier):
    return json.loads((ROOT / nom_fichier).read_text(encoding='utf-8'))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('cible', nargs='?', choices=['armes', 'armures', 'munitions'],
                    help='catalogue a traiter')
    ap.add_argument('--liste', action='store_true', help='traiter tous les catalogues')
    args = ap.parse_args()

    cibles = ['armes', 'armures', 'munitions'] if args.liste else [args.cible]
    total = 0
    for cible in cibles:
        if cible == 'armes':
            data = charger('js/data/weapons.json')
            catalogue = data['armes']
        elif cible == 'armures':
            data = charger('js/data/armor.json')
            catalogue = data['pieces']
        elif cible == 'munitions':
            data = charger('js/data/ammo.json')
            catalogue = data['munitions']
        total += traiter(catalogue, cible)
    print(f'TOTAL : {total} images recuperees')


if __name__ == '__main__':
    main()
