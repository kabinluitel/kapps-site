Static copy of the KAPPS marketing pages (landing, team, tools, terms, privacy), served by GitHub Pages at https://kapps.ai.

Rebuild after editing templates in the main app (local server on :8000):

    python3 _build/export_site.py /tmp/site && python3 _build/make_static.py /tmp/site
    rsync -a --delete --exclude .git --exclude _build /tmp/site/ ./
