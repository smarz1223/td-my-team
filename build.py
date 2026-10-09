"""
td-my-team: build.py

Reads data/data.json (written by fetch_data.py) and writes index.html.
Never edit index.html by hand. Change this file and rebuild. See SPEC.md.
"""

import json
import os

DATA_PATH = os.path.join("data", "data.json")
OUT_PATH = "index.html"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>The Morning Soft Dump</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8' shape-rendering='crispEdges'><rect x='1' y='3' width='6' height='2' fill='%23111'/><rect x='2' y='2' width='4' height='1' fill='%23333'/><rect x='2' y='5' width='4' height='1' fill='%23333'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#0e2557;
  --blue:#2350c4;
  --red:#d42a1e;
  --ice:#f5f8fc;
  --grid:#d3d9e3;
  --head:#e9eef6;
  --text:#1d2533;
  --soft:#5d6778;
  --good:99,190,123;
  --bad:248,105,107;
  --ui:"Segoe UI", Calibri, "Helvetica Neue", Arial, sans-serif;
  --pixel:"Press Start 2P", "Courier New", monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0; background:var(--ice); color:var(--text); font-family:var(--ui); font-size:14px; line-height:1.4;
  padding-bottom:env(safe-area-inset-bottom,0px)}
button{font:inherit; color:inherit}
:focus-visible{outline:2px solid var(--red); outline-offset:1px}

