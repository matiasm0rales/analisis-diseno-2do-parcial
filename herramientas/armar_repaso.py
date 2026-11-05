"""Genera repaso.html (presentación de repaso) a partir de repaso.md.

Las definiciones ({{def:Término}}) se toman de los recuadros "¿Qué es?" de resumen.md,
así cada concepto tiene una sola definición en todo el material.

Uso: python3 herramientas/armar_repaso.py
Requiere: markdown-it-py.
"""
import html
import re
import sys

from markdown_it import MarkdownIt

import armar_resumen as base

RAIZ = base.RAIZ
MD = RAIZ / "repaso.md"
SALIDA = RAIZ / "repaso.html"
TEMAS = {"petri", "bi", "dm", "bd", "rep", "gen"}


def definiciones():
    defs = {}
    for linea in (RAIZ / "resumen.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"> \*\*¿Qué es\? · (.+?)\.\*\* (.*)$", linea)
        if m:
            defs[m.group(1)] = linea
    return defs


def buscar_def(defs, clave):
    for termino, linea in defs.items():
        if termino.startswith(clave):
            return linea
    sys.exit(f"No hay definición en resumen.md para: {clave}")


def caja(dentro):
    m = re.match(r"\s*<p><strong>¿Qué es\? · (.*?)\.</strong>\s*", dentro, flags=re.S)
    if not m:
        return f'<div class="warnline">{base.ic("alert")}<div>{dentro}</div></div>'
    return (f'<div class="def"><div class="def-h"><span class="side">¿Qué es?</span>'
            f'<span class="def-t">{m.group(1)}</span></div><p>{dentro[m.end():]}</div>')


def armar_diapositivas(texto):
    defs = definiciones()
    md = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table")
    diapos = []
    for bloque in re.split(r"\n---\n", texto.strip()):
        lineas = bloque.strip().splitlines()
        tema = "gen"
        if lineas and lineas[0].startswith("@"):
            tema = lineas.pop(0)[1:].strip()
            assert tema in TEMAS, tema
        cuerpo = "\n".join(lineas)
        cuerpo = re.sub(r"^\{\{def:(.+?)\}\}$", lambda m: buscar_def(defs, m.group(1)), cuerpo, flags=re.M)
        portada = cuerpo.lstrip().startswith("# ")
        titulo = re.search(r"^#{1,2} (.+)$", cuerpo, flags=re.M).group(1).strip()
        h = md.render(cuerpo)
        h = h.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
        h = h.replace("❌", '<span class="mk no">Incorrecto</span>').replace("✅", '<span class="mk si">Correcto</span>')
        h = re.sub(r"<blockquote>\s*(.*?)\s*</blockquote>", lambda m: caja(m.group(1)), h, flags=re.S)
        diapos.append({"tema": tema, "portada": portada, "titulo": base.texto_plano(md.renderInline(titulo)), "html": h})
    return diapos


CSS = r"""
html,body{height:100%}
body{overflow:hidden;display:flex;flex-direction:column}
.bar{flex:none;display:flex;align-items:center;gap:10px;padding:10px 18px;border-bottom:var(--dp-border-outline-width) solid var(--dp-color-outline);background:var(--dp-color-ground)}
.bar .t{font:800 17px/1.1 var(--dp-typography-display);margin-right:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bar .t small{display:block;font:500 var(--dp-typography-metadata)/1.3 var(--dp-typography-reading);color:var(--muted)}
.cnt{font:700 var(--dp-typography-label)/1 var(--mono);color:var(--muted);white-space:nowrap}
.hbtn{display:inline-flex;align-items:center;gap:6px;background:var(--dp-color-panel);border:var(--dp-border-detail-width) solid var(--dp-color-outline);color:var(--dp-color-ink);border-radius:999px;padding:6px 13px;cursor:pointer;text-decoration:none;font-size:var(--dp-typography-label);font-weight:600;white-space:nowrap;box-shadow:3px 3px 0 var(--shadow-ink);transition:transform var(--dp-motion-interaction),box-shadow var(--dp-motion-interaction)}
.hbtn:hover{transform:translate(-1px,-1px);box-shadow:4px 4px 0 var(--shadow-ink)}
.hbtn:active{transform:translate(2px,2px);box-shadow:1px 1px 0 var(--shadow-ink)}
.hbtn.pri{background:var(--dp-color-accent);color:var(--on-accent)}
.hbtn[disabled]{opacity:.35;pointer-events:none}
.deck{flex:1;position:relative;min-height:0}
.slide{position:absolute;inset:0;display:none;overflow:auto;padding:28px 22px 96px}
.slide.on{display:block;animation:in .22s ease-out}
@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.card{max-width:1060px;margin:0 auto;background:var(--dp-color-panel);border:var(--dp-border-outline-width) solid var(--dp-color-outline);border-radius:22px;box-shadow:8px 8px 0 var(--c);padding:26px 34px 18px;font-size:18px}
.card h2{font-size:clamp(26px,3.2vw,36px);line-height:1.1;font-weight:800;margin:0 0 18px;padding-bottom:14px;border-bottom:var(--dp-border-detail-width) solid var(--dp-color-rule-muted);display:flex;align-items:center;gap:12px}
.card h2::before{content:"";flex:none;width:16px;height:16px;border-radius:50%;background:var(--c);border:2px solid var(--dp-color-outline)}
.card table{font-size:16px}
.card .def{margin:12px 0 16px}
.card .def p{font-size:17px}
.slide.portada.on{display:flex;align-items:center;justify-content:center}
.portada .card{margin:auto;background:var(--cs);text-align:center;padding:48px 40px 36px;max-width:820px}
.portada h1{font-size:clamp(40px,6vw,68px);line-height:1;font-weight:800;margin:0 0 16px}
.portada p{font-size:19px}
details{background:var(--cs);border:var(--dp-border-detail-width) solid var(--dp-color-outline);border-radius:14px;padding:10px 16px;margin:0 0 10px}
summary{cursor:pointer;font-weight:700}
details[open] summary{margin-bottom:6px}
.nav{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);display:flex;gap:10px;z-index:5}
.prog{position:fixed;left:0;bottom:0;height:6px;background:var(--dp-color-accent);transition:width .2s}
.idx{position:fixed;inset:0;z-index:10;background:rgba(10,12,20,.55);display:none;align-items:flex-start;justify-content:center;padding:4vh 16px}
.idx.on{display:flex}
.idx .box{background:var(--dp-color-ground);border:var(--dp-border-outline-width) solid var(--dp-color-outline);border-radius:22px;box-shadow:8px 8px 0 var(--shadow-ink);max-width:760px;width:100%;max-height:92vh;overflow:auto;padding:20px 24px}
.idx h2{font-size:24px;margin:0 0 10px;display:flex;justify-content:space-between;align-items:center}
.idx ol{list-style:none;padding:0;margin:0}
.idx li{margin:0}
.idx a{display:flex;gap:10px;align-items:baseline;padding:6px 10px;border-radius:10px;color:var(--dp-color-ink);text-decoration:none}
.idx a:hover,.idx a.cur{background:var(--cs)}
.idx a .n{font:700 12px/1 var(--mono);color:var(--muted);min-width:24px}
.idx li.sec a{font-weight:800;margin-top:8px}
.idx li.sec a::before{content:"";width:11px;height:11px;border-radius:50%;background:var(--c);border:2px solid var(--dp-color-outline);flex:none;align-self:center}
@media (max-width:700px){
  .bar .lbl{display:none} .hbtn{padding:7px 9px}
  .card{padding:18px 18px 10px;font-size:16px;box-shadow:5px 5px 0 var(--c)}
  .card table{font-size:14px} .slide{padding:16px 12px 90px}
}
@media print{
  @page{size:A4 landscape;margin:12mm}
  html,body{height:auto;overflow:visible;display:block}
  .bar,.nav,.prog,.idx{display:none!important}
  .deck{position:static}
  .slide{display:block!important;position:static;overflow:visible;padding:0;break-after:page;animation:none}
  .card{box-shadow:none;font-size:12pt}
  details{display:block} details>*{display:block}
}
"""

JS = r"""
(function(){
  var PFX="ads2p_", root=document.documentElement;
  function load(k,d){try{var v=localStorage.getItem(PFX+k);return v===null?d:JSON.parse(v);}catch(e){return d;}}
  function save(k,v){try{localStorage.setItem(PFX+k,JSON.stringify(v));}catch(e){}}
  var th=load("theme",null); if(th) root.setAttribute("data-theme",th);
  function tema(){
    var dark=root.getAttribute("data-theme")?root.getAttribute("data-theme")==="dark":window.matchMedia("(prefers-color-scheme: dark)").matches;
    root.setAttribute("data-theme",dark?"light":"dark"); save("theme",root.getAttribute("data-theme"));
  }
  var S=[].slice.call(document.querySelectorAll(".slide")), n=S.length, i=0;
  var cnt=document.getElementById("cnt"), prog=document.getElementById("prog");
  var prev=document.getElementById("prev"), next=document.getElementById("next");
  var idx=document.getElementById("idx"), links=[].slice.call(idx.querySelectorAll("a"));
  function ir(k,noHash){
    i=Math.max(0,Math.min(n-1,k));
    S.forEach(function(s,j){s.classList.toggle("on",j===i);});
    S[i].scrollTop=0;
    cnt.textContent=(i+1)+" / "+n;
    prog.style.width=((i+1)/n*100)+"%";
    prev.disabled=i===0; next.disabled=i===n-1;
    links.forEach(function(a,j){a.classList.toggle("cur",j===i);});
    if(!noHash) history.replaceState(null,"","#"+(i+1));
    save("repaso_pos",i);
  }
  function abrir(on){idx.classList.toggle("on",on); if(on){var c=idx.querySelector("a.cur"); if(c) c.scrollIntoView({block:"center"});}}
  prev.onclick=function(){ir(i-1);}; next.onclick=function(){ir(i+1);};
  document.getElementById("idxBtn").onclick=function(){abrir(true);};
  document.getElementById("idxClose").onclick=function(){abrir(false);};
  document.getElementById("themeBtn").onclick=tema;
  idx.onclick=function(e){if(e.target===idx) abrir(false);};
  links.forEach(function(a,j){a.onclick=function(e){e.preventDefault(); ir(j); abrir(false);};});
  document.addEventListener("keydown",function(e){
    if(e.altKey||e.ctrlKey||e.metaKey) return;
    var k=e.key;
    if(idx.classList.contains("on")){ if(k==="Escape"||k==="i"||k==="I") abrir(false); return; }
    if(k==="ArrowRight"||k==="PageDown"||(k===" "&&!e.shiftKey)){e.preventDefault(); ir(i+1);}
    else if(k==="ArrowLeft"||k==="PageUp"||(k===" "&&e.shiftKey)){e.preventDefault(); ir(i-1);}
    else if(k==="Home"){ir(0);} else if(k==="End"){ir(n-1);}
    else if(k==="Escape"||k==="i"||k==="I"){abrir(true);}
    else if(k==="t"||k==="T"){tema();}
  });
  var x0=null,y0=null;
  document.addEventListener("touchstart",function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
  document.addEventListener("touchend",function(e){
    if(x0===null) return; var dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0;
    if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.5) ir(i+(dx<0?1:-1)); x0=null;
  },{passive:true});
  var h=parseInt(location.hash.slice(1),10);
  ir(h>0?h-1:load("repaso_pos",0),!(h>0));
})();
"""


def tema_oscuro():
    return "".join(re.findall(r"@media \(prefers-color-scheme:dark\)\{.*?\} \}|:root\[data-theme=\"dark\"\]\{.*?\}",
                              base.CSS_PANTALLA, flags=re.S))


def armar_html(diapos):
    slides, indice = [], []
    for k, d in enumerate(diapos, 1):
        cls = f"slide t-{d['tema']}" + (" portada" if d["portada"] else "")
        slides.append(f'<section class="{cls}" aria-label="Diapositiva {k}: {html.escape(d["titulo"])}"><div class="card">{d["html"]}</div></section>')
        li = "sec " if d["portada"] else ""
        indice.append(f'<li class="{li}t-{d["tema"]}"><a href="#{k}"><span class="n">{k}</span><span>{html.escape(d["titulo"])}</span></a></li>')
    ic = base.ic
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Repaso del 2do parcial, Análisis y Diseño de Sistemas II</title>
<style>{base.fuentes_embebidas()}{base.CSS_BASE}{tema_oscuro()}{CSS}</style>
</head>
<body>
{base.sprite()}
<header class="bar">
  <div class="t">Repaso del 2do parcial<small>Análisis y Diseño de Sistemas II · actualizado {base.fecha_actualizacion()[1]}</small></div>
  <span class="cnt" id="cnt"></span>
  <button class="hbtn" id="idxBtn" title="Ver todas las diapositivas (Esc)">{ic("list")}<span class="lbl">Índice</span></button>
  <a class="hbtn" href="resumen.html" title="Abrir el resumen completo">{ic("file-text")}<span class="lbl">Resumen</span></a>
  <a class="hbtn" href="index.html" title="Ir a la práctica">{ic("layers")}<span class="lbl">Práctica</span></a>
  <button class="hbtn" id="themeBtn" title="Cambiar entre tema claro y oscuro (T)">{ic("contrast")}<span class="lbl">Tema</span></button>
</header>
<main class="deck">{"".join(slides)}</main>
<nav class="nav" aria-label="Navegación">
  <button class="hbtn" id="prev" title="Anterior (←)">← <span class="lbl">Anterior</span></button>
  <button class="hbtn pri" id="next" title="Siguiente (→)"><span class="lbl">Siguiente</span> →</button>
</nav>
<div class="prog" id="prog"></div>
<div class="idx" id="idx" role="dialog" aria-label="Índice de diapositivas"><div class="box">
  <h2>Índice <button class="hbtn" id="idxClose" title="Cerrar (Esc)">{ic("x")}<span class="lbl">Cerrar</span></button></h2>
  <ol>{"".join(indice)}</ol>
</div></div>
<script>{JS}</script>
</body>
</html>
"""


def main():
    diapos = armar_diapositivas(MD.read_text(encoding="utf-8"))
    SALIDA.write_text(armar_html(diapos), encoding="utf-8")
    print("HTML:", SALIDA, SALIDA.stat().st_size, "bytes;", len(diapos), "diapositivas")


if __name__ == "__main__":
    main()
