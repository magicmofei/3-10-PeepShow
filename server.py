import os
import json
import http.server
import socketserver

# 1. 配置参数
PORT = 8888
VIDEO_DIR = 'pic/Slides-video'
JSON_FILE = 'reels.json'
EXTS = ('.mp4', '.mov', '.avi', '.webm', '.mkv', '.m4v')

def generate_static_list():
    """扫描文件夹并生成静态 JSON 名单"""
    reels = []
    if os.path.exists(VIDEO_DIR):
        files = sorted(os.listdir(VIDEO_DIR))
        for f in files:
            if f.lower().endswith(EXTS):
                reels.append({
                    "src": f"{VIDEO_DIR}/{f}",
                    "label": f"REEL · {os.path.splitext(f)[0].upper()}"
                })
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(reels, f, indent=2, ensure_ascii=False)
    print(f"✅ 已自动更新名单: {JSON_FILE} (共 {len(reels)} 个视频)")

# 启动时先生成一次名单
generate_static_list()

# 2. 启动基础服务器 (Vercel 不需要这段，但你本地预览需要)
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🚀 本地服务器已启动: http://localhost:{PORT}")
    httpd.serve_forever()
