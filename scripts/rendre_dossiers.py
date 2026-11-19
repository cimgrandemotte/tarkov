#!/usr/bin/env python3
"""Génère les dossiers de P3 en HTML statique à partir de leurs gabarits et du manifeste."""
import argparse
from html import escape
import json
import os
import posixpath
import re
from string import Template

from rendre_accueil import ROOT, load, public_base


def text(value):
    return escape(str(value), quote=True)


def render(check=False):
    template = Template((ROOT / 'templates/dossier.html.tmpl').read_text(encoding='utf-8'))
    book = {d['route']: d for d in load('docs/pages.json')['pages']}
    sources = load('docs/sources.json')['sources']
    dossiers = load('templates/dossiers-phase-3.json')
    base = public_base(os.getenv('TUG_PUBLIC_URL', ''))
    assert {item['route'] for item in dossiers} == {r for r, page in book.items() if page['phase'] == 'PHASE_3'}
    for item in dossiers:
        route = item['route']
        rel_root = '../' * route.count('/')
        page = book[route]
        image = item['image']
        assert (ROOT / image).is_file()
        assert 145 <= len(item['description']) <= 165, item['slug']
        src = set()

        def external(match):
            key = match[1]
            src.add(key)
            return text(sources[key]['url'])

        body = Template((ROOT / f"templates/dossiers/{item['slug']}.html.part").read_text(encoding='utf-8')).substitute(root=rel_root)
        body = re.sub(r'@source:([a-z0-9-]+)@', external, body)
        if not src <= set(page['sourcesDeDepart']):
            raise ValueError(f"Sources non déclarées dans le manifeste pour {route}: {', '.join(sorted(src - set(page['sourcesDeDepart'])))}")
        labels = {row['route']: row['crumb'] for row in dossiers}

        def nav(to, short=False):
            href = posixpath.relpath(to, posixpath.dirname(route))
            label = ('Norvinsk' if to == dossiers[1]['route'] else labels[to]) if short else labels[to]
            current = ' aria-current="page"' if to == route else ''
            style = ' class="commandbar__nav-link"' if short else ''
            return f'<a href="{text(href)}"{style}{current}>{text(label)}</a>'

        links = ''.join(f'<a class="button {"button--primary" if i == 0 else "button--quiet"}" href="#{text(section)}" data-expand-target>{text(label)} <span class="button__arrow" aria-hidden="true">{"↓" if i == 0 else "↘"}</span></a>' for i, (section,label) in enumerate(item['hero_links']))
        toc = ''.join(f'<li><a href="#{text(section)}" data-expand-target><span aria-hidden="true">{i:02d}</span>{text(label)}</a></li>' for i,(section,label) in enumerate(item['toc'], 1))
        strip = ''.join(f'<div><dt>{text(label)}</dt><dd>{text(value)}</dd></div>' for value,label in item['strip'])
        canonical = base + route if base != './' else './' + posixpath.basename(route)
        shareimage = (base if base != './' else rel_root) + image
        title = f"{page['titre']} — Tarkov Ultimate Guide"
        ld = {'@context':'https://schema.org','@type':'Article','headline':page['titre'],'description':item['description'],
              'dateModified':'2026-11-18','inLanguage':'fr-FR','author':{'@type':'Organization','name':'Tarkov Ultimate Guide'}}
        if base != './':
            ld.update(url=canonical, image=shareimage)
        values = {key:text(item[key]) for key in ('slug','description','image','alt','crumb','kicker','headline','headline_tail','lead','scene','aside_note')}
        values.update(title=text(title), canonical=text(canonical), shareimage=text(shareimage), root=rel_root,
                      article_label=text(page['titre']), structured=json.dumps(ld,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'),
                      guide_entry=nav(dossiers[0]['route']), lore_entry=nav(dossiers[1]['route']), guide_nav=nav(dossiers[0]['route'],True),
                      lore_nav=nav(dossiers[1]['route'],True), hero_links=links, strip=strip, toc=toc, content=body.rstrip())
        out = template.substitute(values)
        target = ROOT / route
        if check:
            if not target.is_file() or target.read_text(encoding='utf-8') != out:
                raise SystemExit(f'Rejouer scripts/rendre_dossiers.py : {route} diverge de son gabarit')
        else:
            stage = target.with_suffix('.html.tmp')
            stage.write_text(out,encoding='utf-8'); stage.replace(target)
        print(f'{route} · {len(src)} références directes · description {len(item["description"])} caractères')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--check', action='store_true', help='vérifier sans réécrire')
    render(cli.parse_args().check)
