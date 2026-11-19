# Tarkov Ultimate Guide — Fondations techniques

**Phase 1 · 18 novembre 2026 UTC**

> Point d’arrêt historique. Depuis la phase 2, `/` présente l’accueil éditorial et l’atelier reste à `/atelier/`. Voir le [bilan actuel](phase-2.md).

L’aperçu **Tarkov Ultimate Guide — Atelier** ouvre le banc d’essai à `/atelier/`. Ce n’est pas l’accueil éditorial : `index.html` à la racine sera créé en phase 2. Il y a **86 routes éditoriales prévues, aucune publiée**, et **un HTML technique** distinct, exclu de l’indexation web.

## Tester l’atelier

| Outil | Ce que l’on peut vérifier |
|---|---|
| Recherche locale | `Ctrl+K` ou `⌘+K`, puis « quetes » ou « munitons ». Les 86 dossiers à venir s’affichent sans lien. Les huit sections testables mènent à des ancres réelles. Aucun chargement de l’index avant l’ouverture. |
| Modes | Utiliser les flèches, `Home` et `End` entre PvP Zone, PvE Zone, Seasonal, Arena et SP‑Tushonka. Les données comparables sont limitées aux trois profils EFT de Tarkov.dev. |
| Catalogue et comparaison | Combiner type et profil dans les filtres, ou ajouter **Icebreaker** en carte C. La table affiche durée, nombre d’entrées d’extract et nombre d’entrées de transit. Une entrée exportée n’est pas une sortie assurée en raid. Les différences sont signalées sans perdre les valeurs du tableau. |
| Composants | Infobulle survolable et fermable, dialogues avec restitution du focus, tier list éditoriale filtrable, accordéons natifs et navigation sticky. Le filtre du catalogue et le rang restent dans l’URL. |
| Audio | Choisir une piste, puis **Écouter**. On peut changer de piste, régler le volume, mettre en pause ou jouer un son UI sur action. Aucune lecture ni requête MP3 au chargement, même après avoir modifié ses préférences. |
| Affichage | La parallaxe et les particules s’arrêtent hors écran et en mode mouvement réduit. Une préférence manuelle et un contraste renforcé sont disponibles en pied de page. Le texte et la comparaison initiale restent lisibles sans JavaScript. |

## Médias et dépendances

- **4 illustrations JPG originales**, chacune en **1376 × 768**, de **169 à 288 Kio** : poste de briefing, kit sur établi, port de Norvinsk et poste radio sous la pluie. Image principale prioritaire, les autres différées. Visuels illustratifs, pas des captures officielles.
- **7 MP3 originaux**, stéréo **44,1 kHz / 160 kbit/s** : pluie, industrie, forêt et ville, quatre boucles de 60 s ; effleurement, clic métallique et signal radio. Les ambiances sont synthétisées sans échantillons externes, avec fondu au raccord. La durée réellement encodée des boucles est d’environ **60,029 s**, délai MP3 compris. Les thèmes d’introduction, d’extraction et de combat distant ne font pas partie de ce lot.
- Polices servies localement avec `font-display: swap` : Inter, Orbitron, Rajdhani, Share Tech Mono. Fuse.js **7.5.0** est importé avec l’index ; la lecture des ambiances utilise l’élément `audio` natif et Howler.js Core **2.2.4** pilote les sons UI, avec repli natif. [Licences, provenance et empreintes](dependances.json) · [Catalogue audio](../audio/catalogue.json).

## Veille éditoriale

**1.3.0.0** reste le patch de référence du guide. Le wiki rapporte le build technique **1.3.0.2.48779** au **13 novembre**, sans vérification directe dans le client. Le déploiement de **Unity 6 / 1.3.5.0** n’est pas confirmé par les sources consultées. BSG annonce la fin de **Kord Breach le 7 décembre 2026**, sans préciser l’heure. Les **Tarkov City Drops** se terminent selon BSG le **23 novembre à 15 h UTC**. L’atelier distingue ces annonces d’Arena **0.6.2.5** et du stable non officiel **SP‑Tushonka 4.1.6**.

[Veille préalable et limites par canal](veille-phase-1.md) · [Registre des sources](sources.json) · [Synthèse JSON](../recherche/versions/veille-2026-11-18.json).

## Validation et reproduction

- [Contrôle statique](validation-phase-1-statique.json) : ancres, chemins locaux, métadonnées, empreintes des dépendances, formats médias, contrastes de palette et distinction entre routes prévues et publiées.
- [Contrôle navigateur](validation-phase-1-navigateur.json) : Playwright sur Chromium, largeurs **320, 390, 768, 1024 et 1440 px**, tap sur mobile émulé, parcours clavier, réduction de mouvement, repli sans JavaScript et lecture des sept MP3. Aucun débordement de page ni erreur de console dans le parcours. Axe ne signale pas de violation automatique dans les états audités. Il laisse à l’examen humain notamment certains contrastes sur photographie et pseudocouches : ce contrôle n’est pas une certification WCAG ni un test exhaustif des lecteurs d’écran.
- `scripts/generer_socle.py` reproduit le même index et le même échantillon de cartes à partir du plan et des instantanés. L’aperçu ne sert pas le dossier de recherche.

Depuis le dossier `tarkov-ultimate-guide/` :

```sh
python scripts/servir.py --port 4173
# Puis ouvrir http://127.0.0.1:4173/atelier/
```

Pour rejouer les contrôles (avec le serveur lancé dans un autre terminal) :

```sh
python -m pip install Pillow mutagen==1.47.0
python scripts/generer_socle.py
python scripts/valider_phase1.py

deps=$(mktemp -d)
npm install --prefix "$deps" playwright@1.56.1 axe-core@4.11.1
"$deps/node_modules/.bin/playwright" install chromium
NODE_PATH="$deps/node_modules" node scripts/verifier_atelier.cjs
```

La synthèse des MP3 est reproductible via `scripts/generer_audio.py` avec `numpy`, `scipy` et `lameenc==1.8.5`. Le serveur de prévisualisation distribue les MP3 avec prise en charge de `Range`. Sur un hébergement statique, publier les dossiers d’assets à côté des HTML, sans serveur applicatif.

**Phase suivante :** accueil `index.html`, hero PMC nocturne sous la pluie, parcours thématiques, méga-menu et compteurs tirés des fiches effectivement publiées. L’atelier restera séparé.