/* ---------- title bar (Blades of Steel) ---------- */
.titlebar{background:var(--navy); color:#fff; padding:calc(10px + env(safe-area-inset-top,0px)) 16px 10px; display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap}
.titlebar h1{margin:0; font-family:var(--pixel); font-weight:400; font-size:clamp(13px, 2.4vw, 20px); letter-spacing:1px; color:#eaf0ff; text-shadow:3px 3px 0 var(--red); display:flex; align-items:center; gap:12px}
.titlebar h1 svg{width:28px; height:28px; flex:none}
.meta{font-size:12.5px; color:#c9d4f0; text-align:right}
.meta b{color:#fff}
.rink{height:9px; background:
  linear-gradient(90deg, transparent calc(50% - 3px), var(--red) calc(50% - 3px), var(--red) calc(50% + 3px), transparent calc(50% + 3px)),
  linear-gradient(90deg, #fff 0 22%, var(--blue) 22% 24%, #fff 24% 76%, var(--blue) 76% 78%, #fff 78% 100%);
  border-bottom:1px solid var(--grid)}

/* ---------- controls ---------- */
.panel{background:#fff; border-bottom:1px solid var(--grid); padding:8px 16px; display:flex; flex-wrap:wrap; gap:8px 18px; align-items:flex-end; position:sticky; top:0; z-index:5}
.slicer{display:flex; flex-direction:column; gap:3px}
.slicer > span{font-size:11.5px; color:var(--soft); font-weight:600}
.btns{display:flex; flex-wrap:wrap; gap:3px}
.btns button{border:1px solid #b8c2d3; background:#fff; padding:3px 9px; border-radius:2px; cursor:pointer; font-size:13px; line-height:1.3}
.btns button:hover{border-color:var(--blue)}
.btns button[aria-pressed="true"]{background:var(--blue); border-color:var(--blue); color:#fff}
.pages button{font-family:var(--pixel); font-size:10px; padding:7px 10px}
.pages button[aria-pressed="true"]{background:var(--navy); border-color:var(--navy)}
.clear{border:0; background:none; color:var(--blue); text-decoration:underline; cursor:pointer; font-size:12.5px; padding:3px 0}

main{padding:10px 16px 30px}
.alert{background:#fde8e6; border:1px solid var(--red); color:#7d140d; padding:6px 10px; margin-bottom:10px; font-size:13px}
.alert ul{margin:2px 0 0; padding-left:18px}

/* ---------- replacement line ---------- */
details.line{margin-bottom:10px; background:#fff; border:1px solid var(--grid); padding:6px 10px}
details.line summary{cursor:pointer; font-weight:700}
details.line p{margin:4px 0 0; font-size:12px; color:var(--soft)}
.line table.grid{margin-top:6px; width:auto; min-width:360px}
.wireline{font-size:13px; margin:0 0 8px}

/* ---------- tables ---------- */
.wrap{overflow:auto; max-height:calc(100vh - 210px); border:1px solid var(--grid); background:#fff; margin-bottom:12px}
table.grid{border-collapse:separate; border-spacing:0; font-variant-numeric:tabular-nums; font-size:13px; width:100%}
.grid th,.grid td{padding:3px 7px; border-right:1px solid var(--grid); border-bottom:1px solid var(--grid); white-space:nowrap; text-align:right}
.grid thead th{position:sticky; top:0; background:var(--head); z-index:2; font-weight:700; font-size:12px}
.grid thead tr:nth-child(2) th{top:23px}
.grid th.sortable{cursor:pointer; user-select:none}
.grid th.sortable:hover{background:#dbe3f1}
.grid th .ar{color:var(--blue); font-size:10px; margin-left:3px}
.grid th.grp{text-align:center; background:#dde5f2; border-bottom:1px solid #b8c2d3}
.grid .l{text-align:left}
.grid td.name{position:sticky; left:0; background:#fff; z-index:1; font-weight:600; min-width:150px}
.grid thead th.name{left:0; z-index:3}
.grid tbody tr:hover td{box-shadow:inset 0 0 0 9999px rgba(35,80,196,.06)}
.grid .gs{border-left:2px solid #9fb0cc}
.dim{color:#8a93a3}
.tag{display:inline-block; font-size:10.5px; font-weight:700; padding:0 4px; border:1px solid currentColor; border-radius:2px; margin-left:4px}
.tag.red{color:var(--red)} .tag.grey{color:var(--soft)}
.note{display:inline-block; font-size:11px; font-weight:700; padding:1px 5px; margin-right:3px; border-radius:2px}
.n-replace{background:var(--red); color:#fff}
.n-poor{background:#fde2df; color:#8f1b12; border:1px solid #f1a69f}
.n-small{background:#eef1f6; color:var(--soft); border:1px solid #cbd3e0}
.n-nostarts{background:#eef1f6; color:var(--soft); border:1px solid #cbd3e0}
.star{color:#c08a00}
.why{font-size:11px; color:var(--red); font-weight:400}
.empty{padding:14px; color:var(--soft)}
h2.tt{font-size:13px; margin:12px 0 4px; color:var(--soft)}
.foot{font-size:12px; color:var(--soft); max-width:110ch}
[hidden]{display:none!important}

@media (max-width:700px){
  .panel{position:static}
  .wrap{max-height:none}
  .meta{text-align:left}
}
</style>
</head>
<body>
<header class="titlebar">
  <h1><svg viewBox="0 0 16 16" shape-rendering="crispEdges" aria-hidden="true">
    <rect x="11" y="1" width="2" height="9" fill="#c9a26b"/><rect x="9" y="10" width="4" height="2" fill="#c9a26b"/><rect x="5" y="12" width="6" height="2" fill="#eaf0ff"/>
    <rect x="1" y="12" width="3" height="1" fill="#111"/><rect x="0" y="13" width="5" height="1" fill="#333"/><rect x="1" y="14" width="3" height="1" fill="#111"/>
  </svg>The Morning Soft Dump</h1>
  <div class="meta"><b id="m-team"></b><br><span id="m-pull"></span></div>
</header>
<div class="rink" aria-hidden="true"></div>

<div class="panel" id="panel"></div>

<main>
  <div id="alert"></div>

  <section id="pg-team">
    <details class="line" open>
      <summary>The replacement line (points per game)</summary>
      <table class="grid" id="line"></table>
      <p id="line-fn"></p>
    </details>
    <div id="team-tables"></div>
    <p class="foot">
      <b>For me</b> = only games he started for you. <b>Season / Last 30 / Last 14</b> = every game he played.
      <b>+/- PPG</b> = points per game above or below the replacement line for that row's position. <b>+/- Pts</b> = +/- PPG times games played.
      Notes: <b>Replace?</b> = Last 30 more than <span id="f-rep"></span> pts under the line. <b>Poor performer</b> = Last 30 PPG under the line.
      <b>Small sample</b> = fewer than <span id="f-small"></span> starts for you. Color scales run against the largest value in each column of the rows shown.
    </p>
  </section>

  <section id="pg-wire" hidden>
    <p class="wireline" id="wireline"></p>
    <div id="wire-tables"></div>
    <p class="foot"><span class="star">&#9733;</span> = counts toward the replacement line. "Upgrade over" = your weakest active player at this position over the same window, and how many PPG this free agent would add.</p>
  </section>
</main>

<script>
const DATA = __DATA__;

/* ============ constants ============ */
const WINDOWS = ["season","l30","l14"];
const WIN = {forme:"For me", season:"Season", l30:"Last 30", l14:"Last 14"};
const POS_ORDER = {C:0, LW:1, RW:2, F:3, D:4, G:5};
const SK_STATS = [["G","G"],["A","A"],["+/-","+/-"],["PIM","PIM"],["PPP","PPP"],["SOG","SOG"],["TOI","TOI/G"]];
const G_STATS  = [["W","W"],["GA","GA"],["SV","SV"],["SHO","SHO"],["SVP","SV%"],["GAA","GAA"]];
const W = Object.assign({}, DATA.config.skater_weights, DATA.config.goalie_weights);
const LINE_ROWS = [["C","C"],["LW","LW"],["RW","RW"],["FWD","Forwards"],["D","D"],["G","G"]];

const S = {
  page:"team", view:"rep", vs:"pos", win:"l30", as:"raw",
  pos:new Set(), status:new Set(["Active","Injured"]), flags:new Set(),
  wpos:"C", wwin:"l30", wshow:false,
  sort:{}  // table id -> {col, dir}
};

/* ============ formatting ============ */
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const MINUS = "\u2212";
const isNum = x => x !== null && x !== undefined && !Number.isNaN(x);
const f1 = x => isNum(x) ? x.toFixed(1) : "";
const f2 = x => isNum(x) ? x.toFixed(2) : "";
const f0 = x => isNum(x) ? String(Math.round(x)) : "";
function sg(x, d=1){ if(!isNum(x)) return ""; const v=Number(x.toFixed(d)); if(v===0) return (0).toFixed(d); return (v>0?"+":MINUS)+Math.abs(v).toFixed(d); }
function toi(m){ if(!isNum(m)) return ""; const mm=Math.floor(m), ss=Math.round((m-mm)*60); return mm+":"+String(ss===60?59:ss).padStart(2,"0"); }
function svp(x){ return isNum(x) ? x.toFixed(3).replace(/^0/,"") : ""; }
function fmtDate(iso){ if(!iso) return ""; const [y,m,d]=iso.split("-").map(Number); return new Date(y,m-1,d).toLocaleDateString("en-US",{month:"short",day:"numeric"}); }

/* ============ color scales ============ */
const GOOD = "99,190,123", BAD = "248,105,107";
function mix(rgb, a){ return `rgba(${rgb},${Math.max(0,Math.min(1,a)).toFixed(3)})`; }
// diverging around 0, scaled to the largest absolute value in the column
function divergeBg(v, maxAbs){
  if(!isNum(v) || !maxAbs) return "";
  const t = v / maxAbs;
  return `background:${mix(t>=0 ? GOOD : BAD, Math.abs(t)*0.85)}`;
}
// 3-color scale: min red, median white, max green. dir=-1 flips (lower is better)
function scaleBg(v, st, dir){
  if(!isNum(v) || !st || st.max===st.min) return "";
  let t;
  if (v >= st.med) t = st.max===st.med ? 0 : (v-st.med)/(st.max-st.med);
  else t = st.med===st.min ? 0 : -(st.med-v)/(st.med-st.min);
  t *= dir;
  return `background:${mix(t>=0 ? GOOD : BAD, Math.abs(t)*0.8)}`;
}
function colStats(vals){
  const a = vals.filter(isNum).sort((x,y)=>x-y);
  if(!a.length) return null;
  const mid = Math.floor(a.length/2);
  return {min:a[0], max:a[a.length-1], med: a.length%2 ? a[mid] : (a[mid-1]+a[mid])/2,
          maxAbs: Math.max(Math.abs(a[0]), Math.abs(a[a.length-1]))};
}

/* ============ generic sortable grid ============
   cols: [{key, label, get(row)->sortable value, html(row, stats)->cell html, cls, group, color:"div"|"scale"|null, dir}]
*/
function renderGrid(id, cols, rows, defSort){
  const st = S.sort[id] || defSort || {col:null, dir:-1};
  if (st.col){
    const c = cols.find(c=>c.key===st.col);
    if (c){
      rows = rows.slice().sort((a,b)=>{
        const x=c.get(a), y=c.get(b);
        const xn = x===null||x===undefined||x==="", yn = y===null||y===undefined||y==="";
        if (xn && yn) return 0; if (xn) return 1; if (yn) return -1;
        if (typeof x === "string" || typeof y === "string") return st.dir*String(x).localeCompare(String(y));
        return st.dir*(x-y);
      });
    }
  }
  const stats = {};
  cols.forEach(c => { if (c.color) stats[c.key] = colStats(rows.map(r=>c.get(r))); });

  const hasGroups = cols.some(c=>c.group);
  let h = `<table class="grid"><thead>`;
  if (hasGroups){
    h += `<tr>`;
    let i = 0;
    while (i < cols.length){
      const g = cols[i].group; let n = 1;
      while (i+n < cols.length && cols[i+n].group === g) n++;
      if (g) h += `<th class="grp${i?" gs":""}" colspan="${n}">${esc(g)}</th>`;
      else for (let k=0;k<n;k++){ const c=cols[i+k]; h += headCell(id,c,st,true); }
      i += n;
    }
    h += `</tr><tr>`;
    cols.forEach(c => { if (c.group) h += headCell(id,c,st,false); });
    h += `</tr>`;
  } else {
    h += `<tr>` + cols.map(c=>headCell(id,c,st,false)).join("") + `</tr>`;
  }
  h += `</thead><tbody>`;
  if (!rows.length) h += `<tr><td class="l empty" colspan="${cols.length}">No rows match these slicers.</td></tr>`;
  for (const r of rows){
    h += `<tr>`;
    for (const c of cols){
      const v = c.get(r);
      let style = "";
      if (c.color === "div") style = divergeBg(v, stats[c.key] && stats[c.key].maxAbs);
      else if (c.color === "scale") style = scaleBg(v, stats[c.key], c.dir || 1);
      const cls = [c.cls||"", c.first?"gs":"", (c.dimIf && c.dimIf(r))?"dim":""].join(" ").trim();
      h += `<td${cls?` class="${cls}"`:""}${style?` style="${style}"`:""}>${c.html(r)}</td>`;
    }
    h += `</tr>`;
  }
  h += `</tbody></table>`;
  return h;
}
function headCell(id, c, st, span2){
  const ar = st.col===c.key ? `<span class="ar">${st.dir>0?"&#9650;":"&#9660;"}</span>` : "";
  const cls = ["sortable", c.cls && c.cls.includes("name") ? "name l" : "", c.cls && c.cls.includes("l") ? "l":"", c.first?"gs":""].join(" ");
  return `<th class="${cls}" data-sort="${id}|${c.key}"${span2?' rowspan="2"':""}>${esc(c.label)}${ar}</th>`;
}

/* ============ my team rows ============ */
function teamRows(){
  const rows = [];
  for (const p of DATA.players){
    if (S.vs === "fwd" && p.group === "F") rows.push({p, pos:"F", key:"FWD"});
    else for (const ps of p.pos){ if (POS_ORDER[ps] !== undefined) rows.push({p, pos:ps, key:ps}); }
  }
  return rows.filter(r => {
    if (!S.status.has(r.p.status)) return false;
    if (S.pos.size){
      let ok = false;
      for (const t of S.pos){
        if (t === "Forwards" && r.p.group === "F") ok = true;
        else if (t === "Skaters" && r.p.group !== "G") ok = true;
        else if (["C","LW","RW"].includes(t) && (r.pos === t || (r.pos === "F" && r.p.pos.includes(t)))) ok = true;
        else if ((t === "D" || t === "G") && r.pos === t) ok = true;
      }
      if (!ok) return false;
    }
    const fl = r.p.flags_by[r.key] || [];
    for (const f of S.flags) if (!fl.includes(f)) return false;
    return true;
  });
}
const lens = (r, w) => w === "forme" ? r.p.forme : (r.p.overall ? r.p.overall[w] : null);
const cmpOf = (r, w) => { const b = lens(r,w); return b && b.cmp ? b.cmp[r.key] : null; };

function statusHtml(p){
  const t = p.tag ? `<span class="tag ${p.tag==="DTD"?"grey":"red"}">${esc(p.tag)}</span>` : "";
  return esc(p.status) + t;
}
function notesHtml(r){
  const fl = r.p.flags_by[r.key] || [], out = [];
  if (fl.includes("replace")) out.push(`<span class="note n-replace">Replace?</span>`);
  if (fl.includes("poor")) out.push(`<span class="note n-poor">Poor performer</span>`);
  if (r.p.pflags.includes("small")) out.push(`<span class="note n-small">Small sample</span>`);
  if (r.p.pflags.includes("nostarts")) out.push(`<span class="note n-nostarts">No starts yet</span>`);
  return out.join("");
}
function trendHtml(t){
  if(!isNum(t)) return "";
  const pct = Math.round(t*100), th = DATA.config.trend_pct;
  if (t > th) return `&#9650; ${pct}%`;
  if (t < -th) return `&#9660; ${Math.abs(pct)}%`;
  return pct===0 ? "even" : (pct>0?"+":MINUS)+Math.abs(pct)+"%";
}
const posLabel = r => r.pos === "F" ? "F" : r.pos;
function baseCols(){
  return [
    {key:"name", label:"Player", cls:"name l", get:r=>r.p.name, html:r=>esc(r.p.name)},
    {key:"pos", label:"Pos", cls:"l", get:r=>POS_ORDER[r.pos], html:r=>posLabel(r)},
    {key:"team", label:"Team", cls:"l", get:r=>r.p.team, html:r=>esc(r.p.team)},
    {key:"status", label:"Status", cls:"l", get:r=>r.p.status, html:r=>statusHtml(r.p)},
  ];
}

function repCols(){
  const cols = baseCols();
  for (const w of ["forme", ...WINDOWS]){
    const dimIf = w === "forme" ? (r => r.p.pflags.includes("small")) : null;
    cols.push(
      {key:w+"gp", group:WIN[w], label:"GP", first:true, get:r=>{const b=lens(r,w); return b&&b.gp?b.gp:null;}, html:r=>{const b=lens(r,w); return b&&b.gp?f0(b.gp):"";}, dimIf},
      {key:w+"ppg", group:WIN[w], label:"PPG", get:r=>{const b=lens(r,w); return b&&b.gp?b.ppg:null;}, html:r=>{const b=lens(r,w); return b&&b.gp?f1(b.ppg):"";}, dimIf},
      {key:w+"gap", group:WIN[w], label:"+/- PPG", color:"div", get:r=>{const c=cmpOf(r,w); return c?c.gap:null;}, html:r=>{const c=cmpOf(r,w); return c?sg(c.gap):"";}, dimIf},
      {key:w+"pts", group:WIN[w], label:"+/- Pts", color:"div", get:r=>{const c=cmpOf(r,w); return c?c.pts:null;}, html:r=>{const c=cmpOf(r,w); return c?sg(c.pts,0):"";}, dimIf},
    );
  }
  cols.push(
    {key:"trend", label:"Trend", get:r=>r.p.trend, html:r=>trendHtml(r.p.trend)},
    {key:"notes", label:"Notes", cls:"l", get:r=>(r.p.flags_by[r.key]||[]).length*10 + r.p.pflags.length, html:notesHtml},
  );
  return cols;
}

function statVal(line, k){
  if (!line) return null;
  const v = line[k];
  if (!isNum(v)) return null;
  if (S.as === "pts" && W[k] !== undefined) return v * W[k];
  return v;
}
function statFmt(k, v){
  if (!isNum(v)) return "";
  if (k === "TOI") return toi(v);
  if (k === "SVP") return svp(v);
  if (k === "GAA") return f2(v);
  if (S.as === "pts" && W[k] !== undefined) return f1(v);
  return f2(v);
}
function statCols(defs, getLine){
  return defs.map(([k,label]) => {
    const lowerBetter = (S.as === "raw" && k === "GA") || k === "GAA";
    const lbl = (S.as === "pts" && W[k] !== undefined) ? label + " pts" : label;
    return {key:"st"+k, label:lbl, color:"scale", dir: lowerBetter ? -1 : 1,
      get:r=>statVal(getLine(r), k), html:r=>statFmt(k, statVal(getLine(r), k))};
  });
}

function renderTeam(){
  const rows = teamRows();
  const blocks = [];
  const wrap = html => `<div class="wrap">${html}</div>`;
  if (S.view === "rep"){
    blocks.push(wrap(renderGrid("team", repCols(), rows, {col:"pos", dir:1})));
  } else {
    const w = S.win;
    const line = r => { const b = lens(r,w); return b && b.gp ? b.stats : null; };
    const common = [
      ...baseCols(),
      {key:"gp", label:"GP", first:true, get:r=>{const b=lens(r,w); return b&&b.gp?b.gp:null;}, html:r=>{const b=lens(r,w); return b&&b.gp?f0(b.gp):"";}},
      {key:"ppg", label:"PPG", color:"scale", get:r=>{const b=lens(r,w); return b&&b.gp?b.ppg:null;}, html:r=>{const b=lens(r,w); return b&&b.gp?f1(b.ppg):"";}},
      {key:"gap", label:"+/- PPG", color:"div", get:r=>{const c=cmpOf(r,w); return c?c.gap:null;}, html:r=>{const c=cmpOf(r,w); return c?sg(c.gap):"";}},
    ];
    const notes = {key:"notes", label:"Notes", cls:"l", first:true, get:r=>(r.p.flags_by[r.key]||[]).length*10 + r.p.pflags.length, html:notesHtml};
    const sub = S.as === "pts" ? "fantasy points per game by category" : "per game";
    const sk = rows.filter(r => r.p.group !== "G"), gl = rows.filter(r => r.p.group === "G");
    if (sk.length || !gl.length){
      const sc = statCols(SK_STATS, line); sc[0].first = true;
      blocks.push(`<h2 class="tt">Skaters, ${WIN[w]}, ${sub}</h2>` + wrap(renderGrid("team-sk", [...common, ...sc, notes], sk, {col:"pos", dir:1})));
    }
    if (gl.length){
      const gc = statCols(G_STATS, line); gc[0].first = true;
      blocks.push(`<h2 class="tt">Goalies, ${WIN[w]}, ${sub}</h2>` + wrap(renderGrid("team-g", [...common, ...gc, notes], gl, {col:"ppg", dir:-1})));
    }
  }
  document.getElementById("team-tables").innerHTML = blocks.join("");
}

/* ============ replacement line ============ */
function renderLine(){
  const c = DATA.config;
  let anyEarly = false, anyShort = false;
  let h = `<thead><tr><th class="l">Position</th>${WINDOWS.map(w=>`<th>${WIN[w]}</th>`).join("")}</tr></thead><tbody>`;
  for (const [k,label] of LINE_ROWS){
    h += `<tr><td class="l">${label}</td>`;
    for (const w of WINDOWS){
      const b = DATA.baselines[w][k];
      let mark = "";
      if (b.early){ mark += "*"; anyEarly = true; }
      if (b.n < c.pool_size){ mark += ` (${b.n})`; anyShort = true; }
      h += `<td>${b.ppg===null ? "n/a" : f1(b.ppg)}${mark}</td>`;
    }
    h += `</tr>`;
  }
  document.getElementById("line").innerHTML = h + "</tbody>";
  let fn = `Top ${c.pool_size} free agents by PPG, weighted by games played. Forwards ${Math.round(c.own_floor.C*100)}%+ owned, D ${Math.round(c.own_floor.D*100)}%+, goalies any. Min GP: ${c.min_gp.season} Season, ${c.min_gp.l30} Last 30 and Last 14.`;
  if (anyEarly) fn += ` * Early season: Season min lowered to ${c.early_min_gp} GP.`;
  if (anyShort) fn += ` (n) = only n free agents qualified.`;
  document.getElementById("line-fn").textContent = fn;
}

/* ============ waiver wire ============ */
function renderWire(){
  const w = S.wwin, wp = S.wpos;
  const bkey = wp === "F" ? "FWD" : wp;
  const b = DATA.baselines[w][bkey];
  let rows = (DATA.waiver[w][wp] || []);
  const hidden = rows.filter(r => r.excluded.length).length;
  if (!S.wshow) rows = rows.filter(r => !r.excluded.length);
  const posName = wp === "F" ? "Forwards" : wp;
  document.getElementById("wireline").innerHTML =
    `<b>${WIN[w]} replacement line, ${posName}:</b> ${b.ppg===null ? "n/a" : f1(b.ppg)+" PPG"} from ${b.n} free agent${b.n===1?"":"s"}${b.early?" (early season, min "+b.min_gp+" GP)":""}.` +
    (S.wshow ? "" : ` ${hidden} disqualified hidden.`);
  const isG = wp === "G";
  const cols = [
    {key:"pool", label:"\u2605", get:r=>r.pool?1:0, html:r=>r.pool?`<span class="star" title="Counts toward the replacement line">&#9733;</span>`:""},
    {key:"name", label:"Player", cls:"name l", get:r=>r.name,
      html:r=>esc(r.name)+(r.tag?`<span class="tag ${r.tag==="DTD"?"grey":"red"}">${esc(r.tag)}</span>`:"")+(r.excluded.length?` <span class="why">${esc(r.excluded.join(", "))}</span>`:"")},
    {key:"pos", label:"Pos", cls:"l", get:r=>r.pos.join(","), html:r=>esc(r.pos.join(", "))},
    {key:"team", label:"Team", cls:"l", get:r=>r.team, html:r=>esc(r.team)},
    {key:"own", label:"Own", get:r=>r.own, html:r=>Math.round(r.own*100)+"%"},
    {key:"gp", label:"GP", get:r=>r.gp, html:r=>f0(r.gp)},
    {key:"ppg", label:"PPG", color:"scale", get:r=>r.ppg, html:r=>f1(r.ppg)},
    {key:"gap", label:"+/- Line", color:"div", get:r=>r.gap, html:r=>sg(r.gap)},
    ...statCols(isG ? G_STATS : SK_STATS, r => r.stats).map((c,i)=> i===0 ? Object.assign(c,{first:true}) : c),
    {key:"up", label:"Upgrade over", cls:"l", first:true, get:r=>r.upgrade?r.upgrade.gain:null,
      html:r=>r.upgrade?`${esc(r.upgrade.over)} <b>${sg(r.upgrade.gain)}</b>`:""},
  ];
  document.getElementById("wire-tables").innerHTML = `<div class="wrap">${renderGrid("wire", cols, rows, {col:"ppg", dir:-1})}</div>`;
}

/* ============ controls ============ */
function btns(group, items, isOn, extraCls=""){
  return `<div class="btns ${extraCls}">` + items.map(([v,l]) =>
    `<button type="button" data-g="${group}" data-v="${esc(v)}" aria-pressed="${isOn(v)}">${esc(l)}</button>`).join("") + `</div>`;
}
function slicer(label, inner){ return `<div class="slicer"><span>${label}</span>${inner}</div>`; }

function renderPanel(){
  let h = slicer("Page", btns("page", [["team","My Team"],["wire","Waiver Wire"]], v=>S.page===v, "pages"));
  if (S.page === "team"){
    h += slicer("View", btns("view", [["rep","vs Replacement"],["stat","Stat line"]], v=>S.view===v));
    h += slicer("Compare forwards to", btns("vs", [["pos","Position"],["fwd","All forwards"]], v=>S.vs===v));
    if (S.view === "stat"){
      h += slicer("Window", btns("win", [["forme","For me"],["season","Season"],["l30","Last 30"],["l14","Last 14"]], v=>S.win===v));
      h += slicer("Stats as", btns("as", [["raw","Stats"],["pts","Fantasy pts"]], v=>S.as===v));
    }
    h += slicer("Position", btns("pos", [["C","C"],["LW","LW"],["RW","RW"],["D","D"],["G","G"],["Forwards","Forwards"],["Skaters","Skaters"]], v=>S.pos.has(v)));
    h += slicer("Status", btns("status", [["Active","Active"],["Injured","Injured"],["Cut","Cut"]], v=>S.status.has(v)));
    h += slicer("Flags", btns("flags", [["poor","Poor performer"],["replace","Replace?"]], v=>S.flags.has(v)));
    h += `<button type="button" class="clear" data-g="clear">Clear slicers</button>`;
  } else {
    h += slicer("Position", btns("wpos", [["C","C"],["LW","LW"],["RW","RW"],["F","Forwards"],["D","D"],["G","G"]], v=>S.wpos===v));
    h += slicer("Window", btns("wwin", [["season","Season"],["l30","Last 30"],["l14","Last 14"]], v=>S.wwin===v));
    h += slicer("Stats as", btns("as", [["raw","Stats"],["pts","Fantasy pts"]], v=>S.as===v));
    h += slicer("Disqualified", btns("wshow", [["1","Show"]], v=>S.wshow));
  }
  document.getElementById("panel").innerHTML = h;
}

function renderAll(){
  renderPanel();
  document.getElementById("pg-team").hidden = S.page !== "team";
  document.getElementById("pg-wire").hidden = S.page !== "wire";
  if (S.page === "team") renderTeam(); else renderWire();
}

function toggleSet(set, v){ if (set.has(v)) set.delete(v); else set.add(v); }

document.addEventListener("click", e => {
  const th = e.target.closest("th[data-sort]");
  if (th){
    const [id, col] = th.dataset.sort.split("|");
    const cur = S.sort[id];
    S.sort[id] = (cur && cur.col === col) ? {col, dir:-cur.dir} : {col, dir: (col==="name"||col==="pos"||col==="team"||col==="status") ? 1 : -1};
    renderAll(); return;
  }
  const b = e.target.closest("button[data-g]");
  if (!b) return;
  const g = b.dataset.g, v = b.dataset.v;
  if (g === "page"){ S.page = v; history.replaceState(null,"", v==="wire"?"#wire":"#"); }
  else if (g === "view") S.view = v;
  else if (g === "vs") S.vs = v;
  else if (g === "win") S.win = v;
  else if (g === "as") S.as = v;
  else if (g === "pos") toggleSet(S.pos, v);
  else if (g === "status") toggleSet(S.status, v);
  else if (g === "flags") toggleSet(S.flags, v);
  else if (g === "wpos") S.wpos = v;
  else if (g === "wwin") S.wwin = v;
  else if (g === "wshow") S.wshow = !S.wshow;
  else if (g === "clear"){ S.pos.clear(); S.flags.clear(); S.status = new Set(["Active","Injured"]); }
  renderAll();
});

/* ============ header + checks ============ */
document.getElementById("m-team").textContent = DATA.team_name;
document.getElementById("m-pull").textContent = (DATA.pull_date ? "Stats through " + fmtDate(DATA.pull_date) : "Stats date unknown") + " | Updated " + DATA.generated_et + " ET";
document.getElementById("f-rep").textContent = Math.abs(DATA.config.replace_pts);
document.getElementById("f-small").textContent = DATA.config.small_sample;
(function(){
  const hl = DATA.health;
  const items = [...hl.warnings, ...hl.name_checks, ...hl.unparsed.map(u => `Could not read a player name on "${u.tab}": ${u.raw}`)];
  if (items.length) document.getElementById("alert").innerHTML = `<div class="alert"><b>Data check:</b><ul>${items.map(i=>`<li>${esc(i)}</li>`).join("")}</ul></div>`;
})();
renderLine();
if (location.hash === "#wire") S.page = "wire";
renderAll();
</script>
</body>
</html>
"""


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", blob)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUT_PATH} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
