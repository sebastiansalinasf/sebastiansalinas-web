"""Blog de www.sebastiansalinas.cl

Fuente de verdad: content/posts.json  (lista de artículos, el más reciente primero o en cualquier orden)
Cada artículo:
{
  "slug": "url-del-articulo",                 # solo minúsculas, números y guiones
  "title": "Título",
  "date": "2026-11-24",                        # AAAA-MM-DD
  "category": "Inmobiliario" | "Empresarial" | "Fallos" | "Actualidad" ...,
  "summary": "Bajada de 1-2 frases",
  "body_html": "<p>Texto en HTML simple: p, h2, ul/li, blockquote, a</p>",
  "sources": [{"title": "Nombre de la fuente", "url": "https://..."}]
}

Genera:
- Capítulo "Blog / Comentarios" al final de index.html (entre marcadores BLOG:START / BLOG:END)
- /blog/index.html (índice) y /blog/<slug>/index.html (artículos), con JSON-LD Blog / BlogPosting
- sitemap.xml y la sección de blog de llms.txt
Luego correr make_en.py y compilar Tailwind (ver tools/publicar.sh).
"""
import json, os, re, html, shutil, datetime

import pathlib
REPO = pathlib.Path(__file__).resolve().parent.parent
ROOT = str(REPO / 'site')
POSTS = str(REPO / 'content' / 'posts.json')
BASE = 'https://www.sebastiansalinas.cl/'
PERSON = BASE + '#person'
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

def fecha(d):
    y, m, dd = map(int, d.split('-'))
    return f'{dd} de {MESES[m-1]} de {y}'

def iso(d):
    return d if 'T' in d else d + 'T09:00:00-03:00'

def esc(s):
    return html.escape(s, quote=True)

def load_posts():
    if not os.path.exists(POSTS):
        return []
    posts = json.load(open(POSTS, encoding='utf-8'))
    for p in posts:
        assert re.fullmatch(r'[a-z0-9-]+', p['slug']), p['slug']
        datetime.date.fromisoformat(p['date'])
    return sorted(posts, key=lambda p: p['date'], reverse=True)

CARD = '''        <article class="flex flex-col rounded-2xl border border-slate2-100 bg-white p-8">
          <p class="text-sm text-slate2-500">{cat} · <time datetime="{date}">{fdate}</time></p>
          <h3 class="mt-2 font-serif text-2xl leading-snug"><a href="{href}" class="hover:text-copper-600">{title}</a></h3>
          <p class="mt-3 flex-1 leading-relaxed text-navy-800">{summary}</p>
          <a href="{href}" class="mt-5 inline-block text-sm font-semibold text-copper-600 hover:text-copper-500">Leer comentario →</a>
        </article>'''

def card(p, prefix):
    return CARD.format(cat=esc(p['category']), date=p['date'], fdate=fecha(p['date']), href=f'{prefix}{p["slug"]}/',
                       title=esc(p['title']), summary=esc(p['summary']))

EMPTY = '''        <div class="rounded-2xl border border-dashed border-copper-500/40 bg-white p-10 md:col-span-3">
          <p class="font-serif text-2xl">Primeros comentarios, muy pronto</p>
          <p class="mt-3 max-w-2xl leading-relaxed text-navy-800">Análisis breves sobre actualidad empresarial, mercado inmobiliario y fallos judiciales relevantes para empresas y personas. Nuevas publicaciones dos veces por semana.</p>
        </div>'''

def section(posts):
    cards = '\n'.join(card(p, 'blog/') for p in posts[:3]) if posts else EMPTY
    more = ('\n      <a href="blog/" class="mt-10 inline-block rounded-full border border-navy-900 px-6 py-3 text-sm font-semibold hover:bg-navy-900 hover:text-white">Ver todos los comentarios →</a>' if posts else '')
    return f'''<!-- BLOG:START -->
<section id="blog" class="bg-paper py-24 sm:py-28">
  <div class="mx-auto max-w-6xl px-6 lg:px-8">
    <p class="eyebrow text-copper-600">Blog · Comentarios</p>
    <h2 class="mt-4 font-serif text-4xl">Derecho, empresa y mercado inmobiliario</h2>
    <p class="mt-4 max-w-3xl text-lg leading-relaxed text-navy-800">Comentarios de Sebastián Salinas Fuenzalida sobre noticias de negocios, el mercado inmobiliario y fallos judiciales con impacto para empresas y personas.</p>
    <div class="mt-12 grid gap-6 md:grid-cols-3">
{cards}
    </div>{more}
  </div>
</section>
<!-- BLOG:END -->
'''

