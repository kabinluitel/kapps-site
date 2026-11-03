"""Export the public KAPPS marketing pages from a running local server into a static folder."""
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

BASE = "http://localhost:8000"
OUT = Path(sys.argv[1])
TOOLS = ["c-calculator", "cn-studio", "design-build-studio", "drainage-cadd-studio", "floodway-studio",
         "geotech-studio", "pond-studio", "time-of-concentration", "usda-hsg"]
PAGES = ["/", "/team/", "/tools/", "/terms/", "/privacy/", "/robots.txt", "/sitemap.xml"] + [f"/tools/{t}/" for t in TOOLS]

ASSET_RE = re.compile(r'''(?:href|src|content)=["'](/static/[^"'?#]+)''')
CSS_URL_RE = re.compile(r'''url\(\s*["']?([^"')?#]+)''')

seen = set()


def fetch(path):
    with urllib.request.urlopen(BASE + path) as r:
        return r.read()


def out_path(path):
    p = OUT / path.lstrip("/")
    return p / "index.html" if path.endswith("/") else p


def save_asset(path):
    if path in seen or not path.startswith("/static/"):
        return
    seen.add(path)
    try:
        data = fetch(path)
    except Exception as e:
        print("MISSING", path, e)
        return
    dest = out_path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    if path.endswith(".css"):
        for ref in CSS_URL_RE.findall(data.decode("utf-8", "ignore")):
            if ref.startswith("data:") or urlparse(ref).scheme:
                continue
            save_asset(urlparse(urljoin(path, ref)).path)


for page in PAGES:
    html = fetch(page)
    dest = out_path(page)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(html)
    for a in ASSET_RE.findall(html.decode("utf-8", "ignore")):
        save_asset(a)
    print("page", page, len(html))
print("assets", len(seen))
