#!/usr/bin/env python3
"""Génère les treize routes de la phase 5 : arsenal, dix familles, balistique et tableau.

Sortie reproductible : les gabarits (templates/armes.html.tmpl),
les fragments éditoriaux (templates/armes/*.html.part) et le manifeste
(templates/armes-phase-5.json) sont les seules sources à éditer. Les chiffres
proviennent de js/data/weapons.json, js/data/ammo.json et
js/data/weapon-pieces.json, issus de l'instantané communautaire du 18 novembre 2026.
"""
import argparse
import json
import os
import posixpath
import re
import sys
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from images_objets import miniature

DATE = '2026-11-18'

FAMILLES_FR = {
    'fusils-assaut': 'Fusils d’assaut et carabines',
    'pistolets-mitrailleurs': 'Pistolets-mitrailleurs',
    'fusils-a-pompe': 'Fusils à pompe',
    'fusils-de-precision': 'Fusils de précision à verrou',
    'dmr': 'Fusils de précision semi-auto',
    'mitrailleuses': 'Mitrailleuses légères',
    'pistolets': 'Pistolets et revolvers',
    'arme-de-melee': 'Armes de mêlée',
    'lance-grenades': 'Lance-grenades et lanceurs',
    'pieces': 'Modifications et accessoires',
}

SLUGS_FAMILLES = {
    'fusils-assaut': 'assault-rifles',
    'pistolets-mitrailleurs': 'smgs',
    'fusils-a-pompe': 'shotguns',
    'fusils-de-precision': 'sniper-rifles',
    'dmr': 'dmrs',
    'mitrailleuses': 'lmgs',
    'pistolets': 'pistols',
    'arme-de-melee': 'melee',
    'lance-grenades': 'grenade-launchers',
    'pieces': 'weapon-mods',
}


def text(valeur):
    return escape(str(valeur), quote=True)


def lire(chemin):
    return json.loads((ROOT / chemin).read_text(encoding='utf-8'))


def nombre(valeur, suffixe=''):
    if valeur is None:
        return '—'
    if isinstance(valeur, float) and valeur.is_integer():
        valeur = int(valeur)
    if isinstance(valeur, (int, float)):
        return f'{valeur:,}'.replace(',', '\u202f') + suffixe
    return text(valeur)


def tableau(caption, entetes, lignes, classes=None, resume='', attributs=None, id_table=None):
    if not lignes:
        return (f'<div class="armes-panel"><p class="armes-note">{text(resume or "Aucun élément relevé dans les sources consultées.")}</p></div>')
    head = ''.join(f'<th scope="col">{text(h)}</th>' for h in entetes)
    corps = ''
    for index, ligne in enumerate(lignes):
        classe = ''
        if classes:
            classe = classes(ligne) or ''
        extra = ''
        if attributs:
            attributs_ligne = attributs[index] or {}
            extra = ''.join(f' {cle}="{text(valeur)}"' for cle, valeur in attributs_ligne.items())
        cells = ''.join(f'<td>{c}</td>' for c in ligne)
        corps += f'<tr class="{classe}"{extra}>{cells}</tr>'
    ident = f' id="{text(id_table)}"' if id_table else ''
    return (f'<div class="table-wrap" tabindex="0" role="group" aria-label="{text(caption)}"><table class="armes-table"{ident}>'
            f'<caption>{text(caption)}</caption><thead><tr>{head}</tr></thead>'
            f'<tbody>{corps}</tbody></table></div>')


# --------------------------------------------------------------------------
# Tableaux de l'arsenal
# --------------------------------------------------------------------------

def lignes_arme(arme):
    modes = ', '.join(arme['modeTirFr']) or '—'
    return [
        miniature('armes', arme.get('nom')) or '—',
        text(arme['nom']),
        f'<small>{text(arme["calibre"])}</small>',
        text(arme['ergonomie']),
        text(arme['reculVertical']),
        text(arme['reculHorizontal']),
        text(arme['cadence']),
        text(arme['distanceEfficace']),
        f'<small>{text(modes)}</small>',
        text(arme['nbMunitions']),
        text(len(arme['presets'])),
    ]


