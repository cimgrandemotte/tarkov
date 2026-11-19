# Veille de la phase 5 — Armes et munitions

**Relevé du 18 novembre 2026 UTC.** Cette note accompagne les treize pages P5 : le hub arsenal, dix fiches de famille, le hub balistique et le tableau balistique. Elle sépare les sources primaires, les données communautaires et les retours de joueurs, et elle signale les points qui restent non déterminés plutôt que de les combler.

## Ce qui a été cherché, et où

| Périmètre | Source retenue | Type | Ce qu’on en tire |
|---|---|---|---|
| Règle de pénétration | Notes de l’éditeur pour les correctifs 0.14.0.0, 0.14.5.0, 0.14.6.0 et 0.15.0.0 | **Primaire** | Durabilité effective = classe × 10, traversée garantie à +15, seuils de corps, retrait de la classe 6 en magasin |
| Correctifs récents | Notes 1.3.0.0 du 29 octobre 2026, mise à jour technique d’Arena de mai 2026, correctif du 12-13 novembre 2026 | **Primaire** | Compétences, munitions de l’IA, rééquilibrage ASh-12 / RPDN en Arena |
| Données de jeu | `json.tarkov.dev`, trois profils (`regular`, `pve`, `pvp-season`), charges utiles conservées dans `recherche/tarkov-dev/` | **Communautaire** | 199 armes, 2 314 objets de modification, 2 314 entrées de pièces, 200 cartouches, 16 marchands |
| Lecture des statistiques | `senseos.gg`, tableau de munitions relu le 26 octobre 2026 | **Communautaire** | 200 cartouches, 31 calibres, 180 balles, 13 plombs, 6 grenades, 1 flashbang |
| Outils de calcul | TarkovGunsmith, TarkovTools, tarkov-ballistics | **Outil communautaire** | Méthodes de calcul balistique, jamais une source de chiffres pour le guide |
| Retours de joueurs | Reddit (loadouts de début de partie de juin 2026, discussions d’équilibrage de 2026) | **Témoignage** | Consensus d’usage, jamais une donnée |
| Suivi des données | API Tarkov Changes, schéma GraphQL de tarkov-api | **Technique** | Structure des champs, absence d’horodatage par champ |

Les familles de valeurs du guide — ergonomie, recul, cadence, distance efficace, pénétration, dégâts, prix de marchand — **ne sont pas confirmées par l’éditeur**. Ce sont des instantanés. Le guide les date à chaque fois.

## Trois décisions issues de la recherche

### 1. Le rééquilibrage ASh-12 / RPDN ne concerne pas le jeu principal

La mise à jour technique d’Arena de mai 2026 annonce que la PS12B passe d’une pénétration de 46 à 45, avec des dégâts d’armure fortement réduits, et que l’ASh-12 comme le RPDN sont discutés.

Dans l’export du jeu principal relevé le 18 novembre 2026, la cartouche **12,7 x 55 mm PS12B est toujours à 46 de pénétration**, avec 102 points de dégâts et 57 de dégâts d’armure, soit une classe 4 atteinte. La PS12, elle, reste à 28 et la PS12A à 10.

Conclusion retenue : l announcement concerne le module Arena, dont l’économie et l’équilibre sont séparés du jeu principal. Le guide ne l’applique donc pas aux chiffres du catalogue, mais il signale cette limite : l’information : un lecteur qui joue en Arena ne lira pas les mêmes valeurs que dans le guide.

### 2. Les tableaux de munitions du joueur n’ont pas bougé depuis quatre correctifs

Le suivi communautaire du 16 novembre 2026 indique que les tables de pénétration et de dégâts des cartouches du joueur sont inchangées depuis les correctifs 1.1.0.0, 1.1.5.0, 1.2.0.0 et 1.3.0.0, et que le correctif du 12-13 novembre 2026 n’a touché que les munitions portées par l’IA de The Wedge et de ses gardes, dans tous les modes.

