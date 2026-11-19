# Tarkov Ultimate Guide — Dossier d’initialisation

**Phase 0 · Vérifications du 18 novembre 2026 (UTC) · Prêt pour les fondations techniques**

Le périmètre est fixé à **86 pages HTML distinctes**, avec les sujets, les interactions, les illustrations et les pistes de recherche de chaque fiche. Les 12 cartes du brief sont conservées et **Terminal** rejoint l’atlas. À la clôture de cette phase, aucune page, image ou piste audio n’avait été publiée.

- [Plan détaillé des 86 pages](plan-des-pages.md) · [Manifeste des routes](pages.json)
- [Architecture, médias et critères de réception](architecture.md) · [Registre des sources](sources.json)
- [Workflow](../workflow.json) · [Machine à états](../state_machine.json) · [Contrôles de la phase 0](validation-phase-0.json)

> Relevé de fin de phase 0. La [veille de phase 1](veille-phase-1.md) complète les correctifs de novembre et la clôture de Kord Breach.

## Jeu live : ce qui est vérifié

| Sujet | Verdict au 18 novembre | Conséquence pour le guide |
| --- | --- | --- |
| Patch de référence | **1.3.0.0 — 29 octobre 2026**, dernière mise à jour numérotée trouvée dans [les actualités BSG](https://www.escapefromtarkov.com/news?lang=en) et le flux officiel Steam. | La [note BSG](https://www.escapefromtarkov.com/news/id/416) confirme l’événement Halloween, l’automne, le rework de Metabolism, la progression Seasonal accélérée, les bots PMC PvE plus difficiles et le correctif Partisan. Le flux est enregistré dans [`eft.json`](../recherche/versions/eft.json) ; il ne recouvre pas tous les hotfixes. |
| Unity 6 | **Annoncé** pour la mi-novembre avec **1.3.5.0** ; aucune publication confirmant son déploiement n’a été retrouvée dans les sources consultées. | Ne pas afficher « en ligne ». Les essais [ETS du 30 avril](https://store.steampowered.com/news/app/3932890/view/672867776636912358) ne sont pas une sortie live. |
| Novembre et Halloween | Le communiqué relayé par [Games Press](https://www.gamespress.com/Escape-from-Tarkov-Celebrates-Halloween-Infected-Enemies-in-Raids-and-) détaille Infected Lab et Infected Factory. BSG annonce le [12 novembre](https://x.com/tarkov/status/2120935917351289274) le retrait des **décorations** et un équilibrage Seasonal ; ce retrait ne suffit pas à dater la fin de toutes les activités Halloween. | Séparer mécanique, variantes et [Twitch Drops Halloween](https://x.com/tarkov/status/2118720129999511853). [Tarkov City Drops](https://www.escapefromtarkov.com/news/id/419) démarre le 16 novembre et annonce une fin le 23 novembre à 15 h UTC. C’est une campagne, pas un patch. |
| Kord Breach et fidélité | [1.1.0.0, 3 août](https://steamcommunity.com/games/3932890/announcements/detail/686386819418294181) : saison, Battle Pass, réforme des tâches et de la loyauté, frais de marché révisés. Les ligues hebdomadaires arrivent avec [1.1.5.1, 15 septembre](https://www.escapefromtarkov.com/news/id/409), pas au lancement de la saison. | Vérifier les paliers, déblocages et prix au niveau de chaque mode et objet ; ne pas recopier des tableaux de fidélité anciens. |
| Icebreaker | Ajouté avec **1.0.5.0 le 25 mai**, avant Kord Breach. Les [notes](https://steamcommunity.com/app/3932890/discussions/1/842880822501639244/) le décrivent comme une expédition contre l’IA, **1–3 joueurs de son groupe**, disponible dans tous les modes. Les [Drops](https://www.escapefromtarkov.com/news/id/394?lang=en) démarrent le 26 mai. | Ne pas confondre *rencontre PvE* et *réservé à PvE Zone*. Documenter **Boreas** et les conditions d’accès modifiées ensuite. |
| Lighthouse, Customs, Interchange | [1.1.5.0, 8 septembre](https://steamcommunity.com/games/3932890/announcements/detail/712285688032135503) : Rogues déplacés aux chalets, retrait des mines **au Water Treatment**, pas sur toute la carte ; BTR, passages et transit Icebreaker. [1.2.0.0, 6 octobre](https://www.escapefromtarkov.com/news/id/411) : Prestige PvE, EXFIL Brothers, changements aux bots, aux extractions et au loot. | Mettre en quarantaine les anciens plans. Une date ou une condition de sortie ne sera publiée qu’après recoupement. |
| Périmètre de l’atlas | Le [wiki](https://escapefromtarkov.fandom.com/wiki/Map_of_Tarkov) compte 13 lieux et confirme **Terminal**. Tarkov.dev remonte 19 entrées techniques : 13 lieux, trois variantes récurrentes (jour/nuit, niveau et tutoriel) et trois entrées événementielles. La durée de Terminal diffère entre le wiki et l’export. | Garder 13 fiches principales, traiter les variantes sous leurs parents ou en archives. Une entrée technique, un champ vide ou un taux brut n’atteste ni l’ouverture d’une carte ni la probabilité finale d’une rencontre. |

### Corrections à reporter dans la chronologie

- **Escape from Duckov** : lancement le **10 février**, recoupé entre le flux Steam pour le 1.0.2.0 et [PCGamesN](https://www.pcgamesn.com/escape-from-tarkov/update-escape-from-duckov-crossover) ; le 5 mars correspond à une autre note de patch (1.0.2.5). Le flux Steam date aussi 1.0.4.5 du **20 avril**, date de déploiement corroborée par [Forbes](https://www.forbes.com/sites/mikestubbs/2026/04/19/a-new-escape-from-tarkov-patch-arrives-tomorrow-downtime-expected/).
- **Full Speed Ahead** : [lancement le 15 mai](https://x.com/tarkov/status/2055322809224536409?lang=en), prolongation annoncée [jusqu’au 25 mai](https://x.com/tarkov/status/2057115736712122446). **Wild Wild Woods** : [25 juin](https://x.com/tarkov/status/2070176456668283361?lang=en), fin [le 1er juillet](https://x.com/tarkov/status/2072279163466047649), et non en mai.
- **Blackout** : départ le **14 juillet** recoupé sur le [wiki](https://escapefromtarkov.fandom.com/wiki/Events) et [TarkovHead](https://www.tarkovhead.com/en/event/blackout-1). La [prolongation officielle](https://x.com/tarkov/status/2081715123064877461) invalide la fin initiale du 27 juillet. Le 2 août est donné par TarkovHead ; une annonce primaire de clôture reste à retrouver avant de l’étiqueter « officielle ».
- **Expansions Hub** : préparé par le [1.0.6.0 du 3 juillet](https://www.escapefromtarkov.com/news/id/402?lang=en), présenté comme ouvert [le 8 juillet](https://www.escapefromtarkov.com/news/id/403). Le **TarCoin** est la devise de cette boutique, pas celle du Flea Market.

## Solo communautaire : deux canaux distincts

- **Version stable jouable : SP-Tushonka 4.1.6**, publiée le 18 septembre. La [release GitHub](https://github.com/SP-Tushonka/build/releases/tag/4.1.6) exige EFT `0.16.9.5.40743` et liste .NET Desktop Runtime et ASP.NET Core Runtime **10.0.9** pour l’installation Windows. Elle renvoie vers [l’installateur de The Forge](https://sp-mod.com/installer). **Cette version ne repose pas sur le patch live 1.3.0.0.**
- **Version expérimentale observée : `5.0.0-pre.202611061606`**, paquet [`SPTushonka.Server.Core` sur NuGet](https://www.nuget.org/packages/SPTushonka.Server.Core/5.0.0-pre.202611061606) daté du 6 novembre. Il ne s’agit pas d’une release jouable 5.0.0 confirmée sur le dépôt de builds. [Relevé des versions](../recherche/versions/sp-tushonka.json).
- La presse relate la décision de l’ancienne équipe de mettre fin à son projet sous cette forme et à son infrastructure d’ici au 12 août après une notification **de marque**, puis la continuité communautaire via [la nouvelle Forge](https://sp-mod.com/). À écrire en distinguant [décision de l’équipe et portée de la notification](https://extraction-compass.com/en/blog/single-player-tarkov-is-back), sans promettre que tous les mods sont compatibles. Project Fika est un mod séparé ; le PvE Zone officiel et Arena ont leurs propres sources et versions.

## Données téléchargées

L’ancienne route GraphQL `api.tarkov.dev/graphql` a retourné **HTTP 422** sur les sondes GET et POST. Les [exports JSON de Tarkov.dev](https://json.tarkov.dev/endpoints), recommandés dans la [documentation TarkovTracker](https://github.com/tarkovtracker-org/TarkovTracker/blob/main/docs/API.md), ont répondu et ont été importés. Les objets, statistiques et noms FR/EN proviennent de réponses distinctes pour **PvP Zone**, **PvE Zone** et **PvP Seasonal**.

| Par mode | Lignes capturées | Précision |
| --- | ---: | --- |
| Objets | 5 498 | Catalogue par identifiant, noms FR/EN, types, catégories et dimensions. Les sous-ensembles ci-dessous ne s’y ajoutent pas. |
| Armes, mêlée et presets | 172 armes à feu, 27 mêlée, 16 grenades lancées, 500 presets | Presets et armes de base séparés ; importer les filtres de compatibilité des slots en phase 5. |
| Munitions | 212 | 200 profils `ItemPropertiesAmmo`, 7 profils grenade, 5 sans profil. Pas de remplissage fictif des champs. |
| Protections et rigs | 390 | Collection élargie : gilets, rigs, équipements de tête, pièces/plaque et lunettes protectrices ; pas 390 gilets blindés. |
| Entrées cartographiques | 19 | Inventaire des durées, tailles de groupe et nombres d’entrées techniques, pas encore une carte annotée. |

L’[inventaire d’import](../recherche/tarkov-dev/manifest.json) fournit les URLs, dates HTTP `Date`/`Last-Modified`, ETag, empreintes SHA-256 et comptes. **Un fichier collecté le 18 novembre ne prouve pas que chaque entrée a été ajustée au 1.3.0.0.** Les observations de prix conservent leur propre horodatage et restent séparées par mode. Les sources ne donnent pas de numéro de build global attesté pour ces lots. Aucune image tierce, archive ni copie du jeu n’a été téléchargée dans le projet.

### Reproduire ou actualiser la collecte

Depuis `tarkov-ultimate-guide/`, avec Python 3.10+ et accès réseau :

```bash
python scripts/capture_tarkov.py
python scripts/verifier_versions.py
python scripts/planifier.py
```

La régénération vise les données disponibles au moment où elle est lancée. L’instantané de référence est celui déjà livré dans `recherche/`. Les répertoires `css/`, `js/`, `pages/`, `images/` et `audio/` sont prêts ; le contenu de production et les médias seront créés dans les phases correspondantes. Les liens externes pour Discord, YouTube et les guides communautaires seront revérifiés avant leur utilisation sur chaque fiche.

**Prochaine phase : Fondations techniques** — styles partagés, navigation et composants, moteur de recherche, animation accessible et premières ambiances MP3.
