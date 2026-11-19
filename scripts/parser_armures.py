#!/usr/bin/env python3
"""Extrait les données d'armure et de boss des instantanés Tarkov.dev.

Les charges utiles brutes sont conservées dans recherche/tarkov-dev/<mode>/.
Ce script en produit trois versions publiques :

- js/data/armor.json : catalogue des pièces d'armure, matériaux, zones et
  compatibilités de plaques ;
- js/data/bosses.json : fiches de boss, points de vie, escortes, apparitions
  et équipement ;
- recherche/versions/armures-phase-6.json : version de travail complète,
  avec la correspondance entre les identifiants de l'export et les noms
  éditorials retenus pour la phase 6.

La correspondance ne repose sur aucune supposition : l'export porte pour
chaque entité un champ `normalizedName` qui reprend le nom de jeu. Les
identifiants internes du jeu (bossBully, bossKojaniy, bossBoar) sont ainsi
rattachés à Reshala, Shturman et Kaban par la donnée elle-même, et non par
une convention de lecture.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SORTIE = ROOT / 'recherche/versions'
DATA = ROOT / 'js/data'

DATE = '2026-11-18'

# ---------------------------------------------------------------------------
# Correspondance éditoriale
# ---------------------------------------------------------------------------
# Chaque fiche éditoriale de la phase 6 renvoie à un ou plusieurs identifiants
# de l'export. La colonne `normalizedName` de l'export porte le nom de jeu ;
# elle est le seul justificatif retenu ici. Le groupe 'principaux' désigne le
# mob dont le portrait et le comportement correspondent à la fiche ; les autres
# identifiants du groupe 'apparences' sont les variantes et escorts qui
# partagent la même identité éditoriale.

FICHES_BOSS = [
    {
        'slug': 'reshala',
        'titre': 'Reshala',
        'mob': 'bossBully',
        'apparences': ['bossBully'],
        'escortes': ['followerBully'],
        'famille': 'scav',
        'nomJeu': 'Reshala',
        'titreFr': 'Reshala, le Marchand',
    },
    {
        'slug': 'killa',
        'titre': 'Killa',
        'mob': 'bossKilla',
        'apparences': ['bossKilla'],
        'escortes': [],
        'famille': 'scav',
        'nomJeu': 'Killa',
        'titreFr': 'Killa',
    },
    {
        'slug': 'shturman',
        'titre': 'Shturman',
        'mob': 'bossKojaniy',
        'apparences': ['bossKojaniy'],
        'escortes': ['followerKojaniy'],
        'famille': 'scav',
        'nomJeu': 'Shturman',
        'titreFr': 'Shturman',
    },
    {
        'slug': 'glukhar',
        'titre': 'Glukhar',
        'mob': 'bossGluhar',
        'apparences': ['bossGluhar'],
        'escortes': ['followerGluharAssault', 'followerGluharSecurity', 'followerGluharScout'],
        'famille': 'scav',
        'nomJeu': 'Glukhar',
        'titreFr': 'Glukhar',
    },
    {
        'slug': 'sanitar',
        'titre': 'Sanitar',
        'mob': 'bossSanitar',
        'apparences': ['bossSanitar'],
        'escortes': ['followerSanitar'],
        'famille': 'scav',
        'nomJeu': 'Sanitar',
        'titreFr': 'Sanitar',
    },
    {
        'slug': 'tagilla',
        'titre': 'Tagilla',
        'mob': 'bossTagilla',
        'apparences': ['bossTagilla'],
        'escortes': [],
        'famille': 'scav',
        'nomJeu': 'Tagilla',
        'titreFr': 'Tagilla',
    },
    {
        'slug': 'kaban',
        'titre': 'Kaban',
        'mob': 'bossBoar',
        'apparences': ['bossBoar'],
        'escortes': ['followerBoar', 'followerBoarClose1', 'followerBoarClose2', 'bossBoarSniper'],
        'famille': 'scav',
        'nomJeu': 'Kaban',
        'titreFr': 'Kaban',
    },
    {
        'slug': 'kollontay',
        'titre': 'Kollontay',
        'mob': 'bossKolontay',
        'apparences': ['bossKolontay'],
        'escortes': ['followerKolontayAssault', 'followerKolontaySecurity'],
        'famille': 'scav',
        'nomJeu': 'Kollontay',
        'titreFr': 'Kollontay',
    },
    {
        'slug': 'zryachiy',
        'titre': 'Zryachiy',
        'mob': 'bossZryachiy',
        'apparences': ['bossZryachiy'],
        'escortes': [],
        'famille': 'cultiste',
        'nomJeu': 'Zryachiy',
        'titreFr': 'Zryachiy',
    },
    {
        'slug': 'partisan',
        'titre': 'Partisan',
        'mob': 'bossPartisan',
        'apparences': ['bossPartisan'],
        'escortes': [],
        'famille': 'pmc',
        'nomJeu': 'Partisan',
        'titreFr': 'Partisan',
    },
    {
        'slug': 'cultist-priest',
        'titre': 'Cultist Priest',
        'mob': 'sectantPriest',
        'apparences': ['sectantPriest'],
        'escortes': ['sectantWarrior'],
        'famille': 'cultiste',
        'nomJeu': 'Cultist Priest',
        'titreFr': 'Prêtre cultiste',
    },
    {
        'slug': 'the-goons',
        'titre': 'The Goons',
        'mob': 'bossKnight',
        'apparences': ['bossKnight'],
        'escortes': ['followerBigPipe', 'followerBirdEye'],
        'famille': 'rogue',
        'nomJeu': 'Knight',
        'titreFr': 'The Goons',
    },
    {
        'slug': 'shadow-of-tagilla',
        'titre': 'Shadow of Tagilla',
        'mob': 'bossTagillaAgro',
        'apparences': ['bossTagillaAgro'],
        'escortes': [],
        'famille': 'scav',
        'nomJeu': 'Shadow of Tagilla',
        'titreFr': 'Shadow of Tagilla',
    },
    {
        'slug': 'the-wedge',
        'titre': 'The Wedge',
        'mob': 'bossWedge',
        'apparences': ['bossWedge', 'bossWedgeLab'],
        'escortes': [],
        'famille': 'black-division',
        'nomJeu': 'The Wedge',
        'titreFr': 'The Wedge',
    },
]

# Mob qui figurent dans l'export mais qui ne font l'objet d'aucune fiche
# éditoriale de la phase 6. Ils sont documentés dans le hub pour que le
# décompte reste exact et que rien ne soit compté deux fois.
MOB_HORS_FICHE = {
    'bossKillaAgro': 'Vengeful Killa',
    'bossWedge': 'The Wedge (renfort d’image)',
    'infectedTagilla': 'Tagilla infecté',
    'sectantWarrior': 'Guerrier cultiste',
    'blackDivision': 'Black Division',
    'pmcBotBlackDiv': 'PMC Black Division',
    'bossBullyBlackDiv': 'Black Division (Icebreaker)',
    'followerBullyBlackDiv': 'Garde Black Division',
    'followerBully': 'Garde de Reshala',
    'followerBigPipe': 'Big Pipe',
    'followerBirdEye': 'Birdeye',
    'followerBoar': 'Garde de Kaban',
    'followerBoarClose1': 'Gus',
    'followerBoarClose2': 'Basmach',
    'bossBoarSniper': 'Snipers de Kaban',
    'followerGluharAssault': 'Garde d’assaut de Glukhar',
    'followerGluharSecurity': 'Garde de sécurité de Glukhar',
    'followerGluharScout': 'Éclaireur de Glukhar',
    'followerKojaniy': 'Garde de Shturman',
    'followerKolontayAssault': 'Garde d’assaut de Kollontay',
    'followerKolontaySecurity': 'Garde de sécurité de Kollontay',
    'followerSanitar': 'Garde de Sanitar',
    'followerWedgeLab': 'Garde de The Wedge (Laboratoire)',
    'PmcBot': 'Raider',
    'ExUsec': 'Rogue (USEC)',
    'exUsecFree': 'Rogue libre',
    'vsRF': 'AF (Terminal)',
    'vsRFSniper': 'AF sniper (Terminal)',
    'Sentry': 'Tour de garde (Shoreline)',
    'infectedAssault': 'Infecté armé',
    'infectedCivil': 'Infecté civil',
    'infectedLaborant': 'Infecté de laboratoire',
    'infectedPmc': 'PMC infecté',
    'infectedScreamer': 'Hurleur infecté',
}

# Libellés français des zones de collision de l'export.
ZONES_FR = {
    'Collider Type ParietalHead': 'Voûte du crâne',
    'Collider Type BackHead': 'Occiput',
    'Collider Type Ears': 'Oreilles',
    'Collider Type HeadCommon': 'Tête (zone commune)',
    'Collider Type Eyes': 'Yeux',
    'Collider Type Jaw': 'Mâchoire',
    'Collider type NeckFront': 'Gorge',
    'Collider Type NeckFront': 'Gorge',
    'Collider Type NeckBack': 'Nuque',
    'Collider Type RibcageUp': 'Cage thoracique haute',
    'Collider Type RibcageLow': 'Cage thoracique basse',
    'Collider Type SpineTop': 'Colonne dorsale haute',
    'Collider Type SpineDown': 'Colonne dorsale basse',
    'Collider Type Pelvis': 'Bassin',
    'Collider Type PelvisBack': 'Bassin (arrière)',
    'Collider Type LeftSideChestDown': 'Flanc gauche',
    'Collider Type RightSideChestDown': 'Flanc droit',
    'Collider Type LeftUpperArm': 'Bras gauche',
    'Collider Type RightUpperArm': 'Bras droit',
}

SLOTS_FR = {
    'Front_plate': 'Plaque avant',
    'Back_plate': 'Plaque arrière',
    'Left_side_plate': 'Plaque latérale gauche',
    'Right_side_plate': 'Plaque latérale droite',
    'Helmet_top': 'Calotte',
    'Helmet_back': 'Arrière du casque',
    'Helmet_ears': 'Protège-oreilles',
    'helmet_eyes': 'Visière oculaire',
    'helmet_jaw': 'Protège-mâchoire',
    'Soft_armor_front': 'Armure souple avant',
    'Soft_armor_back': 'Armure souple arrière',
    'Soft_armor_left': 'Armure souple gauche',
    'Soft_armor_right': 'Armure souple droite',
    'soft_armor_front': 'Armure souple avant',
    'soft_armor_back': 'Armure souple arrière',
    'soft_armor_left': 'Armure souple gauche',
    'soft_armor_right': 'Armure souple droite',
    'Groin': 'Bas-ventre',
}

# Types d-properties de l'export vers le gabarit éditorial.
TYPES_FR = {
    'ItemPropertiesArmor': 'Gilet pare-balles',
    'ItemPropertiesChestRig': 'Gilet tactique',
    'ItemPropertiesHelmet': 'Casque ou masque',
    'ItemPropertiesGlasses': 'Protection oculaire',
    'ItemPropertiesArmorAttachment': 'Accessoire blindé',
}

CATEGORIES_FR = {
    'Gilet pare-balles': 'Gilet pare-balles',
    'Gilet tactique': 'Gilet tactique',
    'Casque': 'Casque',
    'Masque': 'Masque',
    'Plaque de blindage': 'Plaque de blindage',
    'Protections oculaires': 'Protection oculaire',
}

MATERIAUX_FR = {
    'Aramid': 'Aramid',
    'UHMWPE': 'UHMWPE',
    'Combined': 'Matériau combiné',
    'ArmoredSteel': 'Acier de blindage',
    'Titan': 'Titane',
    'Aluminium': 'Aluminium',
    'Ceramic': 'Céramique',
    'Glass': 'Verre',
}

ARMOR_TYPE_FR = {
    'Light': 'Légère',
    'Medium': 'Moyenne',
    'Heavy': 'Lourde',
    'None': 'Aucune',
}

MARCHANDS_FR = {
    '54cb50c76803fa8b248b4571': 'Prapor',
    '54cb57776803fa8b248b456e': 'Therapeute',
    '579dc571d53a0658a154fbec': 'Fence',
    '58330581ace78e27b8b10cee': 'Skier',
    '5935c25fb3acc3127c3d8cd9': 'Peacekeeper',
    '5a7c2eca46aef81a7ca2145d': 'Mechanic',
    '5ac3b934156ae10c4430e83c': 'Ragman',
    '5c0647fdd443bc2504c2d371': 'Jaeger',
    '638f541a29ffd1183d187f57': 'Lightkeeper',
    '68fe15910f29ba3fdbba9d54': 'Taran',
    '68fe15990f29ba3fdbba9d55': 'Station radio',
    '656f0f98d80a697f855d34b1': 'Conducteur BTR',
    '6617beeaa9cfa777ca915b7c': 'Reference',
    '688246518448b05efd61d461': 'M. Kerman',
    '688246958448b05efd61d462': 'Voevoda',
    '69e0d6cc77b63940375b9173': 'Survivant',
}

# Modes de jeu : le dossier exporté par profil.
MODES = ('regular', 'pve', 'pvp-season')
MODE_FR = {'regular': 'PvP Zone', 'pve': 'PvE Zone', 'pvp-season': 'Seasonal'}


def lire(chemin):
    return json.loads((ROOT / chemin).read_text(encoding='utf-8'))


def ecrit(chemin, donnees):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def nom_marchand(identifiant):
    return MARCHANDS_FR.get(identifiant, identifiant)


def zone_fr(nom):
    if not nom:
        return None
    if nom in ZONES_FR:
        return ZONES_FR[nom]
    if nom.startswith('Armor Zone Plate_'):
        return nom.replace('Armor Zone Plate_', '').replace('_', ' ')
    return nom


# ---------------------------------------------------------------------------
# Armures
# ---------------------------------------------------------------------------

def categorie_item(categories, catalogue):
    for identifiant in categories:
        libelle = catalogue.get(identifiant, {}).get('nameFr')
        if libelle in CATEGORIES_FR:
            return CATEGORIES_FR[libelle], libelle
    return None, None


def bloc_marchand(entree):
    """Offres marchandes relevées sur la pièce."""
    achats = []
    for offre in entree.get('buyFromTrader') or []:
        achats.append({
            'marchand': nom_marchand(offre.get('trader')),
            'prix': offre.get('price'),
            'devise': offre.get('currency') or 'RUB',
            'niveau': offre.get('minLevel'),
        })
    ventes = []
    for offre in entree.get('sellToTrader') or []:
        ventes.append({
            'marchand': nom_marchand(offre.get('trader')),
            'prix': offre.get('price'),
            'devise': offre.get('currency') or 'RUB',
        })
    return achats, ventes


def parser_armure():
    armor = lire('recherche/tarkov-dev/regular/armor.json')
    items = lire('recherche/tarkov-dev/regular/items.json')
    catalogue = items['itemCategories']
    table_items = items['items']
    materiaux_export = armor['armorMaterials']

    materiaux = []
    for identifiant, donnees in materiaux_export.items():
        destructibilite = donnees.get('destructibility')
        materiaux.append({
            'id': identifiant,
            'nom': MATERIAUX_FR.get(identifiant, identifiant),
            'destructibilite': destructibilite,
            'destructibiliteExplosion': donnees.get('explosionDestructibility'),
            'usureReparationMin': donnees.get('minRepairDegradation'),
            'usureReparationMax': donnees.get('maxRepairDegradation'),
            'usureKitReparationMin': donnees.get('minRepairKitDegradation'),
            'usureKitReparationMax': donnees.get('maxRepairKitDegradation'),
        })
    materiaux.sort(key=lambda m: (m['destructibilite'] is None, m['destructibilite'] or 0, m['id']))

    plaques = {}
    for entree in armor['rows']:
        objet = table_items.get(entree['id'])
        if not objet:
            continue
        categorie, _ = categorie_item(objet.get('categories') or [], catalogue)
        if categorie == 'Plaque de blindage':
            plaques[entree['id']] = {
                'id': entree['id'],
                'nom': objet.get('nameFr') or objet.get('name'),
                'classe': (entree['properties'] or {}).get('class'),
                'materiau': (entree['properties'] or {}).get('material'),
                'duree': (entree['properties'] or {}).get('durability'),
                'poids': objet.get('weight'),
            }

    pieces = []
    for entree in armor['rows']:
        objet = table_items.get(entree['id'])
        if not objet:
            continue
        proprietes = entree['properties'] or {}
        categorie, libelle_source = categorie_item(objet.get('categories') or [], catalogue)
        type_properties = proprietes.get('propertiesType')
        achats, ventes = bloc_marchand(entree)

        emplacements = []
        for emplacement in proprietes.get('armorSlots') or []:
            identifiant = emplacement.get('nameId')
            autorisees = emplacement.get('allowedPlates') or []
            emplacements.append({
                'id': identifiant,
                'nom': SLOTS_FR.get(identifiant, identifiant),
                'zones': [zone_fr(z) for z in emplacement.get('zones') or []],
                'plaquesAutorisees': len(autorisees),
                'idsPlaquesAutorisees': autorisees,
                'classeMax': None,
                'duree': emplacement.get('durability'),
                'materiau': emplacement.get('armorMaterial'),
                'typeArmure': emplacement.get('armorType'),
            })
            # Classe maximale réellement acceptée, calculée sur les plaques
            # autorisées : l'export ne publie pas la classe maximale par
            # emplacement, elle se déduit des plaques elles-mêmes.
            classes = [plaques[p]['classe'] for p in autorisees if p in plaques and plaques[p]['classe']]
            if classes:
                emplacements[-1]['classeMax'] = max(classes)

        zones = [zone_fr(z) for z in proprietes.get('zones') or []]
        materiau = proprietes.get('material')
        destructibilite = None
        if materiau in materiaux_export:
            destructibilite = materiaux_export[materiau].get('destructibility')

        duree = proprietes.get('durability')
        # Durabilité effective : rapport de la durée nominale à la
        # destructibilité du matériau. La règle est celle décrite par les
        # analyses communautaires et reproductible sur l'export.
        effective = None
        if duree is not None and destructibilite:
            effective = round(duree / destructibilite, 1)

        encrements = {}
        for emplacement in proprietes.get('slots') or []:
            filtres = emplacement.get('filters') or {}
            autorises = filtres.get('allowedItems') or []
            encrements[emplacement.get('nameId')] = {
                'id': emplacement.get('nameId'),
                'requis': bool(emplacement.get('required')),
                'filtres': {
                    'categoriesAutorisees': filtres.get('allowedCategories') or [],
                    'objetsAutorises': autorises,
                    'categoriesExclues': filtres.get('excludedCategories') or [],
                    'objetsExclus': filtres.get('excludedItems') or [],
                },
            }

        pieces.append({
            'id': entree['id'],
            'nom': objet.get('nameFr') or objet.get('name'),
            'nomCourt': objet.get('shortNameFr') or objet.get('shortName'),
            'categorie': categorie or 'Accessoire blindé',
            'categorieSource': libelle_source,
            'typeProperties': type_properties,
            'typeLibelle': TYPES_FR.get(type_properties, type_properties),
            'classe': proprietes.get('class'),
            'materiau': MATERIAUX_FR.get(materiau, materiau),
            'materiauId': materiau,
            'duree': duree,
            'dureeEffective': effective,
            'usureReparation': proprietes.get('repairCost'),
            'typeArmure': ARMOR_TYPE_FR.get(proprietes.get('armorType'), proprietes.get('armorType')),
            'zones': zones,
            'zonesCodes': proprietes.get('zones') or [],
            'emplacements': emplacements,
            'encrements': list(encrements.values()),
            'capacite': proprietes.get('capacity'),
            'blindage': proprietes.get('blindnessProtection'),
            'ricochet': {
                'x': proprietes.get('ricochetX'),
                'y': proprietes_safe(proprietes, 'ricochetY'),
                'z': proprietes_safe(proprietes, 'ricochetZ'),
            },
            'attenuationChoc': proprietes.get('bluntThroughput'),
            'surditE': proprietes.get('deafening'),
            'bloqueCasqueAudio': proprietes.get('blocksHeadset'),
            'bloqueLunettes': proprietes.get('blocksEyewear'),
            'bloqueCouvreChef': proprietes.get('blocksHeadwear'),
            'penaliteVitesse': proprietes.get('speedPenalty'),
            'penaliteRotation': proprietes.get('turnPenalty'),
            'penaliteErgonomie': proprietes.get('ergoPenalty'),
            'poids': objet.get('weight'),
            'prixBase': objet.get('basePrice'),
            'achats': achats,
            'ventes': ventes,
            'prixMarche': {
                'bas': entree.get('lastLowPrice'),
                'moyen24h': entree.get('avg24hPrice'),
                'bas24h': entree.get('low24hPrice'),
                'haut24h': entree.get('high24hPrice'),
                'offres': entree.get('lastOfferCount'),
                'horodatage': entree.get('lastScan'),
            },
            'niveauFlea': entree.get('minLevelForFlea'),
        })

    categories = Counter(p['categorie'] for p in pieces)
    classes = Counter(p['classe'] for p in pieces if p['classe'])
    for piece in pieces:
        piece['emplacements'] = [
            {**e, 'idsPlaquesAutorisees': []} if e['plaquesAutorisees'] == 0 else e
            for e in piece['emplacements']
        ]

    return {
        'schemaVersion': 1,
        'genereLe': DATE,
        'langue': 'fr-FR',
        'source': {
            'export': 'recherche/tarkov-dev/regular/armor.json',
            'items': 'recherche/tarkov-dev/regular/items.json',
            'nature': 'Export communautaire Tarkov.dev, relevé du 18 novembre 2026.',
            'regleDureeEffective': 'Durée nominale divisée par la destructibilité du matériau relevée dans l’export.',
        },
        'materiaux': materiaux,
        'plaques': sorted(plaques.values(), key=lambda p: (-(p['classe'] or 0), p['nom'] or '')),
        'pieces': pieces,
        'statistiques': {
            'pieces': len(pieces),
            'parCategorie': dict(sorted(categories.items())),
            'parClasse': {str(c): n for c, n in sorted(classes.items())},
            'parMateriau': dict(sorted(Counter(p['materiau'] or 'Non relevé' for p in pieces).items())),
            'avecPlaques': sum(1 for p in pieces if any(e['plaquesAutorisees'] for e in p['emplacements'])),
            'avecEmplacementEquipement': sum(1 for p in pieces if p['encrements']),
        },
    }


def proprietes_safe(proprietes, cle):
    return proprietes.get(cle)


# ---------------------------------------------------------------------------
# Boss
# ---------------------------------------------------------------------------

def pv_total(mob):
    return sum(part['max'] for part in mob.get('health') or [])


def pv_par_membre(mob):
    libelles = {
        'Chest': 'Poitrine',
        'Stomach': 'Ventre',
        'Head': 'Tête',
        'LeftArm': 'Bras gauche',
        'RightArm': 'Bras droit',
        'LeftLeg': 'Jambe gauche',
        'RightLeg': 'Jambe droite',
    }
    return [{'membre': libelles.get(part['id'], part['id']), 'pv': part['max'], 'id': part['id']}
            for part in mob.get('health') or []]


def escortes_entree(entree):
    """Escortes d'une entrée d'apparition, avec le nombre attendu par tirage."""
    escortes = []
    for escorte in entree.get('escorts') or []:
        quantites = [{'chance': a.get('chance'), 'nombre': a.get('count')}
                     for a in escorte.get('amount') or []]
        escortes.append({'mob': escorte.get('mob'), 'quantites': quantites})
    return escortes


def relever_apparitions(mode):
    """Apparitions d'un boss, par carte, sur un profil de jeu.

    L'export décrit une apparition par emplacement : sur Icebreaker, The Wedge
    est ainsi listé douze fois, une fois par zone, avec un nombre d'escortes
    différent. Les entrées sont donc regroupées par carte, chance et délai,
    et chaque zone conserve ses propres escortes.
    """
    cartes = lire(f'recherche/tarkov-dev/{mode}/maps.json')['data']['maps']
    resultat = defaultdict(list)
    groupes = {}
    for carte in cartes.values():
        for entree in carte.get('bosses') or []:
            mob = entree.get('mob')
            cle = (carte.get('id'), mob, entree.get('spawnChance'),
                   entree.get('spawnTime'), entree.get('spawnTimeRandom'),
                   json.dumps(entree.get('spawnTrigger'), sort_keys=True))
            groupe = groupes.get(cle)
            if groupe is None:
                groupe = groupes[cle] = {
                    'carte': carte.get('normalizedName'),
                    'carteId': carte.get('id'),
                    'chance': entree.get('spawnChance'),
                    'declencheur': entree.get('spawnTrigger'),
                    'tempsApparition': entree.get('spawnTime'),
                    'tempsAleatoire': entree.get('spawnTimeRandom'),
                    'zones': [],
                }
                resultat[mob].append(groupe)
            escortes = escortes_entree(entree)
            for emplacement in entree.get('spawnLocations') or []:
                nom = emplacement.get('name')
                cible = None
                for zone in groupe['zones']:
                    if zone['zone'] == nom:
                        cible = zone
                        break
                if cible is None:
                    cible = {'zone': nom, 'chance': emplacement.get('chance'),
                             'positions': 0, 'escortes': []}
                    groupe['zones'].append(cible)
                cible['positions'] += len(emplacement.get('positions') or [])
                for escorte in escortes:
                    if escorte not in cible['escortes']:
                        cible['escortes'].append(escorte)
    return resultat


SLOTS_EQUIPEMENT_FR = {
    'FirstPrimaryWeapon': 'Arme principale',
    'SecondPrimaryWeapon': 'Arme secondaire',
    'Holster': 'Pistolet',
    'TacticalVest': 'Gilet tactique',
    'ArmorVest': 'Gilet pare-balles',
    'Headwear': 'Couvre-chef',
    'FaceCover': 'Masque',
    'Eyewear': 'Protection oculaire',
    'Front_plate': 'Plaque avant',
    'Back_plate': 'Plaque arrière',
    'Left_side_plate': 'Plaque latérale gauche',
    'Right_side_plate': 'Plaque latérale droite',
    'Backpack': 'Sac à dos',
    'Earpiece': 'Protection auditive',
}

CATEGORIES_EQUIPEMENT = {
    'Gilet tactique': 'Gilet tactique',
    'Gilet pare-balles': 'Gilet pare-balles',
    'Casque': 'Casque',
    'Masque': 'Masque',
    'Plaque de blindage': 'Plaque de blindage',
    'Protections oculaires': 'Protection oculaire',
    'Arme': 'Arme',
    'Sac à dos': 'Sac à dos',
    'Protection auditive': 'Protection auditive',
}


def equipement_significatif(mob, table_items, catalogue, limite=18):
    """Protection et armes portées par le boss, déduites de son équipement.

    L'export liste plusieurs jeux d'équipement possibles pour un même boss.
    On retient le premier objet trouvé pour chaque emplacement afin de ne pas
    compter un même emplacement plusieurs fois, et l'on sépare les
    protections (gilets, casques, plaques, masques, protections oculaires)
    des armes.
    """
    protections = []
    armes = []
    sacs = []
    vus = set()
    emplacements_vus = set()
    for entree in mob.get('equipment') or []:
        identifiant = entree.get('item')
        if identifiant in vus:
            continue
        objet = table_items.get(identifiant)
        if not objet:
            continue
        slot = (entree.get('attributes') or {}).get('slot')
        if slot not in SLOTS_EQUIPEMENT_FR:
            continue
        libelle = None
        for categorie in objet.get('categories') or []:
            nom = catalogue.get(categorie, {}).get('nameFr')
            if nom in CATEGORIES_EQUIPEMENT:
                libelle = CATEGORIES_EQUIPEMENT[nom]
                break
        if libelle is None:
            continue
        vus.add(identifiant)
        if libelle == 'Arme':
            armes.append({
                'id': identifiant,
                'nom': objet.get('nameFr') or objet.get('name'),
                'slot': slot,
                'slotFr': SLOTS_EQUIPEMENT_FR[slot],
                'categorie': libelle,
            })
            continue
        if libelle == 'Sac à dos':
            sacs.append({
                'id': identifiant,
                'nom': objet.get('nameFr') or objet.get('name'),
                'slot': slot,
                'slotFr': SLOTS_EQUIPEMENT_FR[slot],
                'categorie': libelle,
            })
            continue
        if slot in emplacements_vus:
            continue
        emplacements_vus.add(slot)
        protections.append({
            'id': identifiant,
            'nom': objet.get('nameFr') or objet.get('name'),
            'slot': slot,
            'slotFr': SLOTS_EQUIPEMENT_FR[slot],
            'categorie': libelle,
        })
    return {'protections': protections[:limite], 'armes': armes[:limite], 'sacs': sacs[:4]}


def loot_significatif(mob, table_items, limite=12):
    """Objets que le boss peut laisser, avec leur probabilité de présence."""
    lignes = []
    for entree in mob.get('items') or []:
        objet = table_items.get(identifiant := entree.get('id'))
        if not objet:
            continue
        attributs = entree.get('attributes') or {}
        prevalence = attributs.get('prevalence')
        lignes.append({
            'id': identifiant,
            'nom': objet.get('nameFr') or objet.get('name'),
            'prevalence': prevalence,
            'difficulte': attributs.get('difficulty'),
            'types': sorted(objet.get('types') or []),
        })
    lignes.sort(key=lambda l: (-(l['prevalence'] or 0), l['nom'] or ''))
    return lignes[:limite]


def parser_boss():
    modes = {mode: lire(f'recherche/tarkov-dev/{mode}/maps.json') for mode in MODES}
    items_brut = lire('recherche/tarkov-dev/regular/items.json')
    items = items_brut['items']
    items_catalogue = items_brut['itemCategories']
    mobs = modes['regular']['data']['mobs']

    apparitions_par_mode = {mode: relever_apparitions(mode) for mode in MODES}

    fiches = []
    for fiche in FICHES_BOSS:
        mob = mobs[fiche['mob']]
        export_noms = sorted({mobs[m]['normalizedName'] for m in fiche['apparences'] if m in mobs})
        escortes_ids = [m for m in fiche['escortes'] if m in mobs]
        pv_escortes = []
        for identifiant in escortes_ids:
            garde = mobs[identifiant]
            pv_escortes.append({
                'id': identifiant,
                'nom': MOB_HORS_FICHE.get(identifiant, mobs[identifiant]['normalizedName']),
                'pvTotal': pv_total(garde),
                'pv': pv_par_membre(garde),
            })

        apparitions = []
        escortes_vus = set(escortes_ids)
        for mode in MODES:
            for identifiant in fiche['apparences']:
                for entree in apparitions_par_mode[mode].get(identifiant, []):
                    ligne = dict(entree)
                    ligne['mode'] = mode
                    ligne['modeFr'] = MODE_FR[mode]
                    ligne['mob'] = identifiant
                    apparitions.append(ligne)
                    for zone in ligne['zones']:
                        for escorte in zone['escortes']:
                            if escorte['mob'] in mobs and escorte['mob'] not in escortes_vus:
                                escortes_vus.add(escorte['mob'])
                                garde = mobs[escorte['mob']]
                                pv_escortes.append({
                                    'id': escorte['mob'],
                                    'nom': MOB_HORS_FICHE.get(escorte['mob'], garde['normalizedName']),
                                    'pvTotal': pv_total(garde),
                                    'pv': pv_par_membre(garde),
                                })
        apparitions.sort(key=lambda a: (a['carte'], a['mode'], a['mob']))

        pv = pv_par_membre(mob)
        total = sum(p['pv'] for p in pv)
        fiches.append({
            'slug': fiche['slug'],
            'titre': fiche['titre'],
            'titreFr': fiche['titleFr'] if 'titleFr' in fiche else fiche['titreFr'],
            'nomJeu': fiche['nomJeu'],
            'famille': fiche['famille'],
            'mobExport': fiche['mob'],
            'mobsApparences': fiche['apparences'],
            'nomsExport': export_noms,
            'pvTotal': total,
            'pv': pv,
            'membreLePlusResistant': max(pv, key=lambda p: p['pv'])['membre'] if pv else None,
            'membreLePlusFaible': min(pv, key=lambda p: p['pv'])['membre'] if pv else None,
            'portrait': mobs[fiche['mob']].get('imagePortraitLink'),
            'affiche': mobs[fiche['mob']].get('imagePosterLink'),
            'escortes': pv_escortes,
            'apparitions': apparitions,
            'equipement': equipement_significatif(mob, items, items_catalogue),
            'loot': loot_significatif(mob, items),
            'nbObjetsLoot': len(mob.get('items') or []),
        })

    hors_fiche = []
    ids_fiches = set()
    for fiche in FICHES_BOSS:
        ids_fiches.update(fiche['apparences'])
        ids_fiches.update(fiche['escortes'])
    for identifiant, mob in mobs.items():
        if identifiant in ids_fiches:
            continue
        hors_fiche.append({
            'id': identifiant,
            'nom': MOB_HORS_FICHE.get(identifiant, mob.get('normalizedName') or identifiant),
            'pvTotal': pv_total(mob),
            'famille': 'autre',
        })
    hors_fiche.sort(key=lambda m: (-(m['pvTotal'] or 0), m['nom']))

    # Cartes où des boss apparaissent, par profil.
    cartes = {}
    for mode in MODES:
        donnees = modes[mode]['data']['maps']
        for cle, carte in donnees.items():
            entree = cartes.setdefault(carte['normalizedName'], {
                'id': carte['id'],
                'nom': carte['normalizedName'],
                'dureeRaid': carte.get('raidDuration'),
                'joueurs': carte.get('players'),
                'wiki': carte.get('wiki'),
                'apparitions': [],
            })
            entree['apparitions'].append({
                'mode': mode,
                'modeFr': MODE_FR[mode],
                'boss': sorted({b['mob'] for b in carte.get('bosses') or []
                                if b['mob'] in {f['mob'] for f in FICHES_BOSS}}),
            })

    return {
        'schemaVersion': 1,
        'genereLe': DATE,
        'langue': 'fr-FR',
        'source': {
            'export': 'recherche/tarkov-dev/<mode>/maps.json',
            'items': 'recherche/tarkov-dev/regular/items.json',
            'nature': 'Export communautaire Tarkov.dev, relevé du 18 novembre 2026.',
            'correspondance': 'La colonne normalizedName de l’export porte le nom de jeu ; elle fonde le rattachement des identifiants bossBully, bossKojaniy, bossBoar et bossKnight aux fiches Reshala, Shturman, Kaban et The Goons.',
        },
        'fiches': fiches,
        'horsFiche': hors_fiche,
        'mobs': {
            identifiant: {
                'id': identifiant,
                'nom': mobs[identifiant].get('normalizedName'),
                'pvTotal': pv_total(mobs[identifiant]),
                'famille': MOB_HORS_FICHE.get(identifiant, mobs[identifiant].get('normalizedName') or identifiant),
            }
            for identifiant in mobs
        },
        'cartes': cartes,
        'statistiques': {
            'fiches': len(fiches),
            'mobsExport': len(mobs),
            'horsFiche': len(hors_fiche),
            'apparitions': sum(len(f['apparitions']) for f in fiches),
            'pvMax': max((f['pvTotal'] for f in fiches), default=0),
            'pvMin': min((f['pvTotal'] for f in fiches), default=0),
        },
    }


def main():
    armor = parser_armure()
    bosses = parser_boss()
    ecrit(DATA / 'armor.json', armor)
    ecrit(DATA / 'bosses.json', bosses)
    ecrit(SORTIE / 'armures-phase-6.json', {
        'schemaVersion': 1,
        'genereLe': DATE,
        'armures': armor,
        'bosses': bosses,
    })
    print(f"armures : {armor['statistiques']['pieces']} pièces, "
          f"{len(armor['materiaux'])} matériaux, {len(armor['plaques'])} plaques")
    print(f"boss : {bosses['statistiques']['fiches']} fiches, "
          f"{bosses['statistiques']['mobsExport']} mobs, "
          f"{bosses['statistiques']['apparitions']} apparitions relevées")


if __name__ == '__main__':
    main()