def page(title, desc, canonical, body, ld, prefix):
    return f'''<!DOCTYPE html>
<html lang="es-CL">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="author" content="Sebastián Salinas Fuenzalida" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{BASE}assets/og-sebastian-salinas-fuenzalida.jpg" />
  <meta property="og:locale" content="es_CL" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="theme-color" content="#06132A" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="alternate" type="application/rss+xml" title="Blog de Sebastián Salinas Fuenzalida" href="/blog/feed.xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{prefix}assets/styles.css" />
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body class="bg-paper font-sans text-navy-900 antialiased">
<header class="border-b border-white/10 bg-navy-950">
  <nav class="mx-auto flex max-w-4xl items-center justify-between px-6 py-4" aria-label="Principal">
    <a href="{prefix}" class="font-serif text-xl text-white">S. Salinas <span class="text-copper-400">F.</span></a>
    <div class="flex items-center gap-6 text-sm text-slate2-300">
      <a class="hover:text-white" href="{prefix}blog/">Blog</a>
      <a class="hover:text-white" href="{prefix}#contacto">Contacto</a>
    </div>
  </nav>
</header>
<main class="mx-auto max-w-3xl px-6 py-16 sm:py-20">
{body}
</main>
<footer class="bg-navy-950 border-t border-white/10 py-8 text-center text-xs text-slate2-500">
  <p>© 2026 Sebastián Salinas Fuenzalida · Abogado · Santiago, Chile · <a class="underline hover:text-copper-300" href="{prefix}">sebastiansalinas.cl</a></p>
</footer>
</body>
</html>
'''

AUTHOR = {"@type": "Person", "@id": PERSON, "name": "Sebastián Salinas Fuenzalida", "url": BASE}

def build_index(posts):
    items = '\n'.join(card(p, '') for p in posts) if posts else EMPTY
    body = f'''  <p class="eyebrow text-copper-600">Blog · Comentarios</p>
  <h1 class="mt-4 font-serif text-5xl leading-tight">Derecho, empresa y mercado inmobiliario</h1>
  <p class="mt-6 text-lg leading-relaxed text-navy-800">Comentarios de Sebastián Salinas Fuenzalida, abogado y cofundador de Dunora, sobre actualidad de negocios, mercado inmobiliario y fallos judiciales relevantes para empresas y personas.</p>
  <div class="mt-12 grid gap-6">
{items}
  </div>'''
    ld = {"@context": "https://schema.org", "@type": "Blog", "@id": BASE + "blog/#blog", "url": BASE + "blog/",
          "name": "Blog de Sebastián Salinas Fuenzalida", "inLanguage": "es-CL", "author": AUTHOR, "publisher": AUTHOR,
          "blogPost": [{"@type": "BlogPosting", "headline": p['title'], "url": f'{BASE}blog/{p["slug"]}/', "datePublished": iso(p['date'])} for p in posts]}
    os.makedirs(f'{ROOT}/blog', exist_ok=True)
    open(f'{ROOT}/blog/index.html', 'w', encoding='utf-8').write(
        page('Blog · Sebastián Salinas Fuenzalida', 'Comentarios de Sebastián Salinas Fuenzalida sobre derecho empresarial, mercado inmobiliario y fallos judiciales.',
             BASE + 'blog/', body, ld, '../'))

def build_post(p):
    srcs = ''
    if p.get('sources'):
        lis = '\n'.join(f'      <li><a href="{esc(s["url"])}" target="_blank" rel="noopener" class="text-copper-600 underline hover:text-copper-500">{esc(s["title"])}</a></li>' for s in p['sources'])
        srcs = f'''
  <aside class="mt-12 rounded-2xl border border-slate2-100 bg-white p-6">
    <p class="eyebrow text-copper-600">Fuentes</p>
    <ul class="mt-3 list-disc space-y-1 pl-5 text-sm">
{lis}
    </ul>
  </aside>'''
    body = f'''  <article>
    <p class="text-sm text-slate2-500"><a href="../" class="hover:text-copper-600">← Blog</a> · {esc(p['category'])} · <time datetime="{p['date']}">{fecha(p['date'])}</time></p>
    <h1 class="mt-4 font-serif text-4xl leading-tight sm:text-5xl">{esc(p['title'])}</h1>
    <p class="mt-6 text-xl leading-relaxed text-navy-800">{esc(p['summary'])}</p>
    <p class="mt-6 text-sm text-slate2-500">Por <a href="../../" class="font-semibold text-navy-900 hover:text-copper-600">Sebastián Salinas Fuenzalida</a> · Abogado</p>
    <div class="prose-post mt-10 space-y-5 text-lg leading-relaxed text-navy-800">
{p['body_html']}
    </div>{srcs}
  </article>'''
    url = f'{BASE}blog/{p["slug"]}/'
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "@id": url + "#post", "mainEntityOfPage": url, "url": url,
          "headline": p['title'], "description": p['summary'], "datePublished": iso(p['date']), "dateModified": iso(p.get('modified', p['date'])),
          "inLanguage": "es-CL", "articleSection": p['category'], "author": AUTHOR, "publisher": AUTHOR,
          "isPartOf": {"@id": BASE + "blog/#blog"}, "image": BASE + "assets/og-sebastian-salinas-fuenzalida.jpg"}
    if p.get('sources'):
        ld["citation"] = [s['url'] for s in p['sources']]
    os.makedirs(f'{ROOT}/blog/{p["slug"]}', exist_ok=True)
    open(f'{ROOT}/blog/{p["slug"]}/index.html', 'w', encoding='utf-8').write(
        page(f'{p["title"]} · Sebastián Salinas Fuenzalida', p['summary'], url, body, ld, '../../'))

