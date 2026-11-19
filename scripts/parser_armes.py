#!/usr/bin/env python3
"""Extrait les données armes, modifications et munitions des instantanés Tarkov.dev.

Les charges utiles brutes sont conservées dans recherche/tarkov-dev/<mode>/.
Ce script en produit deux versions :

- recherche/versions/armes-<mode>.json : version de travail complète ;
- js/data/weapons.json et js/data/ammo.json : versions publiques, allégées,
  destinées aux pages de la phase 5 (catalogue, fiches de famille, tableau
  balistique).

La classification des armes suit les catégories d'objets publiées par
l'export communautaire, et non un classement éditorial : un « fusil
d'assaut » du jeu est un fusil d'assaut dans le guide.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SORTIE = ROOT / 'recherche/versions'
DATA = ROOT / 'js/data'

MODES = ('regular', 'pve', 'pvp-season')

# Catégories d'objets relevées dans l'export, avec leur identifiant exact.
CATEGORIES_ARMES = {
    '5447b5f14bdc2d61278b4567': 'fusils-assaut',
    '5447b5fc4bdc2d87278b4567': 'fusils-assaut',
    '5447b5e04bdc2d62278b4567': 'pistolets-mitrailleurs',
    '5447b6094bdc2dc3278b4567': 'fusils-a-pompe',
    '5447b6254bdc2dc3278b4568': 'fusils-de-precision',
    '5447b6194bdc2d67278b4567': 'dmr',
    '5447b5cf4bdc2d65278b4567': 'pistolets',
    '617f1ef5e8b54b0998387733': 'pistolets',
    '5447bed64bdc2d97278b4568': 'mitrailleuses',
    '5447bedf4bdc2d87278b4568': 'lance-grenades',
    '67446d4f04141c10630604e7': 'lance-grenades',
    '5447e1d04bdc2dff2f8b4567': 'arme-de-melee',
}

# Sous-familles affichées séparément quand la catégorie du jeu les regroupe.
SOUS_FAMILLES = {
    '5447b5fc4bdc2d87278b4567': 'carabine',
    '617f1ef5e8b54b0998387733': 'revolver',
    '67446d4f04141c10630604e7': 'lance-roquettes',
}

# Catégories de pièces, pour la page « Modifications et accessoires ».
CATEGORIES_PIECES = {
    '5448fe394bdc2d0d028b456c': 'bouche de canon',
    '550aa4bf4bdc2dd6348b456b': 'cache-flamme',
    '550aa4cd4bdc2dd8348b456b': 'reducteur de son',
    '550aa4dd4bdc2dc9348b4569': 'accessoire de bouche combine',
    '55818b164bdc2d5b648b4570': 'dispositif tactique combine',
    '55818a594bdc2db9688b456a': 'crosse',
    '55818a104bdc2db9688b4569': 'garde-main',
    '55818b224bdc2dde698b456f': 'rail',
    '5448fe7a4bdc2d6f028b456b': 'viseur',
    '55818ad54bdc2ddc698b4569': 'viseur reflex',
    '55818acf4bdc2dde698b456c': 'viseur reflex compact',
    '55818ae44bdc2dde698b456c': 'lunette telescopique',
    '55818add4bdc2d5b648b456f': 'lunette d\'assaut',
    '55818aeb4bdc2dde698b456c': 'lunette speciale',
    '5448bc234bdc2d3c308b4569': 'chargeur',
    '610720f290b75a49ff2e5e25': 'chargeur de revolver',
    '555ef6e44bdc2de9068b457e': 'canon',
    '55818a684bdc2ddd698b456d': 'poignee pistolet',
    '55818af64bdc2d5b648b4570': 'poignee tactique',
    '55818a304bdc2db5418b457d': 'boitier',
    '55818ac54bdc2d5b648b456e': 'mire',
    '55818a6f4bdc2db9688b456b': 'levier d\'armement',
    '56ea9461d2720b67698b456f': 'bloc d\'emprunt de gaz',
    '55818afb4bdc2d5b648b456d': 'bipied',
    '55818b084bdc2d5b648b4571': 'lampe tactique',
    '55818b014bdc2ddc698b456b': 'lance-grenades monte',
    '5a2c3a9486f774688b05e574': 'module auxiliaire',
    '5a74651486f7744e73386dd1': 'module auxiliaire',
    '5d21f59b6dbe99052b54ef83': 'vision thermique',
}

CALIBRES_FR = {
    'Caliber556x45NATO': '5,56 x 45 mm NATO',
    'Caliber545x39': '5,45 x 39 mm',
    'Caliber762x39': '7,62 x 39 mm',
    'Caliber762x51': '7,62 x 51 mm NATO',
    'Caliber762x54R': '7,62 x 54 mm R',
    'Caliber9x39': '9 x 39 mm',
    'Caliber9x19': '9 x 19 mm',
    'Caliber9x19PARA': '9 x 19 mm Para',
    'Caliber9x18PM': '9 x 18 mm PM',
    'Caliber9x18PMM': '9 x 18 mm PMM',
    'Caliber9x33R': '9 x 33 mm R',
    'Caliber9x21': '9 x 21 mm',
    'Caliber46x30': '4,6 x 30 mm',
    'Caliber57x28': '5,7 x 28 mm',
    'Caliber58x42': '5,8 x 42 mm',
    'Caliber300BLK': '.300 Blackout',
    'Caliber68x51': '6,8 x 51 mm',
    'Caliber366TKM': '.366 TKM',
    'Caliber127x55': '12,7 x 55 mm',
    'Caliber127x33': '12,7 x 33 mm',
    'Caliber127x99': '12,7 x 99 mm',
    'Caliber1143x23ACP': '11,43 x 23 mm ACP',
    'Caliber762x25TT': '7,62 x 25 mm TT',
    'Caliber762x35': '7,62 x 35 mm',
    'Caliber23x75': '23 x 75 mm',
    'Caliber26x75': '26 x 75 mm',
    'Caliber20x1mm': '20 x 1 mm',
    'Caliber40mmRU': '40 mm RU',
    'Caliber725': '7,25 x 25 mm',
    'Caliber784x49': '7,84 x 49 mm',
    'Caliber86x70': '8,6 x 70 mm',
    'Caliber93x64': '9,3 x 64 mm',
    'Caliber114x54': '11,4 x 54 mm',
    'Caliber338LM': '.338 Lapua Magnum',
    'Caliber408x55': '4,8 x 55 mm',
    'Caliber50AE': '5,0 x 50 AE',
    'Caliber40x46': '4,0 x 46 mm',
    'Caliber12g': '12 gauges',
    'Caliber20g': '20 gauges',
    'Caliber16g': '16 gauges',
    'Caliber870x50': '8,7 x 50 mm',
    'Caliber325x35': '3,25 x 35 mm',
    'Caliber9x18': '9 x 18 mm',
    'Caliber6.5x52': '6,5 x 52 mm',
    'Caliber115x40': '11,5 x 40 mm',
    'Caliber866x33': '8,66 x 33 mm',
    'Caliber95x32': '9,5 x 32 mm',
    'Caliber54x42': '5,4 x 42 mm',
}

MODES_TIR = {
    'single': 'Semi-automatique',
    'burst': 'Burst',
    'fullauto': 'Automatique',
    'repeater': 'Repetition',
    'grenade': 'Lance-grenades',
    'rocket': 'Lance-roquettes',
    'pipe': 'Tube',
    'bolt': 'Cuirasse',
    'launcher': 'Lanceur',
    'underbarrel': 'Sous-canon',
    'NVG': 'Vision nocturne',
}

MARCHANDS_FR = {
    '54cb50c76803fa8b248b4571': 'Prapor',
    '54cb57776803fa99248b456e': 'Therapeute',
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


def lire(chemin):
    return json.loads((ROOT / chemin).read_text(encoding='utf-8'))


def caliber_fr(identifiant):
    if not identifiant:
        return '—'
    if identifiant in CALIBRES_FR:
        return CALIBRES_FR[identifiant]
    return identifiant.replace('Caliber', '').replace('x', ' x ') + ' mm'


def nom_marchand(identifiant):
    return MARCHANDS_FR.get(identifiant, identifiant)


def categorie_arme(categories_objet, catalogue_categories):
    """Première catégorie d'arme reconnue, dans l'ordre du catalogue."""
    for identifiant in categories_objet:
        if identifiant in CATEGORIES_ARMES:
            libelle = catalogue_categories.get(identifiant, {}).get('nameFr')
            return CATEGORIES_ARMES[identifiant], SOUS_FAMILLES.get(identifiant), libelle
    return None, None, None


def offres(entree):
    """Déduit les offres marchandes : prix en roubles, devise, niveau, tâches.

    Certaines offres sont libellées en dollars et non en roubles : le guide
    conserve alors le prix en roubles tel que l'export le donne et signale la
    devise plutôt que de convertir sur un taux qui change chaque jour.
    """
    achats = entree.get('buyFromTrader') or []
    if not achats:
        return None, None, [], [], None, []
    rub = [a for a in achats if a.get('currency') == 'RUB']
    autre = [a for a in achats if a.get('currency') != 'RUB']
    prix = next((a['priceRUB'] for a in rub), None)
    devise = 'RUB' if rub else (autre[0].get('currency') if autre else None)
    niveau = min((a.get('minTraderLevel') or 0 for a in achats), default=None)
    marchands = sorted({nom_marchand(a['trader']) for a in achats})
    taches = sorted({a['taskUnlock'] for a in achats if a.get('taskUnlock')})
    return prix, niveau, marchands, taches, devise, len(achats)


def construire_armes(mode):
    items = lire(f'recherche/tarkov-dev/{mode}/items.json')
    armes = lire(f'recherche/tarkov-dev/{mode}/weapons.json')
    catalogue = items['items']
    categories = items['itemCategories']
    parId = {row['id']: row for row in armes['rows']}

    # Presets : chaque preset renvoie vers l'arme de base et porte ses propres mesures.
    presets_par_arme = {}
    for row in armes['rows']:
        proprietes = row.get('properties') or {}
        if proprietes.get('propertiesType') != 'ItemPropertiesPreset':
            continue
        base = proprietes.get('baseItem')
        if base:
            presets_par_arme.setdefault(base, []).append({
                'id': row['id'],
                'nom': (catalogue.get(row['id']) or {}).get('nameFr')
                       or (catalogue.get(row['id']) or {}).get('name') or row['id'],
                'ergonomie': proprietes.get('ergonomics'),
                'reculVertical': proprietes.get('recoilVertical'),
                'reculHorizontal': proprietes.get('recoilHorizontal'),
                'precision': proprietes.get('moa'),
                'parDefaut': bool(proprietes.get('default')),
            })

    resultat = []
    for identifiant, item in catalogue.items():
        types = item.get('types') or []
        est_arme = 'gun' in types or 'wearable' in types and 'melee' not in types
        if not est_arme:
            continue
        famille, sous_famille, libelle_categorie = categorie_arme(item.get('categories') or [], categories)
        if famille is None:
            continue
        entree = parId.get(identifiant, {})
        stats = entree.get('properties') or {}
        type_propriete = stats.get('propertiesType')
        if type_propriete not in ('ItemPropertiesWeapon', 'ItemPropertiesMelee'):
            continue
        prix, niveau, marchands, taches, devise, nbOffres = offres(entree)
        modes_tir = stats.get('fireModes') or []
        munitions = stats.get('allowedAmmo') or []
        presets = sorted(presets_par_arme.get(identifiant, []), key=lambda p: (not p['parDefaut'], p['nom'] or ''))
        record = {
            'id': identifiant,
            'nom': item.get('nameFr') or item.get('name'),
            'nomEn': item.get('name'),
            'court': item.get('shortNameFr') or item.get('shortName') or item.get('name'),
            'famille': famille,
            'sousFamille': sous_famille,
            'categorieJeu': libelle_categorie,
            'wiki': item.get('wikiLink'),
            'poids': item.get('weight'),
            'taille': [item.get('width'), item.get('height')],
            'prixBase': item.get('basePrice'),
            'calibre': caliber_fr(stats.get('caliber')) if stats.get('caliber') else ('Sans munition' if type_propriete == 'ItemPropertiesMelee' else '—'),
            'calibreId': stats.get('caliber'),
            'ergonomie': stats.get('ergonomics'),
            'reculVertical': stats.get('recoilVertical'),
            'reculHorizontal': stats.get('reculHorizontal') if 'reculHorizontal' in stats else stats.get('recoilHorizontal'),
            'cadence': stats.get('fireRate'),
            'distanceEfficace': stats.get('effectiveDistance'),
            'porteeVisée': stats.get('sightingRange'),
            'dispersions': stats.get('deviationMax'),
            'dispersionCourbe': stats.get('deviationCurve'),
            'modeTir': modes_tir,
            'modeTirFr': [MODES_TIR.get(m, m) for m in modes_tir],
            'munitionsAutorisees': munitions,
            'nbMunitions': len(munitions),
            'nbPresets': len(presets),
            'presets': presets,
            'degatsLame': stats.get('slashDamage'),
            'degatsPoignard': stats.get('stabDamage'),
            'rayonAtteinte': stats.get('hitRadius'),
            'prixMarchand': prix,
            'niveauMarchand': niveau,
            'marchands': marchands,
            'tachesDeverrouillage': taches,
            'disponibleChezMarchand': bool(marchands),
            'deviseMarchand': devise,
            'nbOffresMarchand': nbOffres,
            'typePropriete': type_propriete,
        }
        resultat.append(record)
    resultat.sort(key=lambda a: (a['famille'], a['sousFamille'] or '', a['nom'] or ''))
    return resultat


def construire_pieces(mode):
    """Pièces d'arme : catégorie de pièce, poids, prix de base, disponibilité."""
    items = lire(f'recherche/tarkov-dev/{mode}/items.json')
    catalogue = items['items']
    categories = items['itemCategories']
    resultat = []
    for identifiant, item in catalogue.items():
        if 'mods' not in (item.get('types') or []):
            continue
        slot = None
        for cat in item.get('categories') or []:
            if cat in CATEGORIES_PIECES:
                slot = CATEGORIES_PIECES[cat]
                break
        if slot is None:
            continue
        resultat.append({
            'id': identifiant,
            'nom': item.get('nameFr') or item.get('name'),
            'court': item.get('shortNameFr') or item.get('shortName'),
            'slot': slot,
            'poids': item.get('weight'),
            'taille': [item.get('width'), item.get('height')],
            'prixBase': item.get('basePrice'),
            'wiki': item.get('wikiLink'),
        })
    resultat.sort(key=lambda p: (p['slot'], p['nom'] or ''))
    return resultat


