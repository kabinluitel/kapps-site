"""Turn the exported KAPPS pages into a static, contact-only site for GitHub Pages."""
import re
import sys
from pathlib import Path

SITE = Path(sys.argv[1])
ARROW = '<i class="fas fa-arrow-right"></i>'
CONTACT = 'href="/#contact"'

BANNER = (
    '<div style="background:#0f172a;color:#e2e8f0;text-align:center;padding:10px 16px;'
    'font:500 14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;position:relative;z-index:1000">'
    'The KAPPS web tools are offline for now. For a demo or project work, email '
    '<a href="mailto:support@kapps.ai" style="color:#7dd3fc">support@kapps.ai</a> or call '
    '<a href="tel:+18044043621" style="color:#7dd3fc">804-404-3621</a>.</div>'
)

SUBS = [
    # top menu
    (r'\s*<a href="/login/" class="sn-ghost">Sign In</a>', ''),
    (rf'<a href="/signup/" class="sn-primary">Try KAPPS Studio {re.escape(ARROW)}</a>',
     f'<a {CONTACT} class="sn-primary">Contact us {ARROW}</a>'),
    # footer
    (r'\s*<a href="/login/">Sign In</a>', ''),
    (r'\s*<a href="/signup/">Try KAPPS Studio</a>', ''),
    # tool pages
    (r'\s*<a href="/login/\?next=[^"]*" class="btn-secondary">Sign in</a>', ''),
    (rf'<a href="/signup/" class="btn-primary">(?:Try KAPPS Studio|Use it free) {re.escape(ARROW)}</a>',
     f'<a {CONTACT} class="btn-primary">Contact us {ARROW}</a>'),
    # landing hero (multi-line) and contact section
    (rf'<a href="/signup/" class="btn-primary">\s*Try KAPPS Studio {re.escape(ARROW)}\s*</a>',
     f'<a href="mailto:support@kapps.ai" class="btn-primary">Email us {ARROW}</a>'),
    (r'\s*<p class="contact-alt">Prefer to start on your own\?.*?</p>', ''),
    # terms / privacy back link
    (r'\s*<a href="/signup/" class="btn-back">.*?</a>', ''),
    # wording
    (r'Sign in and run ', 'Run '),
]

for page in SITE.rglob('index.html'):
    html = page.read_text()
    for pat, rep in SUBS:
        html = re.sub(pat, rep, html, flags=re.S)
    html = re.sub(r'(<body[^>]*>)', r'\1' + BANNER, html, count=1)
    left = re.findall(r'href="/(?:signup|login)/[^"]*"', html)
    if left:
        print('LEFTOVER', page, left)
    page.write_text(html)

(SITE / 'CNAME').write_text('kapps.ai\n')
(SITE / '.nojekyll').write_text('')
(SITE / '404.html').write_text(
    '<!doctype html><meta charset="utf-8"><title>KAPPS</title>'
    '<meta http-equiv="refresh" content="0; url=/"><a href="/">Go to kapps.ai</a>\n'
)
print('done')
