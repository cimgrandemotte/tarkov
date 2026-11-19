#!/usr/bin/env python3
"""Relever les annonces du jeu et les branches stables/expérimentales du projet solo."""

import argparse
import concurrent.futures
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
STEAM_FEED = 'steam_community_announcements'
STEAM = 'https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?' + urlencode({
    'appid': '3932890', 'count': 100, 'maxlength': 400, 'feeds': STEAM_FEED,
})
GITHUB = 'https://api.github.com/repos/SP-Tushonka/build/releases'
NUGET_API = 'https://api.nuget.org/v3-flatcontainer/sptushonka.server.core/index.json'
NUGET_PACKAGE = 'https://www.nuget.org/packages/SPTushonka.Server.Core'
PATCH_NUMBER = re.compile(r'^(?:patch|update)\s+([0-9]+(?:\.[0-9]+){2,3})(?![\d.])', re.I)
PRE_TIME = re.compile(r'-pre\.(\d{12})$')


def download(url):
    request = Request(url, headers={'Accept': 'application/json', 'User-Agent': 'TarkovUltimateGuide/0.1'})
    with urlopen(request, timeout=20) as response:
        return json.load(response), {'url': url, 'dateServeurHttp': response.headers.get('Date')}


def publish(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    tmp.replace(path)


def version_tuple(name):
    base, _, label = name.partition('-')
    version = tuple(map(int, base.split('.')))
    match = PRE_TIME.search(name)
    return version, not bool(label), int(match[1]) if match else 0, label


def release_entry(item):
    return {key: item[key] for key in ('tag_name', 'name', 'published_at', 'prerelease', 'html_url')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'recherche' / 'versions')
    args = parser.parse_args()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        steam, stable, releases, nuget = pool.map(download, (
            STEAM, GITHUB + '/latest', GITHUB + '?per_page=10', NUGET_API,
        ))
    announcements = []
    for item in steam[0]['appnews']['newsitems']:
        if item['feedname'] != STEAM_FEED:
            continue
        announcement = {'titre': item['title'], 'dateUtc': datetime.fromtimestamp(item['date'], timezone.utc).isoformat(),
                        'urlFlux': item['url']}
        match = PATCH_NUMBER.search(item['title'])
        if match:
            announcement['version'] = match[1]
        announcements.append(announcement)
    announcements.sort(key=lambda item: item['dateUtc'], reverse=True)
    if not announcements:
        raise ValueError('Aucune annonce officielle dans le flux Steam')
    numbered = next((item for item in announcements if item.get('version')), None)
    if not numbered:
        raise ValueError('Aucun patch numéroté dans le flux Steam')
    if stable[0].get('draft') or stable[0].get('prerelease'):
        raise ValueError('La réponse GitHub latest ne correspond pas à une release stable')
    description = stable[0]['body']
    target = re.search(r'Requires EFT\s+`([^`]+)`', description, flags=re.I)
    runtimes = re.findall(r'\[([^\]\n]*Runtime\s+[\d.]+|ASP\.NET\s+[\d.]+)\]\((https://dotnet\.microsoft\.com/[^)]+)\)', description, flags=re.I)
    previews = [value for value in nuget[0]['versions'] if '-' in value]
    newest = max(previews, key=version_tuple, default=None)
    timestamp = PRE_TIME.search(newest or '')
    github_releases = [release_entry(item) for item in releases[0] if not item.get('draft')]
    publish(args.out / 'eft.json', {
        'schemaVersion': 1, 'sourceFlux': steam[1],
        'dernierPatchNumeroteDansCeFlux': numbered,
        'derniereAnnonceDansCeFlux': announcements[0],
        'annoncesOfficiellesRecuperees': announcements,
        'limite': 'Ce flux Steam n’épuise ni les hotfixes, ni les annonces BSG diffusées ailleurs.',
    })
    publish(args.out / 'sp-tushonka.json', {
        'schemaVersion': 1, 'sources': [stable[1], releases[1], nuget[1]],
        'releaseStableJouable': {
            **release_entry(stable[0]), 'buildEftRequis': target[1] if target else None,
            'prerequisRuntime': [{'nom': name.strip(), 'url': link} for name, link in runtimes],
        },
        'releasesGitHubRecuperees': github_releases,
        'prereleaseNuGet': {
            'package': 'SPTushonka.Server.Core', 'version': newest,
            'dateIndiqueeDansLeTag': datetime.strptime(timestamp[1], '%Y%m%d%H%M').date().isoformat() if timestamp else None,
            'url': f'{NUGET_PACKAGE}/{newest}' if newest else None,
            'statut': 'BIBLIOTHEQUE_EXPERIMENTALE_NON_ASSIMILABLE_A_UN_BUILD_JOUABLE',
        },
    })
    print(f'Steam : {len(announcements)} annonces officielles ; dernier patch numéroté {numbered["version"]}.')
    print(f'SP-Tushonka : stable {stable[0]["tag_name"]} ; paquet NuGet {newest}.')


if __name__ == '__main__':
    main()