def construire_munitions(mode):
    munitions = lire(f'recherche/tarkov-dev/{mode}/ammo.json')
    items = lire(f'recherche/tarkov-dev/{mode}/items.json')['items']
    resultat = []
    grenades = []
    for row in munitions['rows']:
        proprietes = row.get('properties') or {}
        item = items.get(row['id']) or {}
        type_propriete = proprietes.get('propertiesType')
        if type_propriete == 'ItemPropertiesGrenade':
            grenades.append({
                'id': row['id'],
                'nom': item.get('nameFr') or item.get('name'),
                'type': proprietes.get('type'),
                'delai': proprietes.get('fuse'),
                'rayonMin': proprietes.get('minExplosionDistance'),
                'rayonMax': proprietes.get('maxExplosionDistance'),
                'fragments': proprietes.get('fragments'),
                'rayonContusion': proprietes.get('contusionRadius'),
                'poids': item.get('weight'),
            })
            continue
        if type_propriete != 'ItemPropertiesAmmo':
            continue
        prix, niveau, marchands, taches, devise, nbOffres = offres(row)
        penetration = proprietes.get('penetrationPower') or 0
        resultat.append({
            'id': row['id'],
            'nom': item.get('nameFr') or item.get('name'),
            'court': item.get('shortNameFr') or item.get('shortName') or item.get('name'),
            'calibre': caliber_fr(proprietes.get('caliber')),
            'calibreId': proprietes.get('caliber'),
            'typeProjectile': proprietes.get('ammoType'),
            'nbProjectiles': proprietes.get('projectileCount', 1),
            'degats': proprietes.get('damage'),
            'penetration': penetration,
            'deviationPenetration': proprietes.get('penetrationPowerDeviation'),
            'degatsArmure': proprietes.get('armorDamage'),
            'fragmentation': proprietes.get('fragmentationChance'),
            'ricochet': proprietes.get('ricochetChance'),
            'chancePenetration': proprietes.get('penetrationChance'),
            'vitesse': proprietes.get('initialSpeed'),
            'coefficient': proprietes.get('ballisticCoeficient'),
            'diametre': proprietes.get('bulletDiameterMilimeters'),
            'masse': proprietes.get('bulletMassGrams'),
            'traceur': proprietes.get('tracer'),
            'couleurTraceur': proprietes.get('tracerColor'),
            'sHemorragieLegere': proprietes.get('lightBleedModifier'),
            'sHemorragieLourde': proprietes.get('heavyBleedModifier'),
            'modificateurRecul': proprietes.get('recoilModifier'),
            'modificateurPrecision': proprietes.get('accuracyModifier'),
            'pileMax': proprietes.get('stackMaxSize'),
            'poids': item.get('weight'),
            'prixMarchand': prix,
            'niveauMarchand': niveau,
            'marchands': marchands,
            'tachesDeverrouillage': taches,
            'disponibleChezMarchand': bool(marchands),
            'deviseMarchand': devise,
            'nbOffresMarchand': nbOffres,
            'dernierBas': row.get('lastLowPrice'),
            'moyenne24h': row.get('avg24hPrice'),
            'bas24h': row.get('low24hPrice'),
            'haut24h': row.get('high24hPrice'),
            'offres': row.get('lastOfferCount'),
            'niveauFlea': row.get('minLevelForFlea'),
            'horodatage': row.get('lastScan'),
            # Règle de lecture dérivée du correctif 0.14.6.0 (BSG) : la classe
            # d'armure atteinte vaut la classe × 10 ; la traversée est garantie
            # à partir de +15 points de pénétration.
            'classeAtteinte': min(6, penetration // 10) if penetration >= 10 else 0,
            'garantie': {c: penetration >= c * 10 + 15 for c in range(1, 7)},
        })
    resultat.sort(key=lambda m: (m['calibre'], -(m['penetration'] or 0), -(m['degats'] or 0)))
    return resultat, grenades


def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    resume = {}
    for mode in MODES:
        armes = construire_armes(mode)
        pieces = construire_pieces(mode)
        munitions, grenades = construire_munitions(mode)
        document = {
            'schemaVersion': 1,
            'mode': mode,
            'reference': '2026-11-18',
            'source': f'json.tarkov.dev/{mode}',
            'armes': armes,
            'pieces': pieces,
            'munitions': munitions,
            'grenades': grenades,
        }
        chemin = SORTIE / f'armes-{mode}.json'
        chemin.write_text(json.dumps(document, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        familles = Counter(a['famille'] for a in armes)
        resume[mode] = {
            'armes': len(armes), 'pieces': len(pieces), 'munitions': len(munitions),
            'grenades': len(grenades), 'familles': dict(sorted(familles.items())),
            'calibres': len({m['calibre'] for m in munitions}),
        }
        print(f'{mode} : {len(armes)} armes, {len(pieces)} pièces, {len(munitions)} munitions, {len(grenades)} grenades')
    (SORTIE / 'armes-resume.json').write_text(json.dumps(resume, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    # --- Versions publiques --------------------------------------------
    reference = lire('recherche/versions/armes-regular.json')
    armes = reference['armes']
    munitions = reference['munitions']

    catalogue = []
    for arme in armes:
        catalogue.append({
            'id': arme['id'], 'nom': arme['nom'], 'court': arme['court'],
            'famille': arme['famille'], 'sousFamille': arme['sousFamille'],
            'categorieJeu': arme['categorieJeu'],
            'calibre': arme['calibre'], 'ergonomie': arme['ergonomie'],
            'reculVertical': arme['reculVertical'], 'reculHorizontal': arme['reculHorizontal'],
            'cadence': arme['cadence'], 'distanceEfficace': arme['distanceEfficace'],
            'porteeVisée': arme['porteeVisée'], 'modeTirFr': arme['modeTirFr'],
            'nbMunitions': arme['nbMunitions'], 'poids': arme['poids'],
            'taille': arme['taille'], 'prixMarchand': arme['prixMarchand'],
            'niveauMarchand': arme['niveauMarchand'], 'marchands': arme['marchands'],
            'disponibleChezMarchand': arme['disponibleChezMarchand'],
            'degatsLame': arme['degatsLame'], 'degatsPoignard': arme['degatsPoignard'],
            'rayonAtteinte': arme['rayonAtteinte'],
            'presets': [{'nom': p['nom'], 'ergonomie': p['ergonomie'],
                         'reculVertical': p['reculVertical'], 'reculHorizontal': p['reculHorizontal'],
                         'precision': p['precision'], 'parDefaut': p['parDefaut']}
                        for p in arme['presets']],
        })
    public_armes = {
        'schemaVersion': 1,
        'reference': '2026-11-18',
        'source': 'json.tarkov.dev/regular (instantané du 18 novembre 2026)',
        'note': ('Les trois profils de jeu consultés (PvP Zone, PvE Zone, PvP Season) exposent le '
                 'même catalogue d\'armes, de pièces et de munitions à cette date : aucun écart de '
                 'contenu n\'a été relevé entre eux. Les prix marchands et les niveaux de fidélité '
                 'sont les valeurs de l\'instantané, pas des prix garantis. Les compatibilités '
                 'pièce par pièce ne figurent pas dans cet export : elles se vérifient dans le client.'),
        'familles': sorted({a['famille'] for a in armes}),
        'armes': catalogue,
    }
    (DATA / 'weapons.json').write_text(json.dumps(public_armes, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    public_pieces = {
        'schemaVersion': 1,
        'reference': '2026-11-18',
        'source': 'json.tarkov.dev/regular (instantané du 18 novembre 2026)',
        'note': ('Catalogue des pièces d\'arme par emplacement. L\'export ne précise pas les armes '
                 'compatibles avec chaque pièce : ce point reste à vérifier dans le client.'),
        'pieces': [{'id': p['id'], 'nom': p['nom'], 'court': p['court'], 'slot': p['slot'],
                    'poids': p['poids'], 'prixBase': p['prixBase']} for p in reference['pieces']],
    }
    (DATA / 'weapon-pieces.json').write_text(json.dumps(public_pieces, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    public_munitions = {
        'schemaVersion': 1,
        'reference': '2026-11-18',
        'source': 'json.tarkov.dev/regular (instantané du 18 novembre 2026)',
        'note': ('Dégâts, pénétration et fractions proviennent des propriétés de l\'export. '
                 'La classe d\'armure atteinte est déduite de la règle du correctif 0.14.6.0 '
                 '(classe × 10 ; traversée garantie à +15) : c\'est une lecture dérivée, '
                 'pas une valeur publiée par l\'éditeur.'),
        'calibres': sorted({m['calibre'] for m in munitions}),
        'munitions': munitions,
        'grenades': reference['grenades'],
    }
    (DATA / 'ammo.json').write_text(json.dumps(public_munitions, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(resume['regular'], ensure_ascii=False))


if __name__ == '__main__':
    main()
