#!/usr/bin/env python3
"""Génère l'accueil HTML autonome et ses compteurs depuis le manifeste public.
TUG_PUBLIC_URL, si renseignée, est l'URL HTTPS de la racine où le site sera hébergé.
"""
import argparse
from collections import Counter
from html import escape
import json
import os
from pathlib import Path
from string import Template
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
TITLE = 'Tarkov Ultimate Guide — Guide FR d’Escape from Tarkov'
DESCRIPTION = 'Guide francophone d’Escape from Tarkov : premier raid, aperçu des cartes et de l’équipement, notes du patch 1.3.0.0 et repères pour le solo SP-Tushonka.'
THEMES = {
    2: 'Accueil et navigation', 3: 'Débutant et lore', 4: 'Atlas et extractions', 5: 'Armes et munitions',
    6: 'Armures et boss', 7: 'Traders, quêtes et Hideout', 8: 'Compétences, économie et stratégies',
    9: 'SP‑Tushonka, Arena et événements', 10: 'Notes de patch, ressources et glossaire',
}
PUBLISHED = {'PUBLIEE', 'PUBLIÉE'}


def load(file):
    return json.loads((ROOT / file).read_text(encoding='utf-8'))


def public_base(raw):
    raw = raw.strip()
    if not raw:
        return './'
    url = urlsplit(raw)
    if url.scheme != 'https' or not url.hostname or url.username or url.password or url.query or url.fragment or any(c.isspace() for c in raw):
        raise ValueError('TUG_PUBLIC_URL doit être une racine HTTPS, sans identifiants, paramètres ni fragment')
    return urlunsplit((url.scheme, url.netloc, url.path.rstrip('/') + '/', '', ''))


def stat(n, pad=0):
    return format(n, f'0{pad},d').replace(',', '\u202f')


def dossier(item, n, published):
    safe = lambda val: escape(str(val), quote=True)
    topic = next((p for p in published if any(p['route'].startswith(prefix) for prefix in item['routes'])), None)
    hint = 'Fiche disponible' if topic else 'Dossier à venir'
    link = {'url': f"./{topic['route']}", 'texte': f"Lire : {topic['titre']}"} if topic else item['lien']
    if not (ROOT / 'images' / 'hero' / item['image']).is_file():
        raise ValueError(f'Illustration du dossier absente : {item["image"]}')
    opt = ' data-expand-target' if link['url'] == '#programme' else ''
    return f'''          <article class="dossier-card" id="dossier-{safe(item['id'])}" tabindex="-1" aria-labelledby="nom-{safe(item['id'])}">
            <details class="dossier-card__details" data-user-expand>
              <summary class="dossier-card__trigger">
                <span class="dossier-card__thumb"><img src="./images/hero/{safe(item['image'])}" width="1376" height="768" loading="lazy" decoding="async" alt="{safe(item['alt'])}"><span class="badge dossier-card__tag"><span aria-hidden="true">{n:02d} / </span>{safe(item['tag'])}</span><span class="dossier-card__name" id="nom-{safe(item['id'])}">{safe(item['titre'])}</span></span>
                <span class="dossier-card__band"><span class="dossier-card__state"><i aria-hidden="true"></i>{hint}</span><span class="dossier-card__toggle" aria-hidden="true"></span></span>
              </summary>
              <div class="dossier-card__content"><p>{safe(item['description'])}</p><a class="text-action" href="{safe(link['url'])}"{opt}>{safe(link['texte'])} <span aria-hidden="true">↗</span></a></div>
            </details>
          </article>'''


