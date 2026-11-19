# Phase 6 — Armures et boss

**Validée le 18 novembre 2026 UTC.** Vingt pages nouvelles, **50 pages éditoriales publiées sur 86**, plus l’atelier technique. L’armure et les boss entrent dans le méta-menu, dans la barre de commande et sur l’accueil, avec deux sauts de lecture vers le hub armures et le hub boss.

| Page | Contenu et interactions |
|---|---|
| **Armures et protection** — `pages/armor/index.html` | Les 390 pièces de l’export : le modèle de protection en quatre couches, les 8 matériaux et leurs usures, les 6 classes, le catalogue filtrable, les 38 plaques et leurs emplacements. |
| **Gilets et porte-plaques** — `pages/armor/body-armor.html` | 49 gilets pare-balles et 38 plaques : l’armure souple d’un côté, la plaque de l’autre, et la compatibilité d’emplacement comme donnée à part. |
| **Casques et visières** — `pages/armor/helmets.html` | 93 casques, 20 masques et 6 protections oculaires : zones couvertes, ricochet, surdité, blocage du casque audio et des lunettes. |
| **Rigs et poches** — `pages/armor/rigs.html` | 105 gilets tactiques : capacité de rangement, poids, prix de base, et la distinction entre porter et protéger. |
| **Comparateur d’armures** — `pages/armor/armor-chart.html` | Outil de comparaison : deux à trois pièces sur les mêmes seize lignes, catalogue filtrable, et signalement explicite des données manquantes. |
| **Boss et rencontres** — `pages/bosses/index.html` | Les 14 fiches, la matrice cartes × boss en profil Regular, les PV comparés, les 18 entrées d’export sans fiche et la section sur les écarts avec les suivis communautaires. |
| **Reshala** — `pages/bosses/reshala.html` | 752 PV, 0,60 sur Customs en Regular et 0,75 en PvE, plus le Terminal à 0,20. Une escorte, le portefeuille à 78,89 %. |
| **Killa** — `pages/bosses/killa.html` | 890 PV, aucune escorte, 228 objets de butin — le plus large inventaire du corpus — et le casque Maska édition Killa. |
| **Shturman** — `pages/bosses/shturman.html` | 812 PV, 657 objets de butin, la clé de cache à 100 % et la carte du champ de mines à 80,2 %. |
| **Glukhar** — `pages/bosses/glukhar.html` | 1 010 PV, trois escortes à rôles distincts, une chance stable à 0,60 sur Reserve dans les trois profils. |
| **Sanitar** — `pages/bosses/sanitar.html` | 1 270 PV, une escorte, le kit chirurgical et le kit Grizzly à 100 %. |
| **Tagilla** — `pages/bosses/tagilla.html` | 1 220 PV, aucune escorte, le masque de soudure Gorilla et 284 objets de butin. |
| **Kaban** — `pages/bosses/kaban.html` | 1 300 PV, quatre escortes, une chance à 0,60 sur le showroom de Streets. |
| **Kollontay** — `pages/bosses/kollontay.html` | 1 055 PV, deux escortes, et un butin réduit à deux objets dans l’export : l’écart est affiché, pas comblé. |
| **Zryachiy** — `pages/bosses/zryachiy.html` | 1 655 PV, le boss le plus résistant du corpus, une chance de 1 sur Lighthouse et un AK-50 en .50 BMG. |
| **Partisan** — `pages/bosses/partisan.html` | 950 PV, une apparition à 0,25 sur quatre cartes avec un délai de 900 secondes, 328 objets de butin. |
| **Cultist Priest** — `pages/bosses/cultist-priest.html` | 850 PV, une escorte, cinq cartes et des chances de 0,15 à 0,30, avec 15 apparitions relevées. |
| **The Goons** — `pages/bosses/the-goons.html` | Knight, Big Pipe et Birdeye : trois totaux de PV distincts, et une composition qui change sur Icebreaker. |
| **Shadow of Tagilla** — `pages/bosses/shadow-of-tagilla.html` | 1 305 PV, une chance de 1 sur le Labyrinth, le masque ZABEY et 285 objets de butin. |
| **The Wedge** — `pages/bosses/the-wedge.html` | 750 PV pour le chef, mais des renforts qui vont de zéro à deux selon la zone, et pas de taux universel. |

Chaque fiche de boss suit la même structure : repères de la rencontre, points de vie par membre, apparitions par profil, escortes, équipement porté, butin, avis de la communauté, sources et limites. Les tableaux sont rendus statiquement : sans JavaScript, ils restent complets et lisibles ; les filtres ne font que masquer des lignes.

## La règle éditoriale de la phase

Trois familles de valeurs cohabitent dans le guide et ne sont jamais fusionnées :