def attributs_arme(arme):
    return {
        'data-nom': arme['nom'] or '',
        'data-famille': arme['famille'] or '',
        'data-calibre': arme['calibre'] or '',
        'data-marchand': 'oui' if arme['disponibleChezMarchand'] else 'non',
        'data-ergonomie': arme['ergonomie'] if arme['ergonomie'] is not None else '',
        'data-recul': arme['reculVertical'] if arme['reculVertical'] is not None else '',
        'data-cadence': arme['cadence'] if arme['cadence'] is not None else '',
    }


def table_catalogue(armes, legende, id_table=None):
    lignes = [lignes_arme(a) for a in armes]
    return tableau(legende,
                   ['Image', 'Arme', 'Calibre', 'Ergonomie', 'Recul vertical', 'Recul horizontal',
                    'Cadence (c/min)', 'Distance efficace (m)', 'Modes de tir', 'Munitions', 'Presets'],
                   lignes,
                   resume='Aucune arme ne correspond à ce périmètre dans l’instantané consulté.',
                   attributs=[attributs_arme(a) for a in armes], id_table=id_table)


def lignes_preset(arme, preset):
    return [
        f'<strong>{text(preset["nom"])}</strong><small>{text(arme["nom"])}</small>',
        text(preset['ergonomie']),
        text(preset['reculVertical']),
        text(preset['reculHorizontal']),
        text(preset['precision']),
        'preset par défaut' if preset['parDefaut'] else 'preset publié',
    ]


def table_presets(armes, limite=None):
    lignes = []
    for arme in armes:
        for preset in arme['presets']:
            if preset['parDefaut']:
                continue
            lignes.append(lignes_preset(arme, preset))
    if limite:
        lignes = lignes[:limite]
    return tableau('Presets publiés pour les armes de la famille, avec les mesures reprises dans l’export.',
                   ['Preset', 'Ergonomie', 'Recul vertical', 'Recul horizontal', 'Précision (MOA)', 'État'],
                   lignes,
                   resume='Aucun preset publié pour cette famille dans l’instantané consulté.')


def table_acquisition(armes):
    lignes = []
    for arme in armes:
        if not arme['disponibleChezMarchand']:
            continue
        marchands = ', '.join(arme['marchands']) or '—'
        lignes.append([
            text(arme['nom']),
            f'<small>{text(marchands)}</small>',
            text(arme['niveauMarchand']),
            nombre(arme['prixMarchand'], ' ₽'),
        ])
    return tableau('Armes vendues en magasin dans l’instantané, avec le niveau de fidélité le plus bas relevé.',
                   ['Arme', 'Marchands', 'Niveau de fidélité', 'Prix'],
                   lignes,
                   resume='Aucune vente en magasin relevée pour cette famille dans l’instantané consulté.')


def table_pieces(pieces, limite=None):
    lignes = []
    for piece in pieces:
        lignes.append([
            text(piece['nom']),
            f'<small>{text(piece["slot"])}</small>',
            text(piece['poids']),
            nombre(piece['prixBase'], ' ₽'),
        ])
    if limite:
        lignes = lignes[:limite]
    return tableau('Pièces d’arme classées par emplacement, avec poids et prix de base de l’export.',
                   ['Pièce', 'Emplacement', 'Poids (kg)', 'Prix de base'],
                   lignes,
                   resume='Aucune pièce relevée pour ce périmètre dans l’instantané consulté.')


def table_emplacements(pieces):
    compte = {}
    for piece in pieces:
        compte.setdefault(piece['slot'], []).append(piece)
    lignes = []
    for slot in sorted(compte, key=lambda s: (-len(compte[s]), s)):
        lot = compte[slot]
        poids = [p['poids'] for p in lot if isinstance(p['poids'], (int, float))]
        prix = [p['prixBase'] for p in lot if isinstance(p['prixBase'], (int, float))]
        lignes.append([
            text(slot),
            text(len(lot)),
            f'{min(poids):.2f} – {max(poids):.2f}' if poids else '—',
            f'{nombre(min(prix))} – {nombre(max(prix))}' if prix else '—',
        ])
    return tableau('Emplacements de pièces d’arme et volume de références dans l’export.',
                   ['Emplacement', 'Références', 'Poids (kg)', 'Prix de base (₽)'],
                   lignes)


# --------------------------------------------------------------------------
# Tableaux de munitions
# --------------------------------------------------------------------------

