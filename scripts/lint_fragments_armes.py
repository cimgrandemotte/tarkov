#!/usr/bin/env python3
"""Contrôle les fragments d'armes : alphabet français, artefacts de langue, marqueurs, balises.

Miroir de scripts/lint_fragments.py pour les fragments de la phase 5
(templates/armes/*.html.part). Sortie : code 1 si au moins un problème.
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOSSIER = ROOT / 'templates/armes'

ARTEFACTS = re.compile(
    r'\b(Preferred|Complete|Overlap|Override|Default|community|attacks|spawns|None|True|False|'
    r'family|results|grouping)\b')
MARQUEUR = re.compile(r'%%[A-Z][A-Z_]*%%')
MARQUEURS_CONNUS = {
    '%%TABLE_CATALOGUE%%', '%%TABLE_PRESETS%%', '%%TABLE_ACQUISITION%%', '%%TABLE_EMPLACEMENTS%%',
    '%%TABLE_PIECES%%', '%%TABLE_SELECTION%%', '%%TABLE_RECUL%%', '%%TABLE_CADENCE%%',
    '%%TABLE_DISTANCE%%', '%%TABLE_CLASSES%%', '%%TABLE_CALIBRES%%', '%%TABLE_TRACEURS%%',
    '%%TABLE_GRENADES%%', '%%TABLE_ACHATS%%', '%%TABLE_MUNITIONS%%', '%%GRILLE_FAMILLES%%',
    '%%JSON_ARSENAL%%', '%%JSON_MUNITIONS%%', '%%SOURCES_ARSENAL%%', '%%SOURCES_AMMO%%',
    '%%SOURCES_FAMILLE%%', '%%SOURCES_OUTIL%%',
}
CAMEL = re.compile(r"(?<![-–—/])(?<![A-Za-zÀ-ÿ])([a-zéèêàç]{2,}[A-ZÉÈÀÇ][a-zéèêàç]{2,})")
ANGLAIS = re.compile(
    r"(?<![-\w])(members|demembers|Those|Proteins|interest|overrides?|default|spawner|bosses|"
    r"extracts|looting|playstyle|keeps|says|tracks|checks|uses|shows|gives|takes|makes)\b")
BALISES = {
    'p', 'div', 'section', 'ul', 'ol', 'li', 'h2', 'h3', 'strong', 'em', 'small',
    'figure', 'figcaption', 'img', 'label', 'select', 'option', 'span', 'a',
    'dl', 'dt', 'dd', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'caption', 'button',
    'script', 'noscript', 'input', 'details', 'summary', 'canvas',
}


def hors_alphabet(ligne):
    suspects = set()
    for caractere in ligne:
        code = ord(caractere)
        if code < 128:
            continue
        if 'À' <= caractere <= 'ÿ':
            continue
        if code in (0x2013, 0x2014, 0x2018, 0x2019, 0x201c, 0x201d, 0x20ac, 0x2026, 0x00a0,
                    0x0152, 0x0153, 0x0178, 0x00ab, 0x00bb, 0x202f, 0x2009):
            continue
        if 0x0400 <= code <= 0x04ff:
            continue
        if unicodedata.category(caractere)[0] in ('L', 'N'):
            suspects.add(caractere)
    return suspects


problemes = 0
fragments = sorted(DOSSIER.glob('*.html.part'))
if not fragments:
    print('Aucun fragment d’armes dans templates/armes.')
    sys.exit(1)
for chemin in fragments:
    texte = chemin.read_text(encoding='utf-8')
    for numero, ligne in enumerate(texte.splitlines(), 1):
        suspects = hors_alphabet(ligne)
        if suspects:
            print(f'{chemin.name}:{numero} · caractères hors alphabet français : {" ".join(sorted(suspects))}')
            problemes += 1
        for camel in CAMEL.finditer(ligne):
            print(f'{chemin.name}:{numero} · collage de mots à corriger : « {camel.group(1)} »')
            problemes += 1
        for anglais in ANGLAIS.finditer(ligne):
            print(f'{chemin.name}:{numero} · mot anglais possible : « {anglais.group(1)} »')
            problemes += 1
        trouve = ARTEFACTS.search(ligne)
        if trouve:
            print(f'{chemin.name}:{numero} · artefact de langue possible : « {trouve.group(0)} »')
            problemes += 1
        if '%%' in ligne and not MARQUEUR.search(ligne):
            print(f'{chemin.name}:{numero} · marqueur de table incomplet')
            problemes += 1
        for marqueur in MARQUEUR.findall(ligne):
            if marqueur not in MARQUEURS_CONNUS:
                print(f'{chemin.name}:{numero} · marqueur inconnu : {marqueur}')
                problemes += 1
        for balise in re.findall(r'</?([a-z0-9]+)[^>]*>$', ligne):
            if balise not in BALISES:
                print(f'{chemin.name}:{numero} · balise inattendue : {balise}')
                problemes += 1
print(f'{len(fragments)} fragments · {problemes} problème(s)')
sys.exit(1 if problemes else 0)
