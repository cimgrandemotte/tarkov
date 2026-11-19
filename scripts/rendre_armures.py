#!/usr/bin/env python3
"""Génère les vingt routes de la phase 6 : armures, comparaison et boss.

Sortie reproductible : les gabarits (templates/armures.html.tmpl),
les fragments éditoriaux (templates/armures/*.html.part) et le manifeste
(templates/armures-phase-6.json) sont les seules sources à éditer. Les chiffres
proviennent de js/data/armor.json et js/data/bosses.json, issus de
l'instantané communautaire du 18 novembre 2026.
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

CATEGORIES_FR = {
    'Gilet tactique': 'Gilet tactique',
    'Gilet pare-balles': 'Gilet pare-balles',
    'Casque': 'Casque',
    'Masque': 'Masque',
    'Plaque de blindage': 'Plaque de blindage',
    'Accessoire blindé': 'Accessoire blindé',
    'Protection oculaire': 'Protection oculaire',
}

MODES_FR = {'regular': 'PvP Zone', 'pve': 'PvE Zone', 'pvp-season': 'Seasonal'}

TYPES_FR = {
    'provisions': 'vivres',
    'keys': 'clés',
    'meds': 'soins',
    'barter': 'troc',
    'noFlea': 'hors marché',
    'injectors': 'injecteurs',
    'grenade': 'grenade',
    'container': 'conteneur',
    'specialSlot': 'emplacement spécial',
}

CARTES_FR = {
    'customs': 'Customs',
    'interchange': 'Interchange',
    'woods': 'Forest',
    'reserve': 'Reserve',
    'shoreline': 'Shoreline',
    'terminal': 'Terminal',
    'factory': 'Factory',
    'streets-of-tarkov': 'Streets of Tarkov',
    'lighthouse': 'Lighthouse',
    'the-lab-dark': 'Laboratoire',
    'the-labyrinth': 'Labyrinth',
    'icebreaker': 'Icebreaker',
    'ground-zero-21': 'Ground Zero',
    'night-factory': 'Factory nocturne',
    'buildings': 'Buildings',
    'laboratory': 'Laboratoire',
    'shoreline-2': 'Shoreline',
    'train-station': 'Gare',
}


def text(valeur):
    return escape(str(valeur), quote=True)


def lire(chemin):
    return json.loads((ROOT / chemin).read_text(encoding='utf-8'))


def nombre(valeur, suffixe='', decimales=None):
    if valeur is None:
        return '—'
    if isinstance(valeur, float):
        if decimales is not None:
            valeur = round(valeur, decimales)
        elif valeur.is_integer():
            valeur = int(valeur)
    if isinstance(valeur, (int, float)):
        if decimales is not None and not isinstance(valeur, int):
            texte = f'{valeur:.{decimales}f}'.replace('.', ',')
        else:
            texte = f'{valeur:,}'.replace(',', '\u202f')
        return texte + suffixe
    return text(valeur)


def pourcentage(valeur):
    if valeur is None:
        return '—'
    return f'{valeur * 100:.0f}\u202f%'.replace('.', ',')


def carte_fr(nom):
    return CARTES_FR.get(nom, (nom or '—').replace('-', ' ').capitalize())


def tableau(caption, entetes, lignes, classes=None, resume='', attributs=None, id_table=None):
    if not lignes:
        return (f'<div class="armures-panel"><p class="armures-note">{text(resume or "Aucun élément relevé dans les sources consultées.")}</p></div>')
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
    return (f'<div class="table-wrap" tabindex="0" role="group" aria-label="{text(caption)}"><table class="armures-table"{ident}>'
            f'<caption>{text(caption)}</caption><thead><tr>{head}</tr></thead>'
            f'<tbody>{corps}</tbody></table></div>')


def sources_html(cles, sources, route=None, livre=None):
    if route is not None and livre is not None:
        declarees = set(livre[route].get('sourcesDeDepart', []))
        manque = sorted(set(cles) - declarees)
        if manque:
            raise ValueError(f'Sources non déclarées dans le manifeste pour {route} : {manque}')
        non_utilisees = sorted(declarees - set(cles))
        if non_utilisees:
            raise ValueError(f'Sources déclarées sans citation pour {route} : {non_utilisees}')
    items = []
    for cle in cles:
        source = sources[cle]
        items.append(f'<li><a class="link" href="{text(source["url"])}" rel="nofollow noopener" target="_blank">{text(source["titre"])}</a>'
                     f'<small>{text(source["type"])}</small></li>')
    return ('<ul class="sources-list">\n' + '\n'.join(items) + '\n</ul>')


# --------------------------------------------------------------------------
# Tableaux d'armure
# --------------------------------------------------------------------------

def table_materiaux(materiaux):
    lignes = []
    for materiau in materiaux:
        lignes.append([
            f'<strong>{text(materiau["nom"])}</strong>',
            text(materiau['destructibilite']),
            f'{materiau["usureReparationMin"] * 100:.0f}\u202f% – {materiau["usureReparationMax"] * 100:.0f}\u202f%'.replace('.', ','),
            f'{materiau["usureKitReparationMin"] * 100:.0f}\u202f% – {materiau["usureKitReparationMax"] * 100:.0f}\u202f%'.replace('.', ','),
        ])
    return tableau('Les huit matériaux de blindage de l’export, avec destructibilité et usure de réparation.',
                   ['Matériau', 'Destructibilité', 'Usure (réparation)', 'Usure (kit de réparation)'],
                   lignes)


def table_classes(pieces):
    lignes = []
    for classe in range(1, 7):
        lot = [p for p in pieces if p['classe'] == classe]
        materiaux = {}
        for piece in lot:
            if piece['materiau']:
                materiaux[piece['materiau']] = materiaux.get(piece['materiau'], 0) + 1
        dominants = ', '.join(nom for nom, _ in sorted(materiaux.items(), key=lambda kv: (-kv[1], kv[0]))[:3])
        durees = [p['duree'] for p in lot if p['duree']]
        lignes.append([
            f'<strong>Classe {classe}</strong>',
            text(len(lot)),
            nombre(min(durees)) + ' – ' + nombre(max(durees)) if durees else '—',
            f'<small>{text(dominants)}</small>',
        ])
    sans = [p for p in pieces if not p['classe']]
    lignes.append([
        '<strong>Sans classe</strong>',
        text(len(sans)),
        '—',
        f'<small>{text(", ".join(sorted({p["categorie"] for p in sans})))}</small>',
    ])
    return tableau('Répartition des pièces de l’export par classe d’armure, avec les matériaux dominants.',
                   ['Classe', 'Pièces', 'Durabilité', 'Matériaux dominants'],
                   lignes)


def lignes_piece(piece):
    emplacements = piece['emplacements']
    plaques = sum(1 for e in emplacements if e['plaquesAutorisees'])
    zones = len(piece['zones'])
    return [
        miniature('armures', piece.get('nom')) or '—',
        f'<strong>{text(piece["nom"])}</strong><small>{text(piece["categorie"])}</small>',
        text(piece['classe']) if piece['classe'] else '—',
        f'<small>{text(piece["materiau"] or "—")}</small>',
        nombre(piece['duree']),
        text(zones),
        nombre(piece['poids'], ' kg', decimales=2),
        f'{plaques} / {len(emplacements)}',
        nombre(piece['prixBase'], ' ₽'),
    ]


def attributs_piece(piece):
    return {
        'data-nom': piece['nom'] or '',
        'data-categorie': piece['categorie'] or '',
        'data-classe': str(piece['classe']) if piece['classe'] else 'sans',
        'data-materiau': piece['materiau'] or 'Non relevé',
        'data-poids': piece['poids'] if piece['poids'] is not None else '',
        'data-plaques': 'oui' if any(e['plaquesAutorisees'] for e in piece['emplacements']) else 'non',
    }


def table_catalogue(pieces, legende, id_table=None):
    lignes = [lignes_piece(p) for p in pieces]
    return tableau(legende,
                   ['Image', 'Pièce', 'Classe', 'Matériau', 'Durabilité', 'Zones', 'Poids (kg)',
                    'Emplacements à plaques', 'Prix de base (₽)'],
                   lignes,
                   resume='Aucune pièce ne correspond à ce périmètre dans l’instantané consulté.',
                   attributs=[attributs_piece(p) for p in pieces],
                   id_table=id_table)


def table_emplacements(pieces):
    compte = {}
    for piece in pieces:
        for emplacement in piece['emplacements']:
            if not emplacement['plaquesAutorisees']:
                continue
            compte.setdefault(emplacement['nom'], []).append(emplacement)
    lignes = []
    for nom in sorted(compte, key=lambda n: (-len(compte[n]), n)):
        lot = compte[nom]
        plaques = set()
        classes = set()
        for emplacement in lot:
            plaques.update(emplacement.get('idsPlaquesAutorisees') or [])
            if emplacement.get('classeMax'):
                classes.add(emplacement['classeMax'])
        lignes.append([
            f'<strong>{text(nom)}</strong>',
            text(len(lot)),
            text(len(plaques)),
            f'{min(classes)} – {max(classes)}' if classes else '—',
        ])
    return tableau('Emplacements acceptant des plaques, avec le nombre de pièces qui les proposent et le nombre de plaques autorisées.',
                   ['Emplacement', 'Pièces', 'Plaques autorisées', 'Classe maximale'],
                   lignes)


def table_plaques(pieces):
    plaques = [p for p in pieces if p['categorie'] == 'Plaque de blindage']
    lignes = []
    for plaque in sorted(plaques, key=lambda p: (-(p['classe'] or 0), p['nom'] or '')):
        lignes.append([
            f'<strong>{text(plaque["nom"])}</strong>',
            text(plaque['classe']) if plaque['classe'] else '—',
            f'<small>{text(plaque["materiau"] or "—")}</small>',
            nombre(plaque['duree']),
            text(len(plaque['zones'])),
            nombre(plaque['poids'], ' kg', decimales=2),
            f'{plaque["ricochet"]["z"]}\u202f%' if plaque['ricochet'].get('z') else '—',
            nombre(plaque['prixBase'], ' ₽'),
        ])
    return tableau('Les trente-huit plaques de blindage de l’export, classées par classe puis par nom.',
                   ['Plaque', 'Classe', 'Matériau', 'Durabilité', 'Zones', 'Poids (kg)', 'Ricochet (z)', 'Prix de base (₽)'],
                   lignes)


def table_mode(lignes_mode):
    return tableau('Les quatre couches de la protection et ce que chacune mesure.',
                   ['Couche', 'Ce qu’elle mesure', 'Où la lire'],
                   lignes_mode)


# --------------------------------------------------------------------------
# Tableaux de boss
# --------------------------------------------------------------------------

def table_pv(fiche):
    total = fiche['pvTotal'] or 1
    lignes = []
    for membre in sorted(fiche['pv'], key=lambda m: -m['pv']):
        part = membre['pv'] / total * 100
        lignes.append([
            f'<strong>{text(membre["membre"])}</strong>',
            nombre(membre['pv']),
            f'{part:.0f}\u202f%'.replace('.', ','),
            f'<small>{text(membre["id"])}</small>',
        ])
    return tableau(f'Points de vie par zone du corps — total de {nombre(fiche["pvTotal"])} points.',
                   ['Zone', 'Points de vie', 'Part du total', 'Identifiant'],
                   lignes)


def table_apparitions(fiche):
    lignes = []
    for apparition in fiche['apparitions']:
        zones = apparition['zones']
        noms = ', '.join(z['zone'] for z in zones)
        chances = ', '.join(
            f'{z["zone"]} ({pourcentage(z["chance"])})' for z in zones if z['chance'] not in (None, 1)
        ) or 'zone unique'
        deltas = []
        for zone in zones:
            for escorte in zone['escortes']:
                for quantite in escorte['quantites']:
                    nom = fiche['nomsEscortes'].get(escorte['mob'], escorte['mob'])
                    deltas.append(f'{nom} × {quantite["nombre"]} ({pourcentage(quantite["chance"])})')
        lignes.append([
            f'<strong>{text(MODES_FR.get(apparition["mode"], apparition["mode"]))}</strong>',
            text(carte_fr(apparition['carte'])),
            f'<strong>{pourcentage(apparition["chance"])}</strong>',
            'dès le début' if apparition['tempsApparition'] in (None, -1) else f'{nombre(apparition["tempsApparition"])} s',
            f'<small>{text(chances)}</small>',
            f'<small>{text(", ".join(dict.fromkeys(deltas)) or "aucune")}</small>',
        ])
        del noms
    return tableau('Apparitions relevées dans l’export, profil par profil.',
                   ['Profil', 'Carte', 'Chance', 'Délai de raid', 'Zones', 'Escortes associées'],
                   lignes)


def table_escortes(fiche):
    lignes = []
    for escorte in fiche['escortes']:
        detail = ', '.join(f'{m["membre"]} {nombre(m["pv"])}' for m in sorted(escorte['pv'], key=lambda m: -m['pv']))
        lignes.append([
            f'<strong>{text(escorte["nom"])}</strong>',
            f'<small>{text(escorte["id"])}</small>',
            nombre(escorte['pvTotal']),
            f'<small>{text(detail)}</small>',
        ])
    return tableau('Escortes de la fiche, avec leurs propres points de vie.',
                   ['Escorte', 'Identifiant', 'Points de vie', 'Détail par zone'],
                   lignes)


def table_equipement(fiche):
    lignes = []
    for protection in fiche['equipement']['protections']:
        lignes.append([
            f'<strong>{text(protection["nom"])}</strong>',
            f'<small>{text(protection["slotFr"])}</small>',
            f'<small>{text(protection["categorie"])}</small>',
        ])
    for arme in fiche['equipement']['armes']:
        lignes.append([
            f'<strong>{text(arme["nom"])}</strong>',
            f'<small>{text(arme["slotFr"])}</small>',
            '<small>Arme</small>',
        ])
    for sac in fiche['equipement'].get('sacs', []):
        lignes.append([
            f'<strong>{text(sac["nom"])}</strong>',
            f'<small>{text(sac["slotFr"])}</small>',
            '<small>Sac à dos</small>',
        ])
    return tableau('Équipement porté par le boss : protections, armes et sacs, retenus par emplacement.',
                   ['Objet', 'Emplacement', 'Catégorie'],
                   lignes)


def table_butin(fiche, limite=18):
    lignes = []
    for loot in fiche['loot'][:limite]:
        lignes.append([
            f'<strong>{text(loot["nom"])}</strong>',
            f'<small>{text(", ".join(TYPES_FR.get(t, t) for t in loot["types"]))}</small>',
            f'<strong>{pourcentage(loot["prevalence"])}</strong>',
        ])
    return tableau('Butin de la fiche, par fréquence de sortie relevée dans l’export.',
                   ['Objet', 'Catégories', 'Prévalence'],
                   lignes)


def table_matrice(fiches, boss_data):
    cartes = sorted({a['carte'] for f in fiches for a in f['apparitions']})
    lignes = []
    for carte in cartes:
        entete = [f'<strong>{text(carte_fr(carte))}</strong>']
        for fiche in fiches:
            valeurs = [a for a in fiche['apparitions']
                       if a['carte'] == carte and a['mode'] == 'regular']
            if valeurs:
                entete.append(f'<strong>{pourcentage(valeurs[0]["chance"])}</strong>')
            else:
                entete.append('—')
        lignes.append(entete)
    return tableau('Matrice des apparitions en profil Regular : chance par carte et par fiche.',
                   ['Carte'] + [f['titre'] for f in fiches],
                   lignes)


def table_pv_compare(fiches):
    lignes = []
    for fiche in fiches:
        escortes = fiche['escortes']
        total_escortes = sum(e['pvTotal'] for e in escortes)
        lignes.append([
            f'<strong>{text(fiche["titre"])}</strong>',
            f'<small>{text(fiche["famille"])}</small>',
            f'<strong>{nombre(fiche["pvTotal"])}</strong>',
            f'{nombre(total_escortes)}',
            f'{nombre(fiche["pvTotal"] + total_escortes)}',
            text(fiche['membreLePlusResistant'] or '—'),
            text(fiche['membreLePlusFaible'] or '—'),
        ])
    return tableau('Points de vie comparés des quatorze fiches, avec le total du groupe escorté.',
                   ['Boss', 'Famille', 'PV du chef', 'PV des escortes', 'PV du groupe', 'Zone la plus résistante', 'Zone la plus faible'],
                   lignes)


def table_horsfiche(hors_fiche):
    lignes = []
    attributs = []
    for entree in sorted(hors_fiche, key=lambda e: (-e['pvTotal'], e['nom'])):
        lignes.append([
            f'<strong>{text(entree["nom"])}</strong>',
            f'<small>{text(entree["id"])}</small>',
            nombre(entree['pvTotal']) if entree['pvTotal'] else '—',
        ])
        attributs.append({'data-nom': entree['nom']})
    return tableau('Entrées de l’export sans fiche éditoriale dans la phase 6.',
                   ['Entrée', 'Identifiant', 'Points de vie'],
                   lignes, attributs=attributs)


# --------------------------------------------------------------------------
# Contenu
# --------------------------------------------------------------------------

GUIDES = {
    'body-armor': {
        'categories': ['Gilet pare-balles', 'Plaque de blindage'],
        'le categorie': "Quarante-neuf gilets pare-balles et trente-huit plaques de blindage : c'est la combinaison la plus regardée du jeu, et celle dont les chiffres sont le plus mal compris. Un gilet ne porte pas de classe ; il porte des emplacements, et c'est la plaque qui protège.",
        'nb pieces': '49 + 38',
        'libelle nb': 'Gilets et plaques.',
        'detail nb': "Quarante-neuf gilets pare-balles et trente-huit plaques de blindage dans l'export du 18 novembre 2026.",
        'detail classes': "De la classe 2 à la classe 6 pour les gilets, de la classe 1 à la classe 6 pour les plaques.",
        'detail materiaux': "Aramid pour l'essentiel des gilets ; céramique, acier de blindage et UHMWPE pour les plaques.",
        'callout titre': 'Le gilet n’a pas de classe.',
        'callout texte': "Les gilets pare-balles de l'export affichent une classe, mais c'est la classe de l'armure souple qu'ils embarquent : elle protège le torse et le ventre, pas les bras ni les jambes. Les plaques montées dans leurs emplacements ont leur propre classe, supérieure. Conflater les deux revient à se tromper de deux ordres de grandeur.",
        'lead modele': "Un gilet pare-balles se lit sur deux lignes : la matière de son armure souple, et les plaques qu'il accepte. La première protège ce qui n'est pas dans une poche à plaque ; la seconde protège ce qui l'est.",
        'titre catalogue': 'Les gilets et les plaques',
        'lead catalogue': "Les quarante-neuf gilets pare-balles de l'export, avec leurs emplacements de plaque et le nombre de plaques autorisées pour chacun. Le filtre porte sur la classe, le matériau et le nombre d'emplacements.",
        'note catalogue': "La colonne <em>Emplacements à plaques</em> donne le rapport entre les emplacements qui acceptent une plaque et le nombre total d'emplacements de la pièce.",
        'titre plaques': 'Emplacements et plaques',
        'lead plaques': "Chaque gilet déclare ses emplacements et la liste des plaques autorisées pour chacun. C'est la compatibilité déclarée par l'export, celle que le client vérifie à l'équipement.",
        'note plaques': "Une plaque autorisée n'est pas une plaque compatible partout : la taille de la poche et la géométrie de l'emplacement interviennent aussi.",
        'lead conduite': "Quatre repères pour arbitrer entre deux gilets, à partir des chiffres du catalogue plutôt que des habitudes de forum.",
        'point 1 titre': 'Choisir la plaque avant le gilet.',
        'point 1': "La plaque décide de la classe et de la durabilité. Le gilet décide des zones et du nombre d'emplacements. Un gilet à deux emplacements bien placés vaut mieux qu'un gilet à quatre emplacements mal placés.",
        'point 2 titre': 'Vérifier les zones de l’armure souple.',
        'point 2': "Le gilet protège le torse, le ventre et le bas-ventre par son armure souple. Les bras, les jambes et la tête ne sont couverts que par les plaques et les autres pièces de l'ensemble.",
        'point 3 titre': 'Compter le poids cumulé.',
        'point 3': "Un gilet de onze kilos, un casque lourd et quatre plaques font un ensemble où la mobilité disparaît. Les pénalités de vitesse, de rotation et d'ergonomie de la fiche s'ajoutent aux vôtres.",
        'point 4 titre': 'Réparer, c’est perdre de la durée de vie.',
        'point 4': "La réparation restitue de la résistance mais retire un pourcentage de la durée de vie de la pièce. Sur l'aramid, l'usure est faible ; sur l'acier de blindage, elle l'est aussi ; sur la céramique, elle est forte.",
        'callout fin titre': 'Sur la compatibilité réelle.',
        'callout fin': "L'export liste les objets autorisés par emplacement, mais la validation finale reste celle du client : deux plaques autorisées dans la même fiche peuvent être refusées à l'équipement selon la configuration. Le guide publie la donnée, pas une garantie de pose.",
    },
    'helmets': {
        'categories': ['Casque', 'Masque', 'Protection oculaire'],
        'le categorie': "Quatre-vingt-treize casques, vingt masques et six protections oculaires : la tête est la zone la plus coûteuse à protéger et la plus sensible au poids.",
        'nb pieces': '93 + 20 + 6',
        'libelle nb': 'Casques, masques et protections.',
        'detail nb': "Quatre-vingt-treize casques, vingt masques et six protections oculaires dans l'export du 18 novembre 2026.",
        'detail classes': "De la classe 1 à la classe 5 pour les casques ; jusqu'à la classe 6 pour les masques de soudure.",
        'detail materiaux': "Matériau combiné pour la moitié des casques, puis UHMWPE, aramid et acier de blindage ; verre pour les protections oculaires.",
        'callout titre': 'Le casque protège, la position de la visière compte.',
        'callout texte': "Une visière de classe 6 peut ne couvrir que les yeux. Le classement des protections oculaires de l'export est trompeur si l'on ne regarde pas les zones : la couverture réelle est dans la colonne des zones de chaque pièce.",
        'lead modele': "La protection de la tête se compose de trois strates qui se recouvrent partiellement : le casque, le masque, la protection oculaire. Les strates se gênent entre elles, et c'est là que les compatibilités de l'export deviennent utiles.",
        'titre catalogue': 'Casques, masques et protections oculaires',
        'lead catalogue': "Les cent dix-neuf pièces de tête de l'export, avec leurs zones, leur poids et leur classe. Le filtre porte sur la catégorie, la classe et le matériau.",
        'note catalogue': "Les accessoires blindés — visières, mâchoires, protections d'oreilles — sont comptés à part : ce sont des pièces compatibles d'un casque précis, et non des pièces de tête autonomes.",
        'titre plaques': 'Zones couvertes et emplacements',
        'lead plaques': "Les emplacements d'un casque sont des points d'accroche : coiffe, arrière, oreilles, visière, mâchoire. Les accessoires listés dans chaque fiche d'export donnent la liste des pièces autorisées pour chacun.",
        'note plaques': "Deux casques d'un même modèle peuvent refuser la même visière si la version diffère : l'export distingue les éditions, et le guide les distingue aussi.",
        'lead conduite': "Quatre repères pour arbitrer entre deux casques, à partir des chiffres du catalogue.",
        'point 1 titre': 'Choisir la zone avant le modèle.',
        'point 1': "La tête compte six zones dans l'export : calotte, arrière, oreilles, yeux, mâchoire. Un casque qui ne couvre pas la mâchoire laisse passer les tirs de face, et c'est le cas le plus fréquent.",
        'point 2 titre': 'Mesurer la surdité.',
        'point 2': "Cent douze pièces de l'export portent une valeur de surdité. Elle ne réduit pas vos dégâts : elle coupe des sons, et l'audio porte une part importante de l'information en jeu.",
        'point 3 titre': 'Vérifier les blocages.',
        'point 3': "Cinquante et une pièces bloquent les lunettes, deux casques bloquent le casque audio, et certaines interdisent le port d'un casque de protection. Ces indications viennent de l'export et se vérifient dans le client.",
        'point 4 titre': 'Le ricochet compte autant que la classe.',
        'point 4': "Deux cent vingt-neuf pièces de l'export portent des valeurs de ricochet. Une visière en acier dévie un tir plus souvent qu'une en verre, même si les deux arrêtent la même munition.",
        'callout fin titre': 'Sur les compatibilités.',
        'callout fin': "L'export indique les objets autorisés par emplacement d'équipement, mais la validation finale reste celle du client. Un casque et une visière autorisés dans la même fiche peuvent être refusés ensemble selon la configuration.",
    },
    'rigs': {
        'categories': ['Gilet tactique'],
        'le categorie': "Cent cinq gilets tactiques, de six à vingt-huit emplacements : le rig ne protège pas, il transporte. Sa valeur tient dans ce qu'il permet d'emporter et dans ce qu'il coûte en mobilité.",
        'nb pieces': '105',
        'libelle nb': 'Gilets tactiques.',
        'detail nb': "Cent cinq gilets tactiques dans l'export du 18 novembre 2026, de 0,22 à 12,2 kilos.",
        'detail classes': "De la classe 1 à la classe 6 pour les pièces qui intègrent un blindage.",
        'detail materiaux': "Aramid pour la grande majorité ; titane et UHMWPE pour quelques pièces.",
        'callout titre': 'Un rig n’est pas une classe de protection.',
        'callout texte': "Le rig porte les poches, les emplacements et les sacs. La classe d'un gilet tactique tient à son matériau et à ses zones, pas à sa capacité de rangement : un rig très blindé reste un porteur, et un porte-plaques très capace reste un porteur.",
        'lead modele': "Le rig se lit sur trois lignes : la capacité de rangement, la géométrie des poches et le poids. Les deux dernières ne se déduisent pas de l'export, et la première ne dit rien de l'agencement.",
        'titre catalogue': 'Les cent cinq gilets tactiques',
        'lead catalogue': "Les rigs de l'export, avec leur capacité de rangement, leur poids et leur prix de base. Le filtre porte sur la classe, le matériau et le poids maximal.",
        'note catalogue': "La capacité est un compte d'emplacements, pas un volume : deux emplacements larges valent moins qu'un espace de six emplacements étroits pour ce que vous comptez y mettre.",
        'titre plaques': 'Ce qu’un rig accepte',
        'lead plaques': "Un rig peut proposer des emplacements de plaque : c'est le cas des porte-plaques, qui sont des gilets tactiques au sens de l'export. Les deux usages se combinent, et les deux se paient en poids.",
        'note plaques': "Les porte-plaques les plus blindés sont aussi les plus lourds : le prix de la protection se règle en mobilité, pas en budget seul.",
        'lead conduite': "Quatre repères pour arbitrer entre deux rigs, à partir des chiffres du catalogue.",
        'point 1 titre': 'Compter les emplacements réels.',
        'point 1': "La capacité annoncée compte les poches et les emplacements d'équipement. Une capacité de vingt-quatre sur un modèle étroit n'accueille pas les cartouches longues : la géométrie compte autant que le compte.",
        'point 2 titre': 'Le poids se paie en raid long.',
        'point 2': "Un rig de douze kilos, plus l'armure, plus les armes : la masse totale détermine la vitesse, l'ergonomie et la fatigued au bout du raid.",
        'point 3 titre': 'Choisir la géométrie avant la capacité.',
        'point 3': "Un modèle large accepte des objets volumineux ; un modèle compact garde l'ensemble manoeuvrable. Les contraintes d'emplacement dépendent de la forme du pouch, pas de sa seule taille.",
        'point 4 titre': 'Le prix de base ne dit pas le prix payé.',
        'point 4': "Le prix de base de l'export ignore les frais de marchand et la devise. Pour un rig acheté en magasin, le prix réel dépend du niveau de fidélité du marchand et de ce que le marché propose.",
        'callout fin titre': 'Sur la comparaison des rigs.',
        'callout fin': "Le comparateur d'armures aligne les rigs sur les mêmes colonnes que les autres pièces. Pour deux rigs de capacité équivalente, la ligne qui décide est presque toujours le poids.",
    },
}

MODES_ARMOR = [
    ['<strong>Zone</strong>', 'La partie du corps touchée par un tir. Une pièce couvre un ensemble de zones ; le jeu calcule zone par zone.',
     'Colonne <em>Zones</em> du catalogue'],
    ['<strong>Classe</strong>', "La capacité d'une matière à arrêter une munition, de 1 à 6. Elle appartient à la plaque ou à l'armure souple.",
     'Colonne <em>Classe</em> du catalogue'],
    ['<strong>Durabilité</strong>', "La résistance totale de la pièce avant qu'elle ne cède. Chaque impact en retire une part liée au matériau.",
     'Colonne <em>Durabilité</em> du catalogue'],
    ['<strong>Mobilité</strong>', "Le poids et les pénalités de vitesse, de rotation et d'ergonomie, qui s'ajoutent aux vôtres.",
     'Colonnes <em>Poids</em> et <em>Prix de base</em> du catalogue'],
]


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--check', action='store_true', help='vérifier que les fichiers sur disque correspondent au rendu')
    args = cli.parse_args()

    gabarit = Template((ROOT / 'templates/armures.html.tmpl').read_text(encoding='utf-8'))
    livre = {p['route']: p for p in lire('docs/pages.json')['pages']}
    sources = lire('docs/sources.json')['sources']
    manifeste = lire('templates/armures-phase-6.json')
    donnees_armor = lire('js/data/armor.json')
    donnees_boss = lire('js/data/bosses.json')
    base = os.getenv('TUG_PUBLIC_URL', '')
    if base and not base.endswith('/'):
        base += '/'

    pieces = donnees_armor['pieces']
    materiaux = donnees_armor['materiaux']
    fiches = donnees_boss['fiches']
    hors_fiche = donnees_boss['horsFiche']
    par_slug = {f['slug']: f for f in fiches}

    def nav(route, cible, libelle, style=''):
        href = posixpath.relpath(cible, posixpath.dirname(route))
        courant = ' aria-current="page"' if cible == route else ''
        return f'<a href="{text(href)}"{style}{courant}>{text(libelle)}</a>'

    def liens_hero(entrees):
        return ''.join(f'<a class="button {"button--primary" if i == 0 else "button--quiet"}" href="#{text(section["id"])}" data-expand-target>{text(section["titre"])} <span class="button__arrow" aria-hidden="true">{"↓" if i == 0 else "↘"}</span></a>'
                       for i, section in enumerate(entrees))

    def toc_html(entrees):
        return ''.join(f'<li><a href="#{text(section["id"])}" data-expand-target><span aria-hidden="true">{i:02d}</span>{text(section["titre"])}</a></li>'
                       for i, section in enumerate(entrees, 1))

    def strip_html(paires):
        return ''.join(f'<div><dt>{text(libelle)}</dt><dd>{text(valeur)}</dd></div>' for valeur, libelle in paires)

    def sortie(route, fiche, corps, hub_route, hub_label, aside, strip=None):
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
            hero_links=liens_hero(fiche['hero_links']), strip=strip_html(strip or []),
            toc=toc_html(fiche['toc']), content=corps.rstrip(),
            crumb_hub=crumb_hub,
            guide_entry=nav(route, 'pages/getting-started.html', 'Premiers pas'),
            lore_entry=nav(route, 'pages/lore/index.html', 'Norvinsk'),
            atlas_entry=nav(route, 'pages/maps/index.html', 'Atlas'),
            arsenal_entry=nav(route, 'pages/weapons/index.html', 'Arsenal'),
            armures_nav=(nav(route, 'pages/armor/index.html', 'Armures', ' class="commandbar__nav-link"') + nav(route, 'pages/bosses/index.html', 'Boss', ' class="commandbar__nav-link"')),
        )
        html = gabarit.substitute(valeurs)
        cible = ROOT / route
        if args.check:
            if not cible.is_file() or cible.read_text(encoding='utf-8') != html:
                raise SystemExit(f'Rejouer scripts/rendre_armures.py : {route} diverge de son gabarit')
        else:
            etape = cible.with_suffix('.html.tmp')
            etape.write_text(html, encoding='utf-8')
            etape.replace(cible)
        return illustration

    def resoudre(corps, route, replacements):
        for cle, valeur in replacements.items():
            corps = corps.replace(f'%%{cle}%%', valeur)
        restant = re.findall(r'%%[A-Z_]+%%', corps)
        if restant:
            raise ValueError(f'Marqueur non résolu dans {route} : {sorted(set(restant))}')
        return corps

    # --- Hub armures -------------------------------------------------------
    hub = manifeste['hub_armor']
    corps = (ROOT / 'templates/armures/hub-armor.html.part').read_text(encoding='utf-8')
    corps = Template(corps).substitute(root='../' * hub['route'].count('/'))
    corps = corps.replace('%%TABLE_MATERIAUX%%', table_materiaux(materiaux))
    corps = corps.replace('%%TABLE_CLASSES%%', table_classes(pieces))
    corps = corps.replace('%%TABLE_CATALOGUE%%', table_catalogue(
        pieces, 'Les trois cent quatre-vingt-dix pièces de l’export du 18 novembre 2026.', id_table='armures-catalogue'))
    corps = corps.replace('%%TABLE_EMPLACEMENTS%%', table_emplacements(pieces))
    corps = corps.replace('%%TABLE_PLAQUES%%', table_plaques(pieces))
    corps = corps.replace('%%SOURCES_ARMOR%%', sources_html(
        livre[hub['route']]['sourcesDeDepart'], sources, hub['route'], livre))
    corps = resoudre(corps, hub['route'], {})
    sortie(hub['route'], hub, corps, hub['route'], hub['titre'], hub['aside_note'],
           strip=[(len(pieces), 'Pièces au catalogue'),
                  (len(materiaux), 'Matériaux de blindage'),
                  ('6', "Classes d’armure"),
                  (donnees_armor['statistiques']['avecPlaques'], 'Pièces acceptant des plaques'),
                  (DATE, 'Instantané des données')])
    print(f'{hub["route"]} · {len(pieces)} pièces · {len(materiaux)} matériaux')

    # --- Guides d'armure ----------------------------------------------------
    for cle, route_manifeste in (('armor_body', 'body-armor'), ('armor_helmets', 'helmets'), ('armor_rigs', 'rigs')):
        fiche = manifeste[cle]
        guide = GUIDES[route_manifeste]
        lot = [p for p in pieces if p['categorie'] in guide['categories']]
        corps = (ROOT / 'templates/armures/guide-armor.html.part').read_text(encoding='utf-8')
        corps = Template(corps).substitute(root='../' * fiche['route'].count('/'))
        classes = sorted({p['classe'] for p in lot if p['classe']})
        mats = sorted({p['materiau'] for p in lot if p['materiau']})
        remplacements = {
            'LEAD_CATEGORIE': text(guide['le categorie']),
            'NB_PIECES': text(guide['nb pieces']),
            'LIBELLE_NB': text(guide['libelle nb']),
            'DETAIL_NB': text(guide['detail nb']),
            'CLASSES': text(f'{classes[0]} – {classes[-1]}' if classes else '—'),
            'DETAIL_CLASSES': text(guide['detail classes']),
            'MATERIAUX': text(len(mats)),
            'DETAIL_MATERIAUX': text(guide['detail materiaux']),
            'CALLOUT_TITRE': text(guide['callout titre']),
            'CALLOUT_TEXTE': text(guide['callout texte']),
            'LEAD_MODELE': text(guide['lead modele']),
            'TITRE_CATALOGUE': text(guide['titre catalogue']),
            'LEAD_CATALOGUE': text(guide['lead catalogue']),
            'NOTE_CATALOGUE': text(guide['note catalogue']),
            'TITRE_PLAQUES': text(guide['titre plaques']),
            'LEAD_PLAQUES': text(guide['lead plaques']),
            'NOTE_PLAQUES': text(guide['note plaques']),
            'LEAD_CONDUITE': text(guide['lead conduite']),
            'POINT_1_TITRE': text(guide['point 1 titre']),
            'POINT_1': text(guide['point 1']),
            'POINT_2_TITRE': text(guide['point 2 titre']),
            'POINT_2': text(guide['point 2']),
            'POINT_3_TITRE': text(guide['point 3 titre']),
            'POINT_3': text(guide['point 3']),
            'POINT_4_TITRE': text(guide['point 4 titre']),
            'POINT_4': text(guide['point 4']),
            'CALLOUT_FIN_TITRE': text(guide['callout fin titre']),
            'CALLOUT_FIN': text(guide['callout fin']),
        }
        corps = corps.replace('%%TABLE_MODELE%%', table_mode(MODES_ARMOR))
        corps = corps.replace('%%TABLE_MATERIAUX%%', table_materiaux(materiaux))
        corps = corps.replace('%%TABLE_CLASSES%%', table_classes(lot))
        corps = corps.replace('%%TABLE_CATALOGUE%%', table_catalogue(
            lot, f'Les {len(lot)} pièces de la catégorie, avec leurs caractéristiques dans l’export du 18 novembre 2026.'))
        corps = corps.replace('%%TABLE_EMPLACEMENTS%%', table_emplacements(lot))
        corps = corps.replace('%%TABLE_PLAQUES%%', table_plaques(pieces))
        corps = corps.replace('%%SOURCES_ARMOR%%', sources_html(
            livre[fiche['route']]['sourcesDeDepart'], sources, fiche['route'], livre))
        corps = resoudre(corps, fiche['route'], remplacements)
        sortie(fiche['route'], fiche, corps, manifeste['hub_armor']['route'],
               manifeste['hub_armor']['titre'], fiche['aside_note'],
               strip=[(len(lot), 'Pièces de la catégorie'),
                      (f'{classes[0]} – {classes[-1]}' if classes else '—', 'Classes présentes'),
                      (len(mats), 'Matériaux utilisés'),
                      (sum(1 for p in lot if any(e['plaquesAutorisees'] for e in p['emplacements'])), 'Pièces à plaques'),
                      (DATE, 'Instantané des données')])
        print(f'{fiche["route"]} · {len(lot)} pièces')

    # --- Comparateur --------------------------------------------------------
    outil = manifeste['armor_chart']
    corps = (ROOT / 'templates/armures/outil-armor.html.part').read_text(encoding='utf-8')
    corps = Template(corps).substitute(root='../' * outil['route'].count('/'))
    corps = corps.replace('%%TABLE_MATERIAUX%%', table_materiaux(materiaux))
    corps = corps.replace('%%TABLE_CLASSES%%', table_classes(pieces))
    corps = corps.replace('%%TABLE_CATALOGUE%%', table_catalogue(
        pieces, 'Les trois cent quatre-vingt-dix pièces de l’export, filtrables et comparables.', id_table='armures-comparateur'))
    corps = corps.replace('%%TABLE_EMPLACEMENTS%%', table_emplacements(pieces))
    corps = corps.replace('%%TABLE_PLAQUES%%', table_plaques(pieces))
    corps = corps.replace('%%JSON_ARMURES%%', json.dumps(
        [{'id': p['id'], 'nom': p['nom'], 'categorie': p['categorie'], 'classe': p['classe'],
          'materiau': p['materiau'], 'duree': p['duree'], 'zones': p['zones'],
          'emplacements': [{'nom': e['nom'], 'plaquesAutorisees': e['plaquesAutorisees'],
                            'classeMax': e['classeMax']} for e in p['emplacements']],
          'poids': p['poids'], 'prixBase': p['prixBase'],
          'penaliteVitesse': p['penaliteVitesse'], 'penaliteRotation': p['penaliteRotation'],
          'penaliteErgonomie': p['penaliteErgonomie'],
          'capacite': p['capacite'], 'typeArmure': p['typeArmure'],
          'bloqueCasqueAudio': p['bloqueCasqueAudio'], 'bloqueLunettes': p['bloqueLunettes'],
          'surditE': p['surditE'], 'ricochet': p['ricochet']}
         for p in pieces], ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'))
    corps = corps.replace('%%SOURCES_ARMOR%%', sources_html(
        livre[outil['route']]['sourcesDeDepart'], sources, outil['route'], livre))
    corps = resoudre(corps, outil['route'], {})
    sortie(outil['route'], outil, corps, manifeste['hub_armor']['route'],
           manifeste['hub_armor']['titre'], outil['aside_note'],
           strip=[(len(pieces), 'Pièces comparables'),
                  ('2 à 3', 'Pièces sélectionnées'),
                  ('6', "Classes d’armure"),
                  (len(materiaux), 'Matériaux de blindage'),
                  (DATE, 'Instantané des données')])
    print(f'{outil["route"]} · comparateur · {len(pieces)} pièces')

    # --- Hub boss -----------------------------------------------------------
    hub_boss = manifeste['hub_boss']
    corps = (ROOT / 'templates/armures/hub-boss.html.part').read_text(encoding='utf-8')
    corps = Template(corps).substitute(root='../' * hub_boss['route'].count('/'))
    grille = []
    for boss in manifeste['bosses']:
        fiche = par_slug[boss['slug']]
        route = posixpath.relpath(boss['route'], 'pages/bosses')
        escortes = ', '.join(e['nom'] for e in fiche['escortes']) or 'aucune'
        appearances = sorted({carte_fr(a['carte']) for a in fiche['apparitions']})
        grille.append(
            f'<article class="boss-card" data-boss-card data-famille="{text(fiche["famille"])}">'
            f'<h3><a href="{text(route)}">{text(fiche["titre"])}</a></h3>'
            f'<p class="boss-card__meta"><span class="badge">{nombre(fiche["pvTotal"])} PV</span>'
            f'<span class="badge">{len(fiche["escortes"])} escorte{"" if len(fiche["escortes"]) == 1 else "s"}</span>'
            f'<span class="badge">{text(fiche["famille"])}</span></p>'
            f'<p class="boss-card__lieu">{text(", ".join(appearances))}</p>'
            f'<p class="boss-card__escortes">{text(escortes)}</p></article>')
    corps = corps.replace('%%GRILLE_BOSS%%', '\n'.join(grille))
    corps = corps.replace('%%TABLE_MATRICE%%', table_matrice(fiches, par_slug))
    corps = corps.replace('%%TABLE_PV%%', table_pv_compare(fiches))
    corps = corps.replace('%%TABLE_HORSFICHE%%', table_horsfiche(hors_fiche))
    corps = corps.replace('%%SOURCES_BOSS%%', sources_html(
        livre[hub_boss['route']]['sourcesDeDepart'], sources, hub_boss['route'], livre))
    corps = resoudre(corps, hub_boss['route'], {})
    sortie(hub_boss['route'], hub_boss, corps, hub_boss['route'], hub_boss['titre'], hub_boss['aside_note'],
           strip=[(len(fiches), 'Fiches de boss'),
                  (donnees_boss['statistiques']['mobsExport'], 'Entrées dans l’export'),
                  (donnees_boss['statistiques']['apparitions'], 'Apparitions relevées'),
                  (len(hors_fiche), 'Entrées sans fiche'),
                  ('3', 'Profils de jeu')])
    print(f'{hub_boss["route"]} · {len(fiches)} fiches · {len(hors_fiche)} entrées hors fiche')

    # --- Fiches de boss -----------------------------------------------------
    for boss in manifeste['bosses']:
        fiche = par_slug[boss['slug']]
        fiche['nomsEscortes'] = {e['id']: e['nom'] for e in fiche['escortes']}
        for e in fiche['equipement']['protections'] + fiche['equipement']['armes']:
            fiche['nomsEscortes'].setdefault(e['id'], e['nom'])
        corps = (ROOT / 'templates/armures/boss.html.part').read_text(encoding='utf-8')
        corps = Template(corps).substitute(root='../' * boss['route'].count('/'))
        corps = corps.replace('%%TABLE_PV%%', table_pv(fiche))
        corps = corps.replace('%%TABLE_APPARITIONS%%', table_apparitions(fiche))
        corps = corps.replace('%%TABLE_ESCORTES%%', table_escortes(fiche))
        corps = corps.replace('%%TABLE_EQUIPEMENT%%', table_equipement(fiche))
        corps = corps.replace('%%TABLE_BUTIN%%', table_butin(fiche))
        corps = corps.replace('%%LISTE_COMMUNAUTE%%', '\n'.join(
            f'<li>{text(point)}</li>' for point in boss['communaute']))
        zones = sorted({a['carte'] for a in fiche['apparitions']})
        remplacements = {
            'LEAD_BOSS': text(boss['lead']),
            'PV_TOTAL': nombre(fiche['pvTotal']),
            'NB_ESCORTES': text(len(fiche['escortes'])),
            'DETAIL_ESCORTES': text(', '.join(e['nom'] for e in fiche['escortes']) or 'Aucune escorte relevée dans l’export pour cette fiche.'),
            'NB_APPARITIONS': text(len(fiche['apparitions'])),
            'DETAIL_APPARITIONS': text(f"Sur {len(zones)} carte{'' if len(zones) == 1 else 's'} : {', '.join(carte_fr(z) for z in zones)}."),
            'NB_LOOT': text(fiche['nbObjetsLoot']),
            'DETAIL_LOOT': text(f"Objets recensés dans le butin de l’export, dont {len(fiche['loot'])} lignes détaillées sur cette page."),
            'CALLOUT_TITRE': text('Ce que cette fiche ne dit pas.'),
            'CALLOUT_TEXTE': text(
                "Les points de vie ne donnent pas un temps de mise à mort, et une chance d'apparition ne dit pas quand le boss sera là. "
                "Les comportements, les stratégies et les taux publiés par les guides communautaires sont dans la section des avis, datés et séparés des chiffres ci-dessus."),
            'NOTE_PV': text(
                f"La zone la plus résistante est {fiche['membreLePlusResistant'].lower()} et la plus faible "
                f"{fiche['membreLePlusFaible'].lower()}. Ces totaux sont ceux de l'export Regular : les autres profils reprennent les mêmes mobs."),
            'NOTE_APPARITIONS': text(
                "Les profils Regular, PvE et Seasonal sont présentés séparément : les valeurs du profil PvE sont plus élevées sur plusieurs cartes, "
                "et les mêler donnerait un taux qui n'existe dans aucun mode de jeu."),
            'LEAD_ESCORTES': text(
                "Les escortes ont leurs propres points de vie et leur propre équipement. L'export les décrit comme des mobs distincts, "
                "et cette fiche ne les fusionne pas avec le boss principal."),
            'NOTE_ESCORTES': text(
                "Les quantities d'escortes indiquées dans le tableau des apparitions dépendent de la zone et du tirage : ce sont des probabilités d'apparition, pas un effectif garanti."),
            'NOTE_EQUIPEMENT': text(
                "L'export propose plusieurs jeux d'équipement pour un même boss : le tableau retient le premier objet de chaque emplacement. "
                "Un boss peut donc porter en jeu une variante que la fiche ne montre pas."),
            'LEAD_BUTIN': text(
                "Les fréquences de sortie viennent de l'export : elles indiquent la part des raids où l'objet apparaît, et non une garantie pour un raid donné."),
            'NOTE_BUTIN': text(
                f"Le butin complet de cette fiche compte {fiche['nbObjetsLoot']} objets ; le tableau en détaille {len(fiche['loot'])} par fréquence décroissante. "
                "Les objets de valeur rare ont une prevalence faible : c'est normal, et c'est ce qui les rend rares."),
        }
        corps = corps.replace('%%SOURCES_BOSS%%', sources_html(
            livre[boss['route']]['sourcesDeDepart'], sources, boss['route'], livre))
        corps = resoudre(corps, boss['route'], remplacements)
        sortie(boss['route'], boss, corps, hub_boss['route'], hub_boss['titre'], boss['aside_note'],
               strip=[(nombre(fiche['pvTotal']), 'Points de vie'),
                      (len(fiche['escortes']), 'Escortes'),
                      (len(fiche['apparitions']), 'Apparitions relevées'),
                      (fiche['nbObjetsLoot'], 'Objets de butin'),
                      (DATE, 'Instantané des données')])
        print(f'{boss["route"]} · {fiche["pvTotal"]} PV · {len(fiche["apparitions"])} apparitions')


if __name__ == '__main__':
    main()
