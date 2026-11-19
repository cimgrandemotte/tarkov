# Architecture et critères de réception

## Site statique, contenu lisible sans script

- Chaque entrée de `pages.json` deviendra un fichier HTML5 distinct. Un générateur léger réutilisera le gabarit pour les chemins relatifs, le menu, le fil d’Ariane, les médias, les sources et les métadonnées. Le résultat ne demandera ni backend ni framework en production.
- `css/` : variables, composants BEM, animations séparées, media queries et éventuelles surcharges par section. `js/` : modules vanilla, composants découplés, données de production par section dans `js/data/`. Les fichiers de `recherche/` ne sont pas servis par l’aperçu ; les dérivés publics sont générés avant déploiement.
- Dépendances locales, versionnées et créditées : Fuse.js pour la recherche accent-insensible, boucles MP3 natives et Howler.js Core pour les sons UI à la demande, Chart.js pour les nuages de points avec tableau équivalent. Cartes à couches consultables au clavier ou sous forme de listes ; Leaflet seulement s’il apporte une projection utile. Animations légères en CSS, `IntersectionObserver` et canvas décoratif ; désactivables, sans animation bloquante au chargement.
- Mode de jeu affiché sur les fiches chiffrées : PvP Zone (`regular`), PvE Zone (`pve`), PvP Seasonal (`pvp-season`). SPT et Arena sont des branches séparées, sans mélange de statistiques. Pas de prix ou de taux inventés. Une valeur source absente reste inconnue, même si l’UI peut illustrer le cas par un exemple explicitement simulé.
- Index de recherche dérivé du manifeste, noms FR/EN et synonymes. Les routes prévues ne sont jamais des liens ; seules les routes publiées et les ancres documentées de l’accueil, de l’atelier ou des dossiers publiés le sont. Navigation clavier (`Échap`, retour du focus, recherche avec résultats accessibles), URLs partageables pour filtres, `localStorage` facultatif pour les préférences et les checklists. Pas de compte requis.
- Fiches SEO : titre et description propres, Open Graph et Twitter Cards, JSON-LD correspondant au contenu (WebSite, Article, FAQ seulement si pertinente), sitemap et canonical absolus générés **uniquement** à partir de l’URL publique configurée.

## Direction artistique et médias

- Interface de briefing : noir profond, olive, kaki et ambre, titres Orbitron, intertitres Rajdhani, corps Inter, données Share Tech Mono. Polices locales avec licence et `font-display: swap`, fond grunge discret plutôt qu’un filtre sur le texte. `#555555` est réservé au décor, pas aux informations nécessaires.
- Idées d’images propres à chaque page dans `plan-des-pages.md`. La cible de publication est **au moins deux JPG pertinents par page**, trois pour les cartes ; vignettes et portraits peuvent resservir entre un hub et une fiche, mais un seul visuel dupliqué ne compte pas deux fois sur la même page. Des visuels originaux inspirés du jeu seront signalés comme illustratifs, jamais présentés comme des captures officielles.
- Carte tactique : schéma JPG original issu de lieux et de coordonnées vérifiés ; le dessin cinématique seul n’est pas une carte. Une couche interactive, quand les données le permettent, restera utilisable en liste. Pour toute carte ou capture tierce, contrôler droits et attribution avant diffusion ; préférer un lien externe si les droits sont incertains.
- JPG optimisés (point de départ : qualité 85, dimensions réservées, chargement différé sous la ligne de flottaison ; hero LCP prioritaire). Revue des cadrages mobile et desktop. Couper tout son au premier affichage ; ambiance MP3 volontaire, volume et arrêt clavier. Aucun son violent inattendu sur un survol ou une notification.
- Plus de dix créations uniques ne tiennent pas dans une réponse. Les phases à forte densité visuelle seront scindées en lots média au sein de la phase, avec inventaire et reprise via `CONTINUE` si nécessaire. Les pages incomplètes en médias ne sont pas labellisées publiées. Aucun lot ne dépassera dix JPG ou dix MP3 créés, aucune archive ZIP ni PDF.

## Règle de publication d’une page

