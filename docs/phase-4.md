# Phase 4 — Cartes

**Validée le 18 novembre 2026 UTC.** Quatorze pages nouvelles, **17 pages éditoriales publiées sur 86**, plus l’atelier technique. L’atlas et les treize fiches de lieu sont dans le menu et sur l’accueil : la vignette « Cartes & extractions » mène à l’atlas, et la rubrique « Lire le terrain » y ouvre directement. La phase 5 n’a pas été lancée.

| Page | Contenu et interactions |
|---|---|
| **Atlas des cartes** — `pages/maps/index.html` | Treize lieux en grille, recherche à facette, filtre par profil de jeu et par danger documenté, comparatif de deux lieux ligne à ligne, réseau des vingt-neuf transits, tableau des six variantes. |
| **Usine (Factory)** — `pages/maps/factory.html` | Trois niveaux, huit sorties documentées, Tagilla et les infectés, divergence entre les deux sources sur les rencontres. |
| **Douanes (Customs)** — `pages/maps/customs.html` | Seize sorties, dortoirs, Big Red, entrepôts, forteresse, nouveaux exfils du 1.2. |
| **Bois (Woods)** — `pages/maps/woods.html` | Lac central, scierie, Shturman, cultistes, limites du terrain, événement Wild Wild Woods séparé. |
| **Littoral (Shoreline)** — `pages/maps/shoreline.html` | Treize sorties, village, jetée, Sanitar, transits vers le Brise-glace, le Labyrinthe et le Terminal. |
| **Échange (Interchange)** — `pages/maps/interchange.html` | ULTRA, Idea, Oli, Goshan, Killa et Tagilla, sept sorties, corrections du 1.2. |
| **Réserve (Reserve)** — `pages/maps/reserve.html` | Onze sorties, bunkers, surface, train blindé, leviers, Raiders et Glukhar. |
| **Laboratoire (The Lab)** — `pages/maps/the-lab.html` | Accès par keycard, trois niveaux, alarmes, Scav Raiders, sorties activables, variantes Blackout et Infecté. |
| **Phare (Lighthouse)** — `pages/maps/lighthouse.html` | Chalets, Rogues déplacés, BTR, Lightkeeper, transition vers le Brise-glace, état après le correctif 1.1.5.0. |
| **Rues de Tarkov (Streets of Tarkov)** — `pages/maps/streets-of-tarkov.html` | Dix-sept sorties, concession, galerie marchande, BTR, Kaban, seul lieu à trois transits sortants. |
| **Point zéro (Ground Zero)** — `pages/maps/ground-zero.html` | Départ, TerraGroup, tutoriel, tranches de niveau, cultistes hors confusion de mode. |
| **Labyrinthe (The Labyrinth)** — `pages/maps/the-labyrinth.html` | Deux sorties, accès par le Littoral, phases, Shadow of Tagilla et Vengeful Killa. |
| **Brise-glace (Icebreaker)** — `pages/maps/icebreaker.html` | Une sortie, transits Littoral et Phare, accès direct après « Stick to It », assurance sans restitution, Boreas. |
| **Terminal** — `pages/maps/terminal.html` | Une sortie, le Zubr Boat, accès nocturne par le Littoral, durée contradictoire, sept rencontres, état du personnage restauré. |

Chaque fiche suit la même structure : repères et accès, sorties et transits, rencontres, dangers de terrain, clés et butin, conduite selon le profil, sources et limites. Deux couches de données sont commutables (sorties documentées, transits, intitulés de jeu) et les tableaux de sorties se filtrent par camp.

## Médias et intégration

- **20 nouveaux JPG, 0 nouvel audio** : un panorama par lieu, deux planches dans l’Usine et les Douanes, une planche de lac, deux planches d’atlas. 4 689 Ko au total, formats 1376 × 768 à 1600 × 672 px. Visuels générés, jamais des captures d’écran ni des cartes officielles ; le relief et les itinéraires sont reconstruits en tableaux de données et en HTML.
- Inventaire cumulé : **41 JPG, 8 MP3**. Aucun média audio n’est demandé par la phase 4.
- **119 entrées dans la recherche** : 17 pages publiées, 69 routes futures sans lien, 6 repères d’accueil, 8 d’atelier et 19 repères de dossiers. Les quatre ancres de l’atlas y entrent avec leur titre.
- Les liens de la barre de commande, du méga-menu et de l’accueil pointent vers les routes publiées ; les routes futures restent sans lien.

