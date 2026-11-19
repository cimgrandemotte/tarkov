# Phase 5 — Armes et munitions

**Validée le 18 novembre 2026 UTC.** Treize pages nouvelles, **30 pages éditoriales publiées sur 86**, plus l’atelier technique. L’arsenal est dans le méta-menu et dans la barre de commande, avec un lien direct sur l’accueil ; le hub munitions et son tableau balistique s’enchaînent sur la même logique.

| Page | Contenu et interactions |
|---|---|
| **Arsenal EFT** — `pages/weapons/index.html` | Les 199 armes du catalogue en un seul tableau filtrable : recherche, famille, calibre, disponibilité en magasin, seuils d’ergonomie, de recul et de cadence. Comparateur à trois entrées sur treize indicateurs, quatre sélections guidées par les données, dix fiches de famille. |
| **Fusils d’assaut et carabines** — `pages/weapons/assault-rifles.html` | Soixante-trois armes, onze calibres, 174 presets, douze ventes en magasin. Le 5,56 et le 5,45 à eux seuls couvrent trente-deux armes de la famille. |
| **Pistolets-mitrailleurs** — `pages/weapons/smgs.html` | Vingt-trois armes, huit calibres, recul vertical de 42 à 89, cadence jusqu’à 1 100 coups par minute. Aucune vente en magasin : la contrainte de budget est traitée comme une donnée. |
| **Fusils à pompe** — `pages/weapons/shotguns.html` | Seize armes, quatre calibres, 13 en 12 gauges, distance efficace plafonnée à 100 mètres. Le coût du sac de plombs et le temps de rechargement sont explicités. |
| **Fusils de précision à verrou** — `pages/weapons/sniper-rifles.html` | Dix armes à verrou, distance efficace de 1 000 mètres, 31 presets. Le coût de l’optique est le premier poste du budget. |
| **Fusils de précision semi-auto** — `pages/weapons/dmrs.html` | Onze DMR, six calibres lourds, cadence jusqu’à 900 en semi-automatique, une seule vente en magasin (M1A). |
| **Mitrailleuses légères** — `pages/weapons/lmgs.html` | Huit armes de feu soutenu, recul vertical de 106 à 138, cadence de 550 à 700, poids jusqu’à 5,76 kilos. |
| **Pistolets et revolvers** — `pages/weapons/pistols.html` | Trente et une armes de poing, douze calibres, les seules exceptions automatiques (Glock 18C, Stechkin APS, APB) et les trois ventes en magasin. |
| **Armes de mêlée** — `pages/weapons/melee.html` | Vingt-sept armes, dégâts de taille et de pointe, rayon d’atteinte de 0,35 à 0,90 mètre, de la baïonnette à la labrys de 19 kilos. |
| **Lance-grenades et lanceurs** — `pages/weapons/grenade-launchers.html` | Dix armes classées en lanceurs par le jeu, dont huit fusées de détresse : le guide le dit plutôt que de faire croire à dix armes offensives. |
| **Modifications et accessoires** — `pages/weapons/weapon-mods.html` | Les 2 283 pièces classées par emplacement, poids et prix de base, avec la limite explicite : les compatibilités ne sont pas dans l’export. |
| **Munitions et balistique** — `pages/ammo/index.html` | La règle du correctif 0.14.6.0, chaque statistique expliquée, les six classes d’armure croisées avec les 200 cartouches, les 31 calibres, les 26 traçantes, les 7 grenades et les prix d’achat. |
| **Tableau balistique** — `pages/ammo/ammo-chart.html` | Les 200 cartouches filtrables et triables, et un nuage pénétration / dégâts rendu avec Chart.js, embarqué localement. |

Chaque fiche de famille suit la même structure : repères, catalogue, presets publiés, acquisition et disponibilité, conduite d’équipement, sources et limites. Les tableaux sont rendus statiquement : sans JavaScript, ils restent complets et lisibles ; les filtres ne font que masquer des lignes.

## Médias et intégration