C’est cohérent avec l’export : les 200 cartouches relevées le 18 novembre 2026 se répartissent exactement comme la lecture du 26 octobre 2026 — 180 balles, 13 projectiles multiples, 6 projectiles explosifs, 1 flashbang, 31 calibres, et 17 cartouches en 12/70, le calibre le plus fourni.

Deux écarts avec les outils de la communauté méritent d’être notés : TarkovTools annonce 175 cartouches sur 29 calibres, relevées sur la table wiki au 8 octobre 2026. La différence ne vient pas d’un désaccord sur les valeurs, mais de la **provenance** : le guide s’appuie sur l’export du jeu, pas sur une table wiki recopiée. C’est la raison pour laquelle le guide affiche son instantané et sa source à chaque tableau.

### 3. Le consensus communautaire rejoint l’éditorial du guide, sans le fonder

Sur les fils Reddit de juin 2026 — « les meilleurs loadouts de début de partie achetables chez les marchands » — le point qui revient n’est pas le nom de l’arme, mais la munition : « ammo is more important than the gun ». Les conseils concrets qui reviennent sont les mêmes : un 5,45 x 39 peu cher et abondant, un 7,62 x 39 PS pour les fusils d’assaut, la loi de poids et de place en raid, et le rifle à verrou comme option de budget.

C’est exactement la ligne éditoriale retenue pour la phase 5 — « la munition décide avant l’arme » — mais elle ne vient pas de là : elle découle de la règle de pénétration de l’éditeur, et le guide la publication par les chiffres de l’export. Les retours de joueurs servent à vérifier que la lecture n’est pas contredite par l’usage, jamais à la fonder.

## Ce qui a été écarté, et pourquoi

- **Classements communautaires d’armes et de munitions.** Les tier lists, y compris celles de novembre 2026, sont datées de façon hétérogène et reposent sur des configurations de raid que l’export ne décrit pas. Aucune n’est reprise. Le guide classe par critère mesurable : ergonomie, recul, cadence, distance effective, pénétration, prix.
- **Pourcentages de probabilité de traversée.** La règle de l’éditeur donne un seuil, pas une probabilité. La classe affichée est une lecture dérivée (pénétration ÷ 10, plafonnée à 6) ; la probabilité de franchissement dépend de l’armure, de sa matière, de son état et du canon, autant de données que l’export ne donne pas.
- **Compatibilités pièce par pièce.** Le catalogue classe 2 283 pièces par emplacement, mais l’export ne dit pas à quelles armes elles s’appliquent. Le guide l’affiche, il ne l’invente pas.
- **Rapprochement par nom de preset.** 107 suffixes de nom de preset sur 401 correspondent à une pièce connue : le rapprochement textuel n’est pas fiable. Seuls les identifiants structurés ont servi.
- **Outils de calcul balistique en source.** TarkovGunsmith, TarkovTools et tarkov-ballistics sont cités comme méthodes de lecture ; aucun chiffre du guide ne vient d’eux.

## Limites assumées

- Le client EFT **n’a pas été testé**. Rien dans ces pages n’atteste du comportement du jeu en direct.
- L’export ne porte pas d’horodatage par champ : toutes les valeurs sont datées du 18 novembre 2026, sans granularité plus fine.
- 31 des 2 314 objets de modification restent sans emplacement reconnu ; ils ne sont pas publiés.
- 8 armes sur 172 à feu ne recoupent aucun preset par identifiant ; leurs presets ne sont donc pas comptés.
- La munition du lance-roquettes RShG-2 n’apparaît pas dans les 200 cartouches : le catalogue du guide ne peut rien dire de son comportement.
- Les prix de marché sont ceux de l’instantané ; ils servent à comparer des ordres de grandeur, pas à faire un budget de raid.

## Sources

Registre complet : [sources.json](sources.json) · Données conservées : [recherche/tarkov-dev/](../recherche/tarkov-dev/) · Scripts de production : [parser_armes.py](../scripts/parser_armes.py)

Bilan : [phase-5.md](phase-5.md) · Contrôles : [statique](validation-phase-5-statique.json) · [navigateur](validation-phase-5-navigateur.json)
