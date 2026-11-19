#!/usr/bin/env python3
"""Construit js/data/maps.json à partir des instantanés json.tarkov.dev et des fiches wiki.

Entrées :
  recherche/tarkov-dev/{regular,pve,pvp-season}/maps.json      (structure du jeu)
  recherche/tarkov-dev/{regular,pve,pvp-season}_maps_fr.json   (libellés français)
  recherche/wiki-cartes/structures.json                          (conditions, clés, notes)
  recherche/wiki-cartes/extracts-fr.json                         (descriptions FR des fiches)

Sortie : js/data/maps.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'recherche/tarkov-dev'
WIKI = ROOT / 'recherche/wiki-cartes'

MODES = ('regular', 'pve', 'pvp-season')
LIEUX = ['factory', 'customs', 'woods', 'shoreline', 'interchange', 'reserve', 'the-lab',
         'lighthouse', 'streets-of-tarkov', 'ground-zero', 'the-labyrinth', 'icebreaker', 'terminal']

# Variantes rattachées à leur carte parente.
VARIANTES = {
    'night-factory': ('factory', 'Variante nocturne de l’Usine'),
    'ground-zero-21': ('ground-zero', 'Variante 21+ de Point zéro'),
    'ground-zero-tutorial': ('ground-zero', 'Variante tutoriel de Point zéro'),
    'the-lab-dark': ('the-lab', 'Variante obscurité du Labo'),
    'infected-factory': ('factory', 'Événement infecté sur l’Usine'),
    'infected-lab': ('the-lab', 'Événement infecté sur le Labo'),
}

CAMP_FR = {'pmc': 'PMC', 'scav': 'Scav', 'shared': 'Partagée', 'both': 'PMC et Scav'}
DANGER_FR = {'minefield': 'Champ de mines', 'sniper': 'Sniper de bordure', 'claymore': 'Claymore'}


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def norm_nom(valeur):
    return ' '.join(str(valeur).split())


def extraire_carte(mode, slug):
    brut = load(DATA / mode / 'maps.json')['data']['maps']
    fr = load(DATA / f'{mode}_maps_fr.json')['data']
    for cid, carte in brut.items():
        if carte['normalizedName'] == slug:
            return cid, carte, fr
    return None, None, fr


def boss_liste(carte, fr, wiki_boss=None):
    vus = {}
    for boss in carte.get('bosses', []):
        mob = boss['mob']
        entree = vus.setdefault(mob, {
            'nom': fr.get(mob, mob),
            'chance': boss.get('spawnChance'),
            'zones': [],
            'escortes': [],
        })
        for zone in boss.get('spawnLocations', []):
            if zone['name'] not in entree['zones']:
                entree['zones'].append(zone['name'])
        for esc in boss.get('escorts', []):
            for compte in esc.get('amount', []):
                entree['escortes'].append({'mob': esc.get('mob'), 'nom': fr.get(esc.get('mob'), esc.get('mob')),
                                            'chance': compte.get('chance'), 'nombre': compte.get('count')})
    for entree in vus.values():
        entree['zones'].sort()
        entree['escortes'].sort(key=lambda e: (e['nom'] or '', e['chance'] or 0))
    if wiki_boss:
        par_nom = {norm_nom(ligne['nom']).lower(): ligne for ligne in wiki_boss}
        for entree in vus.values():
            ligne = par_nom.get(norm_nom(entree['nom']).lower())
            if ligne:
                entree['zone'] = ligne.get('zone', '')
                entree['equipement'] = ligne.get('equipement', '')
                entree['escorteWiki'] = ligne.get('escorte', '')
    return sorted(vus.values(), key=lambda e: e['nom'])


def dangers(carte):
    compte = {}
    for danger in carte.get('hazards', []):
        type_ = danger.get('hazardType') or 'inconnu'
        compte[type_] = compte.get(type_, 0) + 1
    return {t: compte[t] for t in sorted(compte, key=lambda k: -compte[k])}


def spawns(carte):
    par_camp = {}
    for spawn in carte.get('spawns', []):
        for camp in spawn.get('sides', []):
            par_camp[camp] = par_camp.get(camp, 0) + 1
    return dict(sorted(par_camp.items()))


def extraire(cle, table):
    for ligne in table:
        if ligne.get('cle') == cle:
            return ligne
    return None


def constructions():
    structures = load(WIKI / 'structures.json')
    extraits_fr = load(WIKI / 'extracts-fr.json')
    wiki_pages = {v['page']: k for k, v in structures.items()}
    lore_fr = load(WIKI / 'extracts-fr-lore.json') if (WIKI / 'extracts-fr-lore.json').is_file() else {}
    page_fr = {
        'factory': 'Factory', 'customs': 'Customs', 'woods': 'Woods', 'shoreline': 'Shoreline',
        'interchange': 'Interchange', 'reserve': 'Base militaire', 'the-lab': 'Le labo',
        'lighthouse': 'Phare', 'streets-of-tarkov': 'Streets_of_Tarkov', 'ground-zero': 'Ground_Zero',
        'the-labyrinth': 'The_Labyrinth', 'icebreaker': 'Icebreaker', 'terminal': 'Terminal',
    }
    sorties = {}
    for slug, data in structures.items():
        sorties[slug] = {norm_nom(e['nom']).lower(): e for e in data['sorties']}

    cartes = []
    for slug in LIEUX:
        id_, carte, fr = extraire_carte('regular', slug)
        if carte is None:
            raise SystemExit(f'carte absente des données : {slug}')
        base = extraire_carte('regular', slug)[2]
        # libellés FR : on prend le mode regular comme référence de nommage
        w = structures.get(slug, {})
        lore = norm_nom(lore_fr.get(page_fr.get(slug, ''), ''))

        table_wiki = sorties.get(slug, {})
        api_brut = carte.get('extracts', [])
        api_par_cle = {norm_nom(e['name']).lower().replace('_', ' '): e for e in api_brut}

        def trouver_api(nom):
            cible = norm_nom(nom).lower()
            if cible in api_par_cle:
                return api_par_cle[cible]
            for cle, ex in api_par_cle.items():
                if cle and (cle.startswith(cible) or cible.startswith(cle)):
                    return ex
            return None

        # Correspondances certaines : libellé de jeu strictement identique au libellé de la fiche.
        certain = {}
        for cle, ex in api_par_cle.items():
            if cle in {norm_nom(n).lower() for n in table_wiki}:
                certain[cle] = ex

        liste_sorties = []
        for cle, wiki_row in sorted(table_wiki.items()):
            ex = certain.get(cle) or api_par_cle.get(cle)
            camp = wiki_row.get('camp') or (ex.get('faction') if ex else 'pmc')
            liste_sorties.append({
                'nom': wiki_row['nom'],
                'camp': camp,
                'campFr': CAMP_FR.get(camp, camp),
                'toujoursDisponible': wiki_row['toujours'],
                'usageUnique': wiki_row['usageUnique'],
                'conditions': wiki_row['conditions'],
                'notes': wiki_row['notes'],
                'nomJeu': ex['name'].replace('_', ' ') if ex else None,
                'libelleJeu': fr.get(ex['name']) if ex else None,
                'interrupteur': bool(ex.get('switch')) if ex else False,
            })
        liste_sorties.sort(key=lambda e: (e['camp'], e['nom']))
        noms_wiki = {norm_nom(l['nom']).lower() for l in liste_sorties}
        liste_jeu = []
        for ex in api_brut:
            cle = norm_nom(ex['name']).lower().replace('_', ' ')
            camp = ex.get('faction', 'pmc')
            liste_jeu.append({
                'nom': ex['name'].replace('_', ' '),
                'libelle': fr.get(ex['name'], ex['name']),
                'camp': camp,
                'campFr': CAMP_FR.get(camp, camp),
                'interrupteur': bool(ex.get('switch')),
                'dansFicheWiki': cle in noms_wiki,
            })
        liste_jeu.sort(key=lambda e: (e['camp'], e['libelle']))
        liste_sorties.sort(key=lambda e: (e['camp'], e['nom']))

        transits = []
        wiki_transits = {norm_nom(t['vers']).lower(): t for t in w.get('transits', [])}
        for tr in carte.get('transits', []):
            cible = None
            for cid, c in load(DATA / 'regular/maps.json')['data']['maps'].items():
                if cid == tr.get('map'):
                    cible = c['normalizedName']
                    break
            wiki_row = None
            for cle, ligne in wiki_transits.items():
                if cible and cle and (cle.startswith(cible) or cible.startswith(cle)):
                    wiki_row = ligne
                    break
            transits.append({
                'nomFr': fr.get(tr['description'], tr['description']),
                'vers': cible,
                'camp': wiki_row['camp'] if wiki_row else None,
                'conditions': wiki_row['conditions'] if wiki_row else '',
                'notes': wiki_row['notes'] if wiki_row else '',
            })

        cles = []
        for key in carte.get('locks', []):
            if key.get('key'):
                cles.append(key['key'])
        cles = sorted(set(cles))

        entree = {
            'slug': slug,
            'nom': fr.get(carte['name'], carte['normalizedName']),
            'nomOfficiel': carte['normalizedName'],
            'id': carte['id'],
            'description': fr.get(carte['description'], carte['description']),
            'descriptionLore': lore,
            'pageWiki': w.get('page', ''),
            'notes': norm_nom(w.get('notes', '')),
            'fonctionnalites': w.get('fonctionnalites', []),
            'dureeMinutes': carte.get('raidDuration'),
            'joueurs': carte.get('players'),
            'niveaux': {'min': carte.get('minPlayerLevel', 0), 'max': carte.get('maxPlayerLevel', 100)},
            'clesAccess': carte.get('accessKeys', []),
            'niveauAccesClefs': carte.get('accessKeysMinPlayerLevel', 0),
            'sorties': liste_sorties,
            'sortiesJeu': liste_jeu,
            'transits': transits,
            'boss': boss_liste(carte, fr, w.get('boss', [])),
            'dangers': dangers(carte),
            'cles': cles,
            'clesWiki': w.get('cles', []),
            'bossWiki': w.get('boss', []),
            'spawns': spawns(carte),
            'parMode': {},
            'variantes': [],
            'ecartsModes': [],
        }
        cartes.append(entree)

    par_slug = {c['slug']: c for c in cartes}
    # Variantes rattachées
    for slug_v, (parent, libelle) in VARIANTES.items():
        id_, carte, fr = extraire_carte('regular', slug_v)
        if carte is None:
            continue
        par_slug[parent]['variantes'].append({
            'slug': slug_v,
            'nom': fr.get(carte['name'], slug_v),
            'libelle': libelle,
            'dureeMinutes': carte.get('raidDuration'),
            'joueurs': carte.get('players'),
            'niveaux': {'min': carte.get('minPlayerLevel', 0), 'max': carte.get('maxPlayerLevel', 100)},
            'sorties': len(carte.get('extracts', [])),
            'boss': boss_liste(carte, fr),
            'dangers': dangers(carte),
        })

    # Écarts entre modes
    for entree in cartes:
        reference = None
        for mode in MODES:
            id_, carte, fr = extraire_carte(mode, entree['slug'])
            if carte is None:
                continue
            bloc = {
                'dureeMinutes': carte.get('raidDuration'),
                'joueurs': carte.get('players'),
                'niveaux': {'min': carte.get('minPlayerLevel', 0), 'max': carte.get('maxPlayerLevel', 100)},
                'sorties': len(carte.get('extracts', [])),
                'sortiesPMC': sum(1 for e in carte.get('extracts', []) if e.get('faction') in ('pmc', 'shared')),
                'sortiesScav': sum(1 for e in carte.get('extracts', []) if e.get('faction') == 'scav'),
                'boss': [b['nom'] for b in boss_liste(carte, fr)],
                'ennemis': [fr.get(e, e) for e in carte.get('enemies', [])],
                'transits': len(carte.get('transits', [])),
                'hazards': len(carte.get('hazards', [])),
            }
            entree['parMode'][mode] = bloc
            if mode == 'regular':
                reference = bloc
        ecarts = []
        for mode in MODES:
            bloc = entree['parMode'].get(mode)
            if not bloc or bloc == reference:
                continue
            details = []
            for champ, libelle in (('sortiesPMC', 'sorties PMC'), ('sortiesScav', 'sorties Scav'),
                                   ('dureeMinutes', 'durée'), ('joueurs', 'effectif'),
                                   ('transits', 'transits')):
                if bloc[champ] != reference[champ]:
                    details.append(f'{libelle} {reference[champ]} → {bloc[champ]}')
            if bloc['ennemis'] != reference['ennemis']:
                ajouts = [e for e in bloc['ennemis'] if e not in reference['ennemis']]
                retraits = [e for e in reference['ennemis'] if e not in bloc['ennemis']]
                if ajouts:
                    details.append('ennemis +' + ', '.join(ajouts))
                if retraits:
                    details.append('ennemis −' + ', '.join(retraits))
            if bloc['boss'] != reference['boss']:
                ajouts = [b for b in bloc['boss'] if b not in reference['boss']]
                retraits = [b for b in reference['boss'] if b not in bloc['boss']]
                if ajouts:
                    details.append('boss +' + ', '.join(ajouts))
                if retraits:
                    details.append('boss −' + ', '.join(retraits))
            if details:
                ecarts.append({'mode': mode, 'details': details})
        entree['ecartsModes'] = ecarts

    return cartes


def main():
    cartes = constructions()
    doc = {
        'schemaVersion': 1,
        'genereLe': '2026-11-18',
        'langue': 'fr-FR',
        'source': {
            'donnees': 'Tarkov.dev / The Hideout (json.tarkov.dev) — instantanés regular, pve et pvp-season du 18 novembre 2026',
            'fiches': 'Escape from Tarkov Wiki (Fandom) — wikitext et résumés du 18 novembre 2026',
            'avertissement': 'Données communautaires. Elles décrivent un instantané, pas un build EFT attesté ni une carte officielle.',
            'versions': ['regular', 'pve', 'pvp-season'],
        },
        'legende': {
            'camp': 'PMC, Scav ou Partagée : camp autorisé à emprunter la sortie.',
            'interrupteur': 'Une sortie commandée par un interrupteur, souvent conditionnée à un temps d’activation.',
            'chance': 'Probabilité d’apparition du boss dans la location, selon l’instantané consulté.',
            'dangers': 'Zones de mines, snipers de bordure et claymores relevées dans les données de la carte.',
        },
        'lieux': cartes,
    }
    cible = ROOT / 'js/data/maps.json'
    cible.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'js/data/maps.json · {len(cartes)} lieux · {cible.stat().st_size} octets')
    for c in cartes:
        ecarts = '; '.join(f"{e['mode']}: {', '.join(e['details'])}" for e in c['ecartsModes'])
        print(f"  {c['slug']:18s} {c['nom'][:16]:18s} {c['dureeMinutes']:>3}min {c['joueurs']:>7} "
              f"sorties {len(c['sorties']):>3} boss {len(c['boss']):>2} | {ecarts[:90]}")


if __name__ == '__main__':
    main()
