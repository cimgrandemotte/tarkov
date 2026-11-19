# Plan des 86 pages HTML

**30 / 86 routes éditoriales publiées.** Les sources de départ ne dispensent pas d’une recherche ciblée. L’atelier de démonstration n’est pas compté.

| Phase | Livrable | Prévues | Publiées |
| --- | --- | ---: | ---: |
| 2 | Accueil et navigation | 1 | 1 |
| 3 | Débutant et lore | 2 | 2 |
| 4 | Cartes | 14 | 14 |
| 5 | Armes et munitions | 13 | 13 |
| 6 | Armures et boss | 20 | 0 |
| 7 | Traders, quêtes et planque | 16 | 0 |
| 8 | Compétences, économie et stratégie | 10 | 0 |
| 9 | SP-Tushonka, Arena et événements | 7 | 0 |
| 10 | Patchs, ressources et glossaire | 3 | 0 |

Les phases 0 et 1 ne publient pas d’articles. En phase 4, les 12 cartes demandées sont conservées et **Terminal** est ajouté. Les variantes sont traitées dans la fiche parente et/ou le dossier Événements.

## Contenu commun des gabarits

- **Accueil** — Point d’entrée vers les hubs effectivement publiés, compteur de contenu vérifiable et dates des annonces.
- **Guide** — Résumé utile, table des matières, données ou étapes, pièges courants, sources et guides à lire ensuite.
- **Hub** — Vue d’ensemble, raccourcis vers les fiches, synthèse et filtres utiles à la section.
- **Carte** — Lore court avec spoilers isolés ; accès, modes, durée et variantes ; spawns et boss datés ; toutes les extractions PMC/Scav couvertes ou dites non applicables, conditions et transits ; POI/loot, clés, routes de quêtes, risques et stratégies par niveau. Vérifier les positions avant annotation. Aucun pourcentage unique hors contexte.
- **Famille-arme** — Inventaire de la famille avec identifiants, modes, cadence, dimensions, ergonomie et recul à configuration égale. Dégâts et vitesse rattachés à la munition et au preset s’il y a lieu. Sources d’achat, configurations testables, alternatives et tiers justifiés en fonction du budget, du mode et de la date.
- **Boss** — Fiche de rencontre par carte et variant : HP par membre si attesté, gardes, zones, conditions et données de spawn datées, équipement et loot garanti/aléatoire distincts. Stratégie dans le jeu, difficulté éditoriale et média de référence contrôlé.
- **Trader** — Fidélité et déblocage par mode, devises, métiers, quêtes et achats/échanges significatifs ; comparer la source primaire consécutive à la refonte d’août et les offres datées. Préciser « sans objet » plutôt qu’inventer un palier.
- **Outil** — Interface avec états chargement/vide/erreur, tableau et méthode accessibles, provenance affichée, option de réinitialisation.

## Phase 2 — Accueil et navigation

### Tarkov Ultimate Guide

`index.html` · accueil · **Publié le 2026-11-18**

