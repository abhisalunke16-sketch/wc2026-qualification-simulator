import streamlit as st
import numpy as np
import pandas as pd
from collections import defaultdict
from data import TEAMS, FIXTURES, GROUPS

st.set_page_config(
    page_title="FIFA WC 2026 — Qualification Simulator",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container { padding-top: 0 !important; padding-bottom: 2rem; max-width: 1140px; }

/* ── Hero banner ── */
.hero {
    background: #1a6b2f;
    border-radius: 0 0 20px 20px;
    padding: 28px 32px 22px;
    margin: -1rem -1rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(
        90deg,
        rgba(255,255,255,0.03) 0px, rgba(255,255,255,0.03) 1px,
        transparent 1px, transparent 60px
    ),
    repeating-linear-gradient(
        0deg,
        rgba(255,255,255,0.03) 0px, rgba(255,255,255,0.03) 1px,
        transparent 1px, transparent 60px
    );
}
.hero-title {
    font-size: 28px; font-weight: 900; color: #ffffff;
    letter-spacing: -0.5px; margin: 0; position: relative;
}
.hero-sub {
    font-size: 13px; color: rgba(255,255,255,0.7);
    margin-top: 4px; position: relative;
}
.hero-badges {
    display: flex; gap: 8px; flex-wrap: wrap;
    margin-top: 12px; position: relative;
}
.hero-badge {
    background: rgba(255,255,255,0.15);
    color: #fff; font-size: 11px; font-weight: 600;
    padding: 4px 10px; border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.25);
}
.hero-badge.live { background: #e63946; border-color: #e63946; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #f0f7f2;
    border-radius: 12px;
    padding: 4px;
    gap: 2px;
    border: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #4a7c59 !important;
    padding: 8px 18px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #1a6b2f !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Group card on overview ── */
.group-card {
    background: #fff;
    border: 1px solid #e2ede6;
    border-radius: 14px;
    padding: 14px;
    height: 100%;
}
.group-card-title {
    font-size: 11px; font-weight: 700; letter-spacing: 0.08em;
    color: #1a6b2f; text-transform: uppercase; margin-bottom: 10px;
    display: flex; align-items: center; gap: 6px;
}
.group-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 5px 8px; border-radius: 8px; margin: 2px 0; font-size: 13px;
}
.group-row.qualify { background: rgba(26,107,47,0.08); }

