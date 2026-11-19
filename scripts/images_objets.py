#!/usr/bin/env python3
"""Lecture du registre des vraies images d'objets recuperees sur le wiki.

Le registre `docs/images-objets.json` recense, pour chaque catalogue, la
correspondance objet -> image JPEG telechargee dans `images/items/`. Les
renderers l'utilisent pour afficher une miniature reelle a chaque objet du
catalogue, quand l'image est disponible.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRE = ROOT / 'docs' / 'images-objets.json'


def slugify(nom):
    """Slug fichier : minuscules, tirets, pas d'accents."""
    import re
    s = nom.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def registre():
    """Retourne le registre, ou une copie vide si absent."""
    if REGISTRE.exists():
        return json.loads(REGISTRE.read_text(encoding='utf-8'))
    return {}


def image_pour(catalogue, nom):
    """Chemin relatif de l'image reelle pour un objet, ou None."""
    if not nom:
        return None
    reg = registre()
    sous = reg.get(catalogue) or {}
    return sous.get(slugify(nom))


def miniature(catalogue, nom, hauteur=48):
    """HTML d'une miniature reelle, ou une cellule vide si pas d'image.

    Pas d'attributs width/height : la taille d'affichage est reglere par CSS,
    ce qui laisse la liberte d'afficher la vraie image sans devoir la
    redimensionner a chaque rendu.
    """
    chemin = image_pour(catalogue, nom)
    if not chemin:
        return ''
    src = chemin.replace('images/', '../../images/')
    return (f'<img class="objet-thumb" src="{src}" alt="Image de {nom}" '
            f'width="360" height="360" loading="lazy" decoding="async">')
