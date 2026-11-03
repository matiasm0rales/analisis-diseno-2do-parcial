"""Genera resumen.html (con índice lateral) y resumen.pdf a partir de resumen.md.

Uso (desde la raíz del repositorio):
    python3 herramientas/armar_resumen.py

Requiere: markdown-it-py y playwright (con Chromium instalado), y poppler-utils (pdftotext) para numerar el índice del PDF.
"""
import base64
import datetime
import html
import math
import pathlib
import re
import subprocess
import sys
import tempfile
import unicodedata

from markdown_it import MarkdownIt

RAIZ = pathlib.Path(__file__).resolve().parent.parent
HERR = pathlib.Path(__file__).resolve().parent
MD = RAIZ / "resumen.md"
SALIDA_HTML = RAIZ / "resumen.html"
SALIDA_PDF = RAIZ / "resumen.pdf"

TEMAS = {"1": "petri", "2": "bi", "3": "dm", "4": "bd", "5": "rep"}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]

# ---------------------------------------------------------------- iconos (los mismos trazos que la plataforma)
ICONOS = {
    "file-text": '<path d="M14 3H6.5A1.5 1.5 0 0 0 5 4.5v15A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V8z"/><path d="M14 3v5h5M8.5 13h7M8.5 17h7M8.5 9h2"/>',
    "layers": '<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="M2.5 12.5 12 17.5l9.5-5M2.5 16.5 12 21.5l9.5-5"/>',
    "contrast": '<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "alert": '<path d="M12 3.5 2.8 19.5h18.4z"/><path d="M12 10v4.2M12 17.2v.1"/>',
    "arrow-up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "filter": '<path d="M4 5h16l-6.5 7.5V19l-3 1.5v-8z"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11M4.5 6h.1M4.5 12h.1M4.5 18h.1"/>',
}


def sprite():
    s = "".join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONOS.items())
    return f'<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">{s}</svg>'


def ic(nombre):
    return f"<svg class='i' aria-hidden='true'><use href='#i-{nombre}'/></svg>"


# ---------------------------------------------------------------- diagramas de las redes de los ejemplos
class Red:
    def __init__(self, ancho, alto):
        self.ancho, self.alto = ancho, alto
        self.nodos, self.partes = {}, []

    def lugar(self, n, x, y, marcas=0, etiqueta=None, pos="abajo"):
        self.nodos[n] = ("c", x, y, 20, 20)
        self.partes.append(("lugar", n, x, y, marcas, etiqueta or n, pos))

    def trans(self, n, x, y, vertical=True, etiqueta=None, pos=None):
        w, h = (12, 44) if vertical else (44, 12)
        self.nodos[n] = ("r", x, y, w / 2, h / 2)
        self.partes.append(("trans", n, x, y, w, h, etiqueta or n, pos or ("arriba" if vertical else "derecha")))

    def arco(self, a, b, control=None):
        self.partes.append(("arco", a, b, control))

    @staticmethod
    def _borde(nodo, hacia):
        tipo, x, y, hw, hh = nodo
        dx, dy = hacia[0] - x, hacia[1] - y
        d = math.hypot(dx, dy) or 1
        if tipo == "c":
            return x + dx / d * hw, y + dy / d * hw
        t = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
        return x + dx * t, y + dy * t

    def svg(self, titulo):
        o = [f'<svg class="net" viewBox="0 0 {self.ancho} {self.alto}" role="img" aria-label="{html.escape(titulo)}">',
             '<defs><marker id="flecha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M0 0 10 5 0 10z" class="punta"/></marker></defs>']
        for p in self.partes:
            if p[0] != "arco":
                continue
            _, a, b, c = p
            na, nb = self.nodos[a], self.nodos[b]
            pa = self._borde(na, c or nb[1:3])
            pb = self._borde(nb, c or na[1:3])
            # deja un pequeño espacio antes de la punta
            ux, uy = (pb[0] - (c or pa)[0]), (pb[1] - (c or pa)[1])
            d = math.hypot(ux, uy) or 1
            pb = (pb[0] - ux / d * 3, pb[1] - uy / d * 3)
            if c:
                o.append(f'<path class="arc" d="M{pa[0]:.1f} {pa[1]:.1f} Q{c[0]} {c[1]} {pb[0]:.1f} {pb[1]:.1f}" marker-end="url(#flecha)"/>')
            else:
                o.append(f'<path class="arc" d="M{pa[0]:.1f} {pa[1]:.1f} L{pb[0]:.1f} {pb[1]:.1f}" marker-end="url(#flecha)"/>')
        for p in self.partes:
            if p[0] == "lugar":
                _, n, x, y, m, et, pos = p
                o.append(f'<circle class="shd" cx="{x + 3}" cy="{y + 3}" r="20"/><circle class="pl" cx="{x}" cy="{y}" r="20"/>')
                if m:
                    o.append(f'<circle class="tok" cx="{x}" cy="{y}" r="5.5"/>')
                ty = y + 40 if pos == "abajo" else y - 29
                o.append(f'<text class="lab" x="{x}" y="{ty}" text-anchor="middle">{et}</text>')
            elif p[0] == "trans":
                _, n, x, y, w, h, et, pos = p
                o.append(f'<rect class="shd" x="{x - w / 2 + 3}" y="{y - h / 2 + 3}" width="{w}" height="{h}" rx="2"/>'
                         f'<rect class="tr" x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="2"/>')
                if pos == "arriba":
                    o.append(f'<text class="lab t" x="{x}" y="{y - h / 2 - 9}" text-anchor="middle">{et}</text>')
                elif pos == "abajo":
                    o.append(f'<text class="lab t" x="{x}" y="{y + h / 2 + 22}" text-anchor="middle">{et}</text>')
                elif pos == "izquierda":
                    o.append(f'<text class="lab t" x="{x - w / 2 - 10}" y="{y + 6}" text-anchor="end">{et}</text>')
                else:
                    o.append(f'<text class="lab t" x="{x + w / 2 + 10}" y="{y + 6}">{et}</text>')
        o.append("</svg>")
        return "".join(o)


