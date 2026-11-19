# Veille de la phase 4 — Cartes

**Relevé du 18 novembre 2026 UTC.** Cette note accompagne les quatorze pages P4 : l’atlas et les treize fiches de lieu. Elle sépare les sources primaires, les sources secondaires et les retours communautaires, et elle signale les points qui restent contradictoires plutôt que de les arbitrer.

## Ce qui a été cherché, et où

| Périmètre | Source retenue | Type | Ce qu’on en tire |
|---|---|---|---|
| Annonces de l’éditeur | Notes 1.1.0.0 à 1.3.0.0, correctif 1.1.5.0 du 8 septembre 2026, mises à jour techniques de novembre 2026 | **Primaire** | Refontes du Phare, correctifs Halloween, version de jeu de référence |
| Fiches publiques par lieu | `escapefromtarkov.fandom.com`, version anglaise et version française, treize pages conservées dans `recherche/wiki-cartes/` | **Communautaire** | Lore, sorties, transits, clés, conditions d’entrée, boss |
| Données de jeu | `json.tarkov.dev` pour les trois profils (`regular`, `pve`, `pvp-season`), six charges utiles conservées dans `recherche/tarkov-dev/` | **Communautaire** | Durées, effectifs, niveaux, sorties, rencontres, dangers, variantes |
| Outils de lecture | MapGenie, Kappa Guide | **Outil externe** | Repères de lecture, jamais une source de chiffres |
| Aides de lecture et retours | Reddit (fils d’extractions, clés du Littoral, itinéraires du Phare), guides vidéo, guide des tricheurs Northern Lights | **Témoignage** | Ordres de grandeur et itinéraires, à ne pas traiter comme attesté |
| Correctifs non annoncés | Chronologie de correctifs de la communauté, agrégateur d’annonces | **Communautaire** | Version publiée, absence de note pour un correctif |

Les cinq familles de valeurs du guide — durées de raid, effectifs de PMC, délais d’activation des transits, conditions de sortie du Terminal, présence des rencontres — **ne sont pas confirmées par l’éditeur**. Ce sont des instantanés. Le guide les date à chaque fois.

## Trois décisions issues de la recherche

### 1. L’horaire d’entrée du Terminal : 22 h–04 h

Les deux versions de la fiche publique ne se recoupent pas : la version française décrit un accès « en solo » de 22 h à 4 h par le Littoral, la version anglaise un transit de 21 h à 6 h après présentation d’un objet d’accès au standard militaire du port.

Deux guides de campagne indépendants, plus récents que la version anglaise de la fiche, indiquent tous deux **22 h–04 h**. La fiche Terminal retient donc 22 h–04 h comme valeur probable, **sans la présenter comme attestée** : la vérification dans le client reste la référence, et l’écart entre les deux versions de la fiche est exposé tel quel.

La durée du raid, elle, reste réellement contradictoire : 50 minutes dans l’instantané des données de jeu, 45 minutes dans la fiche publique. Le guide retient 50 minutes comme valeur de travail et signale l’écart.

### 2. Les sources de jeu sont distinguées des sources publiques

Pour chaque sortie, deux listes coexistent et ne se recouvrent pas tout à fait : celle de la fiche publique (`sorties`, en français, avec conditions et notes) et celle de l’instantané de jeu (`sortiesJeu`, avec intitulés bruts et interrupteurs). Le guide les publie côte à côte et n’établit une correspondance que sur une **égalité stricte de libellé**. Les tableaux « Sorties documentées » et « Intitulés de jeu » donnent la liste brute ; la colonne « Correspondance » indique pour chaque ligne si elle est retrouvée dans la fiche publique ou absente de celle-ci.

C’est la seule façon de ne pas faire dire à une source ce qu’elle ne dit pas.

### 3. Le Phare après le correctif 1.1.5.0

Le correctif du 8 septembre 2026 a déplacé les Rogues vers les chalets, retiré les armes fixes et les mines de la station, ajouté la transition vers le Brise-glace, des caches de Rogue, une patrouille de BTR et des passages souterrains. La fiche Phare décrit cet état, sans reproduire la version antérieure.

## Ce qui a été écarté, et pourquoi

- **Positions de spawn.** Les zones disponibles sont des identifiants de zone issus des données, pas des repères de terrain. Aucune coordonnée n’est donnée comme point à viser.
- **Carte tactique de Tarkov.** Les fonds SVG de la communauté (`tarkov-dev-svg-maps`) sont sous licence CC BY-NC-SA 4.0 et non commerciale. Les atlas du guide sont donc des **planches originales** : le visuel est illustratif, la carte est reconstruite en tableaux de données, et le lecteur n’y trouve pas de tracé du blocus.
- **Pourcentages uniques hors contexte.** Les chances d’apparition sont celles de l’instantané consulté, à la date indiquée. Elles ne sont pas transformées en probabilité de raid tant qu’elles ne sont pas recoupées dans le client.
- **Itinéraires de butin « optimaux ».** Les retours de joueurs et les guides vidéo servent à comprendre la carte. Aucun chiffre de rentabilité n’est repris.

## Limites assumées

- Le client EFT **n’a pas été testé**. Rien dans ces pages n’atteste du comportement du jeu en direct.
- Les durées divergent parfois entre les sources : 20 à 50 minutes selon les lieux, et le Terminal cumule deux valeurs concurrentes.
- Les variantes d’événement (Usine infectée, Laboratoire infecté, Point zéro 21+, Point zéro Tutoriel) remplacent tout ou partie des rencontres habituelles : le tutoriel n’a **aucune sortie**.
- Les trois lieux sans transit sortant — Brise-glace, Labyrinthe et Terminal — et l’unique lieu à trois destinations — les Rues de Tarkov — contraignent la logique de rotation. Un transit n’est pas une sortie.
- Les rencontres peuvent apparaître à chaque sortie, y compris les Scav Raiders au Labo lorsque les sorties sont activées.

## Sources

Registre complet : [sources.json](sources.json) · Données conservées : [recherche/tarkov-dev/](../recherche/tarkov-dev/) · Fiches par lieu : [recherche/wiki-cartes/](../recherche/wiki-cartes/)

Bilan : [phase-4.md](phase-4.md) · Contrôles : [statique](validation-phase-4-statique.json) · [navigateur](validation-phase-4-navigateur.json) · [accueil](validation-phase-4-accueil.json)
