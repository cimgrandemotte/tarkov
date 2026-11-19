#!/usr/bin/env python3
"""Génère l'atlas et les treize fiches de lieu de la phase 4.

Sortie reproductible : les gabarits (templates/atlas.html.tmpl, templates/carte.html.tmpl),
les fragments éditoriaux (templates/cartes/*.html.part) et le manifeste
(templates/cartes-phase-4.json) sont les seules sources à éditer.
"""
import argparse
import json
import os
import posixpath
import re
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
CAMP_FR = {'pmc': 'PMC', 'scav': 'Scav', 'shared': 'PMC et Scav', 'both': 'PMC et Scav'}
DANGER_FR = {'minefield': 'Champ de mines', 'sniper': 'Sniper de bordure', 'claymore': 'Claymore'}
MODE_FR = {'regular': 'PvP Zone', 'pve': 'PvE Zone', 'pvp-season': 'PvP Season'}
MENACE_FR = {'minefield': 'mines', 'sniper': 'snipers', 'claymore': 'claymores'}
DATE = '2026-11-18'


def text(value):
    return escape(str(value), quote=True)


def charger(chemin):
    return json.loads((ROOT / chemin).read_text(encoding='utf-8'))


def tableau(caption, entetes, lignes, classes=None, resume='', attributs=None):
    if not lignes:
        return (f'<div class="map-panel"><p class="map-note">{text(resume or "Aucun élément relevé dans les sources consultées.")}</p></div>')
    head = ''.join(f'<th scope="col">{text(h)}</th>' for h in entetes)
    corps = ''
    for ligne in lignes:
        classe = ''
        if classes:
            classe = classes(ligne) or ''
        extra = ''
        if attributs:
            attributs_ligne = attributs(ligne) or {}
            extra = ''.join(f' {cle}="{text(valeur)}"' for cle, valeur in attributs_ligne.items())
        cells = ''.join(f'<td>{c}</td>' for c in ligne)
        corps += f'<tr class="{classe}"{extra}>{cells}</tr>'
    return (f'<div class="table-wrap" tabindex="0" role="group" aria-label="{text(caption)}"><table class="map-table">'
            f'<caption>{text(caption)}</caption><thead><tr>{head}</tr></thead>'
            f'<tbody>{corps}</tbody></table></div>')


def _camp_associe(camp):
    if camp in ('shared', 'both'):
        return 'shared'
    if camp == 'scav':
        return 'scav'
    return 'pmc'


def petit(valeur, vrai='✔', faux='✘'):
    if valeur is None:
        return '<small>non précisé</small>'
    return vrai if valeur else faux


def table_sorties(lieu):
    lignes = []
    for sortie in lieu['sorties']:
        conditions = sortie['conditions'] or '—'
        notes = sortie['notes'] or ''
        libelle = sortie.get('libelleJeu')
        nom = text(sortie['nom'])
        if libelle:
            nom += f'<small>libellé de jeu : {text(libelle)}</small>'
        lignes.append([
            nom,
            text(sortie['campFr']),
            petit(sortie['toujoursDisponible']),
            petit(sortie['usageUnique']),
            f'<small>{text(conditions)}</small>',
            f'<small>{text(notes)}</small>' if notes else '—',
            _camp_associe(sortie['camp']),
        ])
    return tableau('Sorties documentées par la fiche publique consultée.',
                   ['Sortie', 'Camp', 'Toujours ouverte', 'Usage unique', 'Conditions', 'Notes'],
                   lignes,
                   classes=lambda l: 'map-table__row--' + l[6],
                   attributs=lambda l: {'data-camp-row': l[6]},
                   resume='Aucune sortie documentée dans la fiche consultée.')


def table_sorties_jeu(lieu):
    lignes = []
    for sortie in lieu['sortiesJeu']:
        lignes.append([
            text(sortie['libelle']),
            f'<small>{text(sortie["nom"])}</small>',
            text(sortie['campFr']),
            'oui' if sortie['interrupteur'] else 'non',
            'retrouvée dans la fiche publique' if sortie['dansFicheWiki'] else 'absente de la fiche publique',
        ])
    return tableau('Intitulés de sortie dans les données de jeu.',
                   ['Libellé français', 'Intitulé de jeu', 'Camp', 'Commandée par un interrupteur', 'Correspondance'],
                   lignes,
                   resume='Aucune sortie recensée dans les données de jeu consultées.')