- **Les données.** Classes, matériaux, durabilités, poids, compatibilités, points de vie, chances, délais, zones, escortes, équipement et butin viennent de l’export communautaire du 18 novembre 2026, et sont datées à chaque tableau.
- **Les calculs reproductibles.** Les totaux de points de vie par zone, les parts relatives, les sommes de PV d’un groupe et les regroupements d’apparitions sont dérivés des données par des formules visibles, jamais posés comme des mesures du jeu.
- **Les avis communautaires.** Comportements observés, stratégies et suivis de taux sont présentés dans une section dédiée, attribués, datés et signalés comme opinions. Aucun taux communautaire n’est présenté comme une valeur de l’export, et l’écart entre les deux est expliqué.

La distinction la plus coûteuse à tenir est celle des apparitions : le profil PvE relève plusieurs chances à 0,75 sans modifier le profil Regular. Les fiches listent donc le profil de chaque ligne, et la matrice du hub n’utilise que Regular, en le disant.

## Médias et intégration

- **20 nouveaux JPG, 0 nouvel audio** : un établi de blindage, un porte-plaques ouvert, un casque en studio, un rig chargé, deux tenues défensives, un couloir de boss et un portrait par boss. Format 1376 × 768 px, fichiers JPEG uniquement. Visuels générés, jamais des captures d’écran ni des images officielles.
- Inventaire cumulé : **74 JPG, 8 MP3**.
- **119 entrées dans la recherche** : 50 pages publiées, 36 routes futures sans lien, 6 repères d’accueil, 8 d’atelier et 19 repères de dossiers.
- Les liens de la barre de commande, du méta-menu et de l’accueil pointent vers les routes publiées ; les routes futures restent sans lien.
- Les données sont publiées séparément : `js/data/armor.json` (390 pièces, 8 matériaux, 38 plaques) et `js/data/bosses.json` (14 fiches, 48 entrées d’export, 89 apparitions).

## Veille et portée

[Veille P6](veille-phase-6.md) · [Registre des sources](sources.json)

Les annonces de l’éditeur sont séparées des données communautaires et des retours de joueurs. Quatre points méritent d’être lus : le profil PvE élève plusieurs chances sans modifier Regular ; The Wedge n’a pas de taux universel et l’export le montre en décrivant douze zones et des renforts variables ; Tagilla, Tagilla infecté et Shadow of Tagilla sont trois entrées distinctes ; enfin, les points de vie d’un groupe ne s’additionnent pas en un total que le jeu calcule. Aucun classement communautaire n’est repris comme classement, et le guide affiche son instantané et sa provenance à chaque tableau.

## Vérifications

- **Statique** : 20 pages contrôlées, ancres et identifiants, légendes de tableaux, en-têtes de portée, JSON-LD et métadonnées cohérentes, correspondances avec `js/data/armor.json` (390 pièces, 8 matériaux, 38 plaques, 97 pièces à plaques) et `js/data/bosses.json` (14 fiches, 48 entrées, 18 hors fiche, 89 apparitions), absence de route fictive indexée et de format interdit. Les rendus sont reproductibles : `rendre_armures.py --check`, `rendre_armes.py --check`, `rendre_cartes.py --check`, `rendre_dossiers.py --check` et `rendre_accueil.py --check` passent.
- **Fragments** : `lint_fragments_armures.py` contrôle les 5 fragments éditoriaux, l’alignement du manifeste sur les 20 routes du plan, la présence d’une source de données et d’une source communautaire par fiche de boss, et au moins trois avis par fiche.
- **Navigateur** : Chromium, largeur 320 à 1440 px, clavier, sans JavaScript et avec stockage bloqué. Filtres du catalogue d’armure, comparateur à trois entrées, filtre de famille de boss, décodage des JPG après défilement, pas d’erreur console ni HTTP.
- **Correctifs apportés en cours de phase** : l’extraction d’équipement des boss ramenait toutes les protections et toutes les armes du mob sans distinction d’emplacement, ce qui comptait plusieurs fois le même emplacement ; elle retient désormais le premier objet de chaque emplacement et sépare protections, armes et sacs. Les apparitions de The Wedge apparaissaient en douze lignes quasi identiques sur Icebreaker ; elles sont regroupées par carte, chance et délai, chaque zone conservant ses renforts. Les types du butin étaient affichés en identifiants techniques anglais ; ils sont désormais traduits, l’identifiant restant disponible dans les données publiées.

Rapports : [statique](validation-phase-6-statique.json) · [navigateur](validation-phase-6-navigateur.json).

## Rejouer les contrôles

Depuis la racine du guide :

```sh
python scripts/planifier.py
python scripts/parser_armures.py
python scripts/publier_armures.py
python scripts/rendre_armures.py
python scripts/rendre_accueil.py
python scripts/generer_socle.py
python scripts/lint_fragments_armures.py
python scripts/valider_phase6.py --final
python scripts/servir.py --host 0.0.0.0 --port 4173
```

Dans un autre terminal, avec Pillow côté Python, Playwright et axe-core côté Node :

```sh
node scripts/verifier_armures.cjs
```
