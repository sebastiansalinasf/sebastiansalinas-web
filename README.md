# www.sebastiansalinas.cl

Sitio personal de Sebastián Salinas Fuenzalida (español + inglés), publicado en Netlify desde este repositorio.

- `site/` — sitio publicado (HTML, CSS compilado, imágenes, llms.txt, robots.txt, sitemap.xml).
- `content/posts.json` — artículos del blog (fuente de verdad).
- `tools/` — scripts: `build_blog.py` (blog), `make_en.py` (versión en inglés), `publicar.sh` (reconstruye todo).

## Publicar un cambio
1. Editar `site/index.html` (español) o agregar un artículo en `content/posts.json`.
2. Ejecutar `tools/publicar.sh`.
3. Commit + push a `main`: Netlify publica automáticamente en www.sebastiansalinas.cl.

## Reglas de contenido
- No inventar datos: todo hecho debe estar respaldado por documentos o fuentes públicas.
- Blog: análisis propio; citar y enlazar las fuentes; no copiar texto de medios.
- No publicar RUT, domicilios ni datos de clientes.
- Mantener sincronizado el texto visible de las preguntas frecuentes con su JSON-LD.