def table_transits(lieu):
    lignes = []
    for transit in lieu['transits']:
        lignes.append([
            text(transit['nomFr']),
            text(transit.get('vers') or '—'),
            text(CAMP_FR.get(transit.get('camp'), '—')) if transit.get('camp') else '—',
            f'<small>{text(transit["conditions"] or "—")}</small>',
            f'<small>{text(transit["notes"] or "—")}</small>',
        ])
    return tableau('Transits relevés dans les données de jeu et la fiche publique.',
                   ['Transit', 'Destination', 'Camp', 'Conditions', 'Emplacement'],
                   lignes,
                   resume='Aucun transit sortant relevé pour ce lieu. Les entrées par transit sont décrites dans la prose de la fiche.')


def table_rencontres(lieu):
    lignes = []
    for boss in lieu['boss']:
        chance = boss.get('chance')
        zones = ', '.join(boss.get('zones') or []) or '—'
        escortes = ', '.join(f"{e['nom']} ×{e['nombre']}" for e in boss.get('escortes') or []) or '—'
        lignes.append([
            text(boss['nom']),
            'présence certaine' if chance == 1 else (f'{int(chance * 100)} %' if isinstance(chance, (int, float)) else '—'),
            f'<small>{text(zones)}</small>',
            f'<small>{text(escortes)}</small>',
            f'<small>{text(boss.get("zone") or "—")}</small>',
        ])
    return tableau('Rencontres et probabilités issues de l’instantané des données de jeu.',
                   ['Rencontre', 'Présence', 'Zones de spawn', 'Escortes', 'Localisation (fiche publique)'],
                   lignes,
                   resume='Aucune rencontre bosses recensée pour ce lieu.')


def table_dangers(lieu):
    lignes = []
    for type_, nombre in (lieu.get('dangers') or {}).items():
        lignes.append([text(DANGER_FR.get(type_, type_)), text(nombre), 'zones invisibles ou balisées selon le type'])
    return tableau('Zones de danger relevées dans les données de la carte.',
                   ['Type de danger', 'Occurrences', 'Nature'],
                   lignes,
                   resume='Aucune zone de danger relevée dans les données de la carte.')


def table_modes(lieu):
    lignes = []
    for mode in ('regular', 'pve', 'pvp-season'):
        bloc = (lieu.get('parMode') or {}).get(mode)
        if not bloc:
            continue
        lignes.append([
            text(MODE_FR[mode]),
            f'{bloc["dureeMinutes"]} min',
            text(bloc['joueurs']),
            text(bloc['sortiesPMC']),
            text(bloc['sortiesScav']),
            f'<small>{text(", ".join(bloc["boss"]) or "—")}</small>',
            f'<small>{text(", ".join(bloc["ennemis"]) or "—")}</small>',
        ])
    return tableau('Comparaison des profils de jeu pour ce lieu.',
                   ['Profil', 'Durée', 'Effectif', 'Sorties PMC', 'Sorties Scav', 'Rencontres', 'Ennemis'],
                   lignes,
                   resume='Aucun profil disponible pour ce lieu.')


def table_variantes(lieu):
    lignes = []
    for variante in lieu.get('variantes') or []:
        lignes.append([
            text(variante['nom']),
            f'<small>{text(variante["libelle"])}</small>',
            f'{variante["dureeMinutes"]} min',
            text(variante['joueurs']),
            text(variante['sorties']),
            f'<small>{text(", ".join(b["nom"] for b in variante.get("boss") or []) or "—")}</small>',
        ])
    return tableau('Variantes rattachées à ce lieu dans les données de jeu.',
                   ['Variante', 'Rattachement', 'Durée', 'Effectif', 'Sorties', 'Rencontres'],
                   lignes,
                   resume='Aucune variante recensée pour ce lieu.')