- **Contenu.** Brief de raid, guide débutant, sélection de dossiers, navigation transversale, 1.3.0.0 et nouvelles datées.
- **Interaction.** Méga-menu, recherche globale, hub par parcours et compteurs issus du manifeste de publication.
- **JPG.** PMC sous la pluie dans Tarkov ; Vue aérienne d’un secteur urbain ; Arsenal sur établi ; Silhouette Scav dans la brume.
- **Sources de départ.** [bsg-news](https://www.escapefromtarkov.com/news?lang=en), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [steam-game](https://store.steampowered.com/app/3932890/Escape_from_Tarkov/), [bsg-city](https://www.escapefromtarkov.com/news/id/419), [data-index](https://json.tarkov.dev/endpoints), [bsg-kord-fin](https://x.com/tarkov/status/2120516987973513381), [bsg-kord-nov](https://x.com/tarkov/status/2120935917351289274), [wiki-changelog](https://escapefromtarkov.fandom.com/wiki/Changelog), [bsg-exfil-brothers](https://www.escapefromtarkov.com/news/id/412), [steam-exfil-forum](https://steamcommunity.com/app/3932890/discussions/1/588439600674137457/), [wiki-start](https://escapefromtarkov.fandom.com/wiki/How_to_Play_Guide_for_Escape_from_Tarkov), [spt-stable](https://github.com/SP-Tushonka/build/releases/tag/4.1.6), [arena-0625](https://arena.tarkov.com/news/patch-0625), [bsg-pve-bundle](https://www.escapefromtarkov.com/news/id/417), [apg-nav](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/), [tracker-home](https://tarkovtracker.org/), [bsg-1200](https://www.escapefromtarkov.com/news/id/411).
- **Contrôle ciblé.** docs/veille-phase-2.md
- **Médias livrés.** 8 JPG et 1 MP3 originaux.


## Phase 3 — Débutant et lore

### Premiers pas dans Tarkov

`pages/getting-started.html` · guide · **Publié le 2026-11-18**

- **Contenu.** USEC/BEAR, choix du mode, pré-raid → raid → après-raid, santé et soins, sorties, stash, traders, paramètres, touches, dix étapes et FAQ 20+.
- **Interaction.** Checklists persistantes, FAQ repliable et aide clavier adaptable.
- **JPG.** PMC vérifiant son kit dans la planque ; Interface de raid légendée ; Schéma des zones de santé.
- **Sources de départ.** [wiki-start](https://escapefromtarkov.fandom.com/wiki/How_to_Play_Guide_for_Escape_from_Tarkov), [youtube-start](https://www.youtube.com/watch?v=P5hyxI-cbb4), [bsg-1200](https://www.escapefromtarkov.com/news/id/411), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [reddit-eft](https://www.reddit.com/r/EscapefromTarkov/comments/1xicxsn/discussion_1300_patch_notes/), [bsg-1100-web](https://www.escapefromtarkov.com/news/id/404), [bsg-pve-bundle](https://www.escapefromtarkov.com/news/id/417), [bsg-exfil-brothers](https://www.escapefromtarkov.com/news/id/412), [steam-exfil-forum](https://steamcommunity.com/app/3932890/discussions/1/588439600674137457/), [wiki-controls](https://escapefromtarkov.fandom.com/wiki/Controls), [wiki-game-modes](https://escapefromtarkov.fandom.com/wiki/Game_modes), [wiki-tour](https://escapefromtarkov.fandom.com/wiki/Tour), [wiki-health](https://escapefromtarkov.fandom.com/wiki/Health_system), [wiki-fir](https://escapefromtarkov.fandom.com/wiki/Found_in_raid), [wiki-insurance](https://escapefromtarkov.fandom.com/wiki/Insurance), [wiki-scavs](https://escapefromtarkov.fandom.com/wiki/Scavs), [wiki-trading](https://escapefromtarkov.fandom.com/wiki/Trading), [forum-first-raid](https://forum.escapefromtarkov.com/topic/173846-love-the-game-but-completely-impossible-for-beginners/), [youtube-field-basic](https://www.youtube.com/watch?v=4vkwJAwVrIs), [youtube-first-raid-26](https://www.youtube.com/watch?v=l39IIf8z87g), [reddit-pve-start-26](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1xjjv08/new_to_tarkov_where_should_i_even_begin_discussion/), [reddit-tour-lab](https://www.reddit.com/r/EscapefromTarkov/comments/1qcwreh/new_player_tips_for_unlocking_labs_for_tour_quest/), [github-tracker-main](https://github.com/tarkovtracker-org/TarkovTracker), [tracker-home](https://tarkovtracker.org/), [bsg-kord-fin](https://x.com/tarkov/status/2120516987973513381).
- **Contrôle ciblé.** docs/veille-phase-3.md
- **Médias livrés.** 5 JPG et 0 MP3 originaux.

### Norvinsk : lore et chronologie

`pages/lore/index.html` · guide · **Publié le 2026-11-18**

- **Contenu.** TerraGroup, Contract Wars, USEC, BEAR, Scavs, protagonistes et liens avec les arcs du jeu. Distinguer canon, interprétations et révélations.
- **Interaction.** Fils temporels et volets de spoilers fermés par défaut.
- **JPG.** Ville de Tarkov au crépuscule ; Carte géopolitique originale de la région.
- **Sources de départ.** [bsg-lore](https://www.escapefromtarkov.com/news/id/98), [wiki-bear](https://escapefromtarkov.fandom.com/wiki/BEAR), [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [bsg-raid-fr](https://www.escapefromtarkov.com/news/id/141?lang=fr), [bsg-anniv](https://www.escapefromtarkov.com/news/id/418), [bsg-1-release](https://steamcommunity.com/games/3932890/announcements/detail/632320262484787939), [bsg-boreas-x](https://x.com/tarkov/status/2058806492518646020), [bsg-boreas-rec](https://x.com/tarkov/status/2060692704783372342), [ice-patch](https://steamcommunity.com/app/3932890/discussions/1/842880822501639244/), [wiki-conflict](https://escapefromtarkov.fandom.com/wiki/Tarkov_conflict), [wiki-norvinsk](https://escapefromtarkov.fandom.com/wiki/Norvinsk_region), [wiki-usec](https://escapefromtarkov.fandom.com/wiki/USEC), [wiki-terra](https://escapefromtarkov.fandom.com/wiki/TerraGroup), [wiki-scavs](https://escapefromtarkov.fandom.com/wiki/Scavs), [wiki-trading](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-chapters](https://escapefromtarkov.fandom.com/wiki/Story_chapters), [wiki-tour](https://escapefromtarkov.fandom.com/wiki/Tour), [wiki-ticket](https://escapefromtarkov.fandom.com/wiki/The_Ticket), [wiki-dogtags](https://escapefromtarkov.fandom.com/wiki/Dogtag), [forum-historic-synopsis](https://forum.escapefromtarkov.com/topic/9-synopsis-of-eft-story/), [forum-contract-wars](https://forum.escapefromtarkov.com/topic/31937-the-interview-with-nikita-buyanov/), [steam-hired-ops](https://store.steampowered.com/app/374280/Hired_Ops/), [x-chapters-2025](https://x.com/VeryBadSCAVR/status/1990401173023809970), [wiki-blue-fire](https://escapefromtarkov.fandom.com/wiki/Blue_Fire), [wiki-falling-skies](https://escapefromtarkov.fandom.com/wiki/Falling_Skies), [wiki-witness](https://escapefromtarkov.fandom.com/wiki/Accidental_Witness), [wiki-unheard-chapter](https://escapefromtarkov.fandom.com/wiki/The_Unheard), [imdb-raid](https://www.imdb.com/title/tt14366164/episodes/), [ign-story-chapters](https://www.ign.com/wikis/escape-from-tarkov/Story_Chapters).
- **Contrôle ciblé.** docs/veille-phase-3.md
- **Médias livrés.** 4 JPG et 0 MP3 originaux.


## Phase 4 — Cartes

### Atlas des cartes

`pages/maps/index.html` · hub · **Publié le 2026-11-18**

- **Contenu.** Treize lieux de référence ; variantes jour/nuit, niveau, tutoriel et événement regroupées sous leur carte ou dossier. Accès, profils, durée, difficulté et menaces.
- **Interaction.** Filtres, navigation par lieu, comparatif deux cartes et tableau équivalent.
- **JPG.** Panorama de Tarkov et de sa périphérie ; Vue portuaire ; Schéma du réseau de transits.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503), [bsg-1200](https://www.escapefromtarkov.com/news/id/411), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [wiki-controls](https://escapefromtarkov.fandom.com/wiki/Controls), [wiki-game-modes](https://escapefromtarkov.fandom.com/wiki/Game_modes), [wiki-changelog](https://escapefromtarkov.fandom.com/wiki/Changelog), [changelog-gg](https://changelog.gg/games/escape-from-tarkov-3932890), [github-goon-tracker](https://github.com/just5ky/goon-tracker), [twistedvoxel-halloween](https://twistedvoxel.com/escape-from-tarkov-technical-update/).
- **Médias livrés.** 16 JPG et 0 MP3 originaux.

### Factory

`pages/maps/factory.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Jour/nuit, sous-sols et passerelles, sorties avec et sans clé, Tagilla et variantes infectées.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Panorama de la halle industrielle ; Carte des niveaux ; Scène près des bureaux.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Factory](https://escapefromtarkov.fandom.com/fr/wiki/Factory), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [halloween-pr](https://www.gamespress.com/Escape-from-Tarkov-Celebrates-Halloween-Infected-Enemies-in-Raids-and-), [reddit-extracts](https://www.reddit.com/r/EscapefromTarkov/comments/1s7khcx/which_map_has_the_easiest_to_remember_extracts/), [twistedvoxel-halloween](https://twistedvoxel.com/escape-from-tarkov-technical-update/).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Factory », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 3 JPG et 0 MP3 originaux.

### Customs

`pages/maps/customs.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Dortoirs, Big Red, entrepôts et forteresse ; circuits de premières quêtes et nouveaux exfils du 1.2.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Vue du pont et de la douane ; Carte des accès et sorties révisés ; Arrivée aux dortoirs.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Customs](https://escapefromtarkov.fandom.com/fr/wiki/Customs), [bsg-1200](https://www.escapefromtarkov.com/news/id/411), [reddit-extracts](https://www.reddit.com/r/EscapefromTarkov/comments/1s7khcx/which_map_has_the_easiest_to_remember_extracts/).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Customs », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 3 JPG et 0 MP3 originaux.

### Woods

`pages/maps/woods.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Scierie et Shturman, limites du terrain, camps et repères naturels ; l’événement Wild Wild Woods séparé des règles normales.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Lac et scierie dans la brume ; Carte des lisières ; Ravitaillement près d’un camp.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Woods](https://escapefromtarkov.fandom.com/fr/wiki/Woods), [wild-wild](https://x.com/tarkov/status/2070176456668283361?lang=en), [wild-wild-end](https://x.com/tarkov/status/2072279163466047649), [reddit-extracts](https://www.reddit.com/r/EscapefromTarkov/comments/1s7khcx/which_map_has_the_easiest_to_remember_extracts/).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Woods », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Shoreline

`pages/maps/shoreline.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Resort, jetée, villages et Sanitar ; différences entre exfils, transits Icebreaker, Labyrinth et Terminal.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Resort Azure Coast ; Carte du littoral et des transits ; Arrivée à la jetée.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Shoreline](https://escapefromtarkov.fandom.com/fr/wiki/Shoreline), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [reddit-shoreline-keys](https://www.reddit.com/r/EscapefromTarkov/comments/1qxyulu/screenshot_help_me_decide_which_shoreline_keys_to/).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Shoreline », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 2 JPG et 0 MP3 originaux.

### Interchange

`pages/maps/interchange.html` · carte · **Publié le 2026-11-18**

- **Contenu.** ULTRA, IDEA/OLI/Goshan, niveaux et alimentation ; Killa, butin tech et corrections du 1.2.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Parking et façades d’ULTRA ; Carte des étages ; Couloir commercial sombre.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Interchange](https://escapefromtarkov.fandom.com/fr/wiki/Interchange), [bsg-1200](https://www.escapefromtarkov.com/news/id/411), [reddit-extracts](https://www.reddit.com/r/EscapefromTarkov/comments/1s7khcx/which_map_has_the_easiest_to_remember_extracts/).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Interchange », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 2 JPG et 0 MP3 originaux.

### Reserve

`pages/maps/reserve.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Bunkers, surface, train, leviers, Raiders et Glukhar ; contraintes des exfils et clés des bâtiments.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Base vue du dôme ; Carte surface/bunker ; Quais du train.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Reserve](https://escapefromtarkov.fandom.com/fr/wiki/Base_militaire), [full-speed](https://x.com/tarkov/status/2055322809224536409?lang=en).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Reserve », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### The Lab

`pages/maps/the-lab.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Accès par keycard, niveaux, alarmes, Raiders et extractions activées ; variantes Blackout et Infected en archives séparées.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Laboratoire TerraGroup éclairé ; Carte des étages et commandes ; Couloir du Lab dans l’obscurité.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [The_Lab](https://escapefromtarkov.fandom.com/fr/wiki/Le_labo), [halloween-pr](https://www.gamespress.com/Escape-from-Tarkov-Celebrates-Halloween-Infected-Enemies-in-Raids-and-), [wiki-events](https://escapefromtarkov.fandom.com/wiki/Events), [blackout-head](https://www.tarkovhead.com/en/event/blackout-1), [twistedvoxel-halloween](https://twistedvoxel.com/escape-from-tarkov-technical-update/).
- **Contrôle ciblé.** Ouvrir la fiche wiki « The Lab », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Lighthouse

`pages/maps/lighthouse.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Chalets, Rogues, BTR, Lightkeeper, transit Icebreaker et passages ; vérifier les zones de danger restantes hors Water Treatment.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Côte et phare ; Carte post-refonte avec chalets ; Arrivée près des voies du BTR.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Lighthouse](https://escapefromtarkov.fandom.com/fr/wiki/Phare), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [wiki-ice](https://escapefromtarkov.fandom.com/wiki/Icebreaker), [youtube-lighthouse-guide](https://m.youtube.com/watch?v=Et4TGFmYwmE), [reddit-lighthouse-loot](https://www.reddit.com/r/EscapefromTarkov/comments/x3uhku/lighthouse_guide/).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Lighthouse », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Streets of Tarkov

`pages/maps/streets-of-tarkov.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Concession, mall, entrées d’immeubles, BTR et signes d’extraction ; Kaban, Kollontay, trajets selon la quête.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Avenue post-industrielle ; Carte par quartiers ; Entrée de la concession.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Streets_of_Tarkov](https://escapefromtarkov.fandom.com/fr/wiki/Streets_of_Tarkov), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Streets of Tarkov », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Ground Zero

`pages/maps/ground-zero.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Départ, TerraGroup et premières tâches ; tutoriel, tranches de niveau et Cultists hors confusions de mode.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Place du centre d’affaires ; Carte tutoriel et variantes ; Entrée TerraGroup.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Ground_Zero](https://escapefromtarkov.fandom.com/fr/wiki/Ground_Zero), [wiki-start](https://escapefromtarkov.fandom.com/wiki/How_to_Play_Guide_for_Escape_from_Tarkov), [wiki-tour](https://escapefromtarkov.fandom.com/wiki/Tour), [reddit-extracts](https://www.reddit.com/r/EscapefromTarkov/comments/1s7khcx/which_map_has_the_easiest_to_remember_extracts/).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Ground Zero », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### The Labyrinth

`pages/maps/the-labyrinth.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Accès Shoreline, conditions d’entrée, phases et sorties ; Shadow of Tagilla, Vengeful Killa, aperçu sans spoiler.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Galerie souterraine ; Plan légendé des zones ; Porte et éclairage industriel.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [The_Labyrinth](https://escapefromtarkov.fandom.com/fr/wiki/The_Labyrinth), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503), [bsg-1200](https://www.escapefromtarkov.com/news/id/411).
- **Contrôle ciblé.** Ouvrir la fiche wiki « The Labyrinth », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Icebreaker

`pages/maps/icebreaker.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Boreas, transits, kit et accès direct ; étages du navire, Wedge, Knight, activités de groupe et sorties.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Brise-glace dans le golfe ; Carte multi-ponts ; Pont intérieur de la salle des machines.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Icebreaker](https://escapefromtarkov.fandom.com/fr/wiki/Icebreaker), [wiki-ice](https://escapefromtarkov.fandom.com/wiki/Icebreaker), [ice-patch](https://steamcommunity.com/app/3932890/discussions/1/842880822501639244/), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503), [bsg-1200](https://www.escapefromtarkov.com/news/id/411), [bsg-boreas-x](https://x.com/tarkov/status/2058806492518646020).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Icebreaker », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Terminal

`pages/maps/terminal.html` · carte · **Publié le 2026-11-18**

- **Contenu.** Port et fin de l’histoire, accès depuis Shoreline, variantes et conditions. Durée et sorties à recouper ; éviter de gâcher les fins.
- **Interaction.** Carte à couches (sorties, transits, quêtes, loot, rencontres), tableau filtrable par rôle et mode.
- **JPG.** Terminal portuaire ; Carte d’approche vérifiée ; Quai de conteneurs.
- **Sources de départ.** [wiki-maps](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov), [wiki-maps-fr](https://escapefromtarkov.fandom.com/fr/wiki/Map_of_Tarkov), [data-maps](https://json.tarkov.dev/regular/maps), [data-maps-fr](https://json.tarkov.dev/regular/maps_fr), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps), [mapgenie](https://mapgenie.io/tarkov), [kappa](https://kappaguide.com/), [Terminal](https://escapefromtarkov.fandom.com/fr/wiki/Terminal), [steam-news](https://steamcommunity.com/app/3932890/announcements/), [bsg-1200](https://www.escapefromtarkov.com/news/id/411), [wiki-ticket](https://escapefromtarkov.fandom.com/wiki/The_Ticket), [ign-terminal](https://www.ign.com/wikis/escape-from-tarkov/How_to_Unlock_Terminal), [ign-ticket](https://www.ign.com/wikis/escape-from-tarkov/The_Ticket_Walkthrough).
- **Contrôle ciblé.** Ouvrir la fiche wiki « Terminal », comparer avec la carte du client et vérifier les écarts de mode et de date.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.


## Phase 5 — Armes et munitions

### Arsenal EFT

`pages/weapons/index.html` · hub · **Publié le 2026-11-18**

- **Contenu.** Catalogue exhaustif au périmètre de l’instantané : familles, objets jouables, presets et variantes distincts. Builds conditionnés par munitions et mode.
- **Interaction.** Filtres calibre/famille/prix/trader/ergo/recul/cadence, comparateur jusqu’à trois entrées, rangs motivés.
- **JPG.** Établi modulaire ; Arsenal rangé par familles ; Détail d’une fiche équipement.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [data-items](https://json.tarkov.dev/regular/items), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons), [bsg-0146](https://www.ign.com/wikis/escape-from-tarkov/Escape_From_Tarkov_April_25_2024_Patch_Notes), [senseos-armure](https://senseos.gg/guides/escape-from-tarkov/how-armor-works/).
- **Contrôle ciblé.** Contrôler les armes cachées ou événementielles et les données des presets dans le client.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Fusils d’assaut et carabines

`pages/weapons/assault-rifles.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** Scinder les classes officielles rifle/carbine ; comparer M4, AK et alternatives pour différents accès.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** M4A1 sur établi ; Famille AK en atelier.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Pistolets-mitrailleurs (SMG)

`pages/weapons/smgs.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** Progression 9×19, 4,6×30 et 5,7×28 ; cadence, chargeur et disponibilité par profil.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** MP5 en vitrine ; MP7 en atelier.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Fusils à pompe et semi-automatiques

`pages/weapons/shotguns.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** Coût d’entrée, longueur, plombs vs slugs et projectiles multiples ; MP-133 et alternatives.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** MP-133 sur établi ; Pompe et semi-auto en râtelier.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Fusils de précision à verrou

`pages/weapons/sniper-rifles.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** Catalogue bolt-action, distance efficace en jeu, stabilité des presets, coût des optiques et quêtes liées.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** SV-98 en studio ; Optique dans un poste de tir virtuel.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Fusils de précision semi-auto (DMR)

`pages/weapons/dmrs.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** Effets de configuration sur SR-25, SVD et autres DMR ; distinguer cadence théorique et confort en jeu.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** SVD sur établi ; DMR en atelier optique.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Mitrailleuses légères et polyvalentes

`pages/weapons/lmgs.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** RPK, familles à bande et autres LMG ; poids, tailles de chargeur et contraintes propres au jeu.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** RPK dans une armurerie ; Détail de caisse d’équipement lourde.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Pistolets et revolvers

`pages/weapons/pistols.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** Regrouper visuellement sans confondre handgun et revolver ; tableaux des calibres, secours et quêtes.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** Pistolet Makarov dans un casier ; Revolver sur tapis de rangement.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Armes de mêlée

`pages/weapons/melee.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** Portée et dégâts de coups (pas de variables de munitions) ; drops, quêtes et usages en jeu.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** Baïonnette d’inventaire ; Outils de mêlée de boss en vitrine.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Lance-grenades et lanceurs spéciaux

`pages/weapons/grenade-launchers.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** Lanceurs autonomes, sous-canon et lance-roquettes annotés comme sous-familles distinctes ; profil et restriction en jeu.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** Lanceur de l’arsenal en studio ; Râtelier de matériel spécialisé.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Modifications et accessoires

`pages/weapons/weapon-mods.html` · famille-arme · **Publié le 2026-11-18**

- **Contenu.** Compatibilité de slots, pièces requises, crosse dépliée/repliée, présélection et mesures de build ; dépendances de pièces.
- **Interaction.** Tri, filtres adaptés, comparables homogènes et presets contextualisés.
- **JPG.** Composants d’un preset de jeu ; Schéma d’arborescence des slots.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [kappa](https://kappaguide.com/), [data-weapons](https://json.tarkov.dev/regular/weapons), [reddit-equilibrage](https://www.reddit.com/r/EscapefromTarkov/comments/1rm900v/new_weapon_part_rebalance_is_terrible_and_did_the/), [reddit-equilibrage-2](https://www.reddit.com/r/EscapefromTarkov/comments/1rlj08u/discussion_weapon_balancing_changes_are_bad/).
- **Contrôle ciblé.** Contrôler les catégories et les slots des armes phares, les offres par mode et les changements récents.
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Munitions : comprendre la balistique

`pages/ammo/index.html` · hub · **Publié le 2026-11-18**

- **Contenu.** Dégâts, pénétration, classes, perte de vitesse, tirs multiples et champs sans effet confirmé. Choix budget et disponibilité par calibre/mode.
- **Interaction.** Cartes par calibre, grille d’efficacité in-game et raccourcis vers le tableau complet ; rangs contextualisés.
- **JPG.** Macro de cartouches d’inventaire ; Infographie des dégâts en jeu ; Schéma de couverture de plaque.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [wiki-ballistics](https://escapefromtarkov.fandom.com/wiki/Ballistics), [wiki-ammo-sample](https://escapefromtarkov.fandom.com/wiki/.45_ACP_AP), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [bsg-0146](https://www.ign.com/wikis/escape-from-tarkov/Escape_From_Tarkov_April_25_2024_Patch_Notes), [bsg-0145](https://escapefromtarkov.fandom.com/wiki/Changelog), [bsg-0140](https://escapefromtarkov.fandom.com/wiki/Changelog), [senseos-armure](https://senseos.gg/guides/escape-from-tarkov/how-armor-works/), [senseos-munitions](https://senseos.gg/guides/escape-from-tarkov/ammo-stats-explained/), [leprestore-munitions](https://leprestore.com/guides/eft/escape-from-tarkov-ammo-tier-list/).
- **Médias livrés.** 1 JPG et 0 MP3 originaux.

### Tableau balistique interactif

`pages/ammo/ammo-chart.html` · outil · **Publié le 2026-11-18**

- **Contenu.** Séparer profils balistiques et autres munitions, indiquer unités, prix et horodatage, comparer munitions, offre trader et craft.
- **Interaction.** Recherche, tri stable, filtres, Chart.js et alternative tabulaire du nuage pénétration/dégâts.
- **JPG.** Séries de cartouches calibrées ; Infographie de lecture du nuage de points.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki-ballistics](https://escapefromtarkov.fandom.com/wiki/Ballistics), [wiki-ammo-sample](https://escapefromtarkov.fandom.com/wiki/.45_ACP_AP), [bsg-0146](https://www.ign.com/wikis/escape-from-tarkov/Escape_From_Tarkov_April_25_2024_Patch_Notes), [senseos-munitions](https://senseos.gg/guides/escape-from-tarkov/ammo-stats-explained/).
- **Médias livrés.** 1 JPG et 0 MP3 originaux.


## Phase 6 — Armures et boss

### Armures et protection

`pages/armor/index.html` · hub · **À venir**

- **Contenu.** Expliquer modèle de zones, classes, matériaux, durabilité et compatibilité de plaques.
- **Interaction.** Hub et fiches reliées ; filtres par slot et classe.
- **JPG.** Gilet et plaques à l’établi ; Schéma des zones couvertes.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki-ballistics](https://escapefromtarkov.fandom.com/wiki/Ballistics), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [armor-analysis-party](https://escapefromtarkov.party/en/gear/armor/), [armor-guide-onlyfarms](https://onlyfarms.gg/guides/escape-from-tarkov-best-armor-guide-2025-onlyfarms-edition/), [armor-tierlist-timesaver](https://timesaver.gg/blog/tarkov-armor-tier-list), [bsg-0140](https://escapefromtarkov.fandom.com/wiki/Changelog), [bsg-0146](https://www.ign.com/wikis/escape-from-tarkov/Escape_From_Tarkov_April_25_2024_Patch_Notes), [bsg-0150](https://escapefromtarkov.fandom.com/wiki/Changelog), [data-armor](https://json.tarkov.dev/regular/armor), [wiki-armor-equipment](https://escapefromtarkov.fandom.com/wiki/Equipment).
- **Contrôle ciblé.** Vérifier les emplacements de plaques, les unités de pénalité et les restrictions de mode.

### Gilets et porte-plaques

`pages/armor/body-armor.html` · guide · **À venir**

- **Contenu.** Séparer tissu, plaques et zones ; exemples légers/lourds et compromis de mobilité.
- **Interaction.** Filtres de classe, couverture et matériau.
- **JPG.** Porte-plaques ouvert ; Croquis des interfaces de plaque.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki-ballistics](https://escapefromtarkov.fandom.com/wiki/Ballistics), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [armor-analysis-party](https://escapefromtarkov.party/en/gear/armor/), [armor-ign-guide](https://www.ign.com/wikis/escape-from-tarkov/Best_Armor_Guide), [armor-reddit-body](https://www.reddit.com/r/EscapefromTarkov/comments/1saaylm/new_player_body_armor_question/), [armor-reddit-plates](https://www.reddit.com/r/EscapefromTarkov/comments/1rw5gi4/discussion_best_armor_materialplates/), [bsg-0140](https://escapefromtarkov.fandom.com/wiki/Changelog), [bsg-0146](https://www.ign.com/wikis/escape-from-tarkov/Escape_From_Tarkov_April_25_2024_Patch_Notes), [bsg-0150](https://escapefromtarkov.fandom.com/wiki/Changelog), [data-armor](https://json.tarkov.dev/regular/armor), [wiki-armor-equipment](https://escapefromtarkov.fandom.com/wiki/Equipment), [wiki-plate-carrier](https://escapefromtarkov.fandom.com/wiki/Crye_Precision_AVS_plate_carrier_(Ranger_Green)).
- **Contrôle ciblé.** Vérifier les emplacements de plaques, les unités de pénalité et les restrictions de mode.

### Casques et visières

`pages/armor/helmets.html` · guide · **À venir**

- **Contenu.** Coquilles, visières, protections d’oreilles, compatibilité de casque audio et ricochet en jeu.
- **Interaction.** Tableau par zone ; compatibilité inspectable.
- **JPG.** Casque et visière en studio ; Schéma de protection du profil.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki-ballistics](https://escapefromtarkov.fandom.com/wiki/Ballistics), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [armor-analysis-party](https://escapefromtarkov.party/en/gear/armor/), [armor-namu-equipment](https://en.namu.wiki/w/Escape%20from%20Tarkov/%EC%9E%A5%EB%B9%84), [armor-reddit-visor](https://www.reddit.com/r/EscapefromTarkov/comments/1jbmmdw/helmetfaceshield_options_without_horrible_blurry/), [armor-ricochet-note](https://note.com/smokesmokesmoker/n/n6ead539d151d), [bsg-0140](https://escapefromtarkov.fandom.com/wiki/Changelog), [bsg-0146](https://www.ign.com/wikis/escape-from-tarkov/Escape_From_Tarkov_April_25_2024_Patch_Notes), [bsg-0150](https://escapefromtarkov.fandom.com/wiki/Changelog), [data-armor](https://json.tarkov.dev/regular/armor), [wiki-armor-equipment](https://escapefromtarkov.fandom.com/wiki/Equipment).
- **Contrôle ciblé.** Vérifier les emplacements de plaques, les unités de pénalité et les restrictions de mode.

### Rigs et poches

`pages/armor/rigs.html` · guide · **À venir**

- **Contenu.** Rigs blindés ou non, capacité brute vs géométrie, coût, poids et place ; ne pas assimiler un rig à une classe de protection.
- **Interaction.** Comparaison des grilles, filtres armuré/non armuré.
- **JPG.** Rig chargé en planque ; Diagramme de rangements.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki-ballistics](https://escapefromtarkov.fandom.com/wiki/Ballistics), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [armor-analysis-party](https://escapefromtarkov.party/en/gear/armor/), [armor-guide-onlyfarms](https://onlyfarms.gg/guides/escape-from-tarkov-best-armor-guide-2025-onlyfarms-edition/), [armor-reddit-body](https://www.reddit.com/r/EscapefromTarkov/comments/1saaylm/new_player_body_armor_question/), [bsg-0140](https://escapefromtarkov.fandom.com/wiki/Changelog), [bsg-0146](https://www.ign.com/wikis/escape-from-tarkov/Escape_From_Tarkov_April_25_2024_Patch_Notes), [bsg-0150](https://escapefromtarkov.fandom.com/wiki/Changelog), [data-armor](https://json.tarkov.dev/regular/armor), [wiki-armor-equipment](https://escapefromtarkov.fandom.com/wiki/Equipment).
- **Contrôle ciblé.** Vérifier les emplacements de plaques, les unités de pénalité et les restrictions de mode.

### Comparateur d’armures

`pages/armor/armor-chart.html` · outil · **À venir**

- **Contenu.** Comparer valeurs à configuration cohérente ; afficher plaques, indices, pénalités et données manquantes.
- **Interaction.** Sélection 2–3 pièces, colonnes normalisées et info-bulles accessibles.
- **JPG.** Deux tenues défensives ; Schéma comparatif de couverture.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki-ballistics](https://escapefromtarkov.fandom.com/wiki/Ballistics), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [armor-analysis-party](https://escapefromtarkov.party/en/gear/armor/), [armor-guide-onlyfarms](https://onlyfarms.gg/guides/escape-from-tarkov-best-armor-guide-2025-onlyfarms-edition/), [armor-tierlist-timesaver](https://timesaver.gg/blog/tarkov-armor-tier-list), [bsg-0140](https://escapefromtarkov.fandom.com/wiki/Changelog), [bsg-0146](https://www.ign.com/wikis/escape-from-tarkov/Escape_From_Tarkov_April_25_2024_Patch_Notes), [bsg-0150](https://escapefromtarkov.fandom.com/wiki/Changelog), [data-armor](https://json.tarkov.dev/regular/armor), [wiki-armor-equipment](https://escapefromtarkov.fandom.com/wiki/Equipment).
- **Contrôle ciblé.** Vérifier les emplacements de plaques, les unités de pénalité et les restrictions de mode.

### Boss et rencontres

`pages/bosses/index.html` · hub · **À venir**

- **Contenu.** Profils majeurs, alternatives événementielles, groupes, gardes et distinction des Raiders/Rogues. Résumé des PV et apparitions sans agrégation trompeuse.
- **Interaction.** Grille de fiches, matrice cartes × boss, comparateur par mode et difficulté éditoriale.
- **JPG.** Reshala aux dortoirs ; Killa dans ULTRA ; Tagilla dans Factory ; The Goons dans les bois ; Black Division à Icebreaker.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-kord-nov](https://x.com/tarkov/status/2120935917351289274), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [blackout-head](https://www.tarkovhead.com/en/event/blackout-1), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-helper](https://github.com/nandosie012/Tarkov-Helper), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-tarkovkit](https://tarkovkit.com/en/guides/bosses), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).

### Reshala

`pages/bosses/reshala.html` · boss · **À venir**

- **Contenu.** Dortoirs, station et Stronghold ; gardes et intérêt du Golden TT.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Portrait aux dortoirs ; Accès à une cour de Customs.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-farming](https://www.reddit.com/r/EscapefromTarkov/comments/17gjtsc/boss_farming_tips/), [boss-tarkovkit](https://tarkovkit.com/en/guides/bosses), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Reshala, les entrées événementielles et les ajustements après le 29 octobre.

### Killa

`pages/bosses/killa.html` · boss · **À venir**

- **Contenu.** ULTRA et variantes ; casque Maska, loot, dissocier l’apparition de Vengeful Killa.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Portrait dans ULTRA ; Allée des commerces.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-farming](https://www.reddit.com/r/EscapefromTarkov/comments/17gjtsc/boss_farming_tips/), [boss-tarkovkit](https://tarkovkit.com/en/guides/bosses), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Killa, les entrées événementielles et les ajustements après le 29 octobre.

### Shturman

`pages/bosses/shturman.html` · boss · **À venir**

- **Contenu.** Scierie, deux gardes, cache dédiée et statut du Red Rebel.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Shturman près de la scierie ; Casiers de la zone boisée.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-reddit-shturman](https://www.reddit.com/r/EscapefromTarkov/comments/1kunjmg/shrturman_discussion/), [boss-reddit-shturman-pve](https://www.reddit.com/r/EscapeFromTarkov/comments/1pzcfmu/new_player_pve_player_easiest_way_to_kill_sturhman/), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Shturman, les entrées événementielles et les ajustements après le 29 octobre.

### Glukhar

`pages/bosses/glukhar.html` · boss · **À venir**

- **Contenu.** Reserve et variantes ; rôles des gardes et mobilité, taux par carte.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Portrait dans une cour militaire ; Couloir de Reserve.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-tarkovkit](https://tarkovkit.com/en/guides/bosses), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Glukhar, les entrées événementielles et les ajustements après le 29 octobre.

### Sanitar

`pages/bosses/sanitar.html` · boss · **À venir**

- **Contenu.** Resort, jetée et autres zones vérifiées ; comportement, soins et objets de quête.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Portrait médical au Resort ; Ponton de Shoreline.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Sanitar, les entrées événementielles et les ajustements après le 29 octobre.

### Tagilla

`pages/bosses/tagilla.html` · boss · **À venir**

- **Contenu.** Factory et variantes jour/nuit, poursuite en jeu, masques et forme infectée séparée.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Soudeur de Factory ; Passerelles de l’usine.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Tagilla, les entrées événementielles et les ajustements après le 29 octobre.

### Kaban

`pages/bosses/kaban.html` · boss · **À venir**

- **Contenu.** Concession, gardes et accès ; inventaire spécial, clés et dangers du secteur.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Kaban dans la concession ; Entrée du garage.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-kaban](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u9qca7/kaban_help_discussion/), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Kaban, les entrées événementielles et les ajustements après le 29 octobre.

### Kollontay

`pages/bosses/kollontay.html` · boss · **À venir**

- **Contenu.** Zones de Streets, équipiers, matraque et conditions de son effet en jeu.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Portrait de Kollontay ; Hall du quartier policier.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-tarkovkit](https://tarkovkit.com/en/guides/bosses), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Kollontay, les entrées événementielles et les ajustements après le 29 octobre.

### Zryachiy

`pages/bosses/zryachiy.html` · boss · **À venir**

- **Contenu.** Île, gardes et relation avec l’accès Lightkeeper ; séparer les variantes saisonnières.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Veilleur du phare ; Presqu’île dans la brume.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Zryachiy, les entrées événementielles et les ajustements après le 29 octobre.

### Partisan

`pages/bosses/partisan.html` · boss · **À venir**

- **Contenu.** Karma PMC et conditions d’apparition : appliquer le correctif 1.3.0.0 et dater les exceptions.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Portrait en lisière de forêt ; Sentier abandonné.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-farming](https://www.reddit.com/r/EscapefromTarkov/comments/17gjtsc/boss_farming_tips/), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Partisan, les entrées événementielles et les ajustements après le 29 octobre.

### Cultist Priest

`pages/bosses/cultist-priest.html` · boss · **À venir**

- **Contenu.** Nuit, classes de lieu et tranches de Ground Zero ; vocabulaire Sectant et distinction des événements.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Cultiste dans une lumière basse ; Abri nocturne sur la carte.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-github-tracker](https://github.com/sayser/TarkovTracker), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Cultist Priest, les entrées événementielles et les ajustements après le 29 octobre.

### The Goons

`pages/bosses/the-goons.html` · boss · **À venir**

- **Contenu.** Sous-fiches Knight, Big Pipe, Birdeye ; rotation selon mode, composition et faux doubles comptages.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** The Goons dans les bois ; Équipement de reconnaissance en jeu.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-tarkovkit](https://tarkovkit.com/en/guides/bosses), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche The Goons, les entrées événementielles et les ajustements après le 29 octobre.

### Shadow of Tagilla

`pages/bosses/shadow-of-tagilla.html` · boss · **À venir**

- **Contenu.** Labyrinth ; séquence de rencontre et apparition de Vengeful Killa si vérifiée.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Silhouette dans le Labyrinth ; Croisement des galeries.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [boss-gametree](https://gametree.me/blog/tarkov-bosses/), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-reddit-pve](https://www.reddit.com/r/EscapeFromTarkovPvE/comments/1u2ggcl/new_playertarkov_bosses/), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche Shadow of Tagilla, les entrées événementielles et les ajustements après le 29 octobre.

### The Wedge

`pages/bosses/the-wedge.html` · boss · **À venir**

- **Contenu.** Icebreaker, escortes par taille de groupe et variante de Blackout ; pas de taux universel.
- **Interaction.** Onglets mode/lieu, tableau de santé et loot, liens vers les cartes associées.
- **JPG.** Portrait Black Division à bord ; Salle de sport du brise-glace.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [wiki-bosses](https://escapefromtarkov.fandom.com/wiki/Bosses), [boss-analysis](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503), [ice-patch](https://steamcommunity.com/app/3932890/discussions/1/842880822501639244/), [blackout-head](https://www.tarkovhead.com/en/event/blackout-1), [boss-github-schema](https://github.com/the-hideout/tarkov-api/blob/main/schema-static.mjs), [boss-tarkovkit](https://tarkovkit.com/en/guides/bosses), [boss-timesaver](https://timesaver.gg/blog/eft-bosses-guide), [boss-tracking-lfcarry](https://lfcarry.com/guides/tarkov-bosses), [boss-tracking-senseos](https://senseos.gg/guides/escape-from-tarkov/boss-spawn-chances/), [data-maps-pve](https://json.tarkov.dev/pve/maps), [data-maps-season](https://json.tarkov.dev/pvp-season/maps).
- **Contrôle ciblé.** Vérifier la fiche The Wedge, les entrées événementielles et les ajustements après le 29 octobre.


## Phase 7 — Traders, quêtes et planque

### Les traders de Tarkov

`pages/traders/index.html` · hub · **À venir**

- **Contenu.** Dix profils, indices de réputation, nouvelles règles de fidélité, relations et inventaires clés.
- **Interaction.** Comparateur de loyauté, filtre par besoin et liens vers les quêtes.
- **JPG.** Bureau de négociation ; Étagères de stock et jetons.
- **Sources de départ.** [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [data-index](https://json.tarkov.dev/endpoints), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests).

### Prapor

`pages/traders/prapor.html` · trader · **À venir**

- **Contenu.** Armes, premiers objectifs, assurance et offres russes à plusieurs niveaux.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Bureau de Prapor ; Caisse de fournitures.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Prapor par mode avant publication.

### Therapist

`pages/traders/therapist.html` · trader · **À venir**

- **Contenu.** Soins, Salewa, matériel médical, achats prioritaires et options d’assurance.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Poste médical de Therapist ; Étagères de soins.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Therapist par mode avant publication.

### Skier

`pages/traders/skier.html` · trader · **À venir**

- **Contenu.** Premiers barters, quêtes d’accès, accessoires, et lien aux activités Halloween/Blackout.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Atelier de Skier ; Stock de pièces.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Skier par mode avant publication.

### Peacekeeper

`pages/traders/peacekeeper.html` · trader · **À venir**

- **Contenu.** Déblocage, USD, offres importées et paliers de quêtes.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Comptoir de Peacekeeper ; Pièces et accessoires dans casiers.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Peacekeeper par mode avant publication.

### Mechanic

`pages/traders/mechanic.html` · trader · **À venir**

- **Contenu.** Pièces, Gunsmith, déblocage de Jaeger, lien vers sorties d’atelier.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Établi de Mechanic ; Modules inspectés.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Mechanic par mode avant publication.

### Ragman

`pages/traders/ragman.html` · trader · **À venir**

- **Contenu.** Rigs, vêtements, armures, quêtes Interchange et accès au kit Icebreaker.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Boutique de Ragman ; Rigs sur portants.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Ragman par mode avant publication.

### Jaeger

`pages/traders/jaeger.html` · trader · **À venir**

- **Contenu.** Quêtes de survie et contraintes, équipement, assurance si attestée par mode.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Abri de Jaeger ; Casier de fournitures de Woods.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Jaeger par mode avant publication.

### Fence

`pages/traders/fence.html` · trader · **À venir**

- **Contenu.** Karma Scav, inventaire changeant, paliers réellement applicables et limites par événement.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Comptoir de Fence ; Marché secondaire nocturne.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Fence par mode avant publication.

### Lightkeeper

`pages/traders/lightkeeper.html` · trader · **À venir**

- **Contenu.** Accès en raid, chaîne To the Light post-refonte, échanges et restrictions de zone.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Intérieur du phare ; Approche de la presqu’île.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Lightkeeper par mode avant publication.

### Ref

`pages/traders/ref.html` · trader · **À venir**

- **Contenu.** Déblocage et échanges, quêtes croisées avec Arena, bilan des devises et conditions par mode.
- **Interaction.** Tableaux de paliers, quêtes liées et liens vers les items/échanges.
- **JPG.** Point d’échange de Ref ; Couloir d’Arena.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests), [arena](https://arena.tarkov.com/).
- **Contrôle ciblé.** Contrôler l’offre et la fiche Ref par mode avant publication.

### Catalogue des quêtes

`pages/quests/index.html` · hub · **À venir**

- **Contenu.** Objectifs, prérequis, récompenses, factions, missions principales/secondaires/opérationnelles et saisonnières séparées.
- **Interaction.** Recherche par nom bilingue, trader, mode ou carte et suivi local.
- **JPG.** Dossier de missions classées ; Kit de sortie d’un PMC.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [bsg-1060](https://www.escapefromtarkov.com/news/id/402?lang=en), [tracker](https://tarkovtracker.org/resources/tarkovdev).

### Arbre de progression des quêtes

`pages/quests/quest-tree.html` · outil · **À venir**

- **Contenu.** Relations d’ordre, conditions composites, prérequis d’histoire et objectifs de groupe ; audit des cycles et liens incomplets.
- **Interaction.** Vue du graphe et liste clavier ; filtres et états de progression exportables.
- **JPG.** Mur de briefing ; Schéma de lecture des prérequis.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [tracker](https://tarkovtracker.org/resources/tarkovdev).

### Obtenir le conteneur Kappa

`pages/quests/kappa-guide.html` · guide · **À venir**

- **Contenu.** Accès à Collector, liste d’objets FIR, tâches requises par version et conditions saisonnières ; éviter de recycler les anciennes exigences.
- **Interaction.** Checklist et progression persistante ; différences de mode.
- **JPG.** Conteneur sécurisé dans un stash ; Étagère d’objets Collector.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [kappa](https://kappaguide.com/), [wiki-quests](https://escapefromtarkov.fandom.com/wiki/Quests), [tracker](https://tarkovtracker.org/resources/tarkovdev).

### Planque : modules et progression

`pages/hideout/index.html` · hub · **À venir**

- **Contenu.** Stations, niveaux, conditions, matériaux, ordre de construction, consommation et coûts ; Bitcoin Farm et calculs par scénario.
- **Interaction.** Plan de modules, progression locale et vérification des dépendances.
- **JPG.** Planque avec établi et ventilations ; Station médicale ; Ferme Bitcoin.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [wiki-hideout](https://escapefromtarkov.fandom.com/wiki/Hideout), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [tracker](https://tarkovtracker.org/resources/tarkovdev).

### Crafts et temps de retour

`pages/hideout/crafting.html` · outil · **À venir**

- **Contenu.** Ingrédients vs outils, quantités de sortie, carburant, déverrouillages et calcul du net horaire.
- **Interaction.** Tableau recherchable ; calculateur de coût éditable, horodatage des sources et simulation transparente.
- **JPG.** Établi de craft ; Générateur dans la planque.
- **Sources de départ.** [data-index](https://json.tarkov.dev/endpoints), [wiki-hideout](https://escapefromtarkov.fandom.com/wiki/Hideout), [tarkov-market](https://tarkov-market.com/), [tracker](https://tarkovtracker.org/resources/tarkovdev).


## Phase 8 — Compétences, économie et stratégie

### Compétences : progresser par mode

`pages/skills/index.html` · guide · **À venir**

- **Contenu.** Familles, XP, maîtrise, effets, limites et rendement ; Metabolism et bonus Seasonal du 1.3.0.0 distingués.
- **Interaction.** Filtres par famille, tableaux chiffrés et comparaison PvE/PvP/Seasonal.
- **JPG.** Salle d’entraînement en planque ; Infographie de suivi des compétences.
- **Sources de départ.** [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [wiki-skills](https://escapefromtarkov.fandom.com/wiki/Character_skills).

### Économie du raid

`pages/economy/index.html` · hub · **À venir**

- **Contenu.** Flea vs traders, stratégies nettes après coût, devises et TarCoin de la boutique distinguées, renvoi aux routes et crafts.
- **Interaction.** Outil d’arbitrage vendable/à garder ; date de saisie et onglets par profil.
- **JPG.** Réserve de monnaies du jeu ; Dépôt de butin trié.
- **Sources de départ.** [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [bsg-tarcoin](https://www.escapefromtarkov.com/news/id/403), [data-items](https://json.tarkov.dev/regular/items), [tarkov-market](https://tarkov-market.com/), [kappa](https://kappaguide.com/).

### Flea Market : accès et frais

`pages/economy/flea-market.html` · outil · **À venir**

- **Contenu.** Niveaux d’accès et restrictions par profil/objet ; coût de transaction, prix observé, ruptures et limites de données.
- **Interaction.** Calculateur net manuel et tableau d’exemples paramétrables, sans flux inventé.
- **JPG.** Marché de revente dans Tarkov ; Illustration d’une comparaison comptable.
- **Sources de départ.** [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [data-index](https://json.tarkov.dev/endpoints), [data-items](https://json.tarkov.dev/regular/items), [tarkov-market](https://tarkov-market.com/), [wiki-traders](https://escapefromtarkov.fandom.com/wiki/Trading).

### Roubles : routes et rendement

`pages/economy/money-making.html` · guide · **À venir**

- **Contenu.** Routes de raid, liquidité, inventaire, revente par trader et butin prioritaire ; estimer en tenant compte des échecs.
- **Interaction.** Filtres par carte, temps, budget et niveau ; comparateur de rendement à hypothèses visibles.
- **JPG.** Casiers de collecte ; Matériaux de récupération stockés.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [data-items](https://json.tarkov.dev/regular/items), [kappa](https://kappaguide.com/), [tarkov-market](https://tarkov-market.com/).

### Stratégies et méta

`pages/strategy/index.html` · hub · **À venir**

- **Contenu.** Parcours apprenti/régulier/vétéran, objectifs PvP/PvE, budget contre fin de progression et choix du kit.
- **Interaction.** Parcours à facettes et raccourcis vers les dossiers.
- **JPG.** Salle de préparation de raid ; Sac et équipements sur banc.
- **Sources de départ.** [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [bsg-1200](https://www.escapefromtarkov.com/news/id/411), [data-items](https://json.tarkov.dev/regular/items), [wiki-start](https://escapefromtarkov.fandom.com/wiki/How_to_Play_Guide_for_Escape_from_Tarkov), [kappa](https://kappaguide.com/).

### 50+ astuces pour bien débuter

`pages/strategy/beginner-tips.html` · guide · **À venir**

- **Contenu.** Conseils triables : inventaire, assurance, exfils, santé, quêtes, Scav, progression et réglages.
- **Interaction.** Checklist par situation.
- **JPG.** Débutant en session de repérage ; Kit économique en planque.
- **Sources de départ.** [wiki-start](https://escapefromtarkov.fandom.com/wiki/How_to_Play_Guide_for_Escape_from_Tarkov), [youtube-start](https://www.youtube.com/watch?v=P5hyxI-cbb4), [bsg-1200](https://www.escapefromtarkov.com/news/id/411).
- **Contrôle ciblé.** Recouper les conseils communautaires datés et identifier les comportements dépendants du mode.

### Tactiques avancées de raid

`pages/strategy/advanced-tactics.html` · guide · **À venir**

- **Contenu.** Rythme, information, rotations, transits, gestion en groupe et analyse des erreurs propres à EFT.
- **Interaction.** Scénarios comparables et débriefs.
- **JPG.** Progression près d’un transit ; Équipe dans un couloir du jeu.
- **Sources de départ.** [data-maps](https://json.tarkov.dev/regular/maps), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503), [wiki-start](https://escapefromtarkov.fandom.com/wiki/How_to_Play_Guide_for_Escape_from_Tarkov).
- **Contrôle ciblé.** Recouper les conseils communautaires datés et identifier les comportements dépendants du mode.

### Guide PvP

`pages/strategy/pvp-guide.html` · guide · **À venir**

- **Contenu.** Progression permanente et Seasonal séparées ; engagement, audio, budget et erreur de lecture du terrain dans le jeu.
- **Interaction.** Choix de contexte par mode et carte.
- **JPG.** Scène d’observation dans Streets ; Entrée de zone d’extraction.
- **Sources de départ.** [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [bsg-1151](https://www.escapefromtarkov.com/news/id/409), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [reddit-eft](https://www.reddit.com/r/EscapefromTarkov/comments/1xicxsn/discussion_1300_patch_notes/).
- **Contrôle ciblé.** Recouper les conseils communautaires datés et identifier les comportements dépendants du mode.

### Guide PvE et Prestige

`pages/strategy/pve-guide.html` · guide · **À venir**

- **Contenu.** Bots, modes local/en ligne, coop et exigences actuelles des six niveaux ; décisions de reset et conservation.
- **Interaction.** Comparatif avant/après, checklist Prestige et avertissements.
- **JPG.** Route solo dans Ground Zero ; Planque avant un Prestige.
- **Sources de départ.** [bsg-1200](https://www.escapefromtarkov.com/news/id/411), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [data-index](https://json.tarkov.dev/endpoints).
- **Contrôle ciblé.** Recouper les conseils communautaires datés et identifier les comportements dépendants du mode.

### Builds méta et équivalents budget

`pages/strategy/meta-builds.html` · guide · **À venir**

- **Contenu.** Combinaisons de pièces documentées, disponibilité trader, coût, calibre et contraintes de la saison. Aucun rang « absolu ».
- **Interaction.** Choix du budget, stat de base/preset et substituts.
- **JPG.** Build budget en râtelier ; Preset haut de gamme sur établi.
- **Sources de départ.** [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [kappa](https://kappaguide.com/).
- **Contrôle ciblé.** Recouper les conseils communautaires datés et identifier les comportements dépendants du mode.


## Phase 9 — SP-Tushonka, Arena et événements

### Single Player Tushonka

`pages/spt-tushonka/index.html` · hub · **À venir**

- **Contenu.** Chronologie de l’ancien SPT, projet successeur, 4.1.6 stable vs paquet 5.0 expérimental, comparaison avec le PvE officiel.
- **Interaction.** Comparateur de modes et orientation vers quatre dossiers.
- **JPG.** Opérateur solitaire dans Tarkov ; Illustration du launcher distincte d’une capture ; Planque privée.
- **Sources de départ.** [spt-history](https://extraction-compass.com/en/blog/single-player-tarkov-is-back), [spt-history-2](https://massivelyop.com/2026/08/04/escape-from-tarkovs-fan-built-single-player-offline-version-ends-dev-following-trademark-complaint/), [spt-stable](https://github.com/SP-Tushonka/build/releases/tag/4.1.6), [spt-nuget](https://www.nuget.org/packages/SPTushonka.Server.Core/5.0.0-pre.202611061606), [spt-forge](https://sp-mod.com/), [reddit-tushonka](https://www.reddit.com/r/sptushonka/).
- **Contrôle ciblé.** Consulter les releases et la documentation des mainteneurs le jour de rédaction ; vérifier chaque version liée.

### Installer SP-Tushonka

`pages/spt-tushonka/installation.html` · guide · **À venir**

- **Contenu.** Prérequis de la version stable, copie légitime et isolée, installateur des mainteneurs, premier lancement et sauvegarde.
- **Interaction.** Checklist de préparation et procédure repliable par système si documentée.
- **JPG.** Écran de configuration vérifié ou recréé et étiqueté ; Diagramme des dossiers.
- **Sources de départ.** [spt-stable](https://github.com/SP-Tushonka/build/releases/tag/4.1.6), [spt-installer](https://sp-mod.com/installer), [spt-wiki](https://wiki.sp-tushonka.com/), [spt-releases](https://github.com/SP-Tushonka/build/releases).
- **Contrôle ciblé.** Consulter les releases et la documentation des mainteneurs le jour de rédaction ; vérifier chaque version liée.

### Mods SP-Tushonka

`pages/spt-tushonka/mods.html` · hub · **À venir**

- **Contenu.** Sélection IA, qualité de vie et progression avec versions Forge, dépendances, conflits et date de contrôle.
- **Interaction.** Filtres par version et catégorie ; fiche « vérifier avant d’installer ».
- **JPG.** Outils de paramétrage illustratifs ; Planche de métadonnées de mods.
- **Sources de départ.** [spt-forge](https://sp-mod.com/), [spt-stable](https://github.com/SP-Tushonka/build/releases/tag/4.1.6), [reddit-tushonka](https://www.reddit.com/r/sptushonka/).
- **Contrôle ciblé.** Consulter les releases et la documentation des mainteneurs le jour de rédaction ; vérifier chaque version liée.

### Coop privée avec Project Fika

`pages/spt-tushonka/fika.html` · guide · **À venir**

- **Contenu.** Versions client/serveur, parité des mods, préparation du groupe et test privé ; aucune confusion avec l’officiel ou le solo strict.
- **Interaction.** Checklist hôte/invité et matrice version par version.
- **JPG.** Deux opérateurs dans une planque ; Schéma de connexion d’un groupe privé.
- **Sources de départ.** [fika](https://sp-mod.com/mod/2326/project-fika), [spt-forge](https://sp-mod.com/), [spt-stable](https://github.com/SP-Tushonka/build/releases/tag/4.1.6), [spt-wiki](https://wiki.sp-tushonka.com/).
- **Contrôle ciblé.** Consulter les releases et la documentation des mainteneurs le jour de rédaction ; vérifier chaque version liée.

### Dépannage SP-Tushonka

`pages/spt-tushonka/troubleshooting.html` · guide · **À venir**

- **Contenu.** Boucle de démarrage, runtimes, erreurs de version et de mod, logs sans secrets, profil sauvegardé et retour au dernier état stable.
- **Interaction.** Diagnostic par symptôme et FAQ accessible.
- **JPG.** Terminal de diagnostic illustratif ; Schéma de sauvegarde de profil.
- **Sources de départ.** [spt-stable](https://github.com/SP-Tushonka/build/releases/tag/4.1.6), [spt-wiki](https://wiki.sp-tushonka.com/), [spt-releases](https://github.com/SP-Tushonka/build/releases), [reddit-tushonka](https://www.reddit.com/r/sptushonka/).
- **Contrôle ciblé.** Consulter les releases et la documentation des mainteneurs le jour de rédaction ; vérifier chaque version liée.

### Escape from Tarkov: Arena

`pages/arena/index.html` · guide · **À venir**

- **Contenu.** BlastGang, TeamFight, CheckPoint et autres modes attestés ; progression Ref, séparation de versions, mécaniques compétitives et tournois vérifiés.
- **Interaction.** Onglets par mode, profils d’équipement en jeu, calendrier sourcé.
- **JPG.** Vue d’une arène inspirée de Stadium ; Écran de préparation d’équipe.
- **Sources de départ.** [arena](https://arena.tarkov.com/), [bsg-1151](https://www.escapefromtarkov.com/news/id/409), [halloween-pr](https://www.gamespress.com/Escape-from-Tarkov-Celebrates-Halloween-Infected-Enemies-in-Raids-and-), [data-index](https://json.tarkov.dev/endpoints).

### Événements de 2026

`pages/events/index.html` · hub · **À venir**

- **Contenu.** Calendrier des activités, dates officielles et extensions, quêtes, récompenses, variantes de carte ; Halloween, Blackout, Icebreaker, Full Speed Ahead, Wild Wild Woods, Duckov et Tarkov City.
- **Interaction.** Timeline filtrable par jeu, saison, mode et statut ; liste de lecture sans script.
- **JPG.** Couloir infecté de Factory ; Brise-glace ; Ambiance de The Lab (Dark).
- **Sources de départ.** [bsg-news](https://www.escapefromtarkov.com/news?lang=en), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [halloween-pr](https://www.gamespress.com/Escape-from-Tarkov-Celebrates-Halloween-Infected-Enemies-in-Raids-and-), [bsg-halloween-drops](https://x.com/tarkov/status/2118720129999511853), [ice-drops](https://www.escapefromtarkov.com/news/id/394?lang=en), [full-speed](https://x.com/tarkov/status/2055322809224536409?lang=en), [full-speed-end](https://x.com/tarkov/status/2057115736712122446), [wild-wild](https://x.com/tarkov/status/2070176456668283361?lang=en), [wild-wild-end](https://x.com/tarkov/status/2072279163466047649), [bsg-city](https://www.escapefromtarkov.com/news/id/419), [data-season](https://json.tarkov.dev/pvp-season/season), [wiki-events](https://escapefromtarkov.fandom.com/wiki/Events), [blackout-x-extension](https://x.com/tarkov/status/2081715123064877461), [blackout-head](https://www.tarkovhead.com/en/event/blackout-1), [duckov](https://www.pcgamesn.com/escape-from-tarkov/update-escape-from-duckov-crossover).
- **Contrôle ciblé.** Vérifier les dates réelles de fin, Blackout et Duckov dans le journal officiel ; séparer l’événement des Drops.


## Phase 10 — Patchs, ressources et glossaire

### Notes de patch depuis la version 1.0

`pages/patch-notes.html` · outil · **À venir**

- **Contenu.** Chronologie officielle, changements par système et impact éditorial justifié ; ETS, équilibrages et roadmap séparés des mises en production.
- **Interaction.** Timeline par année/mode/type avec vue tableau et accès aux annonces originales.
- **JPG.** Archives de communications Tarkov ; Tableau technique dans une salle de briefing.
- **Sources de départ.** [bsg-news](https://www.escapefromtarkov.com/news?lang=en), [steam-news](https://steamcommunity.com/app/3932890/announcements/), [bsg-1300](https://www.escapefromtarkov.com/news/id/416), [bsg-1200](https://www.escapefromtarkov.com/news/id/411), [bsg-1151](https://www.escapefromtarkov.com/news/id/409), [bsg-1150](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503), [bsg-1100](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181), [bsg-1060](https://www.escapefromtarkov.com/news/id/402?lang=en), [ice-forum](https://forum.escapefromtarkov.com/topic/185040-%D0%BF%D0%B0%D1%82%D1%87-1050/), [bsg-ets-april](https://store.steampowered.com/news/app/3932890/view/672867776636912358), [patched](https://patched.gg/games/escape-from-tarkov).

### Ressources et outils

`pages/resources/index.html` · hub · **À venir**

- **Contenu.** Cartes, bases, marchés, trackers, YouTube, wiki, réseaux et Discord publics ; distinguer service officiel, outil tiers et contenu ancien.
- **Interaction.** Filtres par besoin, mode et langue. Liens vérifiés ; pas d’intégration de compte requise.
- **JPG.** Bureau de consultation de cartes ; Carnet d’archives de raid.
- **Sources de départ.** [bsg-news](https://www.escapefromtarkov.com/news?lang=en), [data-index](https://json.tarkov.dev/endpoints), [tarkov-dev](https://tarkov.dev/), [tracker](https://tarkovtracker.org/resources/tarkovdev), [mapgenie](https://mapgenie.io/tarkov), [tarkov-market](https://tarkov-market.com/), [tarkovhead](https://www.tarkovhead.com/), [kappa](https://kappaguide.com/), [patched](https://patched.gg/games/escape-from-tarkov), [reddit-eft](https://www.reddit.com/r/EscapefromTarkov/comments/1xicxsn/discussion_1300_patch_notes/), [spt-forge](https://sp-mod.com/), [arena](https://arena.tarkov.com/), [bsg-legal](https://www.escapefromtarkov.com/news/id/415).

### Glossaire EFT (FR / EN)

`pages/resources/glossary.html` · outil · **À venir**

- **Contenu.** Au moins 200 termes et sigles, définitions courtes et contextualisées ; aliases, jargon, items, synonymes FR/EN et renvois.
- **Interaction.** Index A–Z et filtre accent-insensible ; ancres partageables pour chaque définition.
- **JPG.** Dictionnaire tactique de briefing ; Fragments d’interface et abréviations.
- **Sources de départ.** [wiki-start](https://escapefromtarkov.fandom.com/wiki/How_to_Play_Guide_for_Escape_from_Tarkov), [wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki), [data-items](https://json.tarkov.dev/regular/items), [data-index](https://json.tarkov.dev/endpoints), [tracker](https://tarkovtracker.org/resources/tarkovdev).
