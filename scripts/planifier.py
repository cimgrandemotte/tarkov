#!/usr/bin/env python3
"""Écrire le manifeste de routes et sa version lisible, sans générer de pages HTML."""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
SOURCES = json.loads((DOCS / 'sources.json').read_text())['sources']
PAGES = []
PUBLISHED = {'PUBLIEE', 'PUBLIÉE'}
TITRES = {
    2: 'Accueil et navigation', 3: 'Débutant et lore', 4: 'Cartes', 5: 'Armes et munitions',
    6: 'Armures et boss', 7: 'Traders, quêtes et planque', 8: 'Compétences, économie et stratégie',
    9: 'SP-Tushonka, Arena et événements', 10: 'Patchs, ressources et glossaire',
}
GABARITS = {
    'accueil': 'Point d’entrée vers les hubs effectivement publiés, compteur de contenu vérifiable et dates des annonces.',
    'guide': 'Résumé utile, table des matières, données ou étapes, pièges courants, sources et guides à lire ensuite.',
    'hub': 'Vue d’ensemble, raccourcis vers les fiches, synthèse et filtres utiles à la section.',
    'carte': ('Lore court avec spoilers isolés ; accès, modes, durée et variantes ; spawns et boss datés ; toutes les extractions PMC/Scav couvertes '
              'ou dites non applicables, conditions et transits ; POI/loot, clés, routes de quêtes, risques et stratégies par niveau. '
              'Vérifier les positions avant annotation. Aucun pourcentage unique hors contexte.'),
    'famille-arme': ('Inventaire de la famille avec identifiants, modes, cadence, dimensions, ergonomie et recul à configuration égale. '
                     'Dégâts et vitesse rattachés à la munition et au preset s’il y a lieu. Sources d’achat, configurations testables, alternatives '
                     'et tiers justifiés en fonction du budget, du mode et de la date.'),
    'boss': ('Fiche de rencontre par carte et variant : HP par membre si attesté, gardes, zones, conditions et données de spawn datées, '
             'équipement et loot garanti/aléatoire distincts. Stratégie dans le jeu, difficulté éditoriale et média de référence contrôlé.'),
    'trader': ('Fidélité et déblocage par mode, devises, métiers, quêtes et achats/échanges significatifs ; comparer la source primaire '
               'consécutive à la refonte d’août et les offres datées. Préciser « sans objet » plutôt qu’inventer un palier.'),
    'outil': 'Interface avec états chargement/vide/erreur, tableau et méthode accessibles, provenance affichée, option de réinitialisation.',
}


def page(n, route, title, content, ui, media, sources, kind='guide', lookup=None):
    ids = sources.split()
    unknown = set(ids) - SOURCES.keys()
    if unknown:
        raise ValueError(f'Sources inconnues : {unknown}')
    images = [part.strip() for part in media.split(';') if part.strip()]
    if len(images) < (3 if kind == 'carte' else 2):
        raise ValueError(f'Plan iconographique incomplet pour {route}')
    PAGES.append({
        'phase': f'PHASE_{n}', 'route': route, 'titre': title, 'gabarit': kind,
        'angleEditorial': content, 'interaction': ui, 'illustrationsJpg': images,
        'sourcesDeDepart': ids, 'rechercheCiblee': lookup, 'etat': 'PLANIFIEE',
    })


page(2, 'index.html', 'Tarkov Ultimate Guide',
     'Brief de raid, guide débutant, sélection de dossiers, navigation transversale, 1.3.0.0 et nouvelles datées.',
     'Méga-menu, recherche globale, hub par parcours et compteurs issus du manifeste de publication.',
     'PMC sous la pluie dans Tarkov; Vue aérienne d’un secteur urbain; Arsenal sur établi; Silhouette Scav dans la brume',
     'bsg-news bsg-1300 steam-game bsg-city data-index', 'accueil', lookup='Consigner les annonces, versions et conseils d’entrée avant publication.')
page(3, 'pages/getting-started.html', 'Premiers pas dans Tarkov',
     'USEC/BEAR, choix du mode, pré-raid → raid → après-raid, santé et soins, sorties, stash, traders, paramètres, touches, dix étapes et FAQ 20+.',
     'Checklists persistantes, FAQ repliable et aide clavier adaptable.',
     'PMC vérifiant son kit dans la planque; Interface de raid légendée; Schéma des zones de santé',
     'wiki-start youtube-start bsg-1200 bsg-1300 reddit-eft', lookup='Recouper l’interface, les touches par défaut et les exceptions PvP/Seasonal.')
page(3, 'pages/lore/index.html', 'Norvinsk : lore et chronologie',
     'TerraGroup, Contract Wars, USEC, BEAR, Scavs, protagonistes et liens avec les arcs du jeu. Distinguer canon, interprétations et révélations.',
     'Fils temporels et volets de spoilers fermés par défaut.',
     'Ville de Tarkov au crépuscule; Carte géopolitique originale de la région',
     'bsg-lore wiki-bear wiki-maps wiki', lookup='Vérifier les dossiers USEC, TerraGroup, story chapters et la provenance du canon.')