def table_cles(lieu):
    cles = lieu.get('clesWiki') or []
    if not cles:
        return '<div class="map-panel"><p class="map-note">Aucune clé recensée dans la fiche publique consultée.</p></div>'
    items = []
    for cle in cles[:24]:
        drapeau = ' <small>accès permanent documenté</small>' if cle.get('toujoursOuvert') else ''
        quete = f' <small>quête : {text(cle["quete"])}</small>' if cle.get('quete') and not cle['quete'].startswith('style=') else ''
        items.append(f'<li><strong>{text(cle["nom"])}</strong>{drapeau}{quete}</li>')
    suite = ''
    if len(cles) > 24:
        suite = f'<p class="map-note">Liste tronquée : {len(cles) - 24} clé(s) supplémentaires figurent dans la fiche publique.</p>'
    return (f'<div class="map-panel"><ul class="map-steps">{chr(10).join(items)}</ul>{suite}</div>')


def table_ecarts(lieu):
    ecarts = lieu.get('ecartsModes') or []
    if not ecarts:
        return ('<div class="map-panel"><p class="map-note">Les trois profils consultés présentent le même découpage '
                'pour ce lieu : aucune différence de durée, d’effectif, de sorties ou de rencontres relevée.</p></div>')
    blocs = []
    for ecart in ecarts:
        details = ''.join(f'<li>{text(detail)}</li>' for detail in ecart['details'])
        blocs.append(f'<div class="map-path"><strong>{text(MODE_FR[ecart["mode"]])}</strong><ul class="map-steps">{details}</ul></div>')
    return f'<div class="map-paths">{"".join(blocs)}</div>'


def table_transits_atlas(lieux):
    lignes = []
    for lieu in lieux:
        for transit in lieu['transits']:
            lignes.append([
                text(lieu['nom']),
                text(transit['nomFr']),
                text(transit.get('vers') or '—'),
                f'<small>{text(transit["conditions"] or "—")}</small>',
                f'<small>{text(transit["notes"] or "—")}</small>',
            ])
    return tableau('Tous les transits sortants relevés dans l’instantané du 18 novembre 2026.',
                   ['Lieu de départ', 'Transit', 'Destination', 'Conditions', 'Emplacement'],
                   lignes,
                   resume='Aucun transit sortant relevé.')


def table_variantes_atlas(lieux):
    lignes = []
    for lieu in lieux:
        for variante in lieu.get('variantes') or []:
            image = IMAGES_VARIANTES.get(variante['slug'])
            img = f'<img class="variante-thumb" src="{text(image)}" alt="Variante {text(variante["nom"])}" width="1376" height="768" loading="lazy">' if image else '<span class="variante-thumb variante-thumb--vide">—</span>'
            lignes.append([
                text(lieu['nom']),
                img,
                text(variante['nom']),
                f'<small>{text(variante["libelle"])}</small>',
                f'{variante["dureeMinutes"]} min',
                text(variante['joueurs']),
                text(variante['sorties']),
                f'<small>{text(", ".join(b["nom"] for b in variante.get("boss") or []) or "—")}</small>',
            ])
    return tableau('Variantes rattachées aux lieux de référence dans l’instantané du 18 novembre 2026.',
                   ['Lieu', 'Image', 'Variante', 'Rattachement', 'Durée', 'Effectif', 'Sorties', 'Rencontres'],
                   lignes,
                   resume='Aucune variante recensée.')


def _profils_ecartes(lieu):
    """Profils dont les rencontres ou ennemis diffèrent du profil de référence PvP Zone."""
    reference = (lieu.get('parMode') or {}).get('regular') or {}
    ecarts = ['regular']
    for mode in ('pve', 'pvp-season'):
        bloc = (lieu.get('parMode') or {}).get(mode)
        if not bloc:
            continue
        if bloc['boss'] != reference.get('boss') or bloc['ennemis'] != reference.get('ennemis'):
            ecarts.append(mode)
    return ecarts


def _menaces(lieu):
    return [MENACE_FR[type_] for type_ in (lieu.get('dangers') or {}) if type_ in MENACE_FR]