1. Rechercher **avant rédaction** : source primaire si disponible, données et mode exacts, recoupement indépendant des points sensibles, puis lecture de la fiche précise et des versions pertinentes. Journaliser URL, périmètre, date, faits et écarts ; un lien repéré n’équivaut pas à une vérification.
2. Rédiger en français, conserver les noms du client et leurs variantes recherchables, indiquer le mode et le patch lorsqu’ils sont attestés. Distinguer la date de collecte, la date de publication et l’état « annoncé / déployé / archivé ». Les conseils éditoriaux, les tier lists et les estimations sont explicitement séparés des statistiques.
3. Valider données et références : ID et joins par mode, unités, valeurs manquantes, cas d’accès conditionnel, cellules comparables, sources des figures et crédits. Marquer une fermeture non prouvée « non confirmée », et non « encore en cours ».
4. Contrôler HTML sémantique, alt pertinents, skip-link et focus visible, contraste WCAG 2.1 AA, absence de dépendance exclusive à la couleur, navigation native clavier et lecteur d’écran, fonctionnement sans script, zoom et mouvement réduit. Tester à 320, 768, 1024 et 1440 px, vérifier liens et ancres, LCP et absence d’erreurs JS.
5. Livrer par lot : mettre à jour l’inventaire, le manifeste des pages publiées, les compteurs, le contrôle du budget média et les deux états JSON. Le site complet ne peut être déclaré `COMPLETE` qu’après les contrôles de phase 10.

## Accueil public et atelier de démonstration

`index.html` est l’entrée éditoriale. `atelier/index.html` reste un banc d’essai `noindex` avec son propre compteur et son module `js/workshop.mjs`. L’accueil utilise les composants partagés sans importer les données de comparaison de l’atelier. L’aperçu sert uniquement les dossiers publics ; `/` renvoie l’accueil, `/atelier/` reste disponible.

- Plan : `scripts/planifier.py` conserve le statut `PUBLIEE`, les données de publication, le relevé ciblé et les références existantes. Une route marquée publiée doit correspondre à un HTML sur disque.
- Rendu : `scripts/rendre_accueil.py` transforme `templates/accueil.html.tmpl` et `templates/dossiers-accueil.json` en HTML statique. Les compteurs lisent le manifeste et l’instantané de données. Aucun domaine fictif : `TUG_PUBLIC_URL=https://…/` permet de produire des liens de partage absolus pour un vrai hébergement HTTPS ; sans cette variable, l’aperçu utilise des chemins relatifs.
- Recherche : `scripts/generer_socle.py` dérive l’index depuis le manifeste et `js/data/sections-{accueil,atelier,dossiers}.json`. Fuse.js et l’index sont demandés seulement à l’ouverture du dialogue. Un fichier non publié n’obtient aucune URL dans les résultats. Les filtres de l’atelier et la checklist locale ne nécessitent pas de backend.
- Audio : la radio d’accueil réutilise les quatre ambiances de l’atelier et ajoute le thème d’introduction non bouclé. Le choix du thème n’écrase pas la préférence de piste de l’atelier. La sélection d’une piste en pause et le rechargement ne demandent aucun MP3.

[Bilan des fondations](phase-1.md) · [Accueil, validation et procédure](phase-2.md) · [Veille de l’accueil](veille-phase-2.md). Les relevés datés sont conservés en UTC et les données communautaires restent distinctes des notes de l’éditeur.

## Dossiers : premier raid et Norvinsk

- Rendu statique par `scripts/rendre_dossiers.py` : `templates/dossier.html.tmpl` (en-tête, navigation, fil d’Ariane, sommaire, recherche, balises de partage), paramètres dans `templates/dossiers-phase-3.json`, articles français dans `templates/dossiers/*.html.part`. Le générateur refuse une référence non déclarée dans le manifeste de la page. `TUG_PUBLIC_URL` suit la même convention que l’accueil.
- L’accueil et les dossiers partagent `css/site-chrome.css`. `css/pages/field-guide.css` gère la composition et les annotations sur JPG ; la piste complète et les légendes restent en HTML. `js/field-guide.mjs` ne gère que le mémo clavier local, le suivi du sommaire et la fermeture des révélations. Les composants d’onglets, recherche, persistance et menu sont réutilisés.
- Le Guide débutant et le Lore ont une URL réelle. La table géopolitique figure une région fictive : ce n’est pas une carte de navigation ou d’extraction. Le texte des révélations n’entre pas dans l’index ; l’indexation des repères s’appuie sur une liste rédigée, non sur l’aspiration aveugle de tout le HTML. Aucun état de révélation n’est stocké.
- Sans script, les légendes, les checklists natives (sans sauvegarde), les touches par défaut, les deux fils chronologiques et les volets restent disponibles. Les préférences d’interface ne modifient pas les réglages d’EFT.

[Bilan P3](phase-3.md) · [Veille ciblée et limites](veille-phase-3.md).
