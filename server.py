#!/usr/bin/env python3
"""轻量本地服务器 — 西洋镜 Peep Show
用法: python3 server.py   (默认端口 8888)
"""
import http.server
import json
import os
import urllib.parse
from pathlib import Path

PORT = 8888
ROOT = Path(__file__).parent
VIDEO_DIR = ROOT / 'pic' / 'Slides-video'
VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.webm', '.mkv', '.m4v'}


class PeepHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/reels':
            self._serve_reels()
        else:
            super().do_GET()

    def _serve_reels(self):
        files = sorted(
            f for f in VIDEO_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in VIDEO_EXTS
        )
        reels = [
            {
                'src': 'pic/Slides-video/' + f.name,
                'label': 'REEL · ' + f.stem.upper()
            }
            for f in files
        ]
        body = json.dumps(reels, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # 只打印 API 和 HTML 请求，忽略其他静态资源
        first = str(args[0]) if args else ''
        if '/api/' in first or '.html' in first:
            super().log_message(fmt, *args)


if __name__ == '__main__':
    import webbrowser
    addr = ('', PORT)
    httpd = http.server.HTTPServer(addr, PeepHandler)
    url = f'http://localhost:{PORT}/'
    print(f'\n  西洋镜服务器已启动 → {url}')
    print(f'  视频目录: {VIDEO_DIR}')
    print(f'  按 Ctrl+C 停止\n')
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n  服务器已停止。')