def grille_lieux(lieux, routes):
    cartes = []
    for lieu in lieux:
        route = routes[lieu['slug']]
        profil = lieu.get('parMode') or {}
        badges = [f'{lieu["dureeMinutes"]} min', f'{lieu["joueurs"]} PMC',
                  f'{len(lieu["sorties"])} sorties', f'{len(lieu["transits"])} transits']
        recherche = ' '.join([lieu['nom'], lieu.get('nomOfficiel') or '', ' '.join(badges),
                              ' '.join(sorted({b['nom'] for b in lieu['boss']})),
                              ' '.join(c['nom'] for c in (lieu.get('clesWiki') or [])[:8])])
        modes = ' '.join(_profils_ecartes(lieu))
        menaces = ' '.join(_menaces(lieu))
        ecarts = [mode for mode in ('pve', 'pvp-season') if mode in modes]
        mention = 'Profils identiques au profil de référence' if not ecarts else 'Écarts : ' + ', '.join(MODE_FR[m] for m in ecarts)
        # Chaque image du site doit être unique : la grille de l'atlas utilise
        # une image d'index dediee, distincte de l'image de la fiche carte.
        slug = lieu['slug']
        image_index = IMAGES_INDEX.get(slug)
        if image_index:
            media = (f'<div class="atlas-card__media"><img src="{text(image_index)}" width="1376" '
                     f'height="768" loading="lazy" decoding="async" alt="Vue generale de " + text(lieu["nom"])></div>')
        else:
            media = f'<div class="atlas-card__media atlas-card__media--plaque"><span class="atlas-card__plaque">{text(lieu["nom"])}</span></div>'
        cartes.append(
            f'<article class="atlas-card" data-atlas-card data-recherche="{text(recherche)}" data-modes="{text(modes)}" data-threat="{text(menaces)}">'
            f'{media}'
            f'<div class="atlas-card__body"><h3><a href="{text(route["lien"])}">{text(lieu["nom"])}</a></h3>'
            f'<p>{text(lieu["description"][:150])}</p>'
            f'<div class="atlas-card__meta">{"".join(f"<span class=\'badge\'>{text(badge)}</span>" for badge in badges)}</div>'
            f'<p class="muted small">{text(mention)}</p></div></article>')
    return '\n'.join(cartes)