/* ── Standings table ── */
.pitch-table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 13px; }
.pitch-table th {
    background: #1a6b2f; color: #fff; padding: 9px 12px;
    text-align: center; font-weight: 600; font-size: 11px; letter-spacing: 0.04em;
}
.pitch-table th:first-child { text-align: left; border-radius: 10px 0 0 0; }
.pitch-table th:last-child { border-radius: 0 10px 0 0; }
.pitch-table td { padding: 9px 12px; text-align: center; border-bottom: 1px solid #f0f5f2; color: #333; }
.pitch-table td:first-child { text-align: left; font-weight: 500; }
.pitch-table tr:last-child td { border-bottom: none; }
.pitch-table tr:nth-child(1) td { background: rgba(26,107,47,0.07); }
.pitch-table tr:nth-child(2) td { background: rgba(26,107,47,0.03); }
.pitch-table-wrap { border: 1px solid #e2ede6; border-radius: 12px; overflow: hidden; }

/* ── Match cards ── */
.match-card {
    background: #fff; border: 1px solid #e2ede6;
    border-radius: 12px; padding: 12px 16px; margin: 6px 0;
}
.match-card-date { font-size: 10px; color: #6b9b7a; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px; }
.match-card-row { display: flex; align-items: center; justify-content: space-between; }
.match-team { font-size: 13px; font-weight: 600; color: #1a1a1a; flex: 1; }
.match-team.right { text-align: right; }
.match-score {
    background: #1a6b2f; color: #fff;
    font-size: 16px; font-weight: 800;
    padding: 4px 14px; border-radius: 8px; min-width: 64px; text-align: center;
}
.match-upcoming { background: #f0f7f2; color: #4a7c59; font-size: 12px; font-weight: 600; padding: 4px 14px; border-radius: 8px; min-width: 64px; text-align: center; }

/* ── Story boxes ── */
.story-card {
    background: linear-gradient(135deg, #f0f7f2 0%, #e8f5ed 100%);
    border: 1px solid #c8e6d0; border-left: 4px solid #1a6b2f;
    border-radius: 0 10px 10px 0; padding: 11px 14px;
    font-size: 13px; color: #2d4a35; margin: 5px 0; line-height: 1.6;
}

/* ── Status pills ── */
.pill { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 10px; font-weight: 700; letter-spacing: 0.04em; }
.pill-alive    { background: #e6f1fb; color: #185FA5; }
.pill-qualified { background: #d4edda; color: #1a6b2f; }
.pill-eliminated { background: #fde8e8; color: #c0392b; }

/* ── Prob bar ── */
.pbar-wrap { display: flex; align-items: center; gap: 8px; }
.pbar-track { height: 8px; background: #e2ede6; border-radius: 4px; overflow: hidden; flex: 1; max-width: 100px; }
.pbar-fill { height: 8px; border-radius: 4px; }

/* ── Section headings ── */
.section-head {
    font-size: 13px; font-weight: 700; color: #1a6b2f;
    letter-spacing: 0.05em; text-transform: uppercase;
    border-bottom: 2px solid #e2ede6; padding-bottom: 6px;
    margin: 1.2rem 0 0.6rem;
}

/* ── What-if panel ── */
.wi-match-block {
    background: #fff; border: 1px solid #e2ede6; border-radius: 12px;
    padding: 14px 16px; margin: 8px 0;
}
.wi-teams-row { display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 600; color: #1a1a1a; margin-bottom: 10px; }
.wi-vs { font-size: 11px; color: #6b9b7a; font-weight: 600; flex: 1; text-align: center; }

/* ── Before/after comparison ── */
.compare-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; border-radius: 10px; margin: 4px 0; background: #f8fbf9; border: 1px solid #e2ede6; }
.compare-team { font-size: 13px; font-weight: 600; flex: 1; }
.compare-before { font-size: 14px; color: #888; font-weight: 500; min-width: 48px; text-align: center; }
.compare-arrow { font-size: 14px; color: #aaa; padding: 0 6px; }
.compare-after { font-size: 16px; font-weight: 800; min-width: 54px; text-align: center; }
.compare-delta { font-size: 11px; font-weight: 700; min-width: 44px; text-align: right; }
.delta-pos { color: #1a6b2f; }
.delta-neg { color: #c0392b; }
.delta-neu { color: #888; }

/* ── All-teams table ── */
.at-row { display: flex; align-items: center; padding: 8px 12px; border-radius: 8px; margin: 3px 0; font-size: 13px; }
.at-row:hover { background: #f0f7f2; }
.at-rank { width: 28px; color: #aaa; font-size: 12px; font-weight: 700; }
.at-team { flex: 1; font-weight: 600; color: #1a1a1a; }
.at-group { width: 44px; color: #6b9b7a; font-size: 12px; font-weight: 600; text-align: center; }
.at-pts { width: 36px; font-weight: 700; text-align: center; }
.at-prob { width: 140px; }

/* ── Footer ── */
.footer { text-align: center; font-size: 12px; color: #6b9b7a; padding: 16px 0 4px; border-top: 1px solid #e2ede6; margin-top: 2rem; }
.footer a { color: #1a6b2f; text-decoration: none; font-weight: 600; }

/* ── Streamlit overrides ── */
.stButton > button {
    background: #1a6b2f !important; color: white !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; font-size: 14px !important;
    padding: 10px 24px !important;
}
.stButton > button:hover { background: #145523 !important; }
.stSelectbox label { font-weight: 600; color: #2d4a35; }
div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 800 !important; color: #1a6b2f !important; }
</style>
""", unsafe_allow_html=True)

AVG_GOALS = 2.65

def get_lambda(h_id, a_id):
    h, a = TEAMS[h_id], TEAMS[a_id]
    hl = max(0.3, h["atk"] * a["def"] * AVG_GOALS)
    al = max(0.3, a["atk"] * h["def"] * AVG_GOALS)
    return hl, al

def calc_standings(scores, group_id, fixtures):
    tids = [t for t, d in TEAMS.items() if d["group"] == group_id]
    stats = {t: {"pts": 0, "gf": 0, "ga": 0, "w": 0, "d": 0, "l": 0, "mp": 0} for t in tids}
    for f in fixtures:
        if f["g"] != group_id:
            continue
        s = scores.get(f["id"])
        if s is None:
            continue
        hg, ag = s
        h, a = f["h"], f["a"]
        stats[h]["mp"] += 1; stats[a]["mp"] += 1
        stats[h]["gf"] += hg; stats[h]["ga"] += ag
        stats[a]["gf"] += ag; stats[a]["ga"] += hg
        if hg > ag:
            stats[h]["pts"] += 3; stats[h]["w"] += 1; stats[a]["l"] += 1
        elif hg < ag:
            stats[a]["pts"] += 3; stats[a]["w"] += 1; stats[h]["l"] += 1
        else:
            stats[h]["pts"] += 1; stats[a]["pts"] += 1
            stats[h]["d"] += 1; stats[a]["d"] += 1
    rows = [{"id": t, **stats[t]} for t in tids]
    rows.sort(key=lambda r: (r["pts"], r["gf"] - r["ga"], r["gf"]), reverse=True)
    return rows

@st.cache_data(show_spinner=False)
def run_simulation(overrides_tuple=(), n=8000):
    overrides = dict(overrides_tuple)
    probs = defaultdict(int)
    for _ in range(n):
        scores = {}
        for f in FIXTURES:
            if f["status"] == "FINISHED":
                scores[f["id"]] = (f["hs"], f["as"])
            elif f["id"] in overrides:
                scores[f["id"]] = overrides[f["id"]]
            else:
                hl, al = get_lambda(f["h"], f["a"])
                scores[f["id"]] = (int(np.random.poisson(hl)), int(np.random.poisson(al)))
        for g in GROUPS:
            ranked = calc_standings(scores, g, FIXTURES)
            for row in ranked[:2]:
                probs[row["id"]] += 1
    return {t: probs[t] / n for t in TEAMS}

def get_actual_standings(group_id):
    scores = {f["id"]: (f["hs"], f["as"]) for f in FIXTURES if f["status"] == "FINISHED"}
    return calc_standings(scores, group_id, FIXTURES)

def get_status(prob):
    if prob >= 0.985: return "QUALIFIED", "pill-qualified"
    if prob <= 0.015: return "ELIMINATED", "pill-eliminated"
    return "ALIVE", "pill-alive"

def story_text(tid, standings, prob):
    t = TEAMS[tid]
    row = next((r for r in standings if r["id"] == tid), None)
    if not row: return ""
    rank = standings.index(row) + 1
    pct = round(prob * 100)
    remaining = sum(1 for f in FIXTURES if f["g"] == t["group"] and f["status"] == "SCHEDULED" and (f["h"] == tid or f["a"] == tid))
    if prob >= 0.985: return f"{t['name']} has mathematically secured their place in the Round of 32."
    if prob <= 0.015: return f"{t['name']} has been mathematically eliminated from Group {t['group']}."
    if prob >= 0.80 and rank <= 2: return f"{t['name']} is in a strong position ({pct}%). A win in their next match would all but seal qualification."
    if prob >= 0.60 and rank == 2: return f"{t['name']} controls their own fate at {pct}%. Avoid defeat and qualification is very likely."
    if prob >= 0.40 and rank == 3: return f"{t['name']} is on the edge at {pct}%. They need a win and help from other results to advance."
    if remaining == 1: return f"It all comes down to the final match for {t['name']}. At {pct}%, every goal counts — especially goal difference."
    if prob < 0.25: return f"{t['name']}'s path is extremely narrow at {pct}%. They need wins and favourable results elsewhere."
    return f"{t['name']} has a {pct}% chance of advancing from {remaining} remaining match{'es' if remaining > 1 else ''}."

def pbar(prob, max_width=110):
    pct = round(prob * 100)
    col = "#1a6b2f" if pct >= 70 else "#2980b9" if pct >= 40 else "#c0392b"
    fill_w = int(max_width * prob)
    return (
        f'<div class="pbar-wrap">'
        f'<div class="pbar-track" style="width:{max_width}px">'
        f'<div class="pbar-fill" style="width:{fill_w}px;background:{col}"></div></div>'
        f'<span style="font-weight:700;font-size:13px;color:{col};min-width:36px">{pct}%</span></div>'
    )

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">⚽ FIFA World Cup 2026 — Qualification Simulator</div>
  <div class="hero-sub">USA · Canada · Mexico &nbsp;|&nbsp; Group stage: Jun 11 – Jun 26, 2026</div>
  <div class="hero-badges">
    <span class="hero-badge live">● Live</span>
    <span class="hero-badge">Runs 8,000 simulations per calculation</span>
    <span class="hero-badge">Predicts scores using team strength data</span>
    <span class="hero-badge">Test any match result instantly</span>
    <span class="hero-badge">48 teams · 12 groups</span>
  </div>
</div>
""", unsafe_allow_html=True)

with st.spinner("Running simulations..."):
    base_probs = run_simulation(n=8000)

tab1, tab2, tab3, tab4 = st.tabs(["🌍  Overview", "📊  Group view", "🔀  What-if simulator", "📈  All probabilities"])

# ── TAB 1: OVERVIEW ───────────────────────────────────────────────────────────
with tab1:
    finished_count = sum(1 for f in FIXTURES if f["status"] == "FINISHED")
    total = len(FIXTURES)
    c1, c2, c3 = st.columns(3)
    c1.metric("Matches played", f"{finished_count} / {total}")
    c2.metric("Teams still alive", sum(1 for t in TEAMS if 0.015 < base_probs.get(t, 0) < 0.985))
    c3.metric("Groups active", 12)

    st.markdown('<div class="section-head">All 12 groups</div>', unsafe_allow_html=True)
    st.caption("Green rows = projected top 2. Click **Group view** tab to explore any group in detail.")

    cols = st.columns(4)
    for i, g in enumerate(GROUPS):
        standings = get_actual_standings(g)
        with cols[i % 4]:
            rows_html = ""
            for j, row in enumerate(standings):
                t = TEAMS[row["id"]]
                prob = base_probs.get(row["id"], 0)
                pct = round(prob * 100)
                col_c = "#1a6b2f" if pct >= 70 else "#2980b9" if pct >= 40 else "#c0392b"
                cls = "qualify" if j < 2 else ""
                rows_html += (
                    f'<div class="group-row {cls}">'
                    f'<span>{t["name"]}</span>'
                    f'<span style="color:{col_c};font-weight:700">{pct}%</span>'
                    f'</div>'
                )
            st.markdown(
                f'<div class="group-card">'
                f'<div class="group-card-title">⬡ Group {g}</div>'
                f'{rows_html}</div>',
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.caption("Each team's qualification % is calculated by simulating all remaining matches 8,000 times using historical team strength data. Green rows = projected top 2.")

# ── TAB 2: GROUP VIEW ─────────────────────────────────────────────────────────
with tab2:
    g = st.selectbox("Select group", GROUPS, key="group_select",
                     format_func=lambda x: f"Group {x}")
    standings = get_actual_standings(g)
    group_fixtures = [f for f in FIXTURES if f["g"] == g]
    completed = [f for f in group_fixtures if f["status"] == "FINISHED"]
    remaining_fx = [f for f in group_fixtures if f["status"] == "SCHEDULED"]

    # Standings table
    header = "<thead><tr><th>Team</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th><th>Qual %</th><th>Status</th></tr></thead>"
    body = "<tbody>"
    for i, row in enumerate(standings):
        t = TEAMS[row["id"]]
        prob = base_probs.get(row["id"], 0)
        status, scls = get_status(prob)
        gd = row["gf"] - row["ga"]
        gd_str = f'+{gd}' if gd > 0 else str(gd)
        body += (
            f'<tr>'
            f'<td>{t["name"]}</td>'
            f'<td>{row["mp"]}</td><td>{row["w"]}</td><td>{row["d"]}</td><td>{row["l"]}</td>'
            f'<td>{row["gf"]}</td><td>{row["ga"]}</td><td><strong>{gd_str}</strong></td>'
            f'<td><strong>{row["pts"]}</strong></td>'
            f'<td>{pbar(prob)}</td>'
            f'<td><span class="pill {scls}">{status}</span></td>'
            f'</tr>'
        )
    body += "</tbody>"
    st.markdown(
        f'<div class="pitch-table-wrap"><table class="pitch-table">{header}{body}</table></div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    if completed:
        with col1:
            st.markdown('<div class="section-head">Results</div>', unsafe_allow_html=True)
            for f in completed:
                h, a = TEAMS[f["h"]], TEAMS[f["a"]]
                st.markdown(
                    f'<div class="match-card">'
                    f'<div class="match-card-date">Matchday {f["md"]} · {f["date"]}</div>'
                    f'<div class="match-card-row">'
                    f'<span class="match-team">{h["name"]}</span>'
                    f'<span class="match-score">{f["hs"]} – {f["as"]}</span>'
                    f'<span class="match-team right">{a["name"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )
    if remaining_fx:
        with col2:
            st.markdown('<div class="section-head">Upcoming</div>', unsafe_allow_html=True)
            for f in remaining_fx:
                h, a = TEAMS[f["h"]], TEAMS[f["a"]]
                st.markdown(
                    f'<div class="match-card">'
                    f'<div class="match-card-date">Matchday {f["md"]} · {f["date"]}</div>'
                    f'<div class="match-card-row">'
                    f'<span class="match-team">{h["name"]}</span>'
                    f'<span class="match-upcoming">vs</span>'
                    f'<span class="match-team right">{a["name"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

    st.markdown('<div class="section-head">Team analysis</div>', unsafe_allow_html=True)
    for row in standings:
        t = TEAMS[row["id"]]
        prob = base_probs.get(row["id"], 0)
        story = story_text(row["id"], standings, prob)
        st.markdown(
            f'<div class="story-card"><strong>{t["name"]}:</strong> {story}</div>',
            unsafe_allow_html=True
        )

# ── TAB 3: WHAT-IF ───────────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div style="background:#f0f7f2;border:1px solid #c8e6d0;border-radius:12px;padding:12px 16px;margin-bottom:1rem;font-size:13px;color:#2d4a35">
    <strong>How it works:</strong> Fix any upcoming match result using the checkboxes below, then hit <strong>Run simulation</strong>.
    The tool re-runs 8,000 scenarios with your chosen score locked in, and shows how each team's qualification chance changes.
    </div>
    """, unsafe_allow_html=True)

    wi_group = st.selectbox("Select group", GROUPS, key="wi_group", format_func=lambda x: f"Group {x}")
    wi_remaining = [f for f in FIXTURES if f["g"] == wi_group and f["status"] == "SCHEDULED"]

    if not wi_remaining:
        st.success(f"All Group {wi_group} matches have been played — no what-if needed!")
    else:
        overrides = {}
        st.markdown('<div class="section-head">Set match results</div>', unsafe_allow_html=True)

        for f in wi_remaining:
            h, a = TEAMS[f["h"]], TEAMS[f["a"]]
            chk_col, rest_col = st.columns([0.28, 0.72])
            with chk_col:
                fix = st.checkbox(
                    f'Fix result',
                    key=f'fix_{f["id"]}',
                    help=f'{h["name"]} vs {a["name"]} · Matchday {f["md"]} · {f["date"]}'
                )
            with rest_col:
                if fix:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:8px;font-size:13px;font-weight:600;margin-top:4px">'
                        f'<span>{h["name"]}</span>'
                        f'<span style="color:#6b9b7a">vs</span>'
                        f'<span>{a["name"]}</span>'
                        f'<span style="font-size:11px;color:#6b9b7a;font-weight:400">· MD{f["md"]} · {f["date"]}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    sc1, sc2, sc3 = st.columns([1, 0.12, 1])
                    with sc1:
                        hg = st.number_input(f'{h["name"]} goals', min_value=0, max_value=15, value=1, key=f'hg_{f["id"]}', label_visibility="collapsed")
                    with sc2:
                        st.markdown("<div style='text-align:center;padding-top:8px;font-weight:700;color:#888'>–</div>", unsafe_allow_html=True)
                    with sc3:
                        ag = st.number_input(f'{a["name"]} goals', min_value=0, max_value=15, value=0, key=f'ag_{f["id"]}', label_visibility="collapsed")
                    overrides[f["id"]] = (int(hg), int(ag))
                else:
                    st.markdown(
                        f'<div style="font-size:13px;color:#aaa;margin-top:4px">'
                        f'{h["name"]} vs {a["name"]} &nbsp;·&nbsp; MD{f["md"]} · {f["date"]}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

        st.markdown("")
        run = st.button("▶  Run simulation", type="primary")

        if run:
            if not overrides:
                st.warning("Tick at least one match to fix before running.")
            else:
                with st.spinner(f"Running 8,000 simulations for Group {wi_group}..."):
                    ov_tuple = tuple(sorted((k, v) for k, v in overrides.items()))
                    wi_probs = run_simulation(overrides_tuple=ov_tuple, n=8000)

                st.markdown(f'<div class="section-head">Probability comparison — Group {wi_group}</div>', unsafe_allow_html=True)
                wi_standings = get_actual_standings(wi_group)

                for row in wi_standings:
                    t = TEAMS[row["id"]]
                    before = base_probs.get(row["id"], 0)
                    after = wi_probs.get(row["id"], 0)
                    before_pct = round(before * 100)
                    after_pct = round(after * 100)
                    delta = after_pct - before_pct
                    dcls = "delta-pos" if delta > 0 else "delta-neg" if delta < 0 else "delta-neu"
                    dstr = f"+{delta}%" if delta > 0 else f"{delta}%" if delta < 0 else "—"
                    after_col = "#1a6b2f" if after_pct >= 70 else "#2980b9" if after_pct >= 40 else "#c0392b"
                    st.markdown(
                        f'<div class="compare-row">'
                        f'<span class="compare-team">{t["name"]}</span>'
                        f'<span class="compare-before">{before_pct}%</span>'
                        f'<span class="compare-arrow">→</span>'
                        f'<span class="compare-after" style="color:{after_col}">{after_pct}%</span>'
                        f'<span class="compare-delta {dcls}">{dstr}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                st.markdown('<div class="section-head">Updated team analysis</div>', unsafe_allow_html=True)
                for row in wi_standings:
                    t = TEAMS[row["id"]]
                    prob = wi_probs.get(row["id"], 0)
                    story = story_text(row["id"], wi_standings, prob)
                    st.markdown(
                        f'<div class="story-card"><strong>{t["name"]}:</strong> {story}</div>',
                        unsafe_allow_html=True
                    )

# ── TAB 4: ALL PROBABILITIES ─────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-head">All 48 teams ranked by qualification probability</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        conf_filter = st.selectbox("Confederation", ["All", "UEFA", "CONMEBOL", "CONCACAF", "CAF", "AFC", "OFC"])
    with c2:
        sort_by = st.selectbox("Sort by", ["Qualification probability", "Points", "Group"])

    all_rows = []
    for tid, t in TEAMS.items():
        s = get_actual_standings(t["group"])
        row = next((r for r in s if r["id"] == tid), None)
        pts = row["pts"] if row else 0
        prob = base_probs.get(tid, 0)
        status, scls = get_status(prob)
        all_rows.append({"id": tid, "name": t["name"], "flag": t["flag"], "group": t["group"],
                         "conf": t.get("conf", ""), "pts": pts, "prob": prob, "status": status, "scls": scls})

    if conf_filter != "All":
        all_rows = [r for r in all_rows if r["conf"] == conf_filter]

    if sort_by == "Qualification probability":
        all_rows.sort(key=lambda r: r["prob"], reverse=True)
    elif sort_by == "Points":
        all_rows.sort(key=lambda r: r["pts"], reverse=True)
    else:
        all_rows.sort(key=lambda r: (r["group"], -r["prob"]))

    # Header row
    st.markdown(
        '<div class="at-row" style="font-size:11px;font-weight:700;color:#6b9b7a;letter-spacing:0.05em;border-bottom:1px solid #e2ede6;margin-bottom:4px">'
        '<span class="at-rank">#</span><span class="at-team">Team</span>'
        '<span class="at-group">Group</span><span class="at-pts">Pts</span>'
        '<span class="at-prob">Qual probability</span>'
        '<span style="min-width:88px;text-align:right">Status</span></div>',
        unsafe_allow_html=True
    )
    for i, r in enumerate(all_rows):
        col_c = "#1a6b2f" if r["prob"] >= 0.70 else "#2980b9" if r["prob"] >= 0.40 else "#c0392b"
        bg = "rgba(26,107,47,0.04)" if i % 2 == 0 else "transparent"
        st.markdown(
            f'<div class="at-row" style="background:{bg}">'
            f'<span class="at-rank">{i+1}</span>'
            f'<span class="at-team">{r["name"]}</span>'
            f'<span class="at-group">{r["group"]}</span>'
            f'<span class="at-pts" style="color:{col_c}">{r["pts"]}</span>'
            f'<span class="at-prob">{pbar(r["prob"])}</span>'
            f'<span style="min-width:88px;text-align:right"><span class="pill {r["scls"]}">{r["status"]}</span></span>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown("")
    st.caption(f"Showing {len(all_rows)} teams · Sorted by {sort_by.lower()} · Qualification % based on 8,000 simulated outcomes")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">'
    'Built by <strong>Abhishek Salunke</strong> · Senior Data Engineer · '
    '<a href="https://linkedin.com/in/abhisheksalunke12" target="_blank">LinkedIn</a> · '
    '<a href="https://medium.com/@abhisheksalunke" target="_blank">Medium</a>'
    '</div>',
    unsafe_allow_html=True
)
