# td-my-team SPEC (v1.0, 2026-10-09)

Personal fantasy hockey analysis for Marz's Type Disgusting team ("Soft Dump in Corner").
Masthead: **The Morning Soft Dump**

## 0. Purpose

Answer two questions for every player on my team, each compared to available free agents by position:

| Lens | Question | Source |
|---|---|---|
| **FOR ME** | How has he performed in games he STARTED for me? (impact on my results) | Team log tabs |
| **OVERALL** | How has he performed in ALL his games, started or not? (bigger sample, new pickups) | Import My Team tabs |

No snapshots and no history storage. Every run rebuilds from the sheet as it stands that morning.

---

## 1. Hosting

- Repo: `smarz1223/td-my-team` (separate from the `type-disgusting` league site)
- URL: `smarz1223.github.io/td-my-team/` (unlisted, no password, not linked from the hub)
- Refresh: GitHub Actions daily cron `30 11 * * *` (7:30 AM EDT), plus manual run button
- Rule: never patch generated HTML. Change the Python and rebuild.

## 2. Data source (no API, no cookies)

Only source: the published Google Sheet (.xlsx export). The sheet's IMPORTHTML formulas pull public Yahoo pages. Python never contacts Yahoo.

`https://docs.google.com/spreadsheets/d/e/2PACX-1vQWduNAcz_oG_y6og2MHut-t4mmCTZe8_n6Od2Gzzg7_xHJycjqNlG2ydKUImdaXJpphHxiBvhcESHP/pub?output=xlsx`

### Tabs read (exact names required)

| Tab | Holds | Yahoo stat1 |
|---|---|---|
| Import My Skaters | Team log, skaters (started games only) | teamlog table 2 |
| Import My Goalies | Team log, goalies | teamlog table 3 |
| Import My Team Season Avg | Current roster. Skaters table + goalies table (row ~125) | S_AS_2026 |
| Import My Team L30 Avg | Same layout | S_AL30 |
| Import My Team L14 Avg | Same layout | S_AL14 |
| Import FA C / LW / RW / D-Season Avg | Free agents, top 25 | S_AS_2026 |
| Import FA C / LW / RW / D-L30 Avg | Free agents, top 25 | S_AL30 |
| Import FA C / LW / RW / D-L14 Avg | Free agents, top 25 | S_AL14 |
| Import FA Goalies-Season Total | Free agents, top 25 | S_S_2026 |
| Import FA Goalies-L30 Total | Free agents, top 25 | S_L30 |
| Import FA Goalies-L14 Total | Free agents, top 25 | S_L14 |
| Status Overrides (optional) | Columns: Player, Status (Active, Injured, Cut) | n/a |
| Name Fixes (optional) | Columns: Raw Name, Use Name | n/a |

### Reading rules

- Find each table by header text (`Forwards/Defensemen` or `Goaltenders`), never fixed rows or columns. Tabs may hold two tables, and some tabs also hold a mirrored copy of the import: take the first complete table per header and dedupe players.
- Read raw Yahoo columns only: name string, Roster Status, GP*, Fan Pts, % Ros, stat columns. Ignore helper columns ("3 lines", "Clean 1-5", "Final", lookups) and any `#REF!` in them.
- Pull date comes from the `Opp: M/D` header (staleness check).
- A missing optional tab is fine. A missing required tab shows in the Health box; the rest of the site still builds.

## 3. Scoring

| Skaters | Pts | Goalies | Pts |
|---|---|---|---|
| G | 15 | W | 20 |
| A | 10 | GA | -5 |
| +/- | 5 | SV | 1 |
| PIM | 2.5 | SHO | 10 |
| PPP | 5 | | |
| SOG | 2 | | |

- Team log tabs have no Fan Pts column. Points are computed from stats (verified: Aho team log = 165).
- Avg tabs: per-game Fan Pts as given by Yahoo.
- Goalie Total tabs: PPG = Fan Pts / GP.

## 4. Name parsing and matching

Example raw string: `Sebastian AhoPlayer NoteCAR - C\n7:00 pm vs VAN`

1. Keep the first line only (drops game time).
2. Remove icon characters (Unicode private-use range).
3. Read `TEAM - POS` from the end. POS is a comma list of C, LW, RW, D, G.
4. Strip note text from the end of the name: `Player Note`, `New Player Note`, `No new player Notes`.
5. Strip injury tag from the end of the name: `IR-LT`, `IR-NR`, `IR`, `DTD`, `O`, `NA`. Save as tag.
6. Apply Name Fixes tab if present.

Match key = accent-folded lowercase name + position group (F, D, G). Team is not in the key (trades do not break matches). Handles same-name players (Sebastian Aho CAR F vs NYI D).

Verified on 2026-10-09 workbook: every name on every tab parsed; team log and roster matched with no fixes.

## 5. Player status (no history needed)

