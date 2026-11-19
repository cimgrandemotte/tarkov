#!/usr/bin/env python3
"""Extrait les tables Extractions / Transits / Bosses / Usable Keys du wikitext des fiches de lieu.

Source : wikitext brut exporté par l'API Fandom (recherche/wiki-cartes/*.wikitext),
croisé avec les instantanés json.tarkov.dev (regular, pve, pvp-season).
Sortie : recherche/wiki-cartes/structures.json
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'recherche/wiki-cartes'

MAPES = {
    'Factory': 'factory',
    'Customs': 'customs',
    'Woods': 'woods',
    'Shoreline': 'shoreline',
    'Interchange': 'interchange',
    'Reserve': 'reserve',
    'The_Lab': 'the-lab',
    'Lighthouse': 'lighthouse',
    'Streets_of_Tarkov': 'streets-of-tarkov',
    'Ground_Zero': 'ground-zero',
    'The_Labyrinth': 'the-labyrinth',
    'Icebreaker': 'icebreaker',
    'Terminal': 'terminal',
}


def sections(wikitext):
    out = {}
    current = 'préambule'
    buf = []
    for line in wikitext.splitlines():
        head = re.match(r'^(={2,4})\s*(.+?)\s*\1\s*$', line)
        if head:
            out[current] = '\n'.join(buf)
            current = head.group(2).strip()
            buf = []
        else:
            buf.append(line)
    out[current] = '\n'.join(buf)
    return out


def _split_cells(block):
    """Découpe un tableau wikitext en lignes, chaque ligne = liste de cellules."""
    rows = []
    cells = []
    buf = []
    kind = None

    def flush():
        nonlocal buf, kind
        if kind is not None:
            cells.append('\n'.join(buf).strip())
        buf = []
        kind = None

    for raw in block:
        line = raw.strip()
        if line.startswith('|-'):
            flush()
            if cells:
                rows.append(cells)
                cells = []
            continue
        if line.startswith('|') and not line.startswith('|}') and not line.startswith('||'):
            flush()
            kind = 'data'
            rest = line[1:]
            if rest.startswith('\n'):
                rest = rest[1:]
            buf.append(rest)
            continue
        if line.startswith('!') and not line.startswith('!!'):
            flush()
            kind = 'head'
            rest = line[1:]
            if rest.startswith('\n'):
                rest = rest[1:]
            buf.append(rest)
            continue
        if kind is not None:
            buf.append(raw)
    flush()
    if cells:
        rows.append(cells)
    return rows


def tables(text):
    """Renvoie [(attributs, lignes)] pour chaque tableau de premier niveau du texte."""
    lines = text.splitlines()
    result = []
    depth = 0
    block = []
    attrs = ''
    for line in lines:
        s = line.strip()
        if s.startswith('{|'):
            if depth == 0:
                block = []
                head = re.match(r'^\{\|([^|]*)', s)
                attrs = head.group(1) if head else ''
            depth += 1
            if depth > 1:
                block.append(line)
            continue
        if s.startswith('|}'):
            depth -= 1
            if depth == 0:
                result.append((attrs, _split_cells(block)))
                block = []
                attrs = ''
            elif depth > 0:
                block.append(line)
            continue
        if depth > 0:
            block.append(line)
    return result


def clean(text):
    if not text:
        return ''
    out = text
    out = re.sub(r'\{\{[^{}]*\}\}', ' ', out)
    out = re.sub(r'\[\[File:[^\]]*\]\]', ' ', out)
    out = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', out)
    out = re.sub(r'\[\[([^\]]*)\]\]', r'\1', out)
    out = re.sub(r'<br\s*/?>', ' ; ', out)
    out = re.sub(r'<[^>]+>', '', out)
    out = re.sub(r'\bstyle="[^"]*"', '', out)
    out = re.sub(r'^\s*\|\s*', '', out)
    out = out.replace(' | ', ' ')
    out = out.replace("'''", '').replace("''", '')
    out = re.sub(r'&[a-z]+;', ' ', out)
    out = re.sub(r'[ \t]+', ' ', out)
    out = re.sub(r'\n{2,}', '\n', out)
    return out.strip()


def cells_of(row):
    return row if isinstance(row, list) else [row]


def parse_extracts(section):
    result = []
    for attrs, rows in tables(section):
        for r in rows:
            cs = [clean(c) for c in cells_of(r)]
            cs = [c for c in cs if c and c not in ('-', '—')]
            if not cs or cs[0] in ('Extraction', 'Exfil', 'Name'):
                continue
            nom = cs[0]
            camp = ''
            reste = cs[1:]
            for i, c in enumerate(reste):
                if c.lower() in ('pmc', 'scav', 'all', 'tous', 'shared'):
                    camp = c.lower()
                    reste = reste[:i] + reste[i + 1:]
                    break
            result.append({
                'nom': nom,
                'camp': {'all': 'shared', 'tous': 'shared'}.get(camp, camp),
                'toujours': '✔' in reste[0] if len(reste) > 0 else None,
                'usageUnique': '✔' in reste[1] if len(reste) > 1 else None,
                'conditions': reste[2] if len(reste) > 2 else '',
                'notes': reste[3] if len(reste) > 3 else '',
            })
    return result


def parse_transits(section):
    result = []
    for attrs, rows in tables(section):
        for r in rows:
            cs = [clean(c) for c in cells_of(r)]
            cs = [c for c in cs if c and c not in ('-', '—')]
            if not cs or cs[0] in ('Transit', 'Name'):
                continue
            nom = cs[0]
            if not nom.lower().startswith('transit'):
                continue
            camp = ''
            reste = cs[1:]
            for i, c in enumerate(reste):
                if c.lower() in ('pmc', 'scav', 'all', 'tous', 'shared'):
                    camp = c.lower()
                    reste = reste[:i] + reste[i + 1:]
                    break
            result.append({
                'nom': nom,
                'vers': nom.split(' to ', 1)[1].strip() if ' to ' in nom else '',
                'camp': {'all': 'shared', 'tous': 'shared'}.get(camp, camp),
                'conditions': reste[2] if len(reste) > 2 else '',
                'notes': reste[3] if len(reste) > 3 else '',
            })
    return result


def parse_bosses(section):
    result = []
    for attrs, rows in tables(section):
        for r in rows:
            cs = cells_of(r)
            if len(cs) < 2:
                continue
            name = clean(cs[0])
            if not name or name == 'Name':
                continue
            result.append({
                'nom': name,
                'zone': clean(cs[1]) if len(cs) > 1 else '',
                'equipement': clean(cs[2]) if len(cs) > 2 else '',
                'escorte': clean(cs[3]) if len(cs) > 3 else '',
            })
    return result


def parse_keys(section):
    result = []
    for attrs, rows in tables(section):
        for r in rows:
            cs = cells_of(r)
            if len(cs) < 2:
                continue
            cells = [clean(c) for c in cs]
            utiles = [c for c in cells if c and not c.startswith('-')]
            if not utiles:
                continue
            nom = utiles[0]
            if nom in ('Key Name', 'Icon', 'Name', 'Item name', 'Item Name'):
                continue
            result.append({
                'nom': nom,
                'quete': utiles[1] if len(utiles) > 1 else '',
                'toujoursOuvert': any('✔' in c for c in utiles),
            })
    return result


def build():
    out = {}
    for page, slug in MAPES.items():
        path = SRC / f'{page}.wikitext'
        if not path.is_file():
            raise SystemExit(f'wikitext manquant : {page}')
        wt = path.read_text(encoding='utf-8')
        sec = sections(wt)
        desc = clean(sec.get('Description', ''))
        notes = clean(sec.get('Notes', ''))
        features = [clean(l.lstrip('*').strip()) for l in sec.get('Features', '').splitlines()
                    if l.strip().startswith('*')]
        out[slug] = {
            'page': page,
            'description': desc,
            'notes': notes,
            'fonctionnalites': [f for f in features if f],
            'cles': parse_keys(sec.get('Usable Keys', '') + sec.get('Key Items', '')),
            'boss': parse_bosses(sec.get('Bosses', '') + sec.get('Boss', '')),
            'sorties': parse_extracts(sec.get('Extractions', '') + sec.get('Extraction', '')),
            'transits': parse_transits(sec.get('Transits', '')),
        }
    (SRC / 'structures.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    for slug, data in out.items():
        print(f"{slug:18s} sorties {len(data['sorties']):>3} · transits {len(data['transits']):>2} · "
              f"boss {len(data['boss']):>2} · clés {len(data['cles']):>3} · features {len(data['fonctionnalites']):>2}")
    return out


if __name__ == '__main__':
    build()
