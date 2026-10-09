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
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🗞️</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&family=UnifrakturCook:wght@700&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#e7e2d4;
  --paper-shade:#d8d0bc;
  --ink:#24211b;
  --ink-soft:#5f594c;
  --rule:#3b362d;
  --spot:#a3291f;
  --display:"Archivo", "Arial Narrow", "Helvetica Neue", Arial, sans-serif;
  --body:"Old Standard TT", Georgia, "Times New Roman", serif;
  --mast:"UnifrakturCook", "Old English Text MT", Georgia, serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:var(--body); font-size:17px; line-height:1.55;
  padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px);
}
.sheet{max-width:1240px; margin:0 auto; padding:18px 22px 40px}
a{color:inherit}
button{font:inherit; color:inherit}
:focus-visible{outline:2px solid var(--spot); outline-offset:2px}

/* ---------- masthead ---------- */
.mast{display:grid; grid-template-columns:150px 1fr 150px; align-items:center; gap:16px; padding-bottom:6px}
.ear{border:1px solid var(--rule); padding:6px 8px; font-family:var(--display); font-stretch:75%; font-size:12px; line-height:1.3; text-align:center}
.ear b{display:block; font-size:14px; font-weight:800}
.mast h1{margin:0; text-align:center; font-family:var(--mast); font-weight:700; font-size:clamp(2.3rem, 6.4vw, 4.8rem); line-height:1; letter-spacing:.01em}
@media (min-width:861px){.mast h1{white-space:nowrap}}
.dateline{border-top:3px double var(--rule); border-bottom:1px solid var(--rule); display:flex; justify-content:space-between; gap:12px; padding:4px 2px; font-family:var(--display); font-stretch:80%; font-size:13px}
.dateline span:nth-child(2){font-weight:700}
nav{display:flex; justify-content:center; gap:4px; border-bottom:3px solid var(--rule); padding:6px 0}
nav button{background:none; border:0; cursor:pointer; padding:4px 14px; font-family:var(--display); font-stretch:85%; font-weight:700; font-size:16px; border-bottom:3px solid transparent}
nav button[aria-current="page"]{border-bottom-color:var(--spot)}

/* ---------- front page top ---------- */
.top{display:grid; grid-template-columns:2fr 1fr; gap:0; margin-top:18px; border-bottom:1px solid var(--rule); padding-bottom:18px}
.stories{padding-right:22px; border-right:1px solid var(--rule)}
.lead h2{font-family:var(--display); font-stretch:70%; font-weight:900; font-size:clamp(2rem, 4.6vw, 3.4rem); line-height:.98; margin:0 0 8px}
.lead p{font-style:italic; font-size:19px; margin:0 0 14px; max-width:62ch}
.briefs{display:grid; grid-template-columns:1fr 1fr; border-top:1px solid var(--rule)}
.brief{padding:10px 14px 0 0}
.brief + .brief{padding-left:14px; padding-right:0; border-left:1px solid var(--rule)}
.brief h3{font-family:var(--display); font-stretch:75%; font-weight:800; font-size:21px; line-height:1.1; margin:0 0 4px}
.brief p{margin:0; font-size:15.5px}
.sidebar{padding-left:22px}
.boxhead{font-family:var(--display); font-stretch:75%; font-weight:900; font-size:20px; margin:0; padding:2px 0 4px; border-bottom:2px solid var(--rule)}
.sidebar .explain{font-size:14px; color:var(--ink-soft); margin:6px 0 8px}