def lignes_munition(munition, armure=False):
    base = [
        miniature('munitions', munition.get('nom')) or '—',
        f'<strong>{text(munition["nom"])}</strong>',
        f'<small>{text(munition["calibre"])}</small>',
        text(munition['degats']),
        text(munition['penetration']),
        text(munition['degatsArmure']),
    ]
    if armure:
        base.append(text(munition['classeAtteinte']) if munition['classeAtteinte'] else '—')
        base.append(text(munition['vitesse']))
    else:
        base.append(f'<small>{text(munition["typeProjectile"])}</small>')
        base.append(text(munition['nbProjectiles']))
        base.append(f'<small>{text(munition["fragmentation"])}</small>')
    return base


def table_calibres(munitions):
    groupes = {}
    for munition in munitions:
        groupes.setdefault(munition['calibre'], []).append(munition)
    lignes = []
    for calibre in sorted(groupes):
        lot = groupes[calibre]
        penetrations = [m['penetration'] for m in lot if m['penetration'] is not None]
        degats = [m['degats'] for m in lot if m['degats'] is not None]
        marchands = sum(1 for m in lot if m['disponibleChezMarchand'])
        meilleure = max(lot, key=lambda m: (m['penetration'] or 0, m['degats'] or 0))
        lignes.append([
            text(calibre),
            text(len(lot)),
            f'{min(penetrations)} – {max(penetrations)}' if penetrations else '—',
            f'{min(degats)} – {max(degats)}' if degats else '—',
            f'<small>{text(meilleure["nom"])}</small>',
            f'{marchands} / {len(lot)}',
        ])
    return tableau('Les trente et un calibres de l’export, avec la pénétration et les dégâts observés.',
                   ['Calibre', 'Cartouches', 'Pénétration', 'Dégâts', 'Cartouche la plus pénétrante', 'En magasin'],
                   lignes)


def table_classes(munitions):
    lignes = []
    for classe in range(1, 7):
        seuil = classe * 10
        garanti = seuil + 15
        atteignent = [m for m in munitions if (m['penetration'] or 0) >= seuil]
        franchissent = [m for m in munitions if (m['penetration'] or 0) >= garanti]
        lignes.append([
            f'<strong>Classe {classe}</strong>',
            f'≈ {seuil}',
            f'≥ {garanti}',
            text(len(atteignent)),
            text(len(franchissent)),
            f'<small>{text(", ".join(m["court"] or m["nom"] for m in franchissent[:4]) or "aucune")}</small>',
        ])
    return tableau('Classes d’armure et cartouches qui les atteignent ou les franchissent selon la règle du correctif 0.14.6.0.',
                   ['Classe d’armure', 'Durabilité effective (intacte)', 'Pénétration franchissant', 'Cartouches à la classe', 'Cartouches franchissant', 'Exemples'],
                   lignes)


def table_achats(munitions):
    niveaux = {}
    for munition in munitions:
        if munition['disponibleChezMarchand']:
            niveaux.setdefault(munition['niveauMarchand'], []).append(munition)
    lignes = []
    for niveau in sorted(niveaux, key=lambda n: (n is None, n)):
        lot = niveaux[niveau]
        prix = [m['prixMarchand'] for m in lot if isinstance(m['prixMarchand'], int)]
        marchands = {}
        for munition in lot:
            for nom in munition['marchands']:
                marchands[nom] = marchands.get(nom, 0) + 1
        detail = ', '.join(f'{nom} ({n})' for nom, n in sorted(marchands.items(), key=lambda kv: (-kv[1], kv[0])))
        lignes.append([
            f'Niveau {niveau}',
            text(len(lot)),
            f'{nombre(min(prix))} – {nombre(max(prix))}' if prix else '—',
            f'<small>{text(detail)}</small>',
        ])
    sans = [m for m in munitions if not m['disponibleChezMarchand']]
    lignes.append(['Sans offre en magasin', text(len(sans)), '—', '<small>prix de marché uniquement</small>'])
    return tableau('Offres marchandes en roubles par niveau de fidélité, sur les deux cents cartouches de l’export.',
                   ['Niveau de fidélité', 'Cartouches', 'Prix en roubles', 'Répartition par marchand'],
                   lignes)


def attributs_munition(munition):
    return {
        'data-nom': munition['nom'] or '',
        'data-calibre': munition['calibre'] or '',
        'data-marchand': 'oui' if munition['disponibleChezMarchand'] else 'non',
        'data-type': munition['typeProjectile'] or '',
        'data-penetration': munition['penetration'] if munition['penetration'] is not None else '',
        'data-degats': munition['degats'] if munition['degats'] is not None else '',
        'data-classe': munition['classeAtteinte'] if munition['classeAtteinte'] else '',
        'data-traceur': 'oui' if munition['traceur'] else 'non',
        'data-multi': 'oui' if (munition['nbProjectiles'] or 1) > 1 else 'non',
    }