| Status | Rule | Example (10/9) |
|---|---|---|
| Active | On roster pull, tag none or DTD (DTD badge) | Aho |
| Active, no starts yet | On roster pull, not in team log. FOR ME blank | Bryan Rust |
| Injured | On roster pull, tag IR, IR-LT, IR-NR, or O | Barzal (IR-NR) |
| Cut | In team log, not on roster pull. FOR ME only | Konecny |
| Override | Status Overrides tab wins over all rules | n/a |

## 6. Replacement baselines

Positions: C, LW, RW, D, G, plus FWD (C + LW + RW pools combined, duplicates removed).
Windows: Season, L30, L14.

| Rule | FWD (C/LW/RW) | D | G |
|---|---|---|---|
| Ownership floor | 20% | 33% | none |
| Min GP, Season | 10 | 10 | 10 |
| Min GP, L30 | 3 | 3 | 3 |
| Min GP, L14 | 3 | 3 | 3 |
| Pool | Top 5 by PPG | Top 5 by PPG | Top 5 by PPG |

- Early-season fallback: if fewer than 5 qualify on Season, Season min GP drops to 3 and the baseline is labeled "EARLY SEASON".
- If any pool still has fewer than 5, use those that qualify and show the count.
- Baseline PPG = GP-weighted: sum of Fan Pts totals / sum of GP.

## 7. Comparisons

For each player, in each lens/window:

- **vs Pos:** toughest (highest) baseline among his eligible positions.
- **vs FWD:** forwards only, combined forward baseline.
- PPG gap = his PPG minus baseline PPG.
- Pts over replacement = PPG gap x GP.

| Lens | Windows | Baseline used |
|---|---|---|
| FOR ME | Team log (whole stint) | Season |
| OVERALL | Season, L30, L14 | Matching window |

- FOR ME with fewer than 5 starts: grayed out, "SMALL SAMPLE" stamp.

## 8. Flags and trend (OVERALL only)

| Flag | Rule |
|---|---|
| Poor Performer | L30 PPG below L30 vs Pos baseline |
| Replace? | L30 pts over replacement below -50 |
| Trend | L30 PPG / Season PPG - 1. Up arrow above +15%, down arrow below -15% |

## 9. Pages

1. **Front Page:** one roster table, two column groups (FOR ME, OVERALL). Sections in order: C, LW, RW, D, G, Injured, then "CUT FROM THE ROSTER" (FOR ME only). Multi-position players listed once, under their first listed position. Table scrolls sideways on mobile.
2. **Waiver Wire:** free agents by position (C, LW, RW, D, G) and window (Season, L30, L14). Pool members marked with a star; rows failing the ownership or GP cutoff grayed with the reason. "Upgrade over" names my weakest Active player eligible at that position, measured in the SAME window, and the PPG gain (shown only when positive).
3. **Front page stories:** three auto-generated briefs: best FOR ME performer (5+ starts), biggest OVERALL L30 drag, best L30 waiver upgrade.
4. **Compare toggle:** box score switches forwards between "Their position" and "All forwards" baselines.

### Press room notes (health box, footer, both pages)

- Sheet pull date. Warn if older than 2 days.
- Row count per tab. Warn on empty or missing tab.
- Unmatched names list.
- Warn if any Season tab shows GP above 82 (stale prior-season link).

## 10. Look and feel: 1990s newspaper sports section

- Newsprint off-white background, ink black text, one faded red accent
- Masthead "The Morning Soft Dump" in blackletter (UnifrakturCook), ears left and right, double-rule dateline
- Headlines, nav, and agate stat tables: Archivo (condensed widths, Franklin Gothic feel). Body and decks: Old Standard TT
- Palette: newsprint #e7e2d4, shade #d8d0bc, ink #24211b, soft ink #5f594c, spot red #a3291f (negatives and flags)
- Flags and SMALL SAMPLE as small all-caps stamps

## 11. Repo files

| File | Purpose |
|---|---|
| `fetch_data.py` | Download sheet, parse, match, compute, write `data/data.json` |
| `build.py` | Generate `index.html` from `data/data.json` |
| `.github/workflows/refresh.yml` | Daily cron + manual run, commits data and HTML |
| `data/data.json` | Generated each run (do not edit) |
| `index.html` | Generated each run (do not edit) |
| `SPEC.md` | This file |

## 12. Out of scope (decided)

No snapshots, no This Week page, no "since dropped" tracking, no Day by Day, no Player Detail page, no Yahoo API or cookies.

## 13. Safety rules in the code

- If the sheet download fails or the roster tables are empty, the run stops and the live site is left unchanged.
- Fan Pts on my-team rows are checked against the scoring weights; mismatches are reported.
- A Cut player sharing a last name and position group with a roster player is flagged as a possible name mismatch.

## 14. Season rollover checklist

- Update `S_AS_2026` / `S_S_2026` to the new year on all Season tabs (4 FA skater tabs, FA goalie tab, both tables on Import My Team Season Avg).
- Update `SEASON_LABEL` in `fetch_data.py`.
- Confirm `MY_TEAM_NAME` and the team log URL (`/hockey/24054/1/teamlog`) if league ID or team number changes.