def red_ejemplo_1():
    r = Red(600, 330)
    r.lugar("p1", 55, 150, 1)
    r.trans("t1", 140, 150)
    r.lugar("p2", 230, 85)
    r.lugar("p3", 230, 225)
    r.trans("t2", 320, 85)
    r.trans("t3", 320, 225, pos="abajo")
    r.lugar("p5", 410, 85)
    r.lugar("p4", 410, 225)
    r.trans("t4", 320, 22, vertical=False, pos="derecha")
    r.trans("t5", 520, 150, pos="derecha")
    for a, b in [("p1", "t1"), ("t1", "p2"), ("t1", "p3"), ("p2", "t2"), ("t2", "p5"), ("p3", "t3"),
                 ("t3", "p4"), ("p5", "t4"), ("t4", "p2"), ("p5", "t5"), ("p4", "t5")]:
        r.arco(a, b)
    r.arco("t5", "p1", control=(290, 410))
    return r.svg("Red del Ejemplo 1")


def red_ejemplo_2():
    r = Red(580, 170)
    r.lugar("p1", 50, 115, 1)
    r.trans("t1", 140, 115, pos="abajo")
    r.lugar("p2", 230, 115)
    r.trans("t2", 320, 115, pos="abajo")
    r.lugar("p3", 410, 115)
    r.trans("t3", 500, 115, pos="abajo")
    for a, b in [("p1", "t1"), ("t1", "p2"), ("p2", "t2"), ("t2", "p3"), ("p3", "t3")]:
        r.arco(a, b)
    r.arco("t2", "p1", control=(185, -10))
    return r.svg("Red del Ejemplo 2")


def red_ejemplo_3():
    r = Red(560, 350)
    r.lugar("a1", 110, 50, 1, pos="arriba")
    r.trans("t1", 110, 135, vertical=False, pos="izquierda")
    r.lugar("b1", 110, 220)
    r.trans("t2", 110, 305, vertical=False, pos="izquierda")
    r.lugar("s", 280, 178, 1)
    r.lugar("a2", 450, 50, 1, pos="arriba")
    r.trans("t3", 450, 135, vertical=False, pos="derecha")
    r.lugar("b2", 450, 220)
    r.trans("t4", 450, 305, vertical=False, pos="derecha")
    for a, b in [("a1", "t1"), ("s", "t1"), ("t1", "b1"), ("b1", "t2"), ("t2", "s"),
                 ("a2", "t3"), ("s", "t3"), ("t3", "b2"), ("b2", "t4"), ("t4", "s")]:
        r.arco(a, b)
    r.arco("t2", "a1", control=(10, 178))
    r.arco("t4", "a2", control=(550, 178))
    return r.svg("Red del Ejemplo 3")


DIAGRAMAS = {
    "Ejemplo 1 —": (red_ejemplo_1, "Red del Ejemplo 1. M0 = (1, 0, 0, 0, 0): una marca en p1."),
    "Ejemplo 2 —": (red_ejemplo_2, "Red del Ejemplo 2. M0 = (1, 0, 0). t3 es una transición sumidero."),
    "Ejemplo 3 —": (red_ejemplo_3, "Red del Ejemplo 3. M0 = (1, 0, 1, 0, 1): el lugar s es el semáforo."),
}