def table_munitions(munitions, id_table=None):
    lignes = [lignes_munition(m) for m in munitions]
    return tableau('Les deux cents cartouches de l’export, avec projectiles, dégâts, pénétration et fragmentation.',
                   ['Image', 'Cartouche', 'Calibre', 'Dégâts', 'Pénétration', 'Dégâts d’armure', 'Type', 'Projectiles', 'Fragmentation'],
                   lignes, attributs=[attributs_munition(m) for m in munitions], id_table=id_table)


def table_grenades(grenades):
    lignes = []
    for grenade in grenades:
        lignes.append([
            text(grenade['nom']),
            f'<small>{text(grenade["type"])}</small>',
            text(grenade['delai']),
            f'{grenade["rayonMin"]} – {grenade["rayonMax"]}' if grenade['rayonMin'] is not None else '—',
            text(grenade['fragments']),
            text(grenade['rayonContusion']),
        ])
    return tableau('Grenades à main de l’export, avec délai, rayons d’explosion et nombre de fragments.',
                   ['Grenade', 'Type', 'Délai (s)', 'Rayon d’explosion (m)', 'Fragments', 'Rayon de contusion (m)'],
                   lignes)


# --------------------------------------------------------------------------
# Contenu
# --------------------------------------------------------------------------

def sources_html(cles, sources, route=None, livre=None):
    if route is not None and livre is not None:
        declarees = set(livre[route].get('sourcesDeDepart', []))
        manque = sorted(set(cles) - declarees)
        if manque:
            raise ValueError(f'Sources non déclarées dans le manifeste pour {route} : {manque}')
    items = []
    for cle in cles:
        source = sources[cle]
        items.append(f'<li><a class="link" href="{text(source["url"])}" rel="nofollow noopener" target="_blank">{text(source["titre"])}</a>'
                     f'<small>{text(source["type"])}</small></li>')
    return ('<ul class="sources-list">\n' + '\n'.join(items) + '\n</ul>')


def bloc_sources(cles, sources, note):
    return (f'<section class="field-section armes-section" id="sources" tabindex="-1">\n'
            f'<h2>Sources</h2>\n<p>{text(note)}</p>\n{sources_html(cles, sources)}\n</section>')