## Veille et portée

[Veille P4](veille-phase-4.md) · [Registre des sources](sources.json)

Les annonces de l’éditeur sont séparées des données communautaires et des retours de joueurs. L’accès au Terminal est donné comme **22 h–04 h probable** : deux guides de campagne indépendants concordent, mais les deux versions de la fiche publique divergent, et la durée du raid reste contradictoire (45 ou 50 minutes). Les sources de jeu et les fiches publiques donnent deux listes de sorties distinctes : elles sont publiées côte à côte, sans correspondance forcée. Aucun point de spawn n’est donné comme repère à viser, et le client n’a pas été testé.

## Vérifications

- **Statique** : 14 pages contrôlées, 40 références externes, 20 JPG avec empreinte et dimensions, ancres et identifiants, légendes de tableaux, en-têtes de portée, JSON-LD et métadonnées cohérentes, correspondances avec `js/data/maps.json` (119 sorties, 29 transits, 48 rencontres, 230 clés, 6 variantes), absence de route fictive indexée et de format interdit. Les deux rendus sont reproductibles : `rendre_cartes.py --check` et `rendre_accueil.py --check` passent.
- **Navigateur** : Chromium 141, largeur 320 à 1440 px, clavier, tactile, sans JavaScript et avec stockage bloqué. Filtres, comparatif, couches et tables focusables, 13 cartes accessibles sans script, décodage des JPG après défilement, pas d’erreur console ni HTTP. **0 violation axe** sur l’atlas et la fiche Usine ; l’accueil, l’atelier et les deux dossiers P3 ont été rejoués après la correction du chrome partagé et repassent également à 0 violation.
- **Correctifs apportés en cours de phase** : le chrome partagé accolait deux spans voisins dans le DOM, ce qui rendait le texte visible « TARKOVUltimate Guide » et « RechercherCtrl K » et violait WCAG 2.5.3 ; les quatre gabarits et l’atelier ont été corrigés, ce qui a bénéficié aux pages P2 et P3. Les sections des fiches ont reçu `tabindex="-1"` pour que les ancres du sommaire déplacent le focus, les conteneurs de tableaux à défilement sont devenus focusables et nommés, et les enfants de grille ont reçu `min-inline-size: 0` pour supprimer le débordement horizontal à 320 px.

Rapports : [statique](validation-phase-4-statique.json) · [navigateur](validation-phase-4-navigateur.json) · [accueil](validation-phase-4-accueil.json).

## Rejouer les contrôles

Depuis la racine du guide :

```sh
python scripts/planifier.py
python scripts/publier_cartes.py
python scripts/rendre_cartes.py
python scripts/rendre_dossiers.py
python scripts/rendre_accueil.py
python scripts/generer_socle.py
python scripts/lint_fragments.py
python scripts/servir.py --host 0.0.0.0 --port 4173
```

Dans un autre terminal, avec Pillow et Mutagen côté Python, Playwright et axe-core côté Node :

```sh
node scripts/verifier_cartes.cjs
node scripts/verifier_accueil.cjs
node scripts/verifier_dossiers.cjs
node scripts/verifier_atelier.cjs
python scripts/valider_phase4.py --final
```

`TUG_URL` change la racine de test ; `TUG_CHROMIUM` accepte un chemin d’exécutable ou `sparticuz` avec `@sparticuz/chromium`. `TUG_TEST_REPORT` sauvegarde le rapport navigateur, `TUG_VISUAL_DIR` les captures JPG hors inventaire, `--out` sauvegarde le rapport statique. Les fichiers `templates/cartes/*.html.part` sont des fragments, pas des routes.

**Point d’arrêt : `ATTENTE_CONTINUE`.** Le prochain `CONTINUER` ouvre la **phase 5 — Armes et munitions**, avec 13 pages prévues.