page(4, 'pages/maps/index.html', 'Atlas des cartes',
     'Treize lieux de référence ; variantes jour/nuit, niveau, tutoriel et événement regroupées sous leur carte ou dossier. Accès, profils, durée, difficulté et menaces.',
     'Filtres, navigation par lieu, comparatif deux cartes et tableau équivalent.',
     'Panorama de Tarkov et de sa périphérie; Vue portuaire; Schéma du réseau de transits',
     'wiki-maps wiki-maps-fr data-maps data-maps-fr data-maps-pve data-maps-season mapgenie kappa bsg-1150 bsg-1200 bsg-1300 wiki-controls wiki-game-modes wiki-changelog changelog-gg github-goon-tracker twistedvoxel-halloween', 'hub')
MAPS = [
    ('factory', 'Factory', 'Jour/nuit, sous-sols et passerelles, sorties avec et sans clé, Tagilla et variantes infectées.', 'Panorama de la halle industrielle; Carte des niveaux; Scène près des bureaux', 'Factory bsg-1300 halloween-pr reddit-extracts twistedvoxel-halloween'),
    ('customs', 'Customs', 'Dortoirs, Big Red, entrepôts et forteresse ; circuits de premières quêtes et nouveaux exfils du 1.2.', 'Vue du pont et de la douane; Carte des accès et sorties révisés; Arrivée aux dortoirs', 'Customs bsg-1200 reddit-extracts'),
    ('woods', 'Woods', 'Scierie et Shturman, limites du terrain, camps et repères naturels ; l’événement Wild Wild Woods séparé des règles normales.', 'Lac et scierie dans la brume; Carte des lisières; Ravitaillement près d’un camp', 'Woods wild-wild wild-wild-end reddit-extracts'),
    ('shoreline', 'Shoreline', 'Resort, jetée, villages et Sanitar ; différences entre exfils, transits Icebreaker, Labyrinth et Terminal.', 'Resort Azure Coast; Carte du littoral et des transits; Arrivée à la jetée', 'Shoreline bsg-1150 bsg-1300 reddit-shoreline-keys'),
    ('interchange', 'Interchange', 'ULTRA, IDEA/OLI/Goshan, niveaux et alimentation ; Killa, butin tech et corrections du 1.2.', 'Parking et façades d’ULTRA; Carte des étages; Couloir commercial sombre', 'Interchange bsg-1200 reddit-extracts'),
    ('reserve', 'Reserve', 'Bunkers, surface, train, leviers, Raiders et Glukhar ; contraintes des exfils et clés des bâtiments.', 'Base vue du dôme; Carte surface/bunker; Quais du train', 'Reserve full-speed'),
    ('the-lab', 'The Lab', 'Accès par keycard, niveaux, alarmes, Raiders et extractions activées ; variantes Blackout et Infected en archives séparées.', 'Laboratoire TerraGroup éclairé; Carte des étages et commandes; Couloir du Lab dans l’obscurité', 'The_Lab halloween-pr wiki-events blackout-head twistedvoxel-halloween'),
    ('lighthouse', 'Lighthouse', 'Chalets, Rogues, BTR, Lightkeeper, transit Icebreaker et passages ; vérifier les zones de danger restantes hors Water Treatment.', 'Côte et phare; Carte post-refonte avec chalets; Arrivée près des voies du BTR', 'Lighthouse bsg-1150 bsg-1300 wiki-ice youtube-lighthouse-guide reddit-lighthouse-loot'),
    ('streets-of-tarkov', 'Streets of Tarkov', 'Concession, mall, entrées d’immeubles, BTR et signes d’extraction ; Kaban, Kollontay, trajets selon la quête.', 'Avenue post-industrielle; Carte par quartiers; Entrée de la concession', 'Streets_of_Tarkov bsg-1100'),
    ('ground-zero', 'Ground Zero', 'Départ, TerraGroup et premières tâches ; tutoriel, tranches de niveau et Cultists hors confusions de mode.', 'Place du centre d’affaires; Carte tutoriel et variantes; Entrée TerraGroup', 'Ground_Zero wiki-start wiki-tour reddit-extracts'),
    ('the-labyrinth', 'The Labyrinth', 'Accès Shoreline, conditions d’entrée, phases et sorties ; Shadow of Tagilla, Vengeful Killa, aperçu sans spoiler.', 'Galerie souterraine; Plan légendé des zones; Porte et éclairage industriel', 'The_Labyrinth bsg-1150 bsg-1200'),
    ('icebreaker', 'Icebreaker', 'Boreas, transits, kit et accès direct ; étages du navire, Wedge, Knight, activités de groupe et sorties.', 'Brise-glace dans le golfe; Carte multi-ponts; Pont intérieur de la salle des machines', 'Icebreaker wiki-ice ice-patch bsg-1150 bsg-1200 bsg-boreas-x'),
    ('terminal', 'Terminal', 'Port et fin de l’histoire, accès depuis Shoreline, variantes et conditions. Durée et sorties à recouper ; éviter de gâcher les fins.', 'Terminal portuaire; Carte d’approche vérifiée; Quai de conteneurs', 'Terminal steam-news bsg-1200 wiki-ticket ign-terminal ign-ticket'),
]
SOURCES_CARTES = 'wiki-maps wiki-maps-fr data-maps data-maps-fr data-maps-pve data-maps-season mapgenie kappa'
for slug, title, content, media, extra in MAPS:
    wiki_id, _, more = extra.partition(' ')
    page(4, f'pages/maps/{slug}.html', title, content,
         'Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.', media,
         f'{SOURCES_CARTES} {wiki_id} {more}', 'carte',
         f'Ouvrir la fiche wiki « {wiki_id.replace("_", " ")} », comparer avec la carte du client et vérifier les écarts de mode et de date.')

