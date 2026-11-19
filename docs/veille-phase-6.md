# Veille de la phase 6 — Armures et boss

**Relevé du 18 novembre 2026 UTC.** Cette note accompagne les vingt pages P6 : le hub armures, trois guides de protection, le comparateur, le hub boss et les quatorze fiches de boss. Elle sépare les sources primaires, les données communautaires et les retours de joueurs, et elle signale les points qui restent non déterminés plutôt que de les combler.

## Ce qui a été cherché, et où

| Périmètre | Source retenue | Type | Ce qu’on en tire |
|---|---|---|---|
| Modèle de protection | Notes de l’éditeur pour les correctifs 0.14.0.0, 0.14.5.0, 0.14.6.0 et 0.15.0.0 | **Primaire** | Zones d’armure, classes 1 à 6, durabilité effective = classe × 10, traversée garantie à +15, retrait de la classe 6 en magasin |
| Apparitions de boss | Notes 1.3.0.0 du 29 octobre 2026, notes 1.1.5.0 sur Lighthouse et Lightkeeper, correctif 1.0.5.0 sur Icebreaker et Boreas | **Primaire** | Dates des changements d’apparition, conditions événementielles, arrêt de la classe 6 en magasin |
| Données de jeu | `json.tarkov.dev`, trois profils (`regular`, `pve`, `pvp-season`), charges utiles conservées dans `recherche/tarkov-dev/` | **Communautaire** | 390 pièces d’armure, 8 matériaux, 38 plaques, 48 entrées de mobs, 89 apparitions, 19 cartes |
| Schéma des apparitions | `tarkov-api`, schéma GraphQL statique ; Tarkov Helper ; SayserTarkovTracker | **Technique** | Structure des champs : chance, emplacements, escortes, délais, déclencheurs |
| Fiches de boss | Wiki communautaire (versions EN et FR) | **Wiki communautaire** | Roster, factions, lieux, escortes, équipements ; le wiki se présente comme officiel et reste communautaire |
| Suivis d’apparition | SenseOS, LFCarry, TarkovGuide, TarkovKit, GameTree, Timesaver | **Suivi et avis communautaires** | Taux publiés, historique des changements, PV et escortes rapportés |
| Retours de joueurs | Reddit PvE (juin 2026 sur les boss, Kaban, Shturman), Reddit général (mai 2025, décembre 2025) | **Témoignage** | Comportements observés, stratégies,expérience de farm ; jamais une donnée |
| Armure | escapedfromtarkov.party, NamuWiki, Timesaver, OnlyFarms, IGN, NamuWiki FR | **Analyse et avis communautaires** | Classes, zones, ricochets, réparation, classements et conseils d’achat |

Les valeurs affichées dans les pages P6 — classe, matériau, destructibilité, usure, durée, zones, emplacements, compatibilités de plaques, points de vie, chances, délais, zones d’apparition, escortes, équipement porté, prevalence du butin — **ne sont pas confirmées par l’éditeur**. Ce sont des instantanés. Le guide les date à chaque fois.

## Quatre décisions issues de la recherche

### 1. Le profil PvE élève plusieurs chances sans modifier le profil Regular

La comparaison des trois profils montre que les apparitions ne sont pas identiques : le profil PvE relève à 0,75 plusieurs chances que le profil Regular laisse à 0,60 (Reshala, Killa, Shturman, Sanitar, Kaban, Kollontay), tandis que le profil Seasonal reste aligné sur Regular pour l’essentiel.

C’est la raison pour laquelle les pages P6 n’affichent jamais une colonne « chance » unique. Chaque fiche liste le profil, la carte, la chance, le délai de raid et les zones, et la matrice du hub n’utilise que le profil Regular, en signalant qu’il s’agit de ce profil-là. Fusionner les trois profils en une valeur unique aurait produit un taux qui n’existe dans aucun mode de jeu.

### 2. The Wedge n’a pas de taux universel, et l’export le montre

La lecture de l’export sur Icebreaker est instructive : The Wedge y est décrit **douze fois**, une fois par zone, avec un nombre de renforts différent selon la zone — aucun renfort dans certaines, un ou deux dans d’autres. Le profil PvE porte en plus une entrée à 0,33 sur la carte du laboratoire, là où Regular la porte à 0,33 et le profile Seasonal l’ignore.

Aucune de ces lignes ne se laisse réduire à « The Wedge apparaît avec un taux de X ». La fiche affiche donc la chance par carte et par profil, le détail des zones et le nombre de renforts associé à chacune. Le guide suit en cela les avis communautaires, qui décrivent eux aussi des escortes dépendant de la taille du groupe — mais il ne leur reprend aucun chiffre.

### 3. Tagilla, Tagilla infecté et Shadow of Tagilla sont trois entrées distinctes

L’export contient `bossTagilla` (1 220 PV), `infectedTagilla` (1 530 PV) et `bossTagillaAgro` (1 305 PV), qui est Shadow of Tagilla. Les confondre produirait un total faux et une probabilité d’apparition fausse.

La phase 6 leur consacre donc trois entrées distinctes : une fiche pour Tagilla, une fiche pour Shadow of Tagilla, et une ligne explicite dans la section « Les entrées sans fiche » du hub pour Tagilla infecté, qui n’a pas de fiche propre. La même règle vaut pour Killa : `bossKilla` a sa fiche, `bossKillaAgro` — Vengeful Killa — reste dans les entrées sans fiche. La correspondance est conservée dans `recherche/versions/armures-phase-6.json`.