def render(check=False):
    book = load('docs/pages.json')
    pages = book['pages']
    plan = [p for p in pages if p['route'] == 'index.html']
    if len(plan) != 1 or book['total'] != len(pages):
        raise ValueError('Manifeste incomplet ou incohérent')
    if plan[0]['etat'] not in PUBLISHED:
        raise ValueError('Publier la route index.html dans le manifeste avant son rendu')
    published = [p for p in pages if p['etat'] in PUBLISHED]
    for p in published:
        if p['route'] != 'index.html' and not (ROOT / p['route']).is_file():
            raise ValueError(f"Route publiée sans HTML : {p['route']}")
    if book['publiees'] != len(published):
        raise ValueError('Le nombre de routes publiées du manifeste est incohérent')
    n = len(published)
    captured = load('recherche/tarkov-dev/manifest.json')['modes']
    counts = [profile['items'] for profile in captured.values()]
    if not counts:
        raise ValueError('Aucun profil de données')
    per_profile = len(set(counts)) == 1
    items = stat(counts[0]) if per_profile else f'{stat(min(counts))}–{stat(max(counts))}'
    assert 150 <= len(DESCRIPTION) <= 160, len(DESCRIPTION)
    public = public_base(os.getenv('TUG_PUBLIC_URL', ''))
    image = public + 'images/hero/tarkov-night-rain.jpg'
    structured = {'@context':'https://schema.org', '@type':'WebSite', 'name':'Tarkov Ultimate Guide', 'inLanguage':'fr-FR', 'description':DESCRIPTION}
    if public != './':
        structured['url'] = public
        structured['image'] = image
    table = Counter(p['phase'] for p in published)
    pieces = []
    for phase, label in THEMES.items():
        num = book['parPhase'][f'PHASE_{phase}']; done = table[f'PHASE_{phase}']
        status = ('publiée' if num == 1 else 'publiées') if done == num else ('à venir' if not done else 'publiées à ce stade')
        detail = f'{num} page' + ('s' if num != 1 else '') if done in (0,num) else f'{done} sur {num} pages'
        pieces.append(f'<li><strong>Phase {phase} · {escape(label)}</strong> — {detail} {status}</li>')
    routes = {p['route'] for p in published}
    has_guide = 'pages/getting-started.html' in routes
    has_lore = 'pages/lore/index.html' in routes
    guide_href = './pages/getting-started.html' if has_guide else '#premiers-pas'
    lore_href = './pages/lore/index.html'
    guides_menu = (f'<li><a href="{guide_href}">Guide débutant en dix étapes</a></li>' if has_guide else '')
    if has_lore:
        guides_menu += f'<li><a href="{lore_href}">Lore de Norvinsk</a></li>'
    lore_menu = (f'<a class="commandbar__nav-link" href="{lore_href}">Norvinsk</a>' if has_lore else
                 '<a class="commandbar__nav-link" href="#actualites">Veille</a>')
    guide_intro = ('<p class="muted small">Coche ces trois repères ou ouvre le <a class="link" href="./pages/getting-started.html">guide débutant en dix étapes</a> pour le kit, les soins et les commandes.</p>' if has_guide else
                   '<p class="muted small">Coche les étapes au fil du raid. Le guide débutant complet est à venir.</p>')
    has_armor = 'pages/armor/index.html' in routes
    has_boss = 'pages/bosses/index.html' in routes
    protection_sauts = []
    if has_armor:
        protection_sauts.append('<a href="./pages/armor/index.html" data-expand-target><span><b>Choisir son armure</b><small>390 pièces, classes et matériaux</small></span><span class="guide-jumps__arrow" aria-hidden="true">↗</span></a>')
    if has_boss:
        protection_sauts.append('<a href="./pages/bosses/index.html" data-expand-target><span><b>Préparer un boss</b><small>14 fiches, apparitions et butin</small></span><span class="guide-jumps__arrow" aria-hidden="true">↗</span></a>')
    protection_jump = ''.join(protection_sauts)
    lore_jump = (f'<a href="{lore_href}"><span><b>Comprendre Norvinsk</b><small>Lore, factions et chronologie</small></span><span class="guide-jumps__arrow" aria-hidden="true">↗</span></a>' if has_lore else
                 '<a href="#actualites"><span><b>Revenir après une pause</b><small>Patch de référence et correctifs</small></span><span class="guide-jumps__arrow" aria-hidden="true">↗</span></a>')
    values = dict(title=escape(TITLE),description=escape(DESCRIPTION),canonical=escape(public,quote=True),shareimage=escape(image,quote=True),
        structured=json.dumps(structured,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'),
        published=stat(n,2),planned=stat(len(pages),2),publication_label='Page publiée' if n == 1 else 'Pages publiées',
        objects=items,objects_label='Objets par profil (export)',profiles=stat(len(captured),2),
        published_fraction=f'{n} page{"s" if n != 1 else ""} publiée{"s" if n != 1 else ""} sur {len(pages)} prévues',
        dossiers='\n'.join(dossier(item,i,published) for i,item in enumerate(load('templates/dossiers-accueil.json'),1)),
        programme=''.join(pieces), guide_href=guide_href, guide_arrow='↗' if has_guide else '↓',
        guides_menu=guides_menu, lore_menu=lore_menu, guide_intro=guide_intro, lore_jump=lore_jump,
        protection_jump=protection_jump)
    body = Template((ROOT / 'templates/accueil.html.tmpl').read_text(encoding='utf-8')).substitute(values)
    target = ROOT / 'index.html'
    if check:
        if target.read_text(encoding='utf-8') != body:
            raise SystemExit('Rejouer scripts/rendre_accueil.py : le HTML et ses sources divergent')
    else:
        stage = target.with_suffix('.html.tmp'); stage.write_text(body,encoding='utf-8'); stage.replace(target)
    print(f'Accueil : {n} / {len(pages)} routes éditoriales, {len(captured)} profils, {items} objets par profil, description {len(DESCRIPTION)} caractères.')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--check', action='store_true', help='vérifier la reproductibilité sans modifier le HTML')
    render(cli.parse_args().check)