page(5, 'pages/weapons/index.html', 'Arsenal EFT',
     'Catalogue exhaustif au périmètre de l’instantané : familles, objets jouables, presets et variantes distincts. Builds conditionnés par munitions et mode.',
     'Filtres calibre/famille/prix/trader/ergo/recul/cadence, comparateur jusqu’à trois entrées, rangs motivés.',
     'Établi modulaire; Arsenal rangé par familles; Détail d’une fiche équipement',
     'data-index data-items wiki kappa', 'hub', 'Contrôler les armes cachées ou événementielles et les données des presets dans le client.')
WEAPONS = [
    ('assault-rifles', 'Fusils d’assaut et carabines', 'Scinder les classes officielles rifle/carbine ; comparer M4, AK et alternatives pour différents accès.', 'M4A1 sur établi; Famille AK en atelier'),
    ('smgs', 'Pistolets-mitrailleurs (SMG)', 'Progression 9×19, 4,6×30 et 5,7×28 ; cadence, chargeur et disponibilité par profil.', 'MP5 en vitrine; MP7 en atelier'),
    ('shotguns', 'Fusils à pompe et semi-automatiques', 'Coût d’entrée, longueur, plombs vs slugs et projectiles multiples ; MP-133 et alternatives.', 'MP-133 sur établi; Pompe et semi-auto en râtelier'),
    ('sniper-rifles', 'Fusils de précision à verrou', 'Catalogue bolt-action, distance efficace en jeu, stabilité des presets, coût des optiques et quêtes liées.', 'SV-98 en studio; Optique dans un poste de tir virtuel'),
    ('dmrs', 'Fusils de précision semi-auto (DMR)', 'Effets de configuration sur SR-25, SVD et autres DMR ; distinguer cadence théorique et confort en jeu.', 'SVD sur établi; DMR en atelier optique'),
    ('lmgs', 'Mitrailleuses légères et polyvalentes', 'RPK, familles à bande et autres LMG ; poids, tailles de chargeur et contraintes propres au jeu.', 'RPK dans une armurerie; Détail de caisse d’équipement lourde'),
    ('pistols', 'Pistolets et revolvers', 'Regrouper visuellement sans confondre handgun et revolver ; tableaux des calibres, secours et quêtes.', 'Pistolet Makarov dans un casier; Revolver sur tapis de rangement'),
    ('melee', 'Armes de mêlée', 'Portée et dégâts de coups (pas de variables de munitions) ; drops, quêtes et usages en jeu.', 'Baïonnette d’inventaire; Outils de mêlée de boss en vitrine'),
    ('grenade-launchers', 'Lance-grenades et lanceurs spéciaux', 'Lanceurs autonomes, sous-canon et lance-roquettes annotés comme sous-familles distinctes ; profil et restriction en jeu.', 'Lanceur de l’arsenal en studio; Râtelier de matériel spécialisé'),
    ('weapon-mods', 'Modifications et accessoires', 'Compatibilité de slots, pièces requises, crosse dépliée/repliée, présélection et mesures de build ; dépendances de pièces.', 'Composants d’un preset de jeu; Schéma d’arborescence des slots'),
]
for slug, title, content, media in WEAPONS:
    page(5, f'pages/weapons/{slug}.html', title, content,
         'Tri, filtres adaptés, comparables homogènes et presets contextualisés.', media, 'data-items data-index wiki kappa',
         'famille-arme', 'Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.')
page(5, 'pages/ammo/index.html', 'Munitions : comprendre la balistique',
     'Dégâts, pénétration, classes, perte de vitesse, tirs multiples et champs sans effet confirmé. Choix budget et disponibilité par calibre/mode.',
     'Cartes par calibre, grille d’efficacité in-game et raccourcis vers le tableau complet ; rangs contextualisés.',
     'Macro de cartouches d’inventaire; Infographie des dégâts en jeu; Schéma de couverture de plaque',
     'data-items wiki-ballistics wiki-ammo-sample bsg-1300', 'hub')