def json_comparatif(lieux):
    entrees = []
    for lieu in lieux:
        entrees.append({
            'slug': lieu['slug'],
            'nom': lieu['nom'],
            'duree': lieu['dureeMinutes'],
            'joueurs': lieu['joueurs'],
            'niveaux': f"{lieu['niveaux']['min']}-{lieu['niveaux']['max']}",
            'sortiesPmc': sum(1 for s in lieu['sorties'] if s['camp'] == 'pmc'),
            'sortiesScav': sum(1 for s in lieu['sorties'] if s['camp'] == 'scav'),
            'sortiesPartagees': sum(1 for s in lieu['sorties'] if s['camp'] in ('shared', 'both')),
            'transits': len(lieu['transits']),
            'boss': ', '.join(sorted({b['nom'] for b in lieu['boss']})) or '—',
            'dangers': ', '.join(f"{DANGER_FR.get(k, k)} ×{v}" for k, v in (lieu.get('dangers') or {}).items()) or '—',
            'variantes': ', '.join(v['nom'] for v in (lieu.get('variantes') or [])) or '—',
            'cles': len(lieu.get('clesWiki') or []),
        })
    return json.dumps(entrees, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')


TABLES = {
    '%%TABLE_SORTIES%%': table_sorties,
    '%%TABLE_SORTIES_JEU%%': table_sorties_jeu,
    '%%TABLE_TRANSITS%%': table_transits,
    '%%TABLE_RENCONTRES%%': table_rencontres,
    '%%TABLE_DANGERS%%': table_dangers,
    '%%TABLE_MODES%%': table_modes,
    '%%TABLE_VARIANTES%%': table_variantes,
    '%%TABLE_CLES%%': table_cles,
    '%%TABLE_ECARTS%%': table_ecarts,
}


def dimensions(chemin):
    from PIL import Image
    with Image.open(ROOT / chemin) as source:
        return source.size


# Correspondance entre un lieu et l'image d'index dediee de la grille de l'atlas.
# Chaque image doit etre unique sur le site : l'index n'utilise jamais l'image de
# la fiche carte, mais une image d'index distincte.
IMAGES_INDEX = {
    'factory': '../../images/maps/index/factory-halle.jpg',
    'customs': '../../images/maps/index/customs-pont.jpg',
    'woods': '../../images/maps/index/woods-lac.jpg',
    'shoreline': '../../images/maps/index/shoreline.jpg',
    'interchange': '../../images/maps/index/interchange.jpg',
    'reserve': '../../images/maps/index/reserve.jpg',
    'the-lab': '../../images/maps/index/the-lab.jpg',
    'lighthouse': '../../images/maps/index/lighthouse.jpg',
    'streets-of-tarkov': '../../images/maps/index/streets-of-tarkov.jpg',
    'ground-zero': '../../images/maps/index/ground-zero.jpg',
    'the-labyrinth': '../../images/maps/index/the-labyrinth.jpg',
    'icebreaker': '../../images/maps/index/icebreaker.jpg',
    'terminal': '../../images/maps/index/terminal.jpg',
}

# Images d'index des variantes de cartes (rattachees a un lieu parent).
# Chaque image est unique sur le site : l'index n'utilise jamais l'image de
# la fiche carte, mais une image d'index distincte.
IMAGES_VARIANTES = {
    'night-factory': '../../images/maps/index/night-factory.jpg',
    'ground-zero-21': '../../images/maps/index/ground-zero-21.jpg',
    'ground-zero-tutorial': '../../images/maps/index/ground-zero-tutorial.jpg',
    'the-lab-dark': '../../images/maps/index/the-lab-dark.jpg',
    'infected-lab': '../../images/maps/index/infected-lab.jpg',
    'infected-factory': '../../images/maps/index/infected-factory.jpg',
}

def image_disponible(chemin):
    return (ROOT / chemin).is_file()


def rendre(check=False):
    gabarit_carte = Template((ROOT / 'templates/carte.html.tmpl').read_text(encoding='utf-8'))
    gabarit_atlas = Template((ROOT / 'templates/atlas.html.tmpl').read_text(encoding='utf-8'))
    livre = {p['route']: p for p in charger('docs/pages.json')['pages']}
    sources = charger('docs/sources.json')['sources']
    manifeste = charger('templates/cartes-phase-4.json')
    hub = manifeste['hub']
    fiches = manifeste['fiches']
    donnees = {lieu['slug']: lieu for lieu in charger('js/data/maps.json')['lieux']}
    base = os.getenv('TUG_PUBLIC_URL', '')
    toc_commun = manifeste['toc_commun']
    hero_commun = manifeste['hero_commun']

    def sources_manquantes(route, corps):
        refs = set()

        def externe(match):
            cle = match.group(1)
            refs.add(cle)
            return text(sources[cle]['url'])

        corps = re.sub(r'@source:([A-Za-z0-9_-]+)@', externe, corps)
        if not refs <= set(livre[route]['sourcesDeDepart']):
            manque = sorted(refs - set(livre[route]['sourcesDeDepart']))
            raise ValueError(f'Sources non déclarées dans le manifeste pour {route} : {manque}')
        return corps, refs

    def nav(route, cible, libelle, style=''):
        href = posixpath.relpath(cible, posixpath.dirname(route))
        courant = ' aria-current="page"' if cible == route else ''
        return f'<a href="{text(href)}"{style}{courant}>{text(libelle)}</a>'

    # --- Atlas -----------------------------------------------------------
    route = hub['route']
    page = livre[route]
    racine = '../' * route.count('/')
    corps = (ROOT / 'templates/cartes/atlas.html.part').read_text(encoding='utf-8')
    corps = Template(corps).substitute(root=racine)
    corps, refs = sources_manquantes(route, corps)
    for lieu in donnees.values():
        pass
    liens_atlas = {}
    for fiche in fiches:
        illustration = image_disponible(fiche['image'])
        largeur, hauteur = dimensions(fiche['image']) if illustration else (0, 0)
        liens_atlas[fiche['slug']] = {
            'image': racine + fiche['image'],
            'alt': fiche['alt'],
            'illustration': illustration,
            'lien': posixpath.relpath(fiche['route'], posixpath.dirname(route)),
            'largeur': largeur,
            'hauteur': hauteur,
        }
    corps = corps.replace('%%GRILLE_LIEUX%%', grille_lieux([donnees[f['slug']] for f in fiches], liens_atlas))
    corps = corps.replace('%%JSON_COMPARATIF%%', json_comparatif([donnees[f['slug']] for f in fiches]))
    corps = corps.replace('%%TABLE_TRANSITS_ATLAS%%', table_transits_atlas([donnees[f['slug']] for f in fiches]))
    corps = corps.replace('%%TABLE_VARIANTES_ATLAS%%', table_variantes_atlas([donnees[f['slug']] for f in fiches]))
    restant = re.findall(r'%%[A-Z_]+%%', corps)
    if restant:
        raise ValueError(f'Marqueur non résolu dans {route} : {sorted(set(restant))}')
    illustration_hub = image_disponible(hub['image'])
    largeur, hauteur = dimensions(hub['image']) if illustration_hub else (0, 0)
    hero_hub = (f'<img src="{text(racine + hub["image"])}" width="{largeur}" height="{hauteur}" fetchpriority="high" '
                f'alt="{text(hub["alt"])}">') if illustration_hub else ''
    preload_hub = (f'<link rel="preload" as="image" href="{text(racine + hub["image"])}" fetchpriority="high">') if illustration_hub else ''
    liens = ''.join(f'<a class="button {"button--primary" if i == 0 else "button--quiet"}" href="#{text(section)}" data-expand-target>{text(label)} <span class="button__arrow" aria-hidden="true">{"↓" if i == 0 else "↘"}</span></a>'
                    for i, (section, label) in enumerate(hub['hero_links']))
    toc = ''.join(f'<li><a href="#{text(section)}" data-expand-target><span aria-hidden="true">{i:02d}</span>{text(label)}</a></li>'
                  for i, (section, label) in enumerate(hub['toc'], 1))
    strip = ''.join(f'<div><dt>{text(label)}</dt><dd>{text(valeur)}</dd></div>' for valeur, label in hub['strip'])
    canonical = (base + route) if base else './' + posixpath.basename(route)
    shareimage = (base if base else racine) + hub['image']
    titre = f"{page['titre']} — Tarkov Ultimate Guide"
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': page['titre'],
          'description': hub['description'], 'dateModified': DATE, 'inLanguage': 'fr-FR',
          'author': {'@type': 'Organization', 'name': 'Tarkov Ultimate Guide'},
          'hasPart': [{'@type': 'Article', 'headline': f["titre"], 'url': posixpath.join(base, f['route'])} for f in fiches]}
    if base:
        ld['url'] = canonical
        ld['image'] = shareimage
    valeurs = {cle: text(hub[cle]) for cle in ('slug', 'description', 'image', 'alt', 'kicker', 'headline',
                                               'headline_tail', 'lead', 'scene', 'aside_note')}
    valeurs.update(title=text(titre), canonical=text(canonical), shareimage=text(shareimage), root=racine,
                   hero_image=hero_hub, preload=preload_hub,
                   shareimage_width=str(largeur), shareimage_height=str(hauteur),
                   hero_class='' if illustration_hub else 'atlas-hero--plaque',
                   article_label=text(page['titre']),
                   structured=json.dumps(ld, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'),
                   guide_entry=nav(route, 'pages/getting-started.html', 'Premiers pas'),
                   lore_entry=nav(route, 'pages/lore/index.html', 'Norvinsk'),
                   atlas_entry=nav(route, 'pages/maps/index.html', 'Atlas', ' class="commandbar__nav-link"'),
                   hero_links=liens, strip=strip, toc=toc, content=corps.rstrip())
    sortie = gabarit_atlas.substitute(valeurs)
    cible = ROOT / route
    if check:
        if not cible.is_file() or cible.read_text(encoding='utf-8') != sortie:
            raise SystemExit(f'Rejouer scripts/rendre_cartes.py : {route} diverge de son gabarit')
    else:
        etape = cible.with_suffix('.html.tmp')
        etape.write_text(sortie, encoding='utf-8')
        etape.replace(cible)
    print(f'{route} · {len(refs)} références directes · {len(fiches)} fiches indexées')

    # --- Fiches de lieu ---------------------------------------------------
    for item in fiches:
        route = item['route']
        slug = item['slug']
        page = livre[route]
        lieu = donnees[slug]
        image = item['image']
        illustration = image_disponible(image)
        assert 145 <= len(item['description']) <= 165, f'description hors gabarit : {slug} ({len(item["description"])})'
        corps = (ROOT / f'templates/cartes/{slug}.html.part').read_text(encoding='utf-8')
        racine = '../' * route.count('/')
        corps = Template(corps).substitute(root=racine)
        corps, refs = sources_manquantes(route, corps)
        for marqueur, fonction in TABLES.items():
            corps = corps.replace(marqueur, fonction(lieu))
        restant = re.findall(r'%%[A-Z_]+%%', corps)
        if restant:
            raise ValueError(f'Marqueur de table non résolu dans {route} : {sorted(set(restant))}')
        navs = {
            'guide_entry': nav(route, 'pages/getting-started.html', 'Premiers pas'),
            'lore_entry': nav(route, 'pages/lore/index.html', 'Norvinsk'),
            'atlas_entry': nav(route, 'pages/maps/index.html', 'Atlas'),
            'atlas_nav': nav(route, 'pages/maps/index.html', 'Cartes', ' class="commandbar__nav-link"'),
        }
        hero_links = item.get('hero_links') or hero_commun
        toc_items = item.get('toc') or toc_commun
        liens = ''.join(f'<a class="button {"button--primary" if i == 0 else "button--quiet"}" href="#{text(section)}" data-expand-target>{text(label)} <span class="button__arrow" aria-hidden="true">{"↓" if i == 0 else "↘"}</span></a>'
                        for i, (section, label) in enumerate(hero_links))
        toc = ''.join(f'<li><a href="#{text(section)}" data-expand-target><span aria-hidden="true">{i:02d}</span>{text(label)}</a></li>'
                      for i, (section, label) in enumerate(toc_items, 1))
        strip = ''.join(f'<div><dt>{text(label)}</dt><dd>{text(valeur)}</dd></div>' for valeur, label in item['strip'])
        canonical = (base + route) if base else './' + posixpath.basename(route)
        shareimage = (base if base else racine) + image
        titre = f"{page['titre']} — Tarkov Ultimate Guide"
        ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': page['titre'],
              'description': item['description'], 'dateModified': DATE, 'inLanguage': 'fr-FR',
              'author': {'@type': 'Organization', 'name': 'Tarkov Ultimate Guide'}}
        if base:
            ld.update(url=canonical, image=shareimage)
        largeur, hauteur = dimensions(image) if illustration else (0, 0)
        valeurs = {cle: text(item[cle]) for cle in ('slug', 'description', 'image', 'alt', 'crumb', 'kicker', 'headline',
                                                    'headline_tail', 'lead', 'scene', 'aside_note')}
        valeurs['hero_image'] = (f'<img class="field-hero__image" src="{text(racine + image)}" width="{largeur}" '
                                 f'height="{hauteur}" fetchpriority="high" alt="{text(item["alt"])}">') if illustration else ''
        valeurs['hero_class'] = '' if illustration else 'field-hero--plaque'
        valeurs['preload'] = (f'<link rel="preload" as="image" href="{text(racine + image)}" fetchpriority="high">') if illustration else ''
        valeurs.update(title=text(titre), canonical=text(canonical), shareimage=text(shareimage), root=racine,
                       image_width=str(largeur), image_height=str(hauteur),
                       shareimage_width=str(largeur), shareimage_height=str(hauteur),
                       article_label=text(page['titre']),
                       structured=json.dumps(ld, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'),
                       hero_links=liens, strip=strip, toc=toc, content=corps.rstrip(), **navs)
        sortie = gabarit_carte.substitute(valeurs)
        cible = ROOT / route
        if check:
            if not cible.is_file() or cible.read_text(encoding='utf-8') != sortie:
                raise SystemExit(f'Rejouer scripts/rendre_cartes.py : {route} diverge de son gabarit')
        else:
            etape = cible.with_suffix('.html.tmp')
            etape.write_text(sortie, encoding='utf-8')
            etape.replace(cible)
        print(f'{route} · {len(refs)} références directes · {len(lieu["sorties"])} sorties documentées · '
              f'{len(lieu["sortiesJeu"])} intitulés de jeu')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--check', action='store_true', help='vérifier sans réécrire')
    rendre(cli.parse_args().check)