def cubierta_red():
    """Red decorativa de la portada: un lugar por tema que alimenta la transición del parcial."""
    o = ['<svg class="net cover-net" viewBox="-40 0 460 300" aria-hidden="true">',
         '<defs><marker id="fl2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0 0 10 5 0 10z" class="punta"/></marker></defs>']
    lugares = [("Petri", 70, 45, "var(--petri)"), ("BI", 70, 115, "var(--bi)"), ("Minería", 70, 185, "var(--dm)"),
               ("Big Data", 70, 255, "var(--bd)")]
    for _, x, y, _c in lugares:
        o.append(f'<path class="arc" d="M{x + 26} {y} C 190 {y} 190 150 {262} 150" marker-end="url(#fl2)"/>')
    o.append('<path class="arc" d="M282 150 L 336 150" marker-end="url(#fl2)"/>')
    for n, x, y, c in lugares:
        o.append(f'<circle class="shd" cx="{x + 4}" cy="{y + 4}" r="24"/><circle class="pl" cx="{x}" cy="{y}" r="24" style="fill:{c}"/>'
                 f'<circle class="tok tok-l" cx="{x}" cy="{y}" r="6"/><text class="lab" x="{x - 36}" y="{y + 6}" text-anchor="end">{n}</text>')
    o.append('<rect class="shd" x="267" y="112" width="16" height="80" rx="3"/><rect class="tr" x="264" y="109" width="16" height="80" rx="3"/>'
             '<text class="lab" x="272" y="92" text-anchor="middle">Parcial</text>')
    o.append('<circle class="shd" cx="370" cy="154" r="26"/><circle class="pl" cx="366" cy="150" r="26"/>'
             '<text class="lab" x="366" y="200" text-anchor="middle">Aprobado</text>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- markdown → html
def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def texto_plano(h):
    return html.unescape(re.sub(r"<[^>]+>", "", h)).strip()


def convertir(md_texto):
    lineas = md_texto.splitlines()
    titulo = lineas[0].lstrip("# ").strip()
    # el bloque inicial (título, datos del grupo y la primera línea divisoria) va a la portada / encabezado
    i = 1
    meta = []
    while i < len(lineas) and not lineas[i].startswith("## "):
        if lineas[i].strip() and lineas[i].strip() != "---":
            meta.append(lineas[i].strip())
        i += 1
    cuerpo_md = "\n".join(lineas[i:])

    md = MarkdownIt("commonmark", {"html": False, "typographer": False}).enable("table")
    h = md.render(cuerpo_md)

    h = re.sub(r"<hr\s*/?>\s*", "", h)

    # tablas con contenedor para desplazamiento horizontal
    h = h.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")

    # árboles de alcanzabilidad
    h = h.replace("<pre><code>", '<pre class="tree"><code>')

    # marcas de correcto / incorrecto
    h = h.replace("❌", '<span class="mk no">Incorrecto</span>').replace("✅", '<span class="mk si">Correcto</span>')

    # citas especiales
    def cita(m):
        dentro = m.group(1)
        txt = texto_plano(dentro)
        if txt.startswith("En una frase"):
            dentro = re.sub(r"<strong>En una frase:</strong>\s*", "", dentro, count=1)
            dentro = re.sub(r"^((?:\s|<[^>]+>)*)(\w)", lambda x: x.group(1) + x.group(2).upper(), dentro, count=1)
            return f'<div class="lead"><span class="side">En una frase</span>{dentro}</div>'
        return f'<div class="warnline">{ic("alert")}<div>{dentro}</div></div>'

    h = re.sub(r"<blockquote>\s*(.*?)\s*</blockquote>", cita, h, flags=re.S)

    # diagramas después del título de cada ejemplo
    for clave, (fn, pie) in DIAGRAMAS.items():
        patron = re.compile(r"(<p><strong>" + re.escape(clave) + r"[^<]*</strong></p>)")
        h = patron.sub(lambda m: f'<div class="ej">{m.group(1)}<figure class="netfig">{fn()}<figcaption>{pie}</figcaption></figure></div>', h, count=1)

    # encabezados: ids, números y armado de secciones
    toc = []
    secciones = []
    actual = None

    partes = re.split(r"(<h[234]>.*?</h[234]>)", h, flags=re.S)
    for parte in partes:
        m = re.match(r"<h([234])>(.*?)</h\1>", parte, flags=re.S)
        if not m:
            if actual is not None:
                actual["html"].append(parte)
            continue
        nivel, contenido = int(m.group(1)), m.group(2)
        plano = texto_plano(contenido)
        num = None
        mm = re.match(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$", plano)
        if mm:
            num, resto = mm.group(1), mm.group(2)
        else:
            resto = plano
        ident = "s-" + num.replace(".", "-") if num else slug(resto)
        if nivel == 2:
            tag = None
            mt = re.match(r"^(.*?)\s*\((.*)\)$", resto)
            if mt:
                resto, tag = mt.group(1), mt.group(2).replace(", entra", " · entra")
            tema = TEMAS.get(num, "gen")
            actual = {"id": ident, "num": num, "titulo": resto, "tag": tag, "tema": tema, "html": []}
            secciones.append(actual)
            toc.append({"nivel": 2, "id": ident, "num": num, "titulo": resto, "tema": tema, "hijos": []})
        else:
            etiqueta = html.escape(resto)
            n_html = f'<span class="n">{num}</span>' if num else ""
            actual["html"].append(f'<h{nivel} id="{ident}">{n_html}{etiqueta}</h{nivel}>')
            if nivel == 3 or (nivel == 4 and num):
                toc[-1]["hijos"].append({"nivel": nivel, "id": ident, "num": num, "titulo": resto})

    cuerpo = []
    for s in secciones:
        num = f'<span class="num">{s["num"]}</span>' if s["num"] else ""
        tag = f'<span class="tag">{html.escape(s["tag"])}</span>' if s["tag"] else ""
        cuerpo.append(
            f'<section class="sec t-{s["tema"]}" id="{s["id"]}">'
            f'<div class="sec-head">{num}<h2>{html.escape(s["titulo"])}</h2>{tag}</div>'
            + "".join(s["html"]) + "</section>")
    return titulo, meta, "".join(cuerpo), toc


# ---------------------------------------------------------------- estilos
def fuentes_embebidas():
    def b64(nombre):
        return base64.b64encode((HERR / "fuentes" / nombre).read_bytes()).decode()
    return (
        f"@font-face{{font-family:'Host Grotesk';font-weight:300 800;src:url(data:font/woff2;base64,{b64('HostGrotesk.woff2')}) format('woff2')}}"
        f"@font-face{{font-family:'Instrument Sans';font-weight:400 700;font-style:normal;src:url(data:font/woff2;base64,{b64('InstrumentSans.woff2')}) format('woff2')}}"
        f"@font-face{{font-family:'Instrument Sans';font-weight:400 700;font-style:italic;src:url(data:font/woff2;base64,{b64('InstrumentSans-Italic.woff2')}) format('woff2')}}"
        f"@font-face{{font-family:'JetBrains Mono';font-weight:500;src:url(data:font/woff2;base64,{b64('JetBrainsMono.woff2')}) format('woff2')}}")


CSS_BASE = r"""
:root{
  --dp-color-ground:#fffdf5; --dp-color-panel:#ffffff; --dp-color-ink:#253044; --dp-color-outline:#252b3a;
  --dp-color-accent:#6434df; --dp-color-accent-secondary:#ff78c5; --dp-color-accent-warm:#ffd05b; --dp-color-accent-fresh:#9bf1cd;
  --dp-color-field-soft:#e9fff5; --dp-color-selection:#f1ebff; --dp-color-rule-muted:#b8b6c5;
  --dp-typography-display:"PlayfulGeometricDisplay","Host Grotesk",ui-sans-serif,system-ui,sans-serif;
  --dp-typography-reading:"PlayfulGeometricReading","Instrument Sans",ui-sans-serif,system-ui,sans-serif;
  --mono:"JetBrains Mono","DejaVu Sans Mono",ui-monospace,Menlo,Consolas,monospace;
  --dp-typography-reading-compact:16px; --dp-typography-label:14px; --dp-typography-metadata:13px; --dp-typography-reading-leading:1.65;
  --dp-radius-corner:17px; --dp-border-outline-width:3px; --dp-border-detail-width:2px; --dp-motion-interaction:180ms;
  --muted:#5a6273; --on-accent:#ffffff; --bad-soft:#ffe8f4; --warn-soft:#fff4d2;
  --petri:#6434df; --bi:#22b97f; --dm:#f0b020; --bd:#ff78c5;
  --petri-soft:#f1ebff; --bi-soft:#e2f9ef; --dm-soft:#fff4d2; --bd-soft:#ffe8f4;
  --shadow-ink:var(--dp-color-outline);
}
*{box-sizing:border-box}
html{background:var(--dp-color-ground)}
body{margin:0;background:var(--dp-color-ground);color:var(--dp-color-ink);font:400 var(--dp-typography-reading-compact)/var(--dp-typography-reading-leading) var(--dp-typography-reading);-webkit-text-size-adjust:100%}
.i{width:1.1em;height:1.1em;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;vertical-align:-.18em;flex:none}
h1,h2,h3,h4{font-family:var(--dp-typography-display);letter-spacing:-.02em;color:var(--dp-color-ink)}
a{color:var(--dp-color-accent)}
strong{font-weight:700}
em{font-style:italic}
code{font-family:var(--mono);font-size:.9em}

/* colores por tema */
.t-petri{--c:var(--petri);--cs:var(--petri-soft)}
.t-bi{--c:var(--bi);--cs:var(--bi-soft)}
.t-dm{--c:var(--dm);--cs:var(--dm-soft)}
.t-bd{--c:var(--bd);--cs:var(--bd-soft)}
.t-rep{--c:var(--dp-color-accent-fresh);--cs:var(--dp-color-field-soft)}
.t-gen{--c:var(--dp-color-accent-warm);--cs:var(--warn-soft)}

/* secciones */
.sec{margin:0 0 72px}
.sec-head{display:flex;align-items:center;flex-wrap:wrap;gap:12px 16px;padding:0 0 18px;margin:0 0 26px;border-bottom:var(--dp-border-outline-width) solid var(--dp-color-outline)}
.sec-head h2{margin:0;font-size:clamp(30px,4vw,42px);line-height:1.05;font-weight:800}
.sec-head .num{flex:none;width:54px;height:54px;border-radius:50%;background:var(--c);color:#14101f;border:var(--dp-border-outline-width) solid var(--dp-color-outline);box-shadow:4px 4px 0 var(--shadow-ink);display:inline-flex;align-items:center;justify-content:center;font:800 26px/1 var(--dp-typography-display)}
.t-petri .sec-head .num{color:#fff}
.tag{display:inline-flex;align-items:center;gap:7px;font-size:var(--dp-typography-metadata);font-weight:700;background:var(--dp-color-panel);border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:999px;padding:2px 11px 2px 7px;white-space:nowrap}
.tag::before{content:"";width:11px;height:11px;border-radius:50%;background:var(--c);border:2px solid var(--dp-color-outline)}
h3{font-size:24px;line-height:1.2;font-weight:800;margin:46px 0 14px;display:flex;align-items:baseline;gap:10px}
h4{font-size:19px;line-height:1.25;font-weight:800;margin:30px 0 10px;display:flex;align-items:baseline;gap:9px}
h3 .n,h4 .n{flex:none;font:800 14px/1 var(--dp-typography-display);letter-spacing:0;background:var(--cs);border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:999px;padding:5px 10px;position:relative;top:-3px}
h4 .n{font-size:12.5px;padding:4px 8px}
p{margin:0 0 14px}
ul,ol{margin:0 0 16px;padding-left:24px}
li{margin:4px 0}
li::marker{color:var(--c);font-weight:800}
li>ul,li>ol{margin:4px 0 6px}

/* recuadros */
.lead{position:relative;background:var(--dp-color-panel);border:var(--dp-border-outline-width) solid var(--dp-color-outline);border-radius:var(--dp-radius-corner);padding:26px 22px 14px;margin:6px 0 30px;box-shadow:6px 6px 0 var(--c);font-size:18px}
.lead p{margin:0 0 10px}
.lead .side{position:absolute;top:-16px;left:20px;font:700 var(--dp-typography-label)/1 var(--dp-typography-reading);background:var(--dp-color-accent-warm);color:#2a2410;border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:10px 10px 4px 4px;padding:7px 12px}
.warnline{display:flex;gap:12px;align-items:flex-start;background:var(--warn-soft);border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:var(--dp-radius-corner);padding:14px 18px;margin:18px 0 22px;font-size:15px}
.warnline .i{margin-top:3px;color:var(--dp-color-ink)}
.warnline p{margin:0}

/* tablas */
.tbl{overflow-x:auto;margin:14px 0 22px;background:var(--dp-color-panel);border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:14px;box-shadow:4px 4px 0 var(--c)}
table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5}
th,td{text-align:left;padding:9px 12px;border-bottom:var(--dp-border-detail-width) solid var(--dp-color-rule-muted);vertical-align:top}
th{font-size:var(--dp-typography-label);font-weight:700;background:var(--cs);border-bottom:var(--dp-border-detail-width) solid var(--dp-color-outline)}
tr:last-child td{border-bottom:0}
td:first-child{font-weight:600}

/* árboles */
pre.tree{background:var(--dp-color-panel);border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:14px;padding:14px 18px;overflow-x:auto;margin:12px 0 20px;font:500 13.5px/1.55 var(--mono);box-shadow:4px 4px 0 var(--c)}
pre.tree code{font-size:inherit}

/* correcto / incorrecto */
.mk{display:inline-block;font:700 12px/1 var(--dp-typography-reading);letter-spacing:.02em;text-transform:uppercase;border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:999px;padding:4px 8px 3px;margin:0 4px 0 0;position:relative;top:-1px;color:var(--dp-color-ink)}
.mk.no{background:var(--bad-soft)}
.mk.si{background:var(--dp-color-field-soft);margin-left:6px}

/* diagramas */
.netfig{margin:14px 0 24px;background:var(--dp-color-panel);border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:14px;padding:16px 16px 10px;box-shadow:4px 4px 0 var(--c)}
.netfig figcaption{font-size:var(--dp-typography-metadata);color:var(--muted);margin-top:6px}
.net{width:100%;height:auto;display:block;overflow:visible;max-height:340px}
.net .pl{fill:var(--dp-color-panel);stroke:var(--dp-color-outline);stroke-width:3}
.net .shd{fill:var(--shadow-ink)}
.net .arc{stroke:var(--dp-color-outline);stroke-width:2;fill:none}
.net .punta{fill:var(--dp-color-outline)}
.net .tr{fill:var(--dp-color-accent-warm);stroke:var(--dp-color-outline);stroke-width:3}
.net .tok{fill:var(--dp-color-outline)}
.net text{font-family:var(--dp-typography-display);fill:var(--dp-color-ink)}
.net .lab{font-size:17px;font-weight:800}
.net .lab.t{font-size:15px;font-weight:700}
"""

CSS_PANTALLA = r"""
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --dp-color-ground:#171b26; --dp-color-panel:#222838; --dp-color-ink:#eef0f8; --dp-color-outline:#aab2cc;
  --dp-color-accent:#9b7bff; --dp-color-field-soft:#16352b; --dp-color-selection:#2e2650; --dp-color-rule-muted:#4a5168;
  --muted:#aeb5c8; --on-accent:#14101f; --bad-soft:#3d2034; --warn-soft:#3a3220; --petri:#9b7bff; --shadow-ink:#05070c;
  --petri-soft:#2e2650; --bi-soft:#16352b; --dm-soft:#3a3220; --bd-soft:#3d2034; } }
:root[data-theme="dark"]{
  --dp-color-ground:#171b26; --dp-color-panel:#222838; --dp-color-ink:#eef0f8; --dp-color-outline:#aab2cc;
  --dp-color-accent:#9b7bff; --dp-color-field-soft:#16352b; --dp-color-selection:#2e2650; --dp-color-rule-muted:#4a5168;
  --muted:#aeb5c8; --on-accent:#14101f; --bad-soft:#3d2034; --warn-soft:#3a3220; --petri:#9b7bff; --shadow-ink:#05070c;
  --petri-soft:#2e2650; --bi-soft:#16352b; --dm-soft:#3a3220; --bd-soft:#3d2034; }
html{scroll-padding-top:calc(var(--hh,78px) + 18px);scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto} *{transition:none!important}}
:focus-visible{outline:3px solid var(--dp-color-accent);outline-offset:4px;border-radius:8px}
button,input{font:inherit;color:inherit}

/* encabezado (igual que la plataforma) */
header#hdr{position:sticky;top:0;z-index:20;background:var(--dp-color-ground);border-bottom:var(--dp-border-outline-width) solid var(--dp-color-outline)}
.htop{max-width:1320px;margin:0 auto;padding:14px 24px;display:flex;align-items:center;gap:10px}
.htop h1{flex:1;margin:0;font-size:22px;line-height:1.1;font-weight:800;min-width:0}
.htop h1 small{display:block;margin-top:4px;font:500 var(--dp-typography-metadata)/1.3 var(--dp-typography-reading);color:var(--muted);letter-spacing:0}
.hbtn{display:inline-flex;align-items:center;gap:6px;background:var(--dp-color-panel);border:var(--dp-border-detail-width) solid var(--dp-color-outline);color:var(--dp-color-ink);border-radius:999px;padding:6px 13px;cursor:pointer;text-decoration:none;font-size:var(--dp-typography-label);font-weight:600;white-space:nowrap;box-shadow:3px 3px 0 var(--shadow-ink);transition:transform var(--dp-motion-interaction),box-shadow var(--dp-motion-interaction)}
.hbtn:hover{transform:translate(-1px,-1px);box-shadow:4px 4px 0 var(--shadow-ink)}
.hbtn:active{transform:translate(2px,2px);box-shadow:1px 1px 0 var(--shadow-ink)}
.hbtn.pri{background:var(--dp-color-accent);color:var(--on-accent)}
#idxBtn{display:none}

/* disposición */
.layout{max-width:1320px;margin:0 auto;padding:0 24px;display:grid;grid-template-columns:300px minmax(0,1fr);gap:48px}
main.doc{padding:40px 0 120px;max-width:860px;min-width:0}

/* índice lateral */
aside#side{position:sticky;top:var(--hh,78px);align-self:start;height:calc(100vh - var(--hh,78px));padding:28px 0 24px;display:flex;flex-direction:column}
.side-card{display:flex;flex-direction:column;min-height:0;flex:1;background:var(--dp-color-panel);border:var(--dp-border-outline-width) solid var(--dp-color-outline);border-radius:var(--dp-radius-corner);box-shadow:6px 6px 0 var(--dp-color-accent)}
.side-top{padding:16px 16px 12px;border-bottom:var(--dp-border-detail-width) solid var(--dp-color-outline)}
.side-top b{display:flex;align-items:center;gap:8px;font:800 17px/1.1 var(--dp-typography-display);margin-bottom:10px}
.find{display:flex;align-items:center;gap:8px;border:var(--dp-border-detail-width) solid var(--dp-color-outline);background:var(--dp-color-ground);border-radius:999px;padding:5px 12px}
.find input{border:0;background:none;outline:none;width:100%;font-size:14px;padding:2px 0}
.find .i{color:var(--muted)}
nav.toc{overflow-y:auto;padding:10px 10px 16px;flex:1;overscroll-behavior:contain;scrollbar-width:thin}
nav.toc ul{list-style:none;margin:0;padding:0}
nav.toc li{margin:0}
nav.toc li::marker{content:none}
nav.toc a{display:flex;gap:8px;align-items:baseline;text-decoration:none;color:var(--muted);border-radius:10px;padding:5px 8px;font-size:14px;line-height:1.35;border:2px solid transparent}
nav.toc a:hover{color:var(--dp-color-ink);background:var(--dp-color-selection)}
nav.toc a .n{flex:none;font:700 12px/1.6 var(--dp-typography-display);color:var(--muted);min-width:26px}
nav.toc .l2>a{color:var(--dp-color-ink);font:800 15px/1.25 var(--dp-typography-display);letter-spacing:-.01em;margin-top:8px;align-items:center}
nav.toc .l2>a::before{content:"";flex:none;width:12px;height:12px;border-radius:50%;background:var(--c);border:2px solid var(--dp-color-outline)}
nav.toc .l2>a .n{display:none}
nav.toc .sub{margin:2px 0 4px 8px;padding-left:10px;border-left:2px solid var(--dp-color-rule-muted)}
nav.toc .l4>a{padding-left:22px;font-size:13px}
nav.toc a[aria-current="true"]{color:var(--dp-color-ink);background:var(--cs);border-color:var(--dp-color-outline);font-weight:700}
nav.toc a[aria-current="true"] .n{color:var(--dp-color-ink)}
nav.toc .vacio{padding:10px 8px;color:var(--muted);font-size:14px}
.side-foot{padding:10px 16px 14px;border-top:var(--dp-border-detail-width) solid var(--dp-color-outline);font-size:var(--dp-typography-metadata);color:var(--muted)}
.prog{height:12px;background:var(--dp-color-ground);border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:999px;overflow:hidden;margin-top:6px}
.prog span{display:block;height:100%;width:0;background:var(--dp-color-accent-warm);border-right:var(--dp-border-detail-width) solid var(--dp-color-outline)}

/* portada de pantalla */
.intro{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:28px;align-items:center;margin:0 0 64px}
.intro h2{font-size:clamp(42px,6vw,76px);line-height:.95;letter-spacing:-.035em;margin:0 0 16px;font-weight:800}
.intro p{margin:0 0 8px;font-size:17px;color:var(--muted)}
.intro .temas{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.intro .temas a{text-decoration:none;color:var(--dp-color-ink)}

#topBtn{position:fixed;right:22px;bottom:22px;z-index:15;opacity:0;pointer-events:none;transition:opacity var(--dp-motion-interaction)}
#topBtn.on{opacity:1;pointer-events:auto}
.velo{display:none}

@media (max-width:1100px){ .layout{grid-template-columns:260px minmax(0,1fr);gap:32px} }
@media (max-width:900px){
  #idxBtn{display:inline-flex}
  .layout{display:block;padding:0 18px}
  aside#side{position:fixed;left:0;top:var(--hh,70px);bottom:auto;align-self:auto;height:calc(100dvh - var(--hh,70px));width:min(340px,88vw);z-index:30;padding:14px;transform:translateX(-105%);transition:transform .25s}
  body.idx aside#side{transform:none}
  body.idx .velo{display:block;position:fixed;inset:var(--hh,70px) 0 0 0;background:rgba(10,12,20,.35);z-index:25}
  main.doc{padding-top:26px}
  .intro{grid-template-columns:1fr}
  .intro .net{max-width:360px}
  .hbtn .lbl{display:none}
  .hbtn{padding:7px 9px}
  .htop{padding:10px 18px}
  .htop h1{font-size:18px}
  .htop h1 small.upd{display:none}
}
@media (max-width:520px){ h3{font-size:21px} .sec-head .num{width:46px;height:46px;font-size:22px} .lead{font-size:17px} table{font-size:14px} }
"""

CSS_IMPRESION = r"""
@page{size:A4;margin:15mm 14mm 17mm;background:var(--dp-color-ground);
  @bottom-left{content:"Análisis y Diseño de Sistemas II · Resumen del 2do parcial";font:500 8pt 'Instrument Sans',sans-serif;color:#5a6273}
  @bottom-right{content:"Página " counter(page) " de " counter(pages);font:600 8pt 'Instrument Sans',sans-serif;color:#5a6273}}
@page portada{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
html,body{background:var(--dp-color-ground)}
body{font-size:10.4pt;line-height:1.55;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.portada{page:portada;height:297mm;width:210mm;padding:22mm 20mm 18mm;display:flex;flex-direction:column;break-after:page;position:relative;overflow:hidden}
.portada .kick{display:inline-flex;align-self:flex-start;font:700 10pt/1 'Instrument Sans';background:var(--dp-color-accent-warm);border:2px solid var(--dp-color-outline);border-radius:10px 10px 4px 4px;padding:7px 12px;box-shadow:3px 3px 0 var(--shadow-ink)}
.portada h1{font-size:50pt;line-height:.95;letter-spacing:-.035em;font-weight:800;margin:14mm 0 6mm}
.portada .sub{font-size:13pt;color:var(--muted);max-width:140mm;margin:0}
.portada .cover-net{width:150mm;max-height:none;margin:12mm 0 0 18mm}
.portada .tarjetas{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:auto}
.portada .tj{background:var(--dp-color-panel);border:3px solid var(--dp-color-outline);border-radius:14px;padding:4mm 5mm;box-shadow:4px 4px 0 var(--c)}
.portada .tj b{display:block;font:800 13pt/1.15 'Host Grotesk';margin-bottom:1.5mm}
.portada .tj span{font-size:9pt;color:var(--muted);line-height:1.4;display:block}
.portada .pie{margin-top:9mm;padding-top:4mm;border-top:3px solid var(--dp-color-outline);font-size:9pt;color:var(--muted);display:flex;justify-content:space-between;gap:10mm}
.indice{break-after:page}
.indice h2{font-size:28pt;margin:0 0 7mm;font-weight:800;padding-bottom:4mm;border-bottom:3px solid var(--dp-color-outline)}
.indice ol{list-style:none;padding:0;margin:0}
.indice li::marker{content:none}
.indice .i2{margin:4.2mm 0 1.2mm}
.indice .i2>a{display:flex;align-items:center;gap:3mm;font:800 12.5pt/1.2 'Host Grotesk';color:var(--dp-color-ink);text-decoration:none}
.indice .i2>a::before{content:"";width:10px;height:10px;border-radius:50%;background:var(--c);border:2px solid var(--dp-color-outline);flex:none}
.indice .i3 a{display:flex;gap:2.5mm;font-size:9.6pt;line-height:1.5;color:var(--dp-color-ink);text-decoration:none;padding-left:7mm}
.indice a .n{color:var(--muted);font-weight:700;min-width:9mm}
.indice a .t{flex:none;max-width:120mm}
.indice a .dots{flex:1;border-bottom:1.5px dotted var(--dp-color-rule-muted);margin:0 2mm .35em}
.indice a .pg{flex:none;font-weight:700;font-variant-numeric:tabular-nums}
.indice .i2>a .t{max-width:none}
.sec{break-before:page;margin:0}
.indice + .sec{break-before:auto}
.sec-head{margin-bottom:6mm}
.sec-head h2{font-size:26pt}
h3{font-size:15.5pt;margin:8mm 0 3mm;break-after:avoid}
h4{font-size:12.5pt;margin:5.5mm 0 2.5mm;break-after:avoid}
h3 .n{font-size:9.5pt;padding:3.5px 8px}
h4 .n{font-size:8.5pt}
p,li{orphans:3;widows:3}
.lead{font-size:12pt;box-shadow:4px 4px 0 var(--c);break-inside:avoid}
.tbl{overflow:visible;box-shadow:3px 3px 0 var(--c)}
table{font-size:9.2pt}
th,td{padding:5px 8px}
tr,.netfig,pre.tree,.warnline,.ej{break-inside:avoid}
thead{display:table-header-group}
pre.tree{font-size:8.8pt;box-shadow:3px 3px 0 var(--c)}
.netfig{box-shadow:3px 3px 0 var(--c)}
.net{max-height:62mm}
.mk{font-size:7.5pt}
a{color:inherit;text-decoration:none}
"""

JS = r"""
(function(){
  var PFX="ads2p_";
  function load(k,d){try{var v=localStorage.getItem(PFX+k);return v===null?d:JSON.parse(v);}catch(e){return d;}}
  function save(k,v){try{localStorage.setItem(PFX+k,JSON.stringify(v));}catch(e){}}
  var root=document.documentElement;
  var t=load("theme",null); if(t) root.setAttribute("data-theme",t);
  document.getElementById("themeBtn").onclick=function(){
    var dark=root.getAttribute("data-theme")?root.getAttribute("data-theme")==="dark":window.matchMedia("(prefers-color-scheme: dark)").matches;
    root.setAttribute("data-theme",dark?"light":"dark"); save("theme",root.getAttribute("data-theme"));
  };
  var hdr=document.getElementById("hdr");
  function hh(){root.style.setProperty("--hh",hdr.offsetHeight+"px");}
  hh(); window.addEventListener("resize",hh);

  /* índice en pantallas chicas */
  var body=document.body, idxBtn=document.getElementById("idxBtn"), toc=document.getElementById("toc");
  function abrir(on){body.classList.toggle("idx",on);idxBtn.setAttribute("aria-expanded",on?"true":"false");
    if(on){var a=toc.querySelector("a[aria-current]");if(a)setTimeout(function(){toc.scrollTop+=a.getBoundingClientRect().top-toc.getBoundingClientRect().top-toc.clientHeight/3;},300);}}
  idxBtn.onclick=function(){abrir(!body.classList.contains("idx"));};
  document.querySelector(".velo").onclick=function(){abrir(false);};
  document.addEventListener("keydown",function(e){if(e.key==="Escape")abrir(false);});

  /* resaltar la sección que se está leyendo */
  var links={};
  toc.querySelectorAll("a[href^='#']").forEach(function(a){links[a.getAttribute("href").slice(1)]=a;
    a.addEventListener("click",function(){if(window.innerWidth<=900)abrir(false);});});
  var heads=[].slice.call(document.querySelectorAll("main .sec, main h3[id], main h4[id]"));
  var marcado=null;
  function actualizar(){
    var y=(hdr.offsetHeight||70)+40, act=null;
    for(var i=0;i<heads.length;i++){ if(heads[i].getBoundingClientRect().top<=y) act=heads[i]; else break; }
    var id=act?act.id:null;
    if(id&&!links[id]){ var s=act.closest?act.closest(".sec"):null; id=s?s.id:null; }
    if(id!==marcado){
      if(marcado&&links[marcado]) links[marcado].removeAttribute("aria-current");
      marcado=id;
      if(id&&links[id]){ var a=links[id]; a.setAttribute("aria-current","true");
        var r=a.getBoundingClientRect(), c=toc.getBoundingClientRect();
        if(r.top<c.top+20||r.bottom>c.bottom-20) toc.scrollTop+=r.top-c.top-c.height/3; }
    }
    var max=document.documentElement.scrollHeight-window.innerHeight;
    document.getElementById("progBar").style.width=(max>0?Math.min(100,window.scrollY*100/max):0)+"%";
    document.getElementById("topBtn").classList.toggle("on",window.scrollY>900);
  }
  var pend=false;
  window.addEventListener("scroll",function(){if(!pend){pend=true;requestAnimationFrame(function(){pend=false;actualizar();});}},{passive:true});
  window.addEventListener("load",actualizar); actualizar();
  document.getElementById("topBtn").onclick=function(){window.scrollTo({top:0});};

  /* filtrar el índice */
  var q=document.getElementById("q"), vacio=document.getElementById("vacio");
  function norm(s){return s.normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();}
  q.addEventListener("input",function(){
    var v=norm(q.value.trim()), hay=0;
    toc.querySelectorAll("li.l2").forEach(function(li2){
      var a2=li2.querySelector(":scope>a"), m2=!v||norm(a2.textContent).indexOf(v)>-1, alguna=false;
      li2.querySelectorAll("li").forEach(function(li){var ok=!v||m2||norm(li.textContent).indexOf(v)>-1;li.hidden=!ok;if(ok)alguna=true;});
      li2.hidden=!(m2||alguna); if(!li2.hidden)hay++;
    });
    vacio.hidden=hay>0;
  });
})();
"""


# ---------------------------------------------------------------- armado
def toc_html(toc):
    o = ['<ul>']
    for s in toc:
        o.append(f'<li class="l2 t-{s["tema"]}"><a href="#{s["id"]}">{html.escape(s["titulo"])}</a>')
        if s["hijos"]:
            o.append('<ul class="sub">')
            for h in s["hijos"]:
                n = f'<span class="n">{h["num"]}</span>' if h["num"] else '<span class="n"></span>'
                o.append(f'<li class="l{h["nivel"]}"><a href="#{h["id"]}">{n}<span>{html.escape(h["titulo"])}</span></a></li>')
            o.append("</ul>")
        o.append("</li>")
    o.append("</ul>")
    return "".join(o)


def fecha_actualizacion():
    ahora = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
    return ahora, f"{ahora:%d/%m/%Y, %H:%M}"


def armar_html(titulo, meta, cuerpo, toc):
    _, upd = fecha_actualizacion()
    chips = "".join(
        f'<a class="tag t-{s["tema"]}" href="#{s["id"]}">{html.escape(s["titulo"])}</a>'
        for s in toc if s["num"] in ("1", "2", "3", "4"))
    intro = (f'<section class="intro"><div><h2>Resumen del 2do parcial</h2>'
             f'<p>{html.escape(meta[0]) if meta else ""}</p>'
             f'<p>Big Data (tema 10) queda como material para el final.</p>'
             f'<div class="temas">{chips}</div></div><div>{cubierta_red()}</div></section>')
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Resumen del 2do parcial, Análisis y Diseño de Sistemas II</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Host+Grotesk:wght@500..800&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>{CSS_BASE}{CSS_PANTALLA}</style>
</head>
<body>
{sprite()}
<header id="hdr">
  <div class="htop">
    <button class="hbtn" id="idxBtn" aria-expanded="false" aria-controls="side" title="Mostrar el índice">{ic("list")}<span class="lbl">Índice</span></button>
    <h1>Resumen del 2do parcial<small>Análisis y Diseño de Sistemas II, temas 6 a 10</small><small class="upd">Última actualización: {upd}</small></h1>
    <a class="hbtn" href="index.html" title="Volver a la práctica">{ic("layers")}<span class="lbl">Práctica</span></a>
    <a class="hbtn" href="resumen.pdf" target="_blank" rel="noopener" title="Abrir el resumen en PDF">{ic("file-text")}<span class="lbl">PDF</span></a>
    <button class="hbtn" id="themeBtn" title="Cambiar entre tema claro y oscuro">{ic("contrast")}<span class="lbl">Tema</span></button>
  </div>
</header>
<div class="velo"></div>
<div class="layout">
  <aside id="side" aria-label="Índice del resumen">
    <div class="side-card">
      <div class="side-top"><b>{ic("list")}Índice</b>
        <label class="find">{ic("filter")}<input id="q" type="search" placeholder="Filtrar temas" aria-label="Filtrar el índice"></label></div>
      <nav class="toc" id="toc">{toc_html(toc)}<p class="vacio" id="vacio" hidden>No hay secciones con ese nombre.</p></nav>
      <div class="side-foot">Leído<div class="prog"><span id="progBar"></span></div></div>
    </div>
  </aside>
  <main class="doc" id="main">
    {intro}
    {cuerpo}
  </main>
</div>
<button class="hbtn pri" id="topBtn" title="Volver arriba">{ic("arrow-up")}<span class="lbl">Arriba</span></button>
<script>{JS}</script>
</body>
</html>
"""


def armar_impresion(titulo, meta, cuerpo, toc, paginas=None):
    ahora, _ = fecha_actualizacion()
    fecha = f"{MESES[ahora.month - 1].capitalize()} de {ahora.year}"
    resumen_tema = {
        "1": "Elementos, definición formal, propiedades, subclases, árbol de alcanzabilidad, máquina de testigos, método matricial y modelos de redes",
        "2": "Definición, beneficios, componentes, ROI, modelo de negocio, KPI, modelo de datos, ETL, datawarehouse, OLAP y herramientas",
        "3": "Definición, KDD y sus etapas, CRISP-DM y SEMMA, tareas, técnicas y evaluación",
        "4": "3 V, Big Analytics, MAD, Hadoop, megatendencias y comparación con BI y minería",
    }
    tarjetas = "".join(
        f'<div class="tj t-{s["tema"]}"><b>{s["num"]} · {html.escape(s["titulo"])}</b><span>{resumen_tema[s["num"]]}</span></div>'
        for s in toc if s["num"] in resumen_tema)
    portada = (f'<section class="portada"><span class="kick">Resumen del 2do parcial</span>'
               f'<h1>Análisis y<br>Diseño de<br>Sistemas II</h1>'
               f'<p class="sub">Redes de Petri, <i>Business Intelligence</i> y Minería de datos para el parcial. Big Data (tema 10) queda como material para el final.</p>'
               f'{cubierta_red()}<div class="tarjetas">{tarjetas}</div>'
               f'<div class="pie"><span>{html.escape(meta[0]) if meta else ""}</span><span>{fecha}</span></div></section>')

    def pg(ident):
        return str(paginas.get(ident, "")) if paginas else "00"

    filas = []
    for s in toc:
        t = html.escape(s["titulo"])
        n = f'{s["num"]}. ' if s["num"] else ""
        filas.append(f'<li class="i2 t-{s["tema"]}"><a href="#{s["id"]}"><span class="t">{n}{t}</span><span class="dots"></span><span class="pg">{pg(s["id"])}</span></a>')
        hijos = [h for h in s["hijos"] if h["nivel"] == 3]
        if hijos:
            filas.append("<ol>")
            for h in hijos:
                filas.append(f'<li class="i3"><a href="#{h["id"]}"><span class="n">{h["num"] or ""}</span><span class="t">{html.escape(h["titulo"])}</span><span class="dots"></span><span class="pg">{pg(h["id"])}</span></a></li>')
            filas.append("</ol>")
        filas.append("</li>")
    indice = f'<section class="indice"><h2>Índice</h2><ol>{"".join(filas)}</ol></section>'
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Resumen del 2do parcial — Análisis y Diseño de Sistemas II</title>
<style>{fuentes_embebidas()}{CSS_BASE}{CSS_IMPRESION}</style></head>
<body>{sprite()}{portada}<main class="doc">{indice}{cuerpo}</main></body></html>"""


def paginas_de(pdf, toc):
    """Busca en qué página empieza cada sección y subsección (para el índice del PDF)."""
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    n = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    textos = []
    for p in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), str(pdf), "-"], capture_output=True, text=True).stdout
        textos.append(re.sub(r"\s+", " ", t))
    res = {}
    # en la primera pasada el índice tiene "00" como número de página: se busca después de esas páginas
    desde = 1
    while desde < n and textos[desde].count(" 00") >= 5:
        desde += 1
    for s in toc:
        buscado = s["titulo"]
        for i in range(desde, n):
            if buscado in textos[i]:
                res[s["id"]] = i + 1
                desde = i
                break
        inicio = res.get(s["id"], desde + 1) - 1
        for h in s["hijos"]:
            if h["nivel"] != 3:
                continue
            buscado = re.sub(r"\s+", " ", f'{h["num"]} {h["titulo"]}')[:34]
            for i in range(inicio, n):
                if buscado in textos[i]:
                    res[h["id"]] = i + 1
                    inicio = i
                    break
    return res