### 4. Les points de vie d’un groupe ne s’additionnent pas en un total de jeu

The Goons illustrate le piège : Knight compte 1 120 PV, Big Pipe 910 et Birdeye 795. L’addition donne 2 825 points de vie, mais le jeu calcule trois mobs distincts, avec trois Armor, trois états et trois localisations de tir. Le hub donne les trois totaux et la somme, en signalant que la somme est un calcul du guide et non une mesure du jeu.

La même prudence vaut pour les escortes de Kaban (4), de Glukhar (3) et de Kollontay (2) : leurs points de vie sont affichés par zone, dans une section distincte de celle du boss principal.

## Ce qui a été écarté, et pourquoi

- **Classements communautaires de plaques et de casques.** Les tier lists de 2026 sont datées de façon hétérogène et reposent sur des configurations de raid que l’export ne décrit pas. Aucune n’est reprise comme classement. Le guide classe par critère mesurable : classe, matériau, destructibilité, usure de réparation, zones, poids, pénalités.
- **Les taux d’apparition publiés par les suivis.** SenseOS, LFCarry, TarkovGuide et GameTree publient des taux propres, qui divergent de l’export. Ils sont cités comme *suivis communautaires* et jamais fusionnés avec les valeurs de données. La section « Ce que disent les suivis » du hub explique pourquoi l’écart est normal : ce sont deux méthodes de mesure différentes, pas une erreur à corriger.
- **Les Pv de boss rapportés par les guides.** Les fiches communautaires donnent des PV souvent différents de l’export, parce qu’elles incluent parfois les escortes dans le total. Le guide s’en tient au mob principal et affiche les escortes à part.
- **Le wiki de la communauté comme source primaire.** Le wiki EFT se présente comme officiel et reste communautaire : il est classé comme source secondaire dans le registre, même pour le roster et les noms français.
- **Les traductions françaises des cartes.** `maps-fr.json` a été interrogé et ne fournit aucune traduction exploitable. Les noms français retenus pour les cartes viennent donc du lexicon éditorial du guide, pas de cet export.
- **Les effets de la matraque de Kollontay et le soin de Sanitar.** Décrits par les forums, absents des données : ils restent dans la section des avis, jamais dans les tableaux.
- **Les probabilités de franchissement d’une classe.** La règle de l’éditeur donne un seuil, pas une probabilité. La probabilité dépend de la munition, de l’armure, de son état et du canon : autant de données que l’export ne donne pas.

## Points qui restent non déterminés

- Les **prix de marché** de l’armure ne sont pas tous datés au 18 novembre 2026 : l’horodatage vient de l’export et varie selon les pièces. Les tableaux n’affichent que le prix de base, qui est stable.
- La **compatibilité réelle d’une plaque** dans une poche donnée n’est pas déductible de l’export : celui-ci donne les objets autorisés, pas la validation finale du client.
- La **composition variable de The Goons** sur Icebreaker (deux Rogue au lieu de Big Pipe et Birdeye) est une donnée, mais la règle qui la produit n’est pas documentée par l’éditeur.
- Les **tranches horaires** de Ground Zero pour le Cultist Priest ne figurent dans aucun champ de l’export : le guide ne les mentionne pas dans les tableaux.

## L’actualité du jeu au 18 novembre 2026

La veille de la phase 6 a vérifié l’état du jeu entre la dernière clôture éditoriale et l’export du 18 novembre 2026.

**Le correctif 1.0.4.0 du 26 mars 2026** (annoncé par Battlestate, repris par la presse et les forums) est antérieur à l’export, que les fiches P6 consomment. Ses effets sur le corpus P6 sont les suivants :

- **Armure.** Les zones de protection des gilets légers et des rigs blindés sont standardisées : ECLiPSE RBAV-AF perd la protection de l’aine, et les gilets Crye AVS et Stich Profi Plate Carrier V2 voient la protection de l’estomac transférée à l’aine, la protection du bas du dos supprimée. Les prix des gilets et des rigs sont réajustés, et les gilets lourds — 6B43 Zabralo-Sh, FORT Redut-M, FORT Redut-T5, IOTV Gen4 — subissent une réduction des pénalités et une augmentation de leur chance d’apparition. De nouvelles bartes à Ragman niveau 4 fidélité permettent d’obtenir ces gilets sans plaques.
- **Boss et cartes.** Les chances d’apparition de plusieurs boss sont réajustées (Killa sur Interchange, escortes de Reshala, détection nocturne de l’équipe Glukhar sur Reserve), la quantité de Raiders à The Lab augmente de 20 %, et la qualité du butin dans les salles fermées et marquées est augmentée. Les présets d’équipement de Kollontay sont corrigés.

**Statut de ces informations dans le guide.** Le correctif 1.0.4.0 est antérieur à l’export du 18 novembre 2026 : les valeurs P6 consomment l’export, qui devrait inclure ces changements. Les annonces de correctif sont des sources officielles ; les reprises par les médias et les forums sont des sources secondaires. Aucune valeur de ce correctif n’est fusionnée avec les chiffres de l’export : si l’export et les annonces divergent, l’export reste la référence des tableaux, et l’écart est signalé comme une différence de date de mesure.

## Sources

[Registre des sources](../docs/sources.json) — 228 entrées au 18 novembre 2026, dont 32 ajoutées ou complétées pour la phase 6. [Plan des pages](../docs/plan-des-pages.md) — 20 routes P6, sources de départ et contrôle ciblé de chacune.
