#!/usr/bin/env python3
"""Recuperer les images manquantes des objets sans image dans les catalogues.

Le script recupere_images.py ne trouvait pas les pages wiki pour certains
objets dont le nom est en francais : le wiki Fandom utilise des titres anglais.
Ce script reessaie avec plusieurs strategies de recherche pour chaque objet
manquant : nom complet, tokens techniques (chiffres/lettres/tirets), calibre,
et traductions de mots francais courants vers l'anglais.
"""
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / 'images' / 'items'
REGISTRE = ROOT / 'docs' / 'images-objets.json'

API = 'https://escapefromtarkov.fandom.com/api.php'
UA = 'TarkovGuide/1.0 (recuperation images manquantes)'
FONDS = (26, 26, 28)

MOTS_FRANCAIS = {
    'pistolet': 'pistol', 'mitrailleur': 'smg', 'fusil': 'rifle', 'fusil de precision': 'sniper rifle',
    'a verrou': 'bolt-action', 'verrou': 'bolt-action', 'cartouche': 'cartridge', 'chevrotine': 'shotshell',
    'chevrotines': 'shotshell', 'munition': 'ammo', 'calibre': 'caliber', 'mm': 'mm',
    'de camping': 'camping', 'hache': 'axe', 'machette': 'machete', 'couteau': 'knife',
    'pied-de-biche': 'crowbar', 'pelle': 'shovel', 'labrys': 'labrys', 'epee': 'sword',
}


def api(params):
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def slugify(nom):
    s = nom.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def rechercher_page(terme):
    s = api({'action': 'query', 'list': 'search', 'srsearch': terme,
             'srnamespace': 0, 'srlimit': 3, 'format': 'json'})
    resultats = s.get('query', {}).get('search', [])
    return resultats[0]['title'] if resultats else None


def image_page(titre):
    pi = api({'action': 'query', 'titles': titre, 'prop': 'pageimages',
              'pithumbsize': 700, 'redirects': 1, 'format': 'json'})
    for pg in pi.get('query', {}).get('pages', {}).values():
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
    fond = Image.new('RGBA', im.size, FONDS + (255,))
    fond.paste(im, mask=im.split()[3])
    im = fond.convert('RGB')
    if im.width > largeur:
        ratio = largeur / im.width
        im = im.resize((largeur, int(im.height * ratio)), Image.LANCZOS)
    im.save(destination, 'JPEG', quality=90, optimize=True)


def termes_recherche(nom):
    """Générer une liste de termes de recherche, du plus précis au plus large."""
    termes = [nom]
    # Version normalisée : " x " -> "x", " mm" -> "mm" (le wiki utilise ce format)
    normalise = re.sub(r'\s*x\s*', 'x', nom)
    normalise = re.sub(r'\s*mm\b', 'mm', normalise)
    if normalise != nom:
        termes.append(normalise)
    # Tokens techniques : chiffres, lettres, tirets (garder les tokens de >= 2 chars)
    tokens = re.findall(r'[A-Za-z0-9][A-Za-z0-9.\-]*', nom)
    # Filtrer les tokens purement francais courts
    tech = [t for t in tokens if re.search(r'\d', t) or len(t) >= 3]
    if tech:
        # Le plus long token technique
        tech_long = max(tech, key=len)
        termes.append(tech_long)
        # Les 2-3 tokens techniques les plus longs joints
        tech_tri = sorted(tech, key=len, reverse=True)[:3]
        termes.append(' '.join(tech_tri))
        # Jointure normalisée (sans espaces)
        termes.append(''.join(tech_tri))
    # Calibre (pattern "X x Y mm")
    calibre = re.search(r'[\d.]+\s*x\s*[\d.]+\s*mm', nom)
    if calibre:
        termes.append(calibre.group(0).replace(' ', ''))
        termes.append(calibre.group(0))
    # Nom sans les mots francais courants
    nettoye = nom
    for mot, ang in MOTS_FRANCAIS.items():
        nettoye = nettoye.replace(mot, '')
    nettoye = re.sub(r'\s+', ' ', nettoye).strip()
    if nettoye and nettoye != nom:
        termes.append(nettoye)
    # Deduplication
    seen = set()
    unique = []
    for t in termes:
        if t and t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


def recuperer(nom):
    """Essayer tous les termes de recherche, retourner True si l'image est récupérée."""
    key = slugify(nom)
    destination = IMAGES / f'{key}.jpg'
    if destination.is_file():
        return True
    # Essayer d'abord le titre wiki normalisé directement (sans espaces autour du x/mm)
    normalise = re.sub(r'\s*x\s*', 'x', nom)
    normalise = re.sub(r'\s*mm\b', 'mm', normalise)
    for titre_candidat in [normalise, nom]:
        try:
            url = image_page(titre_candidat)
            if url:
                data = telecharger(url, destination)
                convertir_jpg(data, destination)
                return True
        except Exception:
            pass
        time.sleep(0.1)
    for terme in termes_recherche(nom):
        try:
            titre = rechercher_page(terme)
            if not titre:
                continue
            url = image_page(titre)
            if not url:
                continue
            data = telecharger(url, destination)
            convertir_jpg(data, destination)
            return True
        except Exception:
            continue
        time.sleep(0.15)
    return False


def traiter(catalogue, label, registre):
    ok, manquant = 0, []
    for obj in catalogue:
        nom = obj.get('nom') or obj.get('shortName') or obj.get('name')
        if not nom:
            continue
        key = slugify(nom)
        if (IMAGES / f'{key}.jpg').is_file():
            continue
        if recuperer(nom):
            sous = registre.setdefault(label, {})
            sous[key] = f'images/items/{key}.jpg'
            ok += 1
            print(f'  [{label}] OK {nom}', flush=True)
        else:
            manquant.append(nom)
            print(f'  [{label}] MANQUANT {nom}', flush=True)
        time.sleep(0.2)
    print(f'[{label}] OK {ok} · manquant {len(manquant)}', flush=True)
    return ok, manquant


def main():
    registre = json.loads(REGISTRE.read_text(encoding='utf-8')) if REGISTRE.exists() else {}
    total = 0
    for cible, fichier, clé in [
        ('armes', 'js/data/weapons.json', 'armes'),
        ('armures', 'js/data/armor.json', 'pieces'),
        ('munitions', 'js/data/ammo.json', 'munitions'),
    ]:
        data = json.loads((ROOT / fichier).read_text(encoding='utf-8'))
        ok, _ = traiter(data[clé], cible, registre)
        total += ok
    REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'TOTAL : {total} images manquantes recuperees')


if __name__ == '__main__':
    main()
