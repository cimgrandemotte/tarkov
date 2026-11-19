#!/usr/bin/env python3
"""Génère la page « Notes de patch depuis la version 1.0 » (PHASE_10).

La page résume la veille EFT actualisée : chronologie des versions,
équilibrage de fin de jeu (Black Division, The Wedge), refonte technique
(Unity 6) et astuces 2026. Le contenu éditorial vit dans
templates/patch-notes.html.part ; le gabarit est templates/dossier.html.tmpl.
"""
import argparse
import json
import os
import re
from html import escape
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = __import__('pathlib').Path(ROOT)


def text(value):
    return escape(str(value), quote=True)


def render(check=False):
    template = Template((ROOT / 'templates/dossier.html.tmpl').read_text(encoding='utf-8'))
    book = {d['route']: d for d in json.loads((ROOT / 'docs/pages.json').read_text(encoding='utf-8'))['pages']}
    sources = json.loads((ROOT / 'docs/sources.json').read_text(encoding='utf-8'))['sources']
    route = 'pages/patch-notes.html'
    page = book[route]
    rel_root = '../' * route.count('/')
    image = 'images/patch-notes/archives-communications-tarkov.jpg'
    assert (ROOT / image).is_file(), image

    src = set()

    def external(match):
        key = match[1]
        src.add(key)
        return text(sources[key]['url'])

    body = Template((ROOT / 'templates/patch-notes.html.part').read_text(encoding='utf-8')).substitute(root=rel_root)
    body = re.sub(r'@source:([a-z0-9-]+)@', external, body)
    if not src <= set(page['sourcesDeDepart']):
        raise ValueError(f"Sources non déclarées dans le manifeste pour {route}: {', '.join(sorted(src - set(page['sourcesDeDepart'])))}")

    slug = 'patch-notes'
    crumb = 'Notes de patch'
    description = ('Veille EFT au 18 novembre 2026 : chronologie des versions, équilibrage Black Division et '
                   'The Wedge, refonte Unity 6 et astuces 2026, avec liens vers les notes officielles.')
    hero_links = [('synthese', 'Situation'), ('chronologie', 'Chronologie'), ('astuces', 'Astuce 2026')]
    toc = [('synthese', 'Situation'), ('chronologie', 'Chronologie'), ('equilibrage', 'Équilibrage'),
           ('technique', 'Technique'), ('saison', 'Saisons'), ('astuces', 'Astuce 2026'), ('impact', 'Impact')]
    strip = [('18 nov 2026', 'Date de référence'), ('1.3.0.2', 'Version vive'), ('Unity 6', 'Moteur attendu')]

    links = ''.join(f'<a class="button {"button--primary" if i == 0 else "button--quiet"}" href="#{text(section)}" data-expand-target>{text(label)} <span class="button__arrow" aria-hidden="true">{"↓" if i == 0 else "↘"}</span></a>' for i, (section, label) in enumerate(hero_links))
    toc_html = ''.join(f'<li><a href="#{text(section)}" data-expand-target><span aria-hidden="true">{i:02d}</span>{text(label)}</a></li>' for i, (section, label) in enumerate(toc, 1))
    strip_html = ''.join(f'<div><dt>{text(label)}</dt><dd>{text(value)}</dd></div>' for value, label in strip)

    def nav(to, short=False):
        href = __import__('posixpath').relpath(to, __import__('posixpath').dirname(route))
        label = 'Guide' if to == 'pages/getting-started.html' else 'Lore'
        if short:
            style = ' class="commandbar__nav-link"'
        else:
            style = ''
        current = ' aria-current="page"' if to == route else ''
        return f'<a href="{text(href)}"{style}{current}>{text(label)}</a>'

    guide_entry = nav('pages/getting-started.html')
    lore_entry = nav('pages/lore/index.html')
    guide_nav = nav('pages/getting-started.html', True)
    lore_nav = nav('pages/lore/index.html', True)

    canonical = './' + route.split('/')[-1]
    shareimage = rel_root + image
    title = f"{page['titre']} — Tarkov Ultimate Guide"
    ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': page['titre'],
          'description': description, 'dateModified': '2026-11-18', 'inLanguage': 'fr-FR',
          'author': {'@type': 'Organization', 'name': 'Tarkov Ultimate Guide'}}
    structured = json.dumps(ld, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')

    values = {
        'slug': text(slug), 'description': text(description), 'image': text(image),
        'alt': text('Archives de communications et tableau de veille EFT'), 'crumb': text(crumb),
        'kicker': text('Veille'), 'headline': text('Les notes de patch depuis la version 1.0'),
        'headline_tail': text('chronologie, équilibrage et refonte technique'),
        'lead': text('Synthèse actualisée au 18 novembre 2026 des communications officielles et de la méta 2026.'),
        'scene': text("Une salle de briefing plongeante, où s'affichent les archives des versions."),
        'aside_note': text('Lecture éditoriale des annonces, pas une transcription intégrale des notes techniques.'),
        'title': text(title), 'canonical': text(canonical), 'shareimage': text(shareimage),
        'root': rel_root, 'article_label': text(page['titre']), 'structured': structured,
        'guide_entry': guide_entry, 'lore_entry': lore_entry, 'guide_nav': guide_nav, 'lore_nav': lore_nav,
        'hero_links': links, 'strip': strip_html, 'toc': toc_html, 'content': body.rstrip(),
    }
    out = template.substitute(values)
    target = ROOT / route
    if check:
        if not target.is_file() or target.read_text(encoding='utf-8') != out:
            raise SystemExit(f'Rejouer scripts/rendre_patch_notes.py : {route} diverge de son gabarit')
    else:
        stage = target.with_suffix('.html.tmp')
        stage.write_text(out, encoding='utf-8')
        stage.replace(target)
    print(f'{route} · {len(src)} références directes · description {len(description)} caractères')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--check', action='store_true', help='vérifier sans réécrire')
    render(cli.parse_args().check)