/* ---------- agate tables ---------- */
.agate{border-collapse:collapse; font-family:var(--display); font-stretch:78%; font-size:14px; font-variant-numeric:tabular-nums; width:100%}
.agate th,.agate td{padding:3px 6px; text-align:right; white-space:nowrap}
.agate th{font-weight:700; font-size:12.5px; border-bottom:1px solid var(--rule)}
.agate td:first-child,.agate th:first-child{text-align:left}
.agate tbody tr{border-bottom:1px dotted #9d9583}
.neg{color:var(--spot)}
.pos{font-weight:700}
.dim{opacity:.42}
.mute{color:var(--ink-soft)}
.fn{font-size:12.5px; color:var(--ink-soft); margin:6px 0 0; font-family:var(--body)}

/* ---------- box score ---------- */
.section-head{display:flex; flex-wrap:wrap; justify-content:space-between; align-items:flex-end; gap:10px; margin:22px 0 6px}
.section-head h2{font-family:var(--display); font-stretch:70%; font-weight:900; font-size:30px; line-height:1; margin:0}
.seg{display:inline-flex; border:1px solid var(--rule)}
.seg button{background:none; border:0; padding:4px 10px; cursor:pointer; font-family:var(--display); font-stretch:80%; font-size:14px; font-weight:600}
.seg button + button{border-left:1px solid var(--rule)}
.seg button[aria-pressed="true"]{background:var(--ink); color:var(--paper)}
.seglabel{font-family:var(--display); font-stretch:80%; font-size:13px; margin-right:6px; color:var(--ink-soft)}
.controls{display:flex; flex-wrap:wrap; gap:14px; align-items:center}
.scroll{overflow-x:auto; border-top:3px solid var(--rule); border-bottom:3px solid var(--rule); -webkit-overflow-scrolling:touch}
.box th.grp{text-align:center; border-bottom:1px solid var(--rule); font-weight:900; font-size:13px}
.box th.grp + th.grp, .box .gs{border-left:1px solid var(--rule)}
.box td.name{position:sticky; left:0; background:var(--paper); min-width:170px; padding-right:12px; box-shadow:1px 0 0 var(--rule)}
.box th.namehd{position:sticky; left:0; background:var(--paper); box-shadow:1px 0 0 var(--rule)}
.box td.name b{font-weight:800; font-size:14.5px}
.box td.name small{display:block; font-size:11.5px; color:var(--ink-soft); line-height:1.2}
.box tr.sec td{background:var(--paper-shade); font-weight:900; font-size:13px; text-align:left; padding-top:5px; position:static}
.box tr.sec td span{position:sticky; left:6px}
.stamp{display:inline-block; font-family:var(--display); font-stretch:75%; font-weight:800; font-size:10.5px; line-height:1; padding:2px 4px 1px; margin:0 3px 2px 0; border:1.5px solid currentColor; transform:rotate(-2deg); vertical-align:middle}
.stamp.red{color:var(--spot)}
.stamp.solid{background:var(--spot); color:var(--paper); border-color:var(--spot)}
.stamp.grey{color:var(--ink-soft)}
td.notes{text-align:left!important; white-space:normal!important; min-width:150px}
.trend-up{font-weight:800}
.trend-dn{color:var(--spot); font-weight:800}

/* ---------- waiver ---------- */
.wire-intro{max-width:70ch; margin:14px 0 0}
.star{color:var(--spot)}
.why{font-size:12px; color:var(--ink-soft)}

/* ---------- press room ---------- */
.press{margin-top:30px; border-top:3px double var(--rule); padding-top:10px; display:grid; grid-template-columns:1fr 1.4fr; gap:22px; font-size:14.5px}
.press h4{font-family:var(--display); font-stretch:75%; font-weight:900; font-size:17px; margin:0 0 4px}
.press ul{margin:0; padding-left:18px}
.press .ok{color:var(--ink-soft)}
.tabgrid{columns:2; column-gap:18px; font-family:var(--display); font-stretch:78%; font-size:12.5px; line-height:1.45}
.tabgrid div{break-inside:avoid; display:flex; justify-content:space-between; border-bottom:1px dotted #9d9583}
.colophon{margin-top:14px; font-size:13px; color:var(--ink-soft); text-align:center}

[hidden]{display:none!important}

@media (max-width:860px){
  .mast{grid-template-columns:1fr}
  .ear{display:none}
  .top{grid-template-columns:1fr}
  .stories{border-right:0; padding-right:0}
  .sidebar{padding-left:0; margin-top:18px}
  .press{grid-template-columns:1fr}
  .dateline span:nth-child(3){display:none}
}
@media (max-width:560px){
  .sheet{padding:12px 12px 30px}
  .briefs{grid-template-columns:1fr}
  .brief + .brief{border-left:0; padding-left:0; border-top:1px solid var(--rule); margin-top:10px}
  .tabgrid{columns:1}
}
@media print{nav,.controls{display:none}}
</style>
</head>
<body>
<div class="sheet">
  <header class="mast">
    <div class="ear"><b id="ear-vol"></b>Type Disgusting<br>Hockey League</div>
    <h1>The Morning Soft Dump</h1>
    <div class="ear"><b>Late Edition</b>Free agents,<br>box scores inside</div>
  </header>
  <div class="dateline"><span id="dl-date"></span><span id="dl-team"></span><span id="dl-pull"></span></div>
  <nav aria-label="Pages">
    <button type="button" data-page="front" aria-current="page">Front Page</button>
    <button type="button" data-page="wire">Waiver Wire</button>
  </nav>

  <main>
    <section id="page-front">
      <div class="top">
        <div class="stories">
          <article class="lead" id="lead"></article>
          <div class="briefs" id="briefs"></div>
        </div>
        <aside class="sidebar">
          <h2 class="boxhead">The replacement line</h2>
          <p class="explain">Points per game from the best available free agents at each position. Beat this number or someone on the wire is better.</p>
          <table class="agate" id="baseline-table"></table>
          <p class="fn" id="baseline-fn"></p>
        </aside>
      </div>

      <div class="section-head">
        <h2>Box score</h2>
        <div class="controls">
          <span><span class="seglabel">Compare forwards to</span>
            <span class="seg" role="group" aria-label="Compare forwards to">
              <button type="button" data-vs="pos" aria-pressed="true">Their position</button>
              <button type="button" data-vs="fwd" aria-pressed="false">All forwards</button>
            </span>
          </span>
        </div>
      </div>
      <div class="scroll"><table class="agate box" id="box"></table></div>
      <p class="fn">
        <b>For me</b> counts only games he started for you. <b>Season, Last 30, Last 14</b> count every game he played.
        <b>+/- PPG</b> is points per game above or below the replacement line; <b>+/- Pts</b> multiplies that by games played.
        Multi-position players are measured against the toughest line among their positions.
        Gray "For me" numbers come from fewer than <span id="fn-small"></span> starts.
      </p>
    </section>

    <section id="page-wire" hidden>
      <div class="section-head">
        <h2>Waiver wire</h2>
        <div class="controls">
          <span class="seg" role="group" aria-label="Position" id="wire-pos"></span>
          <span class="seg" role="group" aria-label="Window" id="wire-win"></span>
        </div>
      </div>
      <p class="wire-intro fn" id="wire-intro"></p>
      <div class="scroll"><table class="agate" id="wire"></table></div>
      <p class="fn"><span class="star">&#9733;</span> = counts toward the replacement line. Gray rows miss the ownership or games-played cutoff.
        "Upgrade over" compares him to your weakest active player at the position over the same window.</p>
    </section>
  </main>

  <footer class="press">
    <div>
      <h4>Press room notes</h4>
      <div id="health"></div>
    </div>
    <div>
      <h4>Wire services received</h4>
      <div class="tabgrid" id="tabs"></div>
    </div>
  </footer>
  <p class="colophon" id="colophon"></p>
</div>

<script>
const DATA = __DATA__;

const WINDOWS = ["season","l30","l14"];
const WIN_LABEL = {season:"Season", l30:"Last 30", l14:"Last 14"};
const SECTIONS = [["C","Centers"],["LW","Left wings"],["RW","Right wings"],["D","Defense"],["G","Goalies"],["IR","Injured reserve"],["CUT","Cut from the roster"]];
const BASE_ROWS = [["C","Center"],["LW","Left wing"],["RW","Right wing"],["FWD","All forwards"],["D","Defense"],["G","Goalie"]];
const state = {page:"front", vs:"pos", wpos:"C", wwin:"l30"};

const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const MINUS = "\u2212";
function num(x, d=1){ return (x===null||x===undefined) ? "" : x.toFixed(d); }
function signed(x, d=1){
  if (x===null||x===undefined) return "";
  const v = Number(x.toFixed(d));
  if (v===0) return (0).toFixed(d);
  return (v>0?"+":MINUS) + Math.abs(v).toFixed(d);
}
function signCls(x){ return (x===null||x===undefined) ? "" : (x < -0.05 ? "neg" : (x > 0.05 ? "pos" : "")); }
function gp(x){ return (x===null||x===undefined) ? "" : String(Math.round(x)); }
function fmtDate(iso, opts){ if(!iso) return ""; const [y,m,d]=iso.split("-").map(Number); return new Date(y,m-1,d).toLocaleDateString("en-US", opts); }

/* ---------- masthead ---------- */
function renderMast(){
  const gen = DATA.generated_et.split(" ")[0];
  document.getElementById("dl-date").textContent = fmtDate(gen,{weekday:"long",year:"numeric",month:"long",day:"numeric"}).toUpperCase();
  document.getElementById("dl-team").textContent = DATA.team_name;
  document.getElementById("dl-pull").textContent = DATA.pull_date ? "Stats through " + fmtDate(DATA.pull_date,{month:"short",day:"numeric"}) : "Stats date unknown";
  document.getElementById("ear-vol").textContent = "Vol. " + DATA.season;
  document.getElementById("fn-small").textContent = DATA.config.small_sample;
  document.getElementById("colophon").textContent = "Printed " + DATA.generated_et + " ET from the " + DATA.source + ".";
}

/* ---------- front page stories ---------- */
function renderStories(){
  const b = DATA.briefs;
  const lead = b[0];
  document.getElementById("lead").innerHTML = lead ? `<h2>${esc(lead.head)}</h2><p>${esc(lead.deck)}</p>` : "";
  document.getElementById("briefs").innerHTML = b.slice(1).map(x => `<div class="brief"><h3>${esc(x.head)}</h3><p>${esc(x.deck)}</p></div>`).join("");
}

function renderBaselines(){
  let anyEarly = false, anyShort = false;
  let h = `<thead><tr><th>Position</th>${WINDOWS.map(w=>`<th>${WIN_LABEL[w]}</th>`).join("")}</tr></thead><tbody>`;
  for (const [p,label] of BASE_ROWS){
    h += `<tr><td>${label}</td>`;
    for (const w of WINDOWS){
      const b = DATA.baselines[w][p];
      let mark = "";
      if (b.early){ mark += "*"; anyEarly = true; }
      if (b.n < DATA.config.pool_size){ mark += `<sup>${b.n}</sup>`; anyShort = true; }
      h += `<td>${b.ppg===null ? "n/a" : num(b.ppg)}${mark}</td>`;
    }
    h += `</tr>`;
  }
  document.getElementById("baseline-table").innerHTML = h + "</tbody>";
  const c = DATA.config;
  let fn = `Top ${c.pool_size} free agents by points per game, weighted by games played. Forwards must be ${Math.round(c.own_floor.C*100)}%+ owned, defensemen ${Math.round(c.own_floor.D*100)}%+. Minimum games: ${c.min_gp.season} for Season, ${c.min_gp.l30} for Last 30 and Last 14.`;
  if (anyEarly) fn += ` * Early season: Season minimum lowered to ${c.early_min_gp} games.`;
  if (anyShort) fn += ` Small number = fewer than ${c.pool_size} free agents qualified.`;
  document.getElementById("baseline-fn").innerHTML = esc(fn);
}

/* ---------- box score ---------- */
function cmp(block){
  if (!block) return null;
  if (state.vs === "fwd" && block.vs_fwd) return block.vs_fwd;
  return block.vs_pos;
}
function cmpTitle(c){ return c ? `Replacement ${c.vs === "FWD" ? "forward" : c.vs}: ${num(c.base)} PPG` : ""; }

function lensCells(block, withPts, dimmed){
  const cls = dimmed ? " dim" : "";
  if (!block || !block.gp) {
    return `<td class="gs${cls}"></td><td class="${cls}"></td><td class="${cls}"></td>` + (withPts ? `<td class="${cls}"></td>` : "");
  }
  const c = cmp(block);
  const t = esc(cmpTitle(c));
  let h = `<td class="gs${cls}">${gp(block.gp)}</td><td class="${cls}">${num(block.ppg)}</td>`;
  h += `<td class="${signCls(c && c.gap)}${cls}" title="${t}">${c ? signed(c.gap) : ""}</td>`;
  if (withPts) h += `<td class="${signCls(c && c.pts)}${cls}" title="${t}">${c ? signed(c.pts,0) : ""}</td>`;
  return h;
}

function notes(p){
  const s = [];
  if (p.flags.includes("replace")) s.push(`<span class="stamp solid">Replace?</span>`);
  if (p.flags.includes("poor")) s.push(`<span class="stamp red">Poor performer</span>`);
  if (p.flags.includes("small")) s.push(`<span class="stamp grey">Small sample</span>`);
  if (p.flags.includes("nostarts")) s.push(`<span class="stamp grey">No starts yet</span>`);
  return s.join("");
}
function trendCell(t){
  if (t===null || t===undefined) return `<td></td>`;
  const th = DATA.config.trend_pct;
  const pct = Math.round(t*100);
  if (t > th) return `<td class="trend-up" title="Last 30 vs Season">&#9650; ${pct}%</td>`;
  if (t < -th) return `<td class="trend-dn" title="Last 30 vs Season">&#9660; ${Math.abs(pct)}%</td>`;
  return `<td class="mute" title="Last 30 vs Season">${pct===0 ? "even" : (pct>0?"+":MINUS)+Math.abs(pct)+"%"}</td>`;
}

function renderBox(){
  const sub = ["GP","PPG","+/- PPG","+/- Pts"];
  let h = `<thead><tr><th class="namehd" rowspan="2">Player</th>
    <th class="grp" colspan="4">For me</th>
    <th class="grp" colspan="4">Season</th>
    <th class="grp" colspan="4">Last 30</th>
    <th class="grp" colspan="4">Last 14</th>
    <th class="grp" rowspan="2">Trend</th>
    <th class="grp" rowspan="2" style="text-align:left">Notes</th></tr><tr>`;
  for (let i=0;i<4;i++) sub.forEach((s,j)=>{ h += `<th${j===0?' class="gs"':''}>${s}</th>`; });
  h += `</tr></thead><tbody>`;

  const sortKey = p => {
    const o = p.overall && p.overall.l30;
    if (o && o.ppg !== null) return o.ppg;
    return p.forme ? p.forme.ppg : -999;
  };
  for (const [sec,label] of SECTIONS){
    const rows = DATA.players.filter(p => p.section === sec).sort((a,b)=>sortKey(b)-sortKey(a));
    if (!rows.length) continue;
    h += `<tr class="sec"><td colspan="19"><span>${label}</span></td></tr>`;
    for (const p of rows){
      const tag = p.tag ? ` <span class="stamp ${p.tag==="DTD"?"grey":"red"}">${esc(p.tag)}</span>` : "";
      h += `<tr><td class="name"><b>${esc(p.name)}</b>${tag}<small>${esc(p.team)} ${esc(p.pos.join(", "))}</small></td>`;
      h += lensCells(p.forme, true, p.forme && p.forme.small);
      for (const w of WINDOWS) h += lensCells(p.overall && p.overall[w], true, false);
      h += trendCell(p.trend);
      h += `<td class="notes">${notes(p)}</td></tr>`;
    }
  }
  document.getElementById("box").innerHTML = h + "</tbody>";
}

/* ---------- waiver wire ---------- */
function renderWireControls(){
  const posEl = document.getElementById("wire-pos");
  posEl.innerHTML = ["C","LW","RW","D","G"].map(p=>`<button type="button" data-wpos="${p}" aria-pressed="${state.wpos===p}">${p}</button>`).join("");
  const winEl = document.getElementById("wire-win");
  winEl.innerHTML = WINDOWS.map(w=>`<button type="button" data-wwin="${w}" aria-pressed="${state.wwin===w}">${WIN_LABEL[w]}</button>`).join("");
}
function renderWire(){
  renderWireControls();
  const rows = DATA.waiver[state.wwin][state.wpos] || [];
  const b = DATA.baselines[state.wwin][state.wpos];
  const intro = b.ppg===null
    ? `No free agent at ${state.wpos} qualifies for the ${WIN_LABEL[state.wwin]} replacement line yet.`
    : `${WIN_LABEL[state.wwin]} replacement line at ${state.wpos}: ${num(b.ppg)} points per game from ${b.n} free agent${b.n===1?"":"s"}${b.early?" (early season, minimum "+b.min_gp+" games)":""}.`;
  document.getElementById("wire-intro").textContent = intro;
  let h = `<thead><tr><th>Player</th><th>Own</th><th>GP</th><th>PPG</th><th>Pts</th><th>+/- line</th><th style="text-align:left">Upgrade over</th></tr></thead><tbody>`;
  if (!rows.length) h += `<tr><td colspan="7">This tab came in empty. Check the sheet.</td></tr>`;
  for (const r of rows){
    const dim = r.excluded.length ? ' class="dim"' : "";
    const tag = r.tag ? ` <span class="stamp ${r.tag==="DTD"?"grey":"red"}">${esc(r.tag)}</span>` : "";
    const star = r.pool ? `<span class="star" title="Counts toward the replacement line">&#9733;</span> ` : "";
    const why = r.excluded.length ? `<br><span class="why">${esc(r.excluded.join(", "))}</span>` : "";
    const up = r.upgrade ? `<b>${esc(r.upgrade.over)}</b> <span class="pos">${signed(r.upgrade.gain)}</span>` : "";
    h += `<tr${dim}><td>${star}<b>${esc(r.name)}</b>${tag} <span class="mute">${esc(r.team)} ${esc(r.pos.join(", "))}</span>${why}</td>
      <td>${Math.round(r.own*100)}%</td><td>${gp(r.gp)}</td><td>${num(r.ppg)}</td><td>${num(r.total,0)}</td>
      <td class="${signCls(r.gap)}">${signed(r.gap)}</td><td style="text-align:left">${up}</td></tr>`;
  }
  document.getElementById("wire").innerHTML = h + "</tbody>";
}

/* ---------- press room ---------- */
function renderHealth(){
  const hl = DATA.health;
  const items = [...hl.warnings, ...hl.name_checks, ...hl.unparsed.map(u => `Could not read a player name on "${u.tab}": ${u.raw}`)];
  document.getElementById("health").innerHTML = items.length
    ? `<ul>${items.map(i=>`<li>${esc(i)}</li>`).join("")}</ul>`
    : `<p class="ok">All tabs arrived and every player name was matched.</p>`;
  document.getElementById("tabs").innerHTML = hl.tabs.map(t =>
    `<div><span>${esc(t.tab)}${t.kind==="goalie" && t.tab.indexOf("My Team")>=0 ? " (goalies)" : ""}</span><span>${t.rows===null ? "missing" : t.rows}</span></div>`).join("");
}

/* ---------- events ---------- */
document.addEventListener("click", e => {
  const t = e.target.closest("button");
  if (!t) return;
  if (t.dataset.page){
    state.page = t.dataset.page;
    document.querySelectorAll("nav button").forEach(b => { if (b===t) b.setAttribute("aria-current","page"); else b.removeAttribute("aria-current"); });
    document.getElementById("page-front").hidden = state.page !== "front";
    document.getElementById("page-wire").hidden = state.page !== "wire";
    history.replaceState(null, "", state.page === "wire" ? "#wire" : "#");
  } else if (t.dataset.vs){
    state.vs = t.dataset.vs;
    document.querySelectorAll("[data-vs]").forEach(b => b.setAttribute("aria-pressed", b.dataset.vs===state.vs));
    renderBox();
  } else if (t.dataset.wpos){
    state.wpos = t.dataset.wpos; renderWire();
  } else if (t.dataset.wwin){
    state.wwin = t.dataset.wwin; renderWire();
  }
});

renderMast(); renderStories(); renderBaselines(); renderBox(); renderWire(); renderHealth();
if (location.hash === "#wire") document.querySelector('nav button[data-page="wire"]').click();
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
