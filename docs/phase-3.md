# Phase 3 — Guide débutant et lore de Norvinsk

**Validée le 18 novembre 2026 UTC.** Deux pages nouvelles, **3 pages éditoriales publiées sur 86**, plus l’atelier technique. Ouvre l’aperçu du site : les entrées **Premiers pas** et **Norvinsk** sont dans le menu et sur l’accueil. La phase 4 n’a pas été lancée.

| Page | Contenu et interactions |
|---|---|
| **Premiers pas dans Tarkov** — `pages/getting-started.html` | Dix étapes, deux checklists distinctes enregistrées dans le navigateur, aide clavier QWERTY/AZERTY/personnalisée (12 actions) et **24 réponses**. Choix USEC/BEAR, profil PvP/PvE/Seasonal, Practice et Scav ; prologue *Tour*, équipement, HUD légendé, sept zones de santé, extractions, FiR, stash et Traders. |
| **Norvinsk : lore et chronologie** — `pages/lore/index.html` | Maquette géopolitique originale à quatre repères, TerraGroup, Contract Wars, USEC, BEAR, Scavs, protagonistes et chapitres. Deux fils interactifs (ordre relatif dans la fiction et dates de publication). Trois volets de révélations **fermés par défaut**, sans mémorisation ni indexation dans la recherche du site. |

## Médias et intégration

- **9 nouveaux JPG, 0 nouvel audio**. Cinq planches/illustrations du guide, quatre du lore, soit 1 468 232 octets au total. Sept JPG en 1376 × 768 px, deux panoramas en 1584 × 672 px. Visuels générés ; marqueurs, interface explicative et légendes en HTML/CSS, pas de PNG ou SVG. Aucun screenshot du client. Le relief ne donne ni coordonnées ni tracé du blocus.
- Inventaire cumulé : **21 JPG, 8 MP3**. L’image d’introduction de chaque dossier est prioritaire ; les autres sont différées. Aucun média audio n’est demandé par les deux dossiers.
- **115 entrées dans la recherche** : 3 pages publiées, 83 futures routes sans lien, 6 repères d’accueil, 8 d’atelier et 15 des deux dossiers. Les deux pages s’ouvrent depuis l’accueil, le méga-menu et les résultats. Les ancres déplacent le focus ; la recherche et Fuse ne se chargent qu’à l’ouverture du dialogue.

## Veille et portée

[Veille P3](veille-phase-3.md) · [Registre des sources](sources.json) · [Relevé structuré](../recherche/versions/recoupement-phase-3.json).

Les conseils de prise en main sont séparés des annonces de l’éditeur. Le document prend **1.3.0.0 pour référence des notes numérotées**, non pour attestation du build installé. Les seuils d’extraction ou d’éligibilité divergents ne sont pas transformés en règles du guide. Le client EFT n’a pas été testé. Dans le lore, le cadre de Battlestate est distingué des lectures communautaires et l’ajout d’un chapitre n’est pas daté comme événement fictif.

## Vérifications

- **Statique** : 167 références locales sur accueil et dossiers ; 21 sources externes sur le guide, 20 sur le lore, 13 sur l’accueil (certaines communes). Liens et fragments locaux, descriptions, fichiers, titres, inventaire et empreintes des JPG, absence de routes fictives indexées. Les deux rendus sont reproductibles.
- **Navigateur** : Chromium 141, largeur 320–1440 px, clavier (dont navigation d’onglets et recherche), tactile, sans JavaScript et avec stockage bloqué. Restauration et remise à zéro des checklists et du mémo, décodage des neuf JPG après défilement, volets fermés à la réouverture, pas d’erreur console/HTTP sur les parcours. **0 violation axe** sur huit états des dossiers d’après les contrôles déclenchés. Les superpositions sur photo ont été relues dans les captures ; l’audit n’est pas une certification et n’inclut pas une session sur lecteur d’écran matériel.
- **Régressions** : scénarios accueil (y compris radio et Range) et atelier rejoués. Dans l’aperçu local, le LCP mesuré sur les pages P3 a été de 280 et 376 ms lors du dernier audit ; ce n’est pas un résultat réseau de production.

Rapports : [statique](validation-phase-3-statique.json) · [dossiers](validation-phase-3-navigateur.json) · [accueil](validation-phase-3-accueil.json) · [atelier](validation-phase-3-atelier.json).

## Rejouer les contrôles

Depuis la racine du guide :

```sh
python scripts/planifier.py
python scripts/rendre_dossiers.py
python scripts/rendre_accueil.py
python scripts/generer_socle.py
python scripts/servir.py --host 0.0.0.0 --port 4173
```

Dans un autre terminal, avec Pillow et Mutagen côté Python, Playwright et axe-core côté Node :

```sh
node scripts/verifier_dossiers.cjs
node scripts/verifier_accueil.cjs
node scripts/verifier_atelier.cjs
python scripts/valider_phase3.py --final
```

`TUG_URL` change la racine de test ; `TUG_CHROMIUM` accepte un chemin d’exécutable ou `sparticuz` avec `@sparticuz/chromium`. `TUG_TEST_REPORT` sauvegarde le rapport navigateur, `TUG_VISUAL_DIR` les captures JPG hors inventaire, `--out` sauvegarde le rapport statique. Les fichiers `templates/dossiers/*.html.part` sont des fragments, pas des routes.

**Point d’arrêt : `ATTENTE_CONTINUE`.** Le prochain `CONTINUER` ouvre la **phase 4 — Cartes**, avec 14 pages prévues (l’atlas et 13 lieux). Le comparateur de l’atelier reste un échantillon, pas une publication de l’atlas.