def rendre(check=False):
    gabarit = Template((ROOT / 'templates/armes.html.tmpl').read_text(encoding='utf-8'))
    livre = {p['route']: p for p in lire('docs/pages.json')['pages']}
    sources = lire('docs/sources.json')['sources']
    manifeste = lire('templates/armes-phase-5.json')
    donnees_armes = lire('js/data/weapons.json')
    donnees_pieces = lire('js/data/weapon-pieces.json')
    donnees_ammo = lire('js/data/ammo.json')
    base = os.getenv('TUG_PUBLIC_URL', '')
    if base and not base.endswith('/'):
        base += '/'

    armes = donnees_armes['armes']
    pieces = donnees_pieces['pieces']
    munitions = donnees_ammo['munitions']
    par_famille = {}
    for arme in armes:
        par_famille.setdefault(arme['famille'], []).append(arme)

    hub_arme = manifeste['hub']
    hub_ammo = manifeste['hub_ammo']
    outil = manifeste['outil']

    def nav(route, cible, libelle, style=''):
        href = posixpath.relpath(cible, posixpath.dirname(route))
        courant = ' aria-current="page"' if cible == route else ''
        return f'<a href="{text(href)}"{style}{courant}>{text(libelle)}</a>'

    def liens_hero(entrees):
        return ''.join(f'<a class="button {"button--primary" if i == 0 else "button--quiet"}" href="#{text(section)}" data-expand-target>{text(label)} <span class="button__arrow" aria-hidden="true">{"↓" if i == 0 else "↘"}</span></a>'
                       for i, (section, label) in enumerate(entrees))

    def toc_html(entrees):
        return ''.join(f'<li><a href="#{text(section)}" data-expand-target><span aria-hidden="true">{i:02d}</span>{text(label)}</a></li>'
                       for i, (section, label) in enumerate(entrees, 1))

    def strip_html(paires):
        return ''.join(f'<div><dt>{text(libelle)}</dt><dd>{text(valeur)}</dd></div>' for valeur, libelle in paires)

    def sortie(route, fiche, corps, hub_route, hub_label, aside):
        page = livre[route]
        racine = '../' * route.count('/')
        if hub_route == route:
            crumb_hub = f'<span>{text(hub_label)}</span>'
        else:
            crumb_hub = (f'<a href="{text(racine + posixpath.relpath(hub_route, "."))}">{text(hub_label)}</a>')
        image = fiche['image']
        illustration = (ROOT / image).is_file()
        largeur = hauteur = 0
        if illustration:
            from PIL import Image
            with Image.open(ROOT / image) as source:
                largeur, hauteur = source.size
        canonical = (base + route) if base else './' + posixpath.basename(route)
        shareimage = (base if base else racine) + image
        titre = f"{page['titre']} — Tarkov Ultimate Guide"
        ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': page['titre'],
              'description': fiche['description'], 'dateModified': DATE, 'inLanguage': 'fr-FR',
              'author': {'@type': 'Organization', 'name': 'Tarkov Ultimate Guide'}}
        if base:
            ld.update(url=canonical, image=shareimage)
        valeurs = {cle: text(fiche[cle]) for cle in ('slug', 'description', 'image', 'alt', 'crumb', 'kicker',
                                                      'headline', 'headline_tail', 'lead', 'scene', 'aside_note')}
        valeurs['hero_image'] = (f'<img class="field-hero__image" src="{text(racine + image)}" width="{largeur}" '
                                  f'height="{hauteur}" fetchpriority="high" alt="{text(fiche["alt"])}">') if illustration else ''
        valeurs['preload'] = (f'<link rel="preload" as="image" href="{text(racine + image)}" fetchpriority="high">') if illustration else ''
        valeurs.update(
            title=text(titre), canonical=text(canonical), shareimage=text(shareimage), root=racine,
            shareimage_width=str(largeur), shareimage_height=str(hauteur),
            article_label=text(page['titre']),
            structured=json.dumps(ld, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'),
            hero_links=liens_hero(fiche['hero_links']), strip=strip_html(fiche['strip']),
            toc=toc_html(fiche['toc']), content=corps.rstrip(),
            hub_link=text(posixpath.relpath(hub_route, posixpath.dirname(route))),
            hub_label=text(hub_label), aside_note=text(aside), crumb_hub=crumb_hub,
            guide_entry=nav(route, 'pages/getting-started.html', 'Premiers pas'),
            lore_entry=nav(route, 'pages/lore/index.html', 'Norvinsk'),
            atlas_entry=nav(route, 'pages/maps/index.html', 'Atlas'),
            arsenal_entry=nav(route, 'pages/weapons/index.html', 'Arsenal'),
            arsenal_nav=nav(route, 'pages/weapons/index.html', 'Arsenal', ' class="commandbar__nav-link"'),
        )
        html = gabarit.substitute(valeurs)
        cible = ROOT / route
        if check:
            if not cible.is_file() or cible.read_text(encoding='utf-8') != html:
                raise SystemExit(f'Rejouer scripts/rendre_armes.py : {route} diverge de son gabarit')
        else:
            etape = cible.with_suffix('.html.tmp')
            etape.write_text(html, encoding='utf-8')
            etape.replace(cible)
        return illustration

    # --- Hub arsenal ------------------------------------------------------
    corps = (ROOT / 'templates/armes/arsenal.html.part').read_text(encoding='utf-8')
    corps = Template(corps).substitute(root='../' * hub_arme['route'].count('/'))
    grille = []
    for fiche in manifeste['families']:
        famille = fiche['famille']
        lot = par_famille.get(famille, [])
        calibre = len({a['calibre'] for a in lot})
        marchands = sum(1 for a in lot if a['disponibleChezMarchand'])
        route = posixpath.relpath(fiche['route'], 'pages/weapons')
        grille.append(
            f'<article class="armes-card" data-armes-card data-famille="{text(famille)}">'
            f'<h3><a href="{text(route)}">{text(fiche["titre"])}</a></h3>'
            f'<p>{text(fiche["description"])}</p>'
            f'<div class="armes-card__meta">'
            f'<span class="badge">{len(lot)} armes</span>'
            f'<span class="badge">{calibre} calibres</span>'
            f'<span class="badge">{marchands} en magasin</span>'
            f'</div></article>')
    corps = corps.replace('%%GRILLE_FAMILLES%%', '\n'.join(grille))
    corps = corps.replace('%%TABLE_CATALOGUE%%', table_catalogue(
        armes, 'Les cent quatre-vingt-dix-neuf armes de l’export, avec leurs mesures à configuration de base.',
        id_table='armes-catalogue'))
    corps = corps.replace('%%JSON_ARSENAL%%', json.dumps(
        [{'id': a['id'], 'nom': a['nom'], 'famille': a['famille'], 'calibre': a['calibre'],
          'ergonomie': a['ergonomie'], 'reculVertical': a['reculVertical'], 'reculHorizontal': a['reculHorizontal'],
          'cadence': a['cadence'], 'distanceEfficace': a['distanceEfficace'], 'porteeVisée': a['porteeVisée'],
          'modeTirFr': a['modeTirFr'], 'nbMunitions': a['nbMunitions'], 'nbPresets': len(a['presets']),
          'poids': a['poids'], 'prixMarchand': a['prixMarchand'], 'niveauMarchand': a['niveauMarchand'],
          'marchands': a['marchands'], 'disponibleChezMarchand': a['disponibleChezMarchand']} for a in armes],
        ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'))
    corps = corps.replace('%%TABLE_SELECTION%%', table_catalogue(
        sorted(armes, key=lambda a: (-(a['ergonomie'] or 0), a['nom'] or ''))[:8],
        'Huit armes à l’ergonomie la plus haute de l’export, toutes configurations confondues.'))
    corps = corps.replace('%%TABLE_RECUL%%', table_catalogue(
        sorted(armes, key=lambda a: (a['reculVertical'] if a['reculVertical'] is not None else 9999, a['nom'] or ''))[:8],
        'Huit armes au recul vertical le plus faible de l’export, à configuration de base.'))
    corps = corps.replace('%%TABLE_CADENCE%%', table_catalogue(
        sorted(armes, key=lambda a: (-(a['cadence'] or 0), a['nom'] or ''))[:8],
        'Huit armes à la cadence de tir la plus élevée de l’export.'))
    corps = corps.replace('%%TABLE_DISTANCE%%', table_catalogue(
        sorted(armes, key=lambda a: (-(a['distanceEfficace'] or 0), a['nom'] or ''))[:8],
        'Huit armes à la distance efficace la plus longue de l’export.'))
    corps = corps.replace('%%SOURCES_ARSENAL%%', sources_html(
        ['data-weapons', 'data-items', 'data-index', 'wiki', 'kappa', 'bsg-0146', 'senseos-armure'],
        sources, hub_arme['route'], livre))
    restant = re.findall(r'%%[A-Z_]+%%', corps)
    if restant:
        raise ValueError(f'Marqueur non résolu dans {hub_arme["route"]} : {sorted(set(restant))}')
    sortie(hub_arme['route'], hub_arme, corps, hub_arme['route'], hub_arme['titre'],
           hub_arme['aside_note'])
    print(f'{hub_arme["route"]} · {len(armes)} armes au catalogue · {len(manifeste["families"])} familles')

    # --- Fiches de famille -------------------------------------------------
    for fiche in manifeste['families']:
        famille = fiche['famille']
        lot = par_famille.get(famille, [])
        if famille == 'pieces':
            corps = (ROOT / 'templates/armes/weapon-mods.html.part').read_text(encoding='utf-8')
            corps = Template(corps).substitute(root='../' * fiche['route'].count('/'))
            corps = corps.replace('%%TABLE_EMPLACEMENTS%%', table_emplacements(pieces))
            corps = corps.replace('%%TABLE_PIECES%%', table_pieces(pieces, limite=120))
            corps = corps.replace('%%SOURCES_FAMILLE%%', sources_html(
                ['data-weapons', 'data-items', 'data-index', 'wiki', 'reddit-equilibrage', 'reddit-equilibrage-2'],
                sources, fiche['route'], livre))
        else:
            corps = (ROOT / f'templates/armes/{fiche["slug"]}.html.part').read_text(encoding='utf-8')
            corps = Template(corps).substitute(root='../' * fiche['route'].count('/'))
            corps = corps.replace('%%TABLE_CATALOGUE%%', table_catalogue(lot, f'Les {len(lot)} armes de la famille, avec leurs mesures à configuration de base.'))
            corps = corps.replace('%%TABLE_PRESETS%%', table_presets(lot, limite=90))
            corps = corps.replace('%%TABLE_ACQUISITION%%', table_acquisition(lot))
            corps = corps.replace('%%SOURCES_FAMILLE%%', sources_html(
                ['data-weapons', 'data-items', 'data-index', 'wiki', 'kappa'], sources, fiche['route'], livre))
        restant = re.findall(r'%%[A-Z_]+%%', corps)
        if restant:
            raise ValueError(f'Marqueur non résolu dans {fiche["route"]} : {sorted(set(restant))}')
        sortie(fiche['route'], fiche, corps, hub_arme['route'], hub_arme['titre'], fiche['aside_note'])
        print(f'{fiche["route"]} · {len(lot)} entrées de catalogue · {fiche["titre"]}')

    # --- Hub munitions -----------------------------------------------------
    corps = (ROOT / 'templates/armes/balistique.html.part').read_text(encoding='utf-8')
    corps = Template(corps).substitute(root='../' * hub_ammo['route'].count('/'))
    corps = corps.replace('%%TABLE_CLASSES%%', table_classes(munitions))
    corps = corps.replace('%%TABLE_CALIBRES%%', table_calibres(munitions))
    corps = corps.replace('%%TABLE_ACHATS%%', table_achats(munitions))
    corps = corps.replace('%%TABLE_GRENADES%%', table_grenades(donnees_ammo['grenades']))
    corps = corps.replace('%%TABLE_TRACEURS%%', table_munitions(
        [m for m in munitions if m['traceur']]))
    corps = corps.replace('%%SOURCES_AMMO%%', sources_html(
        ['data-items', 'wiki-ballistics', 'wiki-ammo-sample', 'bsg-0146', 'bsg-0145', 'bsg-0140',
         'senseos-armure', 'senseos-munitions', 'leprestore-munitions'], sources, hub_ammo['route'], livre))
    restant = re.findall(r'%%[A-Z_]+%%', corps)
    if restant:
        raise ValueError(f'Marqueur non résolu dans {hub_ammo["route"]} : {sorted(set(restant))}')
    sortie(hub_ammo['route'], hub_ammo, corps, hub_ammo['route'], hub_ammo['titre'], hub_ammo['aside_note'])
    print(f'{hub_ammo["route"]} · {len(munitions)} cartouches · {len(donnees_ammo["calibres"])} calibres')

    # --- Tableau balistique ------------------------------------------------
    corps = (ROOT / 'templates/armes/tableau-balistique.html.part').read_text(encoding='utf-8')
    corps = Template(corps).substitute(root='../' * outil['route'].count('/'))
    corps = corps.replace('%%TABLE_MUNITIONS%%', table_munitions(munitions, id_table='ammo-tableau'))
    corps = corps.replace('%%JSON_MUNITIONS%%', json.dumps(
        [{'id': m['id'], 'nom': m['nom'], 'calibre': m['calibre'], 'degats': m['degats'],
          'penetration': m['penetration'], 'degatsArmure': m['degatsArmure'],
          'typeProjectile': m['typeProjectile'], 'nbProjectiles': m['nbProjectiles'],
          'fragmentation': m['fragmentation'], 'vitesse': m['vitesse'],
          'classeAtteinte': m['classeAtteinte'], 'traceur': m['traceur'],
          'prixMarchand': m['prixMarchand'], 'niveauMarchand': m['niveauMarchand'],
          'disponibleChezMarchand': m['disponibleChezMarchand'],
          'dernierBas': m['dernierBas'], 'moyenne24h': m['moyenne24h'], 'horodatage': m['horodatage']}
         for m in munitions],
        ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'))
    corps = corps.replace('%%SOURCES_OUTIL%%', sources_html(
        ['data-items', 'data-index', 'wiki-ballistics', 'wiki-ammo-sample', 'bsg-0146', 'senseos-munitions'],
        sources, outil['route'], livre))
    restant = re.findall(r'%%[A-Z_]+%%', corps)
    if restant:
        raise ValueError(f'Marqueur non résolu dans {outil["route"]} : {sorted(set(restant))}')
    sortie(outil['route'], outil, corps, hub_ammo['route'], hub_ammo['titre'], outil['aside_note'])
    print(f'{outil["route"]} · {len(munitions)} cartouches listées')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--check', action='store_true', help='vérifier sans réécrire')
    rendre(cli.parse_args().check)