page(5, 'pages/ammo/ammo-chart.html', 'Tableau balistique interactif',
     'Séparer profils balistiques et autres munitions, indiquer unités, prix et horodatage, comparer munitions, offre trader et craft.',
     'Recherche, tri stable, filtres, Chart.js et alternative tabulaire du nuage pénétration/dégâts.',
     'Séries de cartouches calibrées; Infographie de lecture du nuage de points',
     'data-items data-index wiki-ballistics wiki-ammo-sample', 'outil')

ARMOR = [
    ('index', 'Armures et protection', 'Expliquer modèle de zones, classes, matériaux, durabilité et compatibilité de plaques.', 'Hub et fiches reliées ; filtres par slot et classe.', 'Gilet et plaques à l’établi; Schéma des zones couvertes', 'hub'),
    ('body-armor', 'Gilets et porte-plaques', 'Séparer tissu, plaques et zones ; exemples légers/lourds et compromis de mobilité.', 'Filtres de classe, couverture et matériau.', 'Porte-plaques ouvert; Croquis des interfaces de plaque', 'guide'),
    ('helmets', 'Casques et visières', 'Coquilles, visières, protections d’oreilles, compatibilité de casque audio et ricochet en jeu.', 'Tableau par zone ; compatibilité inspectable.', 'Casque et visière en studio; Schéma de protection du profil', 'guide'),
    ('rigs', 'Rigs et poches', 'Rigs blindés ou non, capacité brute vs géométrie, coût, poids et place ; ne pas assimiler un rig à une classe de protection.', 'Comparaison des grilles, filtres armuré/non armuré.', 'Rig chargé en planque; Diagramme de rangements', 'guide'),
    ('armor-chart', 'Comparateur d’armures', 'Comparer valeurs à configuration cohérente ; afficher plaques, indices, pénalités et données manquantes.', 'Sélection 2–3 pièces, colonnes normalisées et info-bulles accessibles.', 'Deux tenues défensives; Schéma comparatif de couverture', 'outil'),
]
for slug, title, content, ui, media, kind in ARMOR:
    page(6, f'pages/armor/{slug}.html', title, content, ui, media, 'data-items data-index wiki-ballistics wiki', kind,
         'Vérifier les emplacements de plaques, les unités de pénalité et les restrictions de mode.')
page(6, 'pages/bosses/index.html', 'Boss et rencontres',
     'Profils majeurs, alternatives événementielles, groupes, gardes et distinction des Raiders/Rogues. Résumé des PV et apparitions sans agrégation trompeuse.',
     'Grille de fiches, matrice cartes × boss, comparateur par mode et difficulté éditoriale.',
     'Reshala aux dortoirs; Killa dans ULTRA; Tagilla dans Factory; The Goons dans les bois; Black Division à Icebreaker',
     'data-maps wiki-bosses boss-analysis bsg-kord-nov bsg-1300', 'hub')
BOSSES = [
    ('reshala', 'Reshala', 'Dortoirs, station et Stronghold ; gardes et intérêt du Golden TT.', 'Portrait aux dortoirs; Accès à une cour de Customs'),
    ('killa', 'Killa', 'ULTRA et variantes ; casque Maska, loot, dissocier l’apparition de Vengeful Killa.', 'Portrait dans ULTRA; Allée des commerces'),
    ('shturman', 'Shturman', 'Scierie, deux gardes, cache dédiée et statut du Red Rebel.', 'Shturman près de la scierie; Casiers de la zone boisée'),
    ('glukhar', 'Glukhar', 'Reserve et variantes ; rôles des gardes et mobilité, taux par carte.', 'Portrait dans une cour militaire; Couloir de Reserve'),
    ('sanitar', 'Sanitar', 'Resort, jetée et autres zones vérifiées ; comportement, soins et objets de quête.', 'Portrait médical au Resort; Ponton de Shoreline'),
    ('tagilla', 'Tagilla', 'Factory et variantes jour/nuit, poursuite en jeu, masques et forme infectée séparée.', 'Soudeur de Factory; Passerelles de l’usine'),
    ('kaban', 'Kaban', 'Concession, gardes et accès ; inventaire spécial, clés et dangers du secteur.', 'Kaban dans la concession; Entrée du garage'),
    ('kollontay', 'Kollontay', 'Zones de Streets, équipiers, matraque et conditions de son effet en jeu.', 'Portrait de Kollontay; Hall du quartier policier'),
    ('zryachiy', 'Zryachiy', 'Île, gardes et relation avec l’accès Lightkeeper ; séparer les variantes saisonnières.', 'Veilleur du phare; Presqu’île dans la brume'),
    ('partisan', 'Partisan', 'Karma PMC et conditions d’apparition : appliquer le correctif 1.3.0.0 et dater les exceptions.', 'Portrait en lisière de forêt; Sentier abandonné'),
    ('cultist-priest', 'Cultist Priest', 'Nuit, classes de lieu et tranches de Ground Zero ; vocabulaire Sectant et distinction des événements.', 'Cultiste dans une lumière basse; Abri nocturne sur la carte'),
    ('the-goons', 'The Goons', 'Sous-fiches Knight, Big Pipe, Birdeye ; rotation selon mode, composition et faux doubles comptages.', 'The Goons dans les bois; Équipement de reconnaissance en jeu'),
    ('shadow-of-tagilla', 'Shadow of Tagilla', 'Labyrinth ; séquence de rencontre et apparition de Vengeful Killa si vérifiée.', 'Silhouette dans le Labyrinth; Croisement des galeries'),
    ('the-wedge', 'The Wedge', 'Icebreaker, escortes par taille de groupe et variante de Blackout ; pas de taux universel.', 'Portrait Black Division à bord; Salle de sport du brise-glace'),
]
for slug, title, content, media in BOSSES:
    page(6, f'pages/bosses/{slug}.html', title, content,
         'Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.', media,
         'data-maps wiki-bosses boss-analysis bsg-1300' + (' bsg-1150 ice-patch blackout-head' if slug == 'the-wedge' else ''),
         'boss', f'Vérifier la fiche {title}, les entrées événementielles et les ajustements après le 29 octobre.')