def imprimir(html_txt, destino):
    from playwright.sync_api import sync_playwright
    tmp = pathlib.Path(tempfile.mkdtemp()) / "resumen_impresion.html"
    tmp.write_text(html_txt, encoding="utf-8")
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(400)
        pg.pdf(path=str(destino), prefer_css_page_size=True, print_background=True, outline=True, tagged=True)
        b.close()


def main():
    titulo, meta, cuerpo, toc = convertir(MD.read_text(encoding="utf-8"))
    SALIDA_HTML.write_text(armar_html(titulo, meta, cuerpo, toc), encoding="utf-8")
    print("HTML:", SALIDA_HTML, SALIDA_HTML.stat().st_size, "bytes")
    if "--sin-pdf" in sys.argv:
        return
    imprimir(armar_impresion(titulo, meta, cuerpo, toc), SALIDA_PDF)
    paginas = paginas_de(SALIDA_PDF, toc)
    imprimir(armar_impresion(titulo, meta, cuerpo, toc, paginas), SALIDA_PDF)
    faltan = [s["id"] for s in toc if s["id"] not in paginas]
    print("PDF:", SALIDA_PDF, SALIDA_PDF.stat().st_size, "bytes; secciones sin página:", faltan or "ninguna")


if __name__ == "__main__":
    main()
