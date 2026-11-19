#!/usr/bin/env python3
"""Contrôle les fragments de la phase 6 : alphabet français, artefacts de langue,
marqueurs, balises et divergences entre le manifeste et les fragments.

Miroir de scripts/lint_fragments_armes.py pour les fragments de la phase 6
(templates/armures/*.html.part). Sortie : code 1 si au moins un problème.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOSSIER = ROOT / 'templates/armures'

ARTEFACTS = re.compile(
    r'\b(Preferred|Complete|Overlap|Override|Default|community|attacks|spawns|None|True|False|'
    r'family|results|grouping)\b')
MARQUEUR = re.compile(r'%%[A-Z0-9_]+%%')
CAMEL = re.compile(r"(?<![-–—/])(?<![A-Za-zÀ-ÿ])([a-zéèêàç]{2,}[A-ZÉÈÀÇ][a-zéèêàç]{2,})")
ANGLAIS = re.compile(
    r"(?<![-\w])(members|demembers|Those|Proteins|interest|overrides?|default|spawner|bosses|"
    r"extracts|looting|playstyle|keeps|says|tracks|checks|uses|shows|gives|takes|makes|"
    r"spawn|spawns|escort|loot|health|armor|plate|plates|helmet)\b")
BALISES = {
    'p', 'div', 'section', 'ul', 'ol', 'li', 'h2', 'h3', 'strong', 'em', 'small',
    'figure', 'figcaption', 'img', 'label', 'select', 'option', 'span', 'a',
    'dl', 'dt', 'dd', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'caption', 'button',
    'script', 'noscript', 'input', 'details', 'summary', 'canvas',
}
IDENTIFIANTS_EXPORTS = re.compile(
    r'^(boss|follower|infected|sectant|blackDivision|pmcBot|exUsec|vsRF|specialSlot|'
    r'noFlea|followerBig|followerBird|followerWedge|followerKojaniy|followerBully|'
    r'followerGluhar|followerKolontay|followerBoar|followerSanitar|followerBigPipe|'
    r'followerBirdEye|followerWedgeLab)')


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
    print('Aucun fragment d’armures dans templates/armures.')
    sys.exit(1)
for chemin in fragments:
    texte = chemin.read_text(encoding='utf-8')
    for numero, ligne in enumerate(texte.splitlines(), 1):
        suspects = hors_alphabet(ligne)
        if suspects:
            print(f'{chemin.name}:{numero} · caractères hors alphabet français : {" ".join(sorted(suspects))}')
            problemes += 1
        for camel in CAMEL.finditer(ligne):
            mot = camel.group(1)
            if IDENTIFIANTS_EXPORTS.match(mot):
                continue
            print(f'{chemin.name}:{numero} · collage de mots à corriger : « {mot} »')
            problemes += 1
        for anglais in ANGLAIS.finditer(ligne):
            mot = anglais.group(0)
            if IDENTIFIANTS_EXPORTS.match(mot):
                continue
            print(f'{chemin.name}:{numero} · mot anglais possible : « {mot} »')
            problemes += 1
        trouve = ARTEFACTS.search(ligne)
        if trouve:
            print(f'{chemin.name}:{numero} · artefact de langue possible : « {trouve.group(0)} »')
            problemes += 1
        if '%%' in ligne and not MARQUEUR.search(ligne):
            print(f'{chemin.name}:{numero} · marqueur de table incomplet')
            problemes += 1
        if ligne.count('<') != ligne.count('>'):
            print(f'{chemin.name}:{numero} · balises non appariées')
            problemes += 1

# Le manifeste doit couvrir toutes les routes de la phase 6.
manifeste = json.loads((ROOT / 'templates/armures-phase-6.json').read_text(encoding='utf-8'))
livre = json.loads((ROOT / 'docs/pages.json').read_text(encoding='utf-8'))
routes_manifeste = [manifeste['hub_armor']['route'], manifeste['armor_body']['route'],
                     manifeste['armor_helmets']['route'], manifeste['armor_rigs']['route'],
                     manifeste['armor_chart']['route'], manifeste['hub_boss']['route']]
routes_manifeste += [boss['route'] for boss in manifeste['bosses']]
routes_livre = sorted(page['route'] for page in livre['pages'] if page['phase'] == 'PHASE_6')
if sorted(routes_manifeste) != routes_livre:
    print(f'Routes du manifeste et routes P6 du plan divergentes : {sorted(set(routes_manifeste) ^ set(routes_livre))}')
    problemes += 1
if len(manifeste['bosses']) != 14:
    print(f'Attendu 14 fiches de boss dans le manifeste, trouvé {len(manifeste["bosses"])}')
    problemes += 1

# Chaque fiche de boss doit déclarer une source de chaque type de données.
sources = json.loads((ROOT / 'docs/sources.json').read_text(encoding='utf-8'))['sources']
for boss in manifeste['bosses']:
    declarees = {page['route']: page for page in livre['pages']}[boss['route']]['sourcesDeDepart']
    types = {sources[cle]['type'] for cle in declarees if cle in sources}
    if 'Données communautaires' not in types:
        print(f'{boss["route"]} · aucune source de données déclarée')
        problemes += 1
    if not any(t.startswith(('Avis communautaire', 'Suivi communautaire', 'Analyse communautaire',
                             'Wiki communautaire', 'Code ouvert')) for t in types):
        print(f'{boss["route"]} · aucune source communautaire déclarée')
        problemes += 1
    if len(boss.get('communaute', [])) < 3:
        print(f'{boss["route"]} · moins de trois avis communautaires')
        problemes += 1

print(f'{len(fragments)} fragments contrôlés · {problemes} problème(s).')
sys.exit(1 if problemes else 0)