- **13 nouveaux JPG, 0 nouvel audio** : un établi d’armement, un visuel par famille, un plat de composants de preset, une macro de cartouches et un alignement de calibres. 2 572 Ko au total, format 1376 × 768 px, fichiers JPEG uniquement. Visuels générés, jamais des captures d’écran ni des images officielles.
- Inventaire cumulé : **54 JPG, 8 MP3**. Aucun média audio n’est demandé par la phase 5.
- **119 entrées dans la recherche** : 30 pages publiées, 56 routes futures sans lien, 6 repères d’accueil, 8 d’atelier et 19 repères de dossiers.
- Les liens de la barre de commande, du méta-menu et de l’accueil pointent vers les routes publiées ; les routes futures restent sans lien.
- Les données sont publiées séparément : `js/data/weapons.json` (199 armes et 401 références de preset), `js/data/weapon-pieces.json` (2 283 pièces dans 23 emplacements) et `js/data/ammo.json` (200 cartouches, 31 calibres, 7 grenades).

## Veille et portée

[Veille P5](veille-phase-5.md) · [Registre des sources](sources.json)

Les annonces de l’éditeur sont séparées des données communautaires et des retours de joueurs. Trois points méritent d’être lus : le rééquilibrage ASh-12 / RPDN annoncé en mai 2026 concerne le module Arena — la PS12B reste à 46 de pénétration dans l’export du jeu principal ; les tables de munitions du joueur n’ont pas bougé depuis quatre correctifs, et celui du 12-13 novembre 2026 n’a touché que les munitions de l’IA ; enfin, le consensus communautaire sur le fait que la munition compte plus que l’arme recoupe l’éditorial du guide sans le fonder. Aucun classement communautaire n’est repris, et le guide affiche son instantané et sa provenance à chaque tableau.

## Vérifications

- **Statique** : 13 pages contrôlées, 40 références externes, 13 JPG avec empreinte et dimensions, ancres et identifiants, légendes de tableaux, en-têtes de portée, JSON-LD et métadonnées cohérentes, correspondances avec `js/data/weapons.json` (199 armes, 401 presets, 9 familles), `js/data/ammo.json` (200 cartouches, 31 calibres, 7 grenades) et `js/data/weapon-pieces.json` (2 283 pièces), absence de route fictive indexée et de format interdit. Les rendus sont reproductibles : `rendre_armes.py --check`, `rendre_cartes.py --check`, `rendre_dossiers.py --check` et `rendre_accueil.py --check` passent.
- **Navigateur** : Chromium, largeur 320 à 1440 px, clavier, sans JavaScript et avec stockage bloqué. Filtres du catalogue, comparateur à trois entrées, filtres du tableau balistique, nuage Chart.js rendu (200 points), décodage des JPG après défilement, pas d’erreur console ni HTTP. **0 violation axe** sur l’arsenal, une fiche de famille, la page balistique et le tableau.
- **Correctifs apportés en cours de phase** : la taxonomie plaçait d’abord toutes les armes en « fusil-assaut » ; le catalogage suit maintenant la catégorie du jeu, ce qui explique les cas singuliers du fusil MTs-255-12 et du lance-grenades M32A1 classés comme revolvers. Les armes de mêlée n’ont ni preset ni vente en magasin, et le validateur a été ajusté pour traiter ces deux tableaux volontairement vides. Le tableau d’acquisition a perdu sa colonne « tâche de déblocage » : l’export ne porte pas de donnée de tâche au niveau de l’arme, et la colonne aurait suggéré une information que les données ne contiennent pas.

Rapports : [statique](validation-phase-5-statique.json) · [navigateur](validation-phase-5-navigateur.json).

## Rejouer les contrôles

Depuis la racine du guide :

```sh
python scripts/planifier.py
python scripts/parser_armes.py
python scripts/publier_armes.py
python scripts/rendre_armes.py
python scripts/rendre_accueil.py
python scripts/generer_socle.py
python scripts/lint_fragments_armes.py
python scripts/servir.py --host 0.0.0.0 --port 4173
```

Dans un autre terminal, avec Pillow côté Python, Playwright et axe-core côté Node :

```sh
node scripts/verifier_armes.cjs
python scripts/valider_phase5.py --final
```

`TUG_URL` change la racine de test ; `TUG_CHROMIUM` accepte un chemin d’exécutable ou `sparticuz` avec `@sparticuz/chromium`. `TUG_TEST_REPORT` sauvegarde le rapport navigateur, `--out` le rapport statique. Les fichiers `templates/armes/*.html.part` sont des fragments, pas des routes.