def build_feed(posts):
    items = ''.join(f'''
  <item><title>{esc(p["title"])}</title><link>{BASE}blog/{p["slug"]}/</link><guid>{BASE}blog/{p["slug"]}/</guid>
    <pubDate>{datetime.date.fromisoformat(p["date"]).strftime("%a, %d %b %Y")} 12:00:00 -0300</pubDate><description>{esc(p["summary"])}</description></item>''' for p in posts)
    open(f'{ROOT}/blog/feed.xml', 'w', encoding='utf-8').write(f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Blog de Sebastián Salinas Fuenzalida</title><link>{BASE}blog/</link>
  <description>Comentarios sobre derecho empresarial, mercado inmobiliario y fallos judiciales.</description><language>es-cl</language>{items}
</channel></rss>
''')

def update_index(posts):
    p = f'{ROOT}/index.html'
    h = open(p, encoding='utf-8').read()
    sec = section(posts)
    if '<!-- BLOG:START -->' in h:
        h = re.sub(r'<!-- BLOG:START -->.*?<!-- BLOG:END -->\n', sec, h, flags=re.S)
    else:
        h = h.replace('<section id="contacto"', sec + '\n<section id="contacto"', 1)
    nav = '      <li><a class="hover:text-white" href="#blog">Blog</a></li>\n'
    if 'href="#blog">Blog<' not in h:
        h = h.replace('      <li><a class="hover:text-white" href="#contacto">Contacto</a></li>', nav + '      <li><a class="hover:text-white" href="#contacto">Contacto</a></li>', 1)
    open(p, 'w', encoding='utf-8').write(h)

def update_sitemap(posts):
    p = f'{ROOT}/sitemap.xml'
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'  <url>\n    <loc>https://www\.sebastiansalinas\.cl/blog/.*?</url>\n', '', s, flags=re.S)
    today = datetime.date.today().isoformat()
    last = posts[0]['date'] if posts else today
    new = f'  <url>\n    <loc>{BASE}blog/</loc>\n    <lastmod>{last}</lastmod>\n  </url>\n'
    new += ''.join(f'  <url>\n    <loc>{BASE}blog/{x["slug"]}/</loc>\n    <lastmod>{x.get("modified", x["date"])}</lastmod>\n  </url>\n' for x in posts)
    s = s.replace('</urlset>', new + '</urlset>')
    open(p, 'w', encoding='utf-8').write(s)

def update_llms(posts):
    p = f'{ROOT}/llms.txt'
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'\n## Blog.*?(?=\n## |\Z)', '', t, flags=re.S)
    lines = '\n'.join(f'- {x["date"]} · {x["title"]}: {BASE}blog/{x["slug"]}/' for x in posts) or '- (primeras publicaciones próximamente)'
    block = f'\n## Blog (comentarios de Sebastián Salinas Fuenzalida)\nAnálisis sobre actualidad empresarial, mercado inmobiliario y fallos judiciales. Índice: {BASE}blog/\n{lines}\n'
    t = t.replace('\n## Perfiles', block + '\n## Perfiles', 1) if '\n## Perfiles' in t else t + block
    open(p, 'w', encoding='utf-8').write(t)

if __name__ == '__main__':
    posts = load_posts()
    if os.path.isdir(f'{ROOT}/blog'):
        for d in os.listdir(f'{ROOT}/blog'):
            if os.path.isdir(f'{ROOT}/blog/{d}') and d not in {x['slug'] for x in posts}:
                shutil.rmtree(f'{ROOT}/blog/{d}')
    update_index(posts); build_index(posts)
    for x in posts: build_post(x)
    build_feed(posts); update_sitemap(posts); update_llms(posts)
    print(f'blog ok · {len(posts)} artículos')
