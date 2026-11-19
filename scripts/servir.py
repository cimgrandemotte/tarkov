#!/usr/bin/env python3
"""Aperçu statique du guide, avec requêtes Range pour les MP3. Pas de backend en production."""
import argparse
from email.utils import formatdate
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from mimetypes import guess_type
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = frozenset(('atelier', 'pages', 'css', 'js', 'images', 'audio', 'fonts'))
FORMATS = {'.mjs': 'application/javascript', '.js': 'application/javascript', '.html': 'text/html; charset=utf-8',
           '.json': 'application/json; charset=utf-8', '.jpg': 'image/jpeg', '.mp3': 'audio/mpeg', '.woff2': 'font/woff2'}


class Preview(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_asset(False)

    def do_HEAD(self):
        self.send_asset(True)

    def redirect(self, safe_location):
        self.send_response(HTTPStatus.FOUND)
        self.send_header('Location', safe_location)
        self.send_header('Content-Length', '0')
        self.end_headers()

    def send_asset(self, head_only):
        try:
            parsed = urlsplit(self.path)
            path = unquote(parsed.path)
            parts = path.strip('/').split('/')
            if parsed.netloc or not path.startswith('/') or any(part.startswith('.') or '\x00' in part or '\\' in part for part in parts):
                return self.send_error(HTTPStatus.NOT_FOUND)
            if path == '/' and not (ROOT / 'index.html').is_file():
                return self.redirect('/atelier/')
            if path not in ('/', '/index.html') and parts[0] not in PUBLIC:
                return self.send_error(HTTPStatus.NOT_FOUND)
            asset = (ROOT / path.lstrip('/')).resolve()
            if not asset.is_relative_to(ROOT):
                return self.send_error(HTTPStatus.NOT_FOUND)
            if asset.is_dir():
                asset = (asset / 'index.html').resolve()
                if asset.is_relative_to(ROOT) and asset.is_file() and not path.endswith('/'):
                    safe_path = parsed.path + '/'
                    if '\r' in safe_path or '\n' in safe_path or safe_path.startswith('//'):
                        return self.send_error(HTTPStatus.BAD_REQUEST)
                    return self.redirect(safe_path)
            if not asset.is_relative_to(ROOT) or not asset.is_file():
                return self.send_error(HTTPStatus.NOT_FOUND)
            stat = asset.stat()
            f = asset.open('rb')
        except (ValueError, OSError):
            return self.send_error(HTTPStatus.NOT_FOUND)
        with f:
            start, end, partial = 0, stat.st_size - 1, False
            request_range = self.headers.get('Range')
            if request_range and asset.suffix.lower() == '.mp3':
                match = re.fullmatch(r'bytes=(\d{0,15})-(\d{0,15})', request_range.strip())
                if match and (match[1] or match[2]):
                    if match[1]:
                        start = int(match[1]); end = min(end, int(match[2])) if match[2] else end
                    else:
                        start = max(0, stat.st_size - int(match[2]))
                    partial = True
                    if start < 0 or start > end:
                        self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                        self.send_header('Content-Range', f'bytes */{stat.st_size}')
                        self.send_header('Content-Length', '0')
                        self.end_headers()
                        return
            self.send_response(HTTPStatus.PARTIAL_CONTENT if partial else HTTPStatus.OK)
            self.send_header('Content-Type', FORMATS.get(asset.suffix.lower()) or guess_type(asset.name)[0] or 'application/octet-stream')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Last-Modified', formatdate(stat.st_mtime, usegmt=True))
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Content-Length', str(end - start + 1))
            if asset.suffix.lower() == '.mp3':
                self.send_header('Accept-Ranges', 'bytes')
            if partial:
                self.send_header('Content-Range', f'bytes {start}-{end}/{stat.st_size}')
            self.end_headers()
            if head_only:
                return
            try:
                if partial:
                    f.seek(start)
                    remaining = end - start + 1
                    while remaining and (chunk := f.read(min(remaining, 128 * 1024))):
                        self.wfile.write(chunk)
                        remaining -= len(chunk)
                else:
                    shutil.copyfileobj(f, self.wfile, length=128 * 1024)
            except (BrokenPipeError, ConnectionResetError):
                pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4173)
    parser.add_argument('--host', default='0.0.0.0')
    args = parser.parse_args()
    with ThreadingHTTPServer((args.host, args.port), Preview) as server:
        print(f'Aperçu du guide sur {args.host}:{args.port} · accueil : / · atelier : /atelier/', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
