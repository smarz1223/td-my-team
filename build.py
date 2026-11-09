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
.titlebar h1{margin:0; flex:1 1 auto; font-family:var(--pixel); font-weight:400; font-size:clamp(13px, 2.4vw, 20px); letter-spacing:1px; color:#eaf0ff; text-shadow:3px 3px 0 var(--red); display:flex; align-items:center; gap:12px}
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
#pages .btns{gap:6px}
#pages button{font-family:var(--pixel); font-size:10px; padding:8px 11px; background:transparent; color:#c9d4f0; border:2px solid #3a5290; border-radius:0}
#pages button:hover{border-color:#fff; color:#fff}
#pages button[aria-pressed="true"]{background:#fff; color:var(--navy); border-color:#fff; box-shadow:3px 3px 0 var(--red)}
tr.mine td{background:#e6eeff}
.chartwrap{background:#fff; border:1px solid var(--grid); padding:6px 6px 2px; position:relative}
.chartwrap svg{display:block; width:100%; height:auto; touch-action:manipulation}
.legend{display:flex; flex-wrap:wrap; gap:4px 16px; font-size:12.5px; margin:0 0 6px}
.legend span{display:inline-flex; align-items:center; gap:5px}
.legend i{display:inline-block; width:11px; height:11px; border-radius:50%}
.tip{position:absolute; pointer-events:none; background:#fff; border:1px solid #9fb0cc; box-shadow:0 2px 8px rgba(14,37,87,.18); padding:6px 9px; font-size:12.5px; line-height:1.45; z-index:4; min-width:170px}
.tip b{font-size:13px}
.tip .k{color:var(--soft)}
svg .dot{cursor:pointer}
svg .dot:hover, svg .dot.hot{stroke:#0e2557; stroke-width:2.5}
tr.mine td.name{background:#d6e2fc}
.tag.mine{color:var(--blue)}
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
  <nav id="pages" aria-label="Pages"></nav>
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

  <section id="pg-scatter" hidden>
    <p class="wireline" id="scatline"></p>
    <div class="legend" id="scatlegend"></div>
    <div class="chartwrap" id="scatwrap"><div class="tip" id="tip" hidden></div><div id="scatsvg"></div></div>
    <p class="foot">X = total fantasy points in the window. Y = fantasy points per game. Dashed line = replacement line for this position and window.
      Labels show your players and the top 5 qualified free agents by PPG. Hover or tap any dot for details. Turning off "Show my team" or "Disqualified" grays those dots out instead of removing them.</p>
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
  wpos:"C", wwin:"l30", wshow:false, wmine:true, wtot:"pg",
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
function renderGrid(id, cols, rows, defSort, rowCls){
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
    const rc = rowCls ? rowCls(r) : "";
    h += rc ? `<tr class="${rc}">` : `<tr>`;
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
const totalFp = b => (b && b.gp && isNum(b.ppg)) ? b.ppg * b.gp : null;
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
      {key:w+"fp", group:WIN[w], label:"Total FP", color:"scale", get:r=>totalFp(lens(r,w)), html:r=>f0(totalFp(lens(r,w))), dimIf},
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

const NO_TOTAL = new Set(["SVP","GAA"]);
function statVal(line, k, gp, totals){
  if (!line) return null;
  let v = line[k];
  if (!isNum(v)) return null;
  if (totals && !NO_TOTAL.has(k)) v = v * (gp || 0);
  if (S.as === "pts" && W[k] !== undefined) return v * W[k];
  return v;
}
function statFmt(k, v, totals){
  if (!isNum(v)) return "";
  if (k === "TOI") return toi(v);
  if (k === "SVP") return svp(v);
  if (k === "GAA") return f2(v);
  if (S.as === "pts" && W[k] !== undefined) return f1(v);
  return totals ? f0(v) : f2(v);
}
function statCols(defs, getLine, getGp, totals){
  return defs.map(([k,label]) => {
    const lowerBetter = (S.as === "raw" && k === "GA") || k === "GAA";
    let lbl = (S.as === "pts" && W[k] !== undefined) ? label + " pts" : label;
    if (k === "TOI" && totals) lbl = "TOI";
    return {key:"st"+k, label:lbl, color:"scale", dir: lowerBetter ? -1 : 1,
      get:r=>statVal(getLine(r), k, getGp ? getGp(r) : 0, totals),
      html:r=>statFmt(k, statVal(getLine(r), k, getGp ? getGp(r) : 0, totals), totals)};
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
      {key:"fp", label:"Total FP", color:"scale", get:r=>totalFp(lens(r,w)), html:r=>f0(totalFp(lens(r,w)))},
      {key:"gap", label:"+/- PPG", color:"div", get:r=>{const c=cmpOf(r,w); return c?c.gap:null;}, html:r=>{const c=cmpOf(r,w); return c?sg(c.gap):"";}},
    ];
    const notes = {key:"notes", label:"Notes", cls:"l", first:true, get:r=>(r.p.flags_by[r.key]||[]).length*10 + r.p.pflags.length, html:notesHtml};
    const sub = S.as === "pts" ? "fantasy points per game by category" : "per game";
    const sk = rows.filter(r => r.p.group !== "G"), gl = rows.filter(r => r.p.group === "G");
    if (sk.length || !gl.length){
      const sc = statCols(SK_STATS, line, null, false); sc[0].first = true;
      blocks.push(`<h2 class="tt">Skaters, ${WIN[w]}, ${sub}</h2>` + wrap(renderGrid("team-sk", [...common, ...sc, notes], sk, {col:"pos", dir:1})));
    }
    if (gl.length){
      const gc = statCols(G_STATS, line, null, false); gc[0].first = true;
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
function myWireRows(w, wp, b){
  return DATA.players.filter(p => {
    if (p.status === "Cut" || !p.overall || !p.overall[w] || !p.overall[w].gp) return false;
    if (wp === "F") return p.group === "F";
    return p.pos.includes(wp);
  }).map(p => {
    const o = p.overall[w];
    return {mine:true, key:p.key, name:p.name, team:p.team, pos:p.pos, tag:p.tag, own:o.own,
      gp:o.gp, ppg:o.ppg, total:o.ppg*o.gp, stats:o.stats, status:p.status,
      gap: (b.ppg!==null && isNum(o.ppg)) ? o.ppg - b.ppg : null,
      pool:false, excluded:[], upgrade:null};
  });
}

function renderWire(){
  const w = S.wwin, wp = S.wpos;
  const bkey = wp === "F" ? "FWD" : wp;
  const b = DATA.baselines[w][bkey];
  let rows = (DATA.waiver[w][wp] || []);
  const hidden = rows.filter(r => r.excluded.length).length;
  if (!S.wshow) rows = rows.filter(r => !r.excluded.length);
  const mine = S.wmine ? myWireRows(w, wp, b) : [];
  rows = rows.concat(mine);
  const totals = S.wtot === "tot";
  const posName = wp === "F" ? "Forwards" : wp;
  document.getElementById("wireline").innerHTML =
    `<b>${WIN[w]} replacement line, ${posName}:</b> ${b.ppg===null ? "n/a" : f1(b.ppg)+" PPG"} from ${b.n} free agent${b.n===1?"":"s"}${b.early?" (early season, min "+b.min_gp+" GP)":""}.` +
    (S.wshow ? "" : ` ${hidden} disqualified hidden.`) + (S.wmine ? ` ${mine.length} of your players shown (blue rows).` : "");
  const isG = wp === "G";
  const sc = statCols(isG ? G_STATS : SK_STATS, r => r.stats, r => r.gp, totals); sc[0].first = true;
  const cols = [
    {key:"pool", label:"\u2605", get:r=>r.pool?1:0, html:r=>r.pool?`<span class="star" title="Counts toward the replacement line">&#9733;</span>`:""},
    {key:"name", label:"Player", cls:"name l", get:r=>r.name,
      html:r=>esc(r.name)+(r.mine?`<span class="tag mine">Mine</span>`:"")+(r.tag?`<span class="tag ${r.tag==="DTD"?"grey":"red"}">${esc(r.tag)}</span>`:"")+(r.excluded.length?` <span class="why">${esc(r.excluded.join(", "))}</span>`:"")},
    {key:"pos", label:"Pos", cls:"l", get:r=>r.pos.join(","), html:r=>esc(r.pos.join(", "))},
    {key:"team", label:"Team", cls:"l", get:r=>r.team, html:r=>esc(r.team)},
    {key:"own", label:"Own", get:r=>r.own, html:r=>isNum(r.own)?Math.round(r.own*100)+"%":""},
    {key:"gp", label:"GP", get:r=>r.gp, html:r=>f0(r.gp)},
    {key:"ppg", label:"PPG", color:"scale", get:r=>r.ppg, html:r=>f1(r.ppg)},
    {key:"fp", label:"Total FP", color:"scale", get:r=>r.total, html:r=>f0(r.total)},
    {key:"gap", label:"+/- Line", color:"div", get:r=>r.gap, html:r=>sg(r.gap)},
    ...sc,
    {key:"up", label:"Upgrade over", cls:"l", first:true, get:r=>r.upgrade?r.upgrade.gain:null,
      html:r=>r.upgrade?`${esc(r.upgrade.over)} <b>${sg(r.upgrade.gain)}</b>`:""},
  ];
  document.getElementById("wire-tables").innerHTML =
    `<h2 class="tt">${posName}, ${WIN[w]}, ${totals ? "totals" : "per game"}${S.as==="pts" ? ", fantasy points by category" : ""}</h2>` +
    `<div class="wrap">${renderGrid("wire", cols, rows, {col:"ppg", dir:-1}, r => r.mine ? "mine" : "")}</div>`;
}

/* ============ scatter ============ */
const SC = {pts:[]};
function niceStep(range, target){
  const raw = range / Math.max(1, target);
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const n = raw / mag;
  return (n < 1.5 ? 1 : n < 3 ? 2 : n < 7 ? 5 : 10) * mag;
}
function ticks(lo, hi, target){
  const st = niceStep(hi - lo, target), out = [];
  for (let v = Math.ceil(lo/st)*st; v <= hi + 1e-9; v += st) out.push(Math.round(v*1000)/1000);
  return out;
}
function renderScatter(){
  const w = S.wwin, wp = S.wpos;
  const bkey = wp === "F" ? "FWD" : wp;
  const b = DATA.baselines[w][bkey];
  const fa = (DATA.waiver[w][wp] || []).filter(r => isNum(r.ppg) && r.gp > 0);
  const mine = myWireRows(w, wp, b);
  const posName = wp === "F" ? "Forwards" : wp;

  // category + grayed state for every dot
  const qualified = fa.filter(r => !r.excluded.length);
  const top5 = new Set(qualified.slice().sort((a,c)=>c.ppg-a.ppg).slice(0,5).map(r=>r.key));
  const pts = [];
  for (const r of fa){
    const dq = r.excluded.length > 0;
    pts.push({r, cat: dq ? "dq" : (r.pool ? "pool" : "fa"), gray: dq && !S.wshow, label: !dq && top5.has(r.key)});
  }
  for (const r of mine) pts.push({r, cat:"mine", gray: !S.wmine, label: S.wmine});
  SC.pts = pts;

  const n = k => pts.filter(p => p.cat === k).length;
  document.getElementById("scatline").innerHTML =
    `<b>${WIN[w]}, ${posName}:</b> replacement line ${b.ppg===null ? "n/a" : f1(b.ppg)+" PPG"} from ${b.n} free agent${b.n===1?"":"s"}${b.early?" (early season, min "+b.min_gp+" GP)":""}.`;
  document.getElementById("scatlegend").innerHTML =
    `<span><i style="background:var(--blue)"></i>My team (${n("mine")})${S.wmine?"":" grayed"}</span>` +
    `<span><i style="background:var(--red)"></i>&#9733; Replacement pool (${n("pool")})</span>` +
    `<span><i style="background:#8a93a3"></i>Other free agents (${n("fa")})</span>` +
    `<span><i style="background:#fff; border:2px solid #8a93a3; width:9px; height:9px"></i>Disqualified (${n("dq")})${S.wshow?"":" grayed"}</span>`;

  const host = document.getElementById("scatsvg");
  if (!pts.length){ host.innerHTML = `<p class="empty">No players to plot for this position and window.</p>`; return; }

  // geometry: draw at the container's real width so text stays readable on phones
  const W = Math.max(320, Math.round(document.getElementById("scatwrap").clientWidth - 12));
  const H = Math.round(Math.min(620, Math.max(360, W < 600 ? W * 1.05 : W * 0.58)));
  const m = {l:52, r:18, t:14, b:44};
  const xs = pts.map(p=>p.r.total), ys = pts.map(p=>p.r.ppg);
  if (b.ppg !== null) ys.push(b.ppg);
  let x0 = 0, x1 = Math.max(...xs) * 1.06 || 10;
  // y axis zooms to the data (it does not force 0) so clustered dots spread out
  let y0 = Math.min(...ys), y1 = Math.max(...ys);
  const pad = (y1 - y0) * 0.08 || 2; y1 += pad; y0 -= pad;
  const ys0 = niceStep(y1 - y0, 6); y0 = Math.floor(y0 / ys0) * ys0;
  const X = v => m.l + (v - x0) / (x1 - x0) * (W - m.l - m.r);
  const Y = v => H - m.b - (v - y0) / (y1 - y0) * (H - m.t - m.b);

  let g = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Total fantasy points versus points per game">`;
  // grid + axes
  for (const t of ticks(y0, y1, 6)) g += `<line x1="${m.l}" x2="${W-m.r}" y1="${Y(t)}" y2="${Y(t)}" stroke="#e3e8f0"/><text x="${m.l-6}" y="${Y(t)+4}" text-anchor="end" font-size="11" fill="#5d6778">${t}</text>`;
  for (const t of ticks(x0, x1, W < 600 ? 5 : 8)) g += `<line y1="${m.t}" y2="${H-m.b}" x1="${X(t)}" x2="${X(t)}" stroke="#eef1f6"/><text x="${X(t)}" y="${H-m.b+16}" text-anchor="middle" font-size="11" fill="#5d6778">${t}</text>`;
  g += `<line x1="${m.l}" x2="${W-m.r}" y1="${H-m.b}" y2="${H-m.b}" stroke="#9fb0cc"/><line x1="${m.l}" x2="${m.l}" y1="${m.t}" y2="${H-m.b}" stroke="#9fb0cc"/>`;
  g += `<text x="${(m.l+W-m.r)/2}" y="${H-6}" text-anchor="middle" font-size="12" font-weight="700" fill="#1d2533">Total fantasy points</text>`;
  g += `<text transform="translate(14 ${(m.t+H-m.b)/2}) rotate(-90)" text-anchor="middle" font-size="12" font-weight="700" fill="#1d2533">Fantasy points per game</text>`;
  // replacement line
  const placed = [];
  if (b.ppg !== null){
    const yy = Y(b.ppg), txt = `Replacement line ${f1(b.ppg)}`, tw = txt.length * 6.3, th = 13;
    // label goes top-right of the line, unless a dot sits there; then try top-left, then below
    const nearDot = box => pts.some(p => { if (p.gray) return false; const dx=X(p.r.total), dy=Y(p.r.ppg); return dx > box.x-8 && dx < box.x+box.w+8 && dy > box.y-8 && dy < box.y+box.h+8; });
    const opts = [{x:W-m.r-4-tw, y:yy-5-th}, {x:m.l+6, y:yy-5-th}, {x:W-m.r-4-tw, y:yy+4}, {x:m.l+6, y:yy+4}];
    const box = Object.assign({w:tw, h:th}, opts.find(o => !nearDot(Object.assign({w:tw, h:th}, o))) || opts[0]);
    placed.push(box);
    g += `<line x1="${m.l}" x2="${W-m.r}" y1="${yy}" y2="${yy}" stroke="#d42a1e" stroke-width="1.5" stroke-dasharray="6 4"/>`;
    g += `<text x="${box.x}" y="${box.y+th-2}" font-size="11.5" font-weight="700" fill="#d42a1e" paint-order="stroke" stroke="#fff" stroke-width="3">${txt}</text>`;
  }
  // dots: grayed first, then FA, pool, mine on top
  const order = {gray:0, dq:1, fa:2, pool:3, mine:4};
  const idx = pts.map((p,i)=>i).sort((a,c)=>{
    const pa = pts[a].gray ? 0 : order[pts[a].cat], pc = pts[c].gray ? 0 : order[pts[c].cat];
    return pa - pc;
  });
  for (const i of idx){
    const p = pts[i], cx = X(p.r.total), cy = Y(p.r.ppg);
    let fill, stroke, sw = 1, op = 1, rad = 5.5;
    if (p.gray){ fill = "#cfd5df"; stroke = "#cfd5df"; op = 0.45; rad = 4.5; }
    else if (p.cat === "mine"){ fill = "#2350c4"; stroke = "#fff"; sw = 1.5; rad = 7; }
    else if (p.cat === "pool"){ fill = "#d42a1e"; stroke = "#fff"; sw = 1.5; rad = 6; }
    else if (p.cat === "dq"){ fill = "#fff"; stroke = "#8a93a3"; sw = 2; }
    else { fill = "#8a93a3"; stroke = "#fff"; }
    g += `<circle class="dot" data-i="${i}" cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${rad}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" opacity="${op}"/>`;
  }
  // labels with simple collision avoidance (replacement line label already reserved)
  const hit = (a) => placed.some(q => a.x < q.x+q.w && a.x+a.w > q.x && a.y < q.y+q.h && a.y+a.h > q.y)
                      || pts.some(p => { if (p.gray) return false; const dx=X(p.r.total), dy=Y(p.r.ppg); return dx > a.x-3 && dx < a.x+a.w+3 && dy > a.y-3 && dy < a.y+a.h+3; });
  const lab = idx.filter(i => pts[i].label && !pts[i].gray).reverse();
  for (const i of lab){
    const p = pts[i], cx = X(p.r.total), cy = Y(p.r.ppg);
    const txt = p.r.name.split(" ").slice(-1)[0], tw = txt.length * 6.6 + 4, th = 13;
    const cands = [[cx+9, cy-th/2], [cx-9-tw, cy-th/2], [cx-tw/2, cy-9-th], [cx-tw/2, cy+9], [cx+9, cy-th-4], [cx+9, cy+4], [cx-9-tw, cy-th-4], [cx-9-tw, cy+4]];
    let pick = null;
    for (const [x,y] of cands){
      const box = {x, y, w:tw, h:th};
      if (x < m.l || x+tw > W-m.r || y < m.t || y+th > H-m.b) continue;
      if (!hit(box)){ pick = box; break; }
    }
    if (!pick){
      if (p.cat !== "mine") continue;  // crowded: drop free agent labels (hover still works), always label my players
      const [x,y] = cands[0]; pick = {x: Math.min(x, W-m.r-tw), y, w:tw, h:th};
    }
    placed.push(pick);
    const col = p.cat === "mine" ? "#2350c4" : "#a81f15";
    g += `<text x="${pick.x+2}" y="${pick.y+th-3}" font-size="11.5" font-weight="700" fill="${col}" paint-order="stroke" stroke="#fff" stroke-width="3" pointer-events="none">${esc(txt)}</text>`;
  }
  g += `</svg>`;
  host.innerHTML = g;
  document.getElementById("tip").hidden = true;
}

function showTip(i, evt){
  const p = SC.pts[i]; if (!p) return;
  const r = p.r, tip = document.getElementById("tip"), wrap = document.getElementById("scatwrap");
  const kind = p.cat === "mine" ? "My team" : p.cat === "pool" ? "&#9733; Replacement pool" : p.cat === "dq" ? "Disqualified: " + esc(r.excluded.join(", ")) : "Free agent";
  tip.innerHTML = `<b>${esc(r.name)}</b>${r.tag?` <span class="tag ${r.tag==="DTD"?"grey":"red"}">${esc(r.tag)}</span>`:""}<br>
    <span class="k">${esc(r.team)} ${esc(r.pos.join(", "))} | ${kind}</span><br>
    <span class="k">Own</span> ${isNum(r.own)?Math.round(r.own*100)+"%":""} &nbsp; <span class="k">GP</span> ${f0(r.gp)}<br>
    <span class="k">PPG</span> <b>${f1(r.ppg)}</b> &nbsp; <span class="k">Total FP</span> <b>${f0(r.total)}</b><br>
    <span class="k">vs line</span> ${sg(r.gap)} PPG` + (r.upgrade ? `<br><span class="k">Upgrade over</span> ${esc(r.upgrade.over)} <b>${sg(r.upgrade.gain)}</b>` : "");
  tip.hidden = false;
  const wr = wrap.getBoundingClientRect();
  let x = evt.clientX - wr.left + 14, y = evt.clientY - wr.top + 14;
  const tw = tip.offsetWidth, th = tip.offsetHeight;
  if (x + tw > wr.width - 4) x = evt.clientX - wr.left - tw - 14;
  if (y + th > wr.height - 4) y = evt.clientY - wr.top - th - 14;
  tip.style.left = Math.max(4, x) + "px"; tip.style.top = Math.max(4, y) + "px";
  document.querySelectorAll("svg .dot.hot").forEach(d => d.classList.remove("hot"));
  const dot = document.querySelector(`svg .dot[data-i="${i}"]`); if (dot) dot.classList.add("hot");
}
document.addEventListener("mousemove", e => {
  if (S.page !== "scatter") return;
  const d = e.target.closest && e.target.closest("svg .dot");
  if (d) showTip(+d.dataset.i, e);
  else if (!e.target.closest || !e.target.closest(".tip")) { const t = document.getElementById("tip"); if (t && !t.hidden && !SC.pinned){ t.hidden = true; document.querySelectorAll("svg .dot.hot").forEach(x=>x.classList.remove("hot")); } }
});
document.addEventListener("click", e => {
  if (S.page !== "scatter") return;
  const d = e.target.closest && e.target.closest("svg .dot");
  if (d){ SC.pinned = true; showTip(+d.dataset.i, e); }
  else if (!e.target.closest("button")){ SC.pinned = false; const t = document.getElementById("tip"); if (t) t.hidden = true; }
});
let scatTimer = null;
window.addEventListener("resize", () => { if (S.page !== "scatter") return; clearTimeout(scatTimer); scatTimer = setTimeout(renderScatter, 150); });

/* ============ controls ============ */
function btns(group, items, isOn, extraCls=""){
  return `<div class="btns ${extraCls}">` + items.map(([v,l]) =>
    `<button type="button" data-g="${group}" data-v="${esc(v)}" aria-pressed="${isOn(v)}">${esc(l)}</button>`).join("") + `</div>`;
}
function slicer(label, inner){ return `<div class="slicer"><span>${label}</span>${inner}</div>`; }

function renderPanel(){
  document.getElementById("pages").innerHTML = btns("page", [["team","My Team"],["wire","Waiver Wire"],["scatter","Scatter"]], v=>S.page===v, "pages");
  let h = "";
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
    if (S.page === "wire"){
      h += slicer("Show", btns("wtot", [["pg","Per game"],["tot","Totals"]], v=>S.wtot===v));
      h += slicer("Stats as", btns("as", [["raw","Stats"],["pts","Fantasy pts"]], v=>S.as===v));
    }
    h += slicer("My team", btns("wmine", [["1","Show my team"]], v=>S.wmine));
    h += slicer("Disqualified", btns("wshow", [["1","Show"]], v=>S.wshow));
  }
  document.getElementById("panel").innerHTML = h;
}

function renderAll(){
  renderPanel();
  document.getElementById("pg-team").hidden = S.page !== "team";
  document.getElementById("pg-wire").hidden = S.page !== "wire";
  document.getElementById("pg-scatter").hidden = S.page !== "scatter";
  if (S.page === "team") renderTeam();
  else if (S.page === "wire") renderWire();
  else renderScatter();
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
  if (g === "page"){ S.page = v; history.replaceState(null,"", v==="team" ? "#" : "#"+v); }
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
  else if (g === "wmine") S.wmine = !S.wmine;
  else if (g === "wtot") S.wtot = v;
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
if (location.hash === "#scatter") S.page = "scatter";
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
