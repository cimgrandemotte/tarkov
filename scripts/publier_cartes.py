#!/usr/bin/env python3
"""Passe les 14 routes de la phase 4 à l'état PUBLIEE dans le manifeste des pages.

Le script ne fait qu'écrire l'état de publication et les médias réellement livrés :
les contenus restent produits par scripts/planifier.py, scripts/rendre_cartes.py
et les fragments éditoriaux. Il refuse de publier une route sans HTML sur disque
ou sans média déclaré.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFESTE = ROOT / 'docs/pages.json'
DATE = '2026-11-18'
PUBLISHED = {'PUBLIEE', 'PUBLIÉE'}
PHASE = 'PHASE_4'


def medias_livres(route):
    """Chemins d'images <img> referencees dans la page, resolus et normalises."""
    contenu = (ROOT / route).read_text(encoding='utf-8')
    page_dir = (ROOT / route).parent
    medias = []
    for m in re.finditer(r'src="([^"]+\.jpg)"', contenu):
        dest = (page_dir / m.group(1)).resolve()
        try:
            rel = dest.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        if (ROOT / rel).is_file():
            medias.append(rel)
    return sorted(set(medias))


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--retirer', action='store_true', help='remettre les routes de la phase 4 en PLANIFIEE')
    args = cli.parse_args()

    document = json.loads(MANIFESTE.read_text(encoding='utf-8'))
    pages = document['pages']
    cibles = [page for page in pages if page['phase'] == PHASE]
    if len(cibles) != 14:
        raise SystemExit(f'Attendu 14 routes de phase 4, trouvé {len(cibles)}')

    for page in cibles:
        route = page['route']
        if args.retirer:
            page['etat'] = 'PLANIFIEE'
            page.pop('dateDePublication', None)
            page.pop('mediasEffectifs', None)
            continue
        if not (ROOT / route).is_file():
            raise SystemExit(f'HTML absent, publication impossible : {route}')
        medias = medias_livres(route)
        if not medias:
            raise SystemExit(f'Aucun média livré pour {route}')
        page['etat'] = 'PUBLIEE'
        page['dateDePublication'] = DATE
        page['mediasEffectifs'] = medias
        page['audiosEffectifs'] = []

    publiees = sum(page['etat'] in PUBLISHED for page in pages)
    document['publiees'] = publiees
    document['etat'] = 'EN_PUBLICATION' if publiees else 'PLANIFIE'
    MANIFESTE.write_text(json.dumps(document, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    action = 'retirées de la publication' if args.retirer else 'publiées'
    print(f'{len(cibles)} routes de la phase 4 {action} · {publiees} / {len(pages)} routes publiées.')


if __name__ == '__main__':
    main()