page(7, 'pages/traders/index.html', 'Les traders de Tarkov',
     'Dix profils, indices de réputation, nouvelles règles de fidélité, relations et inventaires clés.',
     'Comparateur de loyauté, filtre par besoin et liens vers les quêtes.',
     'Bureau de négociation; Étagères de stock et jetons', 'bsg-1100 data-index wiki-traders wiki-quests', 'hub')
TRADERS = [
    ('prapor', 'Prapor', 'Armes, premiers objectifs, assurance et offres russes à plusieurs niveaux.', 'Bureau de Prapor; Caisse de fournitures'),
    ('therapist', 'Therapist', 'Soins, Salewa, matériel médical, achats prioritaires et options d’assurance.', 'Poste médical de Therapist; Étagères de soins'),
    ('skier', 'Skier', 'Premiers barters, quêtes d’accès, accessoires, et lien aux activités Halloween/Blackout.', 'Atelier de Skier; Stock de pièces'),
    ('peacekeeper', 'Peacekeeper', 'Déblocage, USD, offres importées et paliers de quêtes.', 'Comptoir de Peacekeeper; Pièces et accessoires dans casiers'),
    ('mechanic', 'Mechanic', 'Pièces, Gunsmith, déblocage de Jaeger, lien vers sorties d’atelier.', 'Établi de Mechanic; Modules inspectés'),
    ('ragman', 'Ragman', 'Rigs, vêtements, armures, quêtes Interchange et accès au kit Icebreaker.', 'Boutique de Ragman; Rigs sur portants'),
    ('jaeger', 'Jaeger', 'Quêtes de survie et contraintes, équipement, assurance si attestée par mode.', 'Abri de Jaeger; Casier de fournitures de Woods'),
    ('fence', 'Fence', 'Karma Scav, inventaire changeant, paliers réellement applicables et limites par événement.', 'Comptoir de Fence; Marché secondaire nocturne'),
    ('lightkeeper', 'Lightkeeper', 'Accès en raid, chaîne To the Light post-refonte, échanges et restrictions de zone.', 'Intérieur du phare; Approche de la presqu’île'),
    ('ref', 'Ref', 'Déblocage et échanges, quêtes croisées avec Arena, bilan des devises et conditions par mode.', 'Point d’échange de Ref; Couloir d’Arena'),
]
for slug, title, content, media in TRADERS:
    page(7, f'pages/traders/{slug}.html', title, content,
         'Tableaux de paliers, quêtes liées et liens vers les items/échanges.', media,
         'data-index bsg-1100 wiki-traders wiki-quests' + (' bsg-1150' if slug == 'lightkeeper' else ' arena' if slug == 'ref' else ''),
         'trader', f'Contrôler l’offre et la fiche {title} par mode avant publication.')
page(7, 'pages/quests/index.html', 'Catalogue des quêtes',
     'Objectifs, prérequis, récompenses, factions, missions principales/secondaires/opérationnelles et saisonnières séparées.',
     'Recherche par nom bilingue, trader, mode ou carte et suivi local.',
     'Dossier de missions classées; Kit de sortie d’un PMC', 'data-index wiki-quests bsg-1100 bsg-1060 tracker', 'hub')
page(7, 'pages/quests/quest-tree.html', 'Arbre de progression des quêtes',
     'Relations d’ordre, conditions composites, prérequis d’histoire et objectifs de groupe ; audit des cycles et liens incomplets.',
     'Vue du graphe et liste clavier ; filtres et états de progression exportables.',
     'Mur de briefing; Schéma de lecture des prérequis', 'data-index wiki-quests bsg-1100 tracker', 'outil')
page(7, 'pages/quests/kappa-guide.html', 'Obtenir le conteneur Kappa',
     'Accès à Collector, liste d’objets FIR, tâches requises par version et conditions saisonnières ; éviter de recycler les anciennes exigences.',
     'Checklist et progression persistante ; différences de mode.',
     'Conteneur sécurisé dans un stash; Étagère d’objets Collector', 'data-index bsg-1100 kappa wiki-quests tracker')
