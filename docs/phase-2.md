# Tarkov Ultimate Guide — Accueil et navigation

**Phase 2 · 18 novembre 2026 UTC**

L’aperçu du **Tarkov Ultimate Guide** ouvre maintenant l’accueil `index.html`. Le comparateur, le catalogue et les autres démonstrations de la phase 1 restent dans `/atelier/`, un espace technique non indexé. Ce lot ne publie pas encore les fiches débutant et lore.

## À essayer dans l’aperçu

| Où | Ce qui est disponible |
| :--- | :--- |
| **Encyclopédie** / **Menu** | Six aperçus illustrés : cartes et extractions, armes et munitions, armures et boss, quêtes et marchands, planque et économie, solo SP‑Tushonka. Le méga-menu et les cartes s’ouvrent au clavier ou au toucher. Les dossiers non rédigés portent « Dossier à venir » sans lien vers un fichier absent. |
| **Rechercher** ou `Ctrl+K` / `⌘+K` | Recherche tolérante aux accents et aux fautes, avec filtres par portée. Essaie `munitons` pour une fiche à venir, `premier raid` pour le brief et `comparateur` pour un outil réel. L’index distingue publication, repères d’accueil, atelier et fiches planifiées. |
| **Préparer mon premier raid** | Une checklist courte : choisir un mode et un objectif, repérer deux possibilités de sortie, noter ce qui a bloqué au débrief. L’état se conserve dans le navigateur et se réinitialise depuis la page. |
| **Modes** | PvP Zone, PvE Zone, Seasonal, Arena et SP‑Tushonka. Seuls les trois profils EFT comparables sont comptés dans l’export. Le contenu des cinq modes reste visible en l’absence de script. |
| **Radio**, dans la barre du haut | Sélectionne **Signal de Norvinsk**, puis **Écouter**. Cette introduction de 30 secondes ne boucle pas. Les quatre ambiances existantes sont aussi disponibles. Ni lecture ni requête MP3 au chargement. |
| **Veille** | Annonces datées avec leurs sources, séparées des versions techniques rapportées et des déploiements non vérifiés. |

## Compteurs et médias

| Mesure | Nouveau dans ce lot | Total au point d’arrêt |
| :--- | ---: | ---: |
| Pages éditoriales | 1 | **1 sur 86 prévues** |
| HTML de l’atelier | 0 | 1, hors décompte éditorial |
| Illustrations JPG originales | 8 | **12** |
| Audio MP3 original | 1 | **8** |

Le hero nocturne et les sept illustrations de dossiers ou du brief font **1 376 × 768 px**. Le hero de 151 Kio est prioritaire ; les autres images chargent au défilement. Les visuels ne sont pas des captures du jeu. **Signal de Norvinsk** : 30,04 s encodées, stéréo 44,1 kHz / 160 kbit/s. Le budget de cette réponse est respecté : 8 JPG et 1 MP3 créés.

Les **5 498 objets par profil** affichés correspondent à l’instantané communautaire Tarkov.dev du 18 novembre pour `regular`, `pve` et `pvp-season`. Ce chiffre n’est ni un total de pages ni une preuve de disponibilité en jeu. Le moteur contient **100 entrées** : 1 page publiée, 6 repères de l’accueil, 8 outils/sections de l’atelier et 85 fiches à venir sans URL.

## Veille retenue

- [Notes de BSG 1.3.0.0](https://www.escapefromtarkov.com/news/id/416) du 29 octobre : référence éditoriale. Le [wiki](https://escapefromtarkov.fandom.com/wiki/Changelog) signale **1.3.0.2.48779** le 13 novembre ; le client n’a pas été contrôlé. **Unity 6 / 1.3.5.0** reste annoncé, pas confirmé dans le relevé.
- [Tarkov City Drops](https://www.escapefromtarkov.com/news/id/419) : fin annoncée **23 novembre, 15 h UTC**. [Offre Standard + PvE Zone](https://www.escapefromtarkov.com/news/id/417) : jusqu’au **22 novembre** sur Steam. [Kord Breach](https://x.com/tarkov/status/2120516987973513381) : clôture annoncée le **7 décembre**. Aucun horaire n’est indiqué pour ces deux dernières échéances.
- L’article BSG et le fil Steam d’EXFIL Brothers ne formulent pas le même seuil de temps de jeu pour l’Opérateur. La page renvoie aux instructions officielles sans fixer de condition contradictoire.

[Journal de veille par canal](veille-phase-2.md) · [Registre des sources](sources.json) · [Recoupement Steam et SP‑Tushonka](../recherche/versions/recoupement-phase-2.json).

## Vérifications et reproduction

- [Contrôle statique](validation-phase-2-statique.json) : manifeste, ancres, sources, métadonnées, compteurs, empreintes et formats des médias. Le plan peut être régénéré sans perdre la publication et ses sources.
- [Contrôle de l’accueil](validation-phase-2-navigateur.json) : Chromium, largeurs **320 à 1 440 px**, clavier, tactile simulé, mouvement réduit, contraste renforcé, lecture et fin du thème, MP3 Range, portraits en chargement différé et repli sans JavaScript. Le parcours nominal n’a fait aucune requête externe automatique. Les résultats axe ne constituent pas une certification : les contrastes sur images et l’usage avec lecteur d’écran restent à vérifier au-delà des états testés.
- [Régression de l’atelier](validation-phase-2-atelier.json) : recherche, filtres, comparateur et sept sons de fondations contrôlés après le branchement de l’accueil. Les audits de la phase 1 demeurent historiques.

Depuis `tarkov-ultimate-guide/` :

```sh
python scripts/planifier.py
python scripts/rendre_accueil.py
python scripts/generer_socle.py
python scripts/servir.py --port 4173
```

Ouvrir `http://127.0.0.1:4173/` dans un navigateur. En local ou dans l’aperçu il n’y a pas de domaine de publication inventé. Avant un déploiement statique, définir `TUG_PUBLIC_URL` avec l’URL HTTPS réelle et régénérer l’accueil. Les dossiers de recherche et le suivi ne sont pas servis par l’aperçu.

Pour les contrôles au point d’arrêt (serveur lancé) :

```sh
python -m pip install Pillow mutagen==1.47.0
python scripts/valider_phase2.py --final

deps=$(mktemp -d)
npm install --prefix "$deps" playwright@1.56.1 axe-core@4.11.1
"$deps/node_modules/.bin/playwright" install chromium
NODE_PATH="$deps/node_modules" node scripts/verifier_accueil.cjs
NODE_PATH="$deps/node_modules" node scripts/verifier_atelier.cjs
```

Les outils de synthèse sont `scripts/generer_audio.py` (ambiances et sons UI) et `scripts/generer_introduction.py` (thème ; numpy, scipy et `lameenc==1.8.5`). Le catalogue garde les lots antérieurs ou ultérieurs.

**En attente de « CONTINUER ».** Prochain lot : guide débutant détaillé et lore de Norvinsk, avec les révélations isolées.
