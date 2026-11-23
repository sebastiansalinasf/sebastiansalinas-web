#!/bin/bash
# Reconstruye el sitio: blog -> versión en inglés -> CSS. Luego hacer commit y push (Netlify publica solo).
set -e
cd "$(dirname "$0")"
[ -d node_modules ] || npm install --silent
python3 build_blog.py
python3 make_en.py
npx tailwindcss -c tailwind.config.js -i in.css -o ../site/assets/styles.css --minify
echo "Sitio reconstruido en site/"