page(7, 'pages/hideout/index.html', 'Planque : modules et progression',
     'Stations, niveaux, conditions, matériaux, ordre de construction, consommation et coûts ; Bitcoin Farm et calculs par scénario.',
     'Plan de modules, progression locale et vérification des dépendances.',
     'Planque avec établi et ventilations; Station médicale; Ferme Bitcoin', 'data-index wiki-hideout bsg-1300 tracker', 'hub')
page(7, 'pages/hideout/crafting.html', 'Crafts et temps de retour',
     'Ingrédients vs outils, quantités de sortie, carburant, déverrouillages et calcul du net horaire.',
     'Tableau recherchable ; calculateur de coût éditable, horodatage des sources et simulation transparente.',
     'Établi de craft; Générateur dans la planque', 'data-index wiki-hideout tarkov-market tracker', 'outil')

page(8, 'pages/skills/index.html', 'Compétences : progresser par mode',
     'Familles, XP, maîtrise, effets, limites et rendement ; Metabolism et bonus Seasonal du 1.3.0.0 distingués.',
     'Filtres par famille, tableaux chiffrés et comparaison PvE/PvP/Seasonal.',
     'Salle d’entraînement en planque; Infographie de suivi des compétences', 'bsg-1300 data-items data-index wiki-skills')
page(8, 'pages/economy/index.html', 'Économie du raid',
     'Flea vs traders, stratégies nettes après coût, devises et TarCoin de la boutique distinguées, renvoi aux routes et crafts.',
     'Outil d’arbitrage vendable/à garder ; date de saisie et onglets par profil.',
     'Réserve de monnaies du jeu; Dépôt de butin trié', 'bsg-1100 bsg-tarcoin data-items tarkov-market kappa', 'hub')
page(8, 'pages/economy/flea-market.html', 'Flea Market : accès et frais',
     'Niveaux d’accès et restrictions par profil/objet ; coût de transaction, prix observé, ruptures et limites de données.',
     'Calculateur net manuel et tableau d’exemples paramétrables, sans flux inventé.',
     'Marché de revente dans Tarkov; Illustration d’une comparaison comptable', 'bsg-1100 data-index data-items tarkov-market wiki-traders', 'outil')
page(8, 'pages/economy/money-making.html', 'Roubles : routes et rendement',
     'Routes de raid, liquidité, inventaire, revente par trader et butin prioritaire ; estimer en tenant compte des échecs.',
     'Filtres par carte, temps, budget et niveau ; comparateur de rendement à hypothèses visibles.',
     'Casiers de collecte; Matériaux de récupération stockés', 'data-maps data-items kappa tarkov-market')
page(8, 'pages/strategy/index.html', 'Stratégies et méta',
     'Parcours apprenti/régulier/vétéran, objectifs PvP/PvE, budget contre fin de progression et choix du kit.',
     'Parcours à facettes et raccourcis vers les dossiers.',
     'Salle de préparation de raid; Sac et équipements sur banc', 'bsg-1300 bsg-1200 data-items wiki-start kappa', 'hub')
STRATEGY = [
    ('beginner-tips', '50+ astuces pour bien débuter', 'Conseils triables : inventaire, assurance, exfils, santé, quêtes, Scav, progression et réglages.', 'Checklist par situation.', 'Débutant en session de repérage; Kit économique en planque', 'wiki-start youtube-start bsg-1200'),
    ('advanced-tactics', 'Tactiques avancées de raid', 'Rythme, information, rotations, transits, gestion en groupe et analyse des erreurs propres à EFT.', 'Scénarios comparables et débriefs.', 'Progression près d’un transit; Équipe dans un couloir du jeu', 'data-maps bsg-1150 wiki-start'),
    ('pvp-guide', 'Guide PvP', 'Progression permanente et Seasonal séparées ; engagement, audio, budget et erreur de lecture du terrain dans le jeu.', 'Choix de contexte par mode et carte.', 'Scène d’observation dans Streets; Entrée de zone d’extraction', 'bsg-1100 bsg-1151 bsg-1300 reddit-eft'),
    ('pve-guide', 'Guide PvE et Prestige', 'Bots, modes local/en ligne, coop et exigences actuelles des six niveaux ; décisions de reset et conservation.', 'Comparatif avant/après, checklist Prestige et avertissements.', 'Route solo dans Ground Zero; Planque avant un Prestige', 'bsg-1200 bsg-1300 data-index'),
    ('meta-builds', 'Builds méta et équivalents budget', 'Combinaisons de pièces documentées, disponibilité trader, coût, calibre et contraintes de la saison. Aucun rang « absolu ».', 'Choix du budget, stat de base/preset et substituts.', 'Build budget en râtelier; Preset haut de gamme sur établi', 'data-items data-index bsg-1300 kappa'),
]
for slug, title, content, ui, media, sources in STRATEGY:
    page(8, f'pages/strategy/{slug}.html', title, content, ui, media, sources, lookup='Recouper les conseils communautaires datés et identifier les comportements dépendants du mode.')

SPT = [
    ('index', 'Single Player Tushonka', 'Chronologie de l’ancien SPT, projet successeur, 4.1.6 stable vs paquet 5.0 expérimental, comparaison avec le PvE officiel.', 'Comparateur de modes et orientation vers quatre dossiers.', 'Opérateur solitaire dans Tarkov; Illustration du launcher distincte d’une capture; Planque privée', 'spt-history spt-history-2 spt-stable spt-nuget spt-forge reddit-tushonka', 'hub'),
    ('installation', 'Installer SP-Tushonka', 'Prérequis de la version stable, copie légitime et isolée, installateur des mainteneurs, premier lancement et sauvegarde.', 'Checklist de préparation et procédure repliable par système si documentée.', 'Écran de configuration vérifié ou recréé et étiqueté; Diagramme des dossiers', 'spt-stable spt-installer spt-wiki spt-releases', 'guide'),
    ('mods', 'Mods SP-Tushonka', 'Sélection IA, qualité de vie et progression avec versions Forge, dépendances, conflits et date de contrôle.', 'Filtres par version et catégorie ; fiche « vérifier avant d’installer ».', 'Outils de paramétrage illustratifs; Planche de métadonnées de mods', 'spt-forge spt-stable reddit-tushonka', 'hub'),
    ('fika', 'Coop privée avec Project Fika', 'Versions client/serveur, parité des mods, préparation du groupe et test privé ; aucune confusion avec l’officiel ou le solo strict.', 'Checklist hôte/invité et matrice version par version.', 'Deux opérateurs dans une planque; Schéma de connexion d’un groupe privé', 'fika spt-forge spt-stable spt-wiki', 'guide'),
    ('troubleshooting', 'Dépannage SP-Tushonka', 'Boucle de démarrage, runtimes, erreurs de version et de mod, logs sans secrets, profil sauvegardé et retour au dernier état stable.', 'Diagnostic par symptôme et FAQ accessible.', 'Terminal de diagnostic illustratif; Schéma de sauvegarde de profil', 'spt-stable spt-wiki spt-releases reddit-tushonka', 'guide'),
]
for slug, title, content, ui, media, sources, kind in SPT:
    page(9, f'pages/spt-tushonka/{slug}.html', title, content, ui, media, sources, kind,
         'Consulter les releases et la documentation des mainteneurs le jour de rédaction ; vérifier chaque version liée.')
page(9, 'pages/arena/index.html', 'Escape from Tarkov: Arena',
     'BlastGang, TeamFight, CheckPoint et autres modes attestés ; progression Ref, séparation de versions, mécaniques compétitives et tournois vérifiés.',
     'Onglets par mode, profils d’équipement en jeu, calendrier sourcé.',
     'Vue d’une arène inspirée de Stadium; Écran de préparation d’équipe', 'arena bsg-1151 halloween-pr data-index')
page(9, 'pages/events/index.html', 'Événements de 2026',
     'Calendrier des activités, dates officielles et extensions, quêtes, récompenses, variantes de carte ; Halloween, Blackout, Icebreaker, Full Speed Ahead, Wild Wild Woods, Duckov et Tarkov City.',
     'Timeline filtrable par jeu, saison, mode et statut ; liste de lecture sans script.',
     'Couloir infecté de Factory; Brise-glace; Ambiance de The Lab (Dark)',
     'bsg-news bsg-1300 halloween-pr bsg-halloween-drops ice-drops full-speed full-speed-end wild-wild wild-wild-end bsg-city data-season wiki-events blackout-x-extension blackout-head duckov',
     'hub', 'Vérifier les dates réelles de fin, Blackout et Duckov dans le journal officiel ; séparer l’événement des Drops.')
page(10, 'pages/patch-notes.html', 'Notes de patch depuis la version 1.0',
     'Chronologie officielle, changements par système et impact éditorial justifié ; ETS, équilibrages et roadmap séparés des mises en production.',
     'Timeline par année/mode/type avec vue tableau et accès aux annonces originales.',
     'Archives de communications Tarkov; Tableau technique dans une salle de briefing',
     'bsg-news steam-news bsg-1300 bsg-1200 bsg-1151 bsg-1150 bsg-1100 bsg-1060 ice-forum bsg-ets-april patched', 'outil')
page(10, 'pages/resources/index.html', 'Ressources et outils',
     'Cartes, bases, marchés, trackers, YouTube, wiki, réseaux et Discord publics ; distinguer service officiel, outil tiers et contenu ancien.',
     'Filtres par besoin, mode et langue. Liens vérifiés ; pas d’intégration de compte requise.',
     'Bureau de consultation de cartes; Carnet d’archives de raid',
     'bsg-news data-index tarkov-dev tracker mapgenie tarkov-market tarkovhead kappa patched reddit-eft spt-forge arena bsg-legal', 'hub')
page(10, 'pages/resources/glossary.html', 'Glossaire EFT (FR / EN)',
     'Au moins 200 termes et sigles, définitions courtes et contextualisées ; aliases, jargon, items, synonymes FR/EN et renvois.',
     'Index A–Z et filtre accent-insensible ; ancres partageables pour chaque définition.',
     'Dictionnaire tactique de briefing; Fragments d’interface et abréviations',
     'wiki-start wiki data-items data-index tracker', 'outil')


def preserve_publication(existing, scheduled):
    """Les descriptions du plan évoluent sans dépublier ni perdre l'historique de la fiche."""
    previous = {row['route']: row for row in existing.get('pages', [])}
    new_paths = {row['route'] for row in scheduled}
    orphaned = [route for route, row in previous.items() if route not in new_paths and row['etat'] in PUBLISHED]
    if orphaned:
        raise ValueError(f'Archiver ou migrer explicitement les routes publiées avant de les retirer du plan : {orphaned}')
    results = []
    for item in scheduled:
        route = item['route']
        saved = previous.get(route, {})
        row = {**saved, **item}
        row.update(etat=saved.get('etat', item['etat']),
                   sourcesDeDepart=list(dict.fromkeys(item['sourcesDeDepart'] + saved.get('sourcesDeDepart', []))),
                   rechercheCiblee=saved.get('rechercheCiblee') or item['rechercheCiblee'])
        missing = set(row['sourcesDeDepart']) - SOURCES.keys()
        if missing:
            raise ValueError(f'Sources non répertoriées pour {route} : {missing}')
        if row['etat'] in PUBLISHED and not (ROOT / route).is_file():
            raise ValueError(f'Route marquée comme publiée mais absente : {route}')
        results.append(row)
    return results


def main():
    paths = [row['route'] for row in PAGES]
    if len(paths) != len(set(paths)) or not all(p.endswith('.html') for p in paths):
        raise ValueError('Routes HTML dupliquées ou invalides')
    for route in paths:
        assert (ROOT / route).parent.is_dir(), route
    target = DOCS / 'pages.json'
    existing = json.loads(target.read_text(encoding='utf-8')) if target.is_file() else {}
    pages = preserve_publication(existing, PAGES)
    counts = Counter(row['phase'] for row in pages)
    published = Counter(row['phase'] for row in pages if row['etat'] in PUBLISHED)
    n = published.total()
    doc = {'schemaVersion': 1, 'etat': 'EN_PUBLICATION' if n else 'PLANIFIE', 'total': len(paths),
           'parPhase': dict(counts), 'gabarits': GABARITS, 'pages': pages, 'publiees': n}
    text = [f'# Plan des {len(paths)} pages HTML', '',
            f'**{n} / {len(paths)} routes éditoriales publiées.** Les sources de départ ne dispensent pas d’une recherche ciblée. '
            'L’atelier de démonstration n’est pas compté.', '',
            '| Phase | Livrable | Prévues | Publiées |', '| --- | --- | ---: | ---: |']
    text += [f'| {n} | {title} | {counts[f"PHASE_{n}"]} | {published[f"PHASE_{n}"]} |' for n, title in TITRES.items()]
    text += ['', 'Les phases 0 et 1 ne publient pas d’articles. En phase 4, les 12 cartes demandées sont conservées et **Terminal** est ajouté. '
             'Les variantes sont traitées dans la fiche parente et/ou le dossier Événements.', '', '## Contenu commun des gabarits', '']
    text += [f'- **{kind.capitalize()}** — {description}' for kind, description in GABARITS.items()]
    for n, title in TITRES.items():
        text += ['', f'## Phase {n} — {title}', '']
        for row in (value for value in pages if value['phase'] == f'PHASE_{n}'):
            urls = ', '.join(f'[{key}]({SOURCES[key]["url"]})' for key in row['sourcesDeDepart'])
            published_label = 'Publié le ' + row.get('dateDePublication', '—') if row['etat'] in PUBLISHED else 'À venir'
            text += [f'### {row["titre"]}', '', f'`{row["route"]}` · {row["gabarit"]} · **{published_label}**', '',
                     f'- **Contenu.** {row["angleEditorial"]}', f'- **Interaction.** {row["interaction"]}',
                     f'- **JPG.** {" ; ".join(row["illustrationsJpg"])}.', f'- **Sources de départ.** {urls}.']
            if row['rechercheCiblee']:
                text.append(f'- **Contrôle ciblé.** {row["rechercheCiblee"]}')
            if row.get('mediasEffectifs') or row.get('audiosEffectifs'):
                text.append(f'- **Médias livrés.** {len(row.get("mediasEffectifs", []))} JPG et {len(row.get("audiosEffectifs", []))} MP3 originaux.')
            text.append('')
    stage = target.with_suffix('.json.tmp')
    stage.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    stage.replace(target)
    (DOCS / 'plan-des-pages.md').write_text('\n'.join(text).rstrip() + '\n', encoding='utf-8')
    print(f'{len(paths)} routes planifiées, {published.total()} publiées : {dict(counts)}')


if __name__ == '__main__':
    main()
