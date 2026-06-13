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
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px; }
    .stButton > button { border-radius: 8px; font-weight: 500; }
    .metric-card { background: #f8f9fa; border-radius: 10px; padding: 12px 16px; text-align: center; }
    .metric-label { font-size: 12px; color: #6c757d; margin-bottom: 4px; }
    .metric-value { font-size: 24px; font-weight: 600; color: #1a1a1a; }
    .story-box { background: #f0f4ff; border-left: 4px solid #185FA5; padding: 10px 14px;
                 border-radius: 0 8px 8px 0; font-size: 14px; color: #333; margin: 4px 0; }
    .pill { display: inline-block; padding: 2px 10px; border-radius: 12px;
            font-size: 11px; font-weight: 600; }
    .pill-alive { background: #e6f1fb; color: #185FA5; }
    .pill-qualified { background: #eaf3de; color: #2d6a0f; }
    .pill-eliminated { background: #fcebeb; color: #a32d2d; }
    thead th { background: #185FA5 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

AVG_GOALS = 2.65

def poisson_goal(lam):
    L = np.exp(-lam)
    k, p = 0, 1.0
    while True:
        k += 1
        p *= np.random.random()
        if p <= L:
            return k - 1

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
        stats[h]["mp"] += 1
        stats[a]["mp"] += 1
        stats[h]["gf"] += hg
        stats[h]["ga"] += ag
        stats[a]["gf"] += ag
        stats[a]["ga"] += hg
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
                scores[f["id"]] = (
                    int(np.random.poisson(hl)),
                    int(np.random.poisson(al))
                )
        for g in GROUPS:
            ranked = calc_standings(scores, g, FIXTURES)
            for row in ranked[:2]:
                probs[row["id"]] += 1
    return {t: probs[t] / n for t in TEAMS}

def get_actual_standings(group_id):
    scores = {}
    for f in FIXTURES:
        if f["status"] == "FINISHED":
            scores[f["id"]] = (f["hs"], f["as"])
    return calc_standings(scores, group_id, FIXTURES)

def get_status(prob):
    if prob >= 0.985:
        return "QUALIFIED", "pill-qualified"
    if prob <= 0.015:
        return "ELIMINATED", "pill-eliminated"
    return "ALIVE", "pill-alive"

def story_text(tid, standings, prob):
    t = TEAMS[tid]
    row = next((r for r in standings if r["id"] == tid), None)
    if not row:
        return ""
    rank = standings.index(row) + 1
    pct = round(prob * 100)
    remaining = sum(
        1 for f in FIXTURES
        if f["g"] == t["group"] and f["status"] == "SCHEDULED"
        and (f["h"] == tid or f["a"] == tid)
    )
    if prob >= 0.985:
        return f"{t['name']} has mathematically secured their place in the Round of 32."
    if prob <= 0.015:
        return f"{t['name']} has been mathematically eliminated from Group {t['group']}."
    if prob >= 0.80 and rank <= 2:
        return f"{t['name']} is in a strong position ({pct}%). A win in their next match would all but seal qualification."
    if prob >= 0.60 and rank == 2:
        return f"{t['name']} controls their own fate at {pct}%. Avoid defeat and qualification is very likely."
    if prob >= 0.40 and rank == 3:
        return f"{t['name']} is on the edge at {pct}%. They need a win and help from other results to advance."
    if remaining == 1:
        return f"It all comes down to the final match for {t['name']}. At {pct}%, every goal counts — especially goal difference."
    if prob < 0.25:
        return f"{t['name']}'s path is extremely narrow at {pct}%. They need wins and favourable results elsewhere."
    return f"{t['name']} has a {pct}% chance of advancing from {remaining} remaining match{'es' if remaining > 1 else ''}."

def prob_bar_html(prob, width=90):
    pct = round(prob * 100)
    col = "#2d6a0f" if pct >= 70 else "#185FA5" if pct >= 40 else "#a32d2d"
    return (
        f'<div style="display:flex;align-items:center;gap:8px">'
        f'<div style="width:{width}px;height:7px;background:#e9ecef;border-radius:4px;overflow:hidden">'
        f'<div style="width:{pct}%;height:7px;background:{col};border-radius:4px"></div></div>'
        f'<span style="font-weight:600;font-size:13px;color:{col}">{pct}%</span></div>'
    )


st.markdown("## ⚽ FIFA World Cup 2026 — Group Qualification Simulator")
st.caption("Monte Carlo simulation · Poisson model · What-if engine · Group stage Jun 11 – Jun 26 · Built by Abhi Salunke")

tab1, tab2, tab3, tab4 = st.tabs(["🌍 Overview", "📊 Group view", "🔀 What-if simulator", "📈 All probabilities"])

with st.spinner("Running 8,000 simulations..."):
    base_probs = run_simulation(n=8000)

with tab1:
    st.markdown("### Group stage at a glance")
    st.caption("Click a group letter in **Group view** to explore standings, results, and team stories.")
    cols = st.columns(4)
    for i, g in enumerate(GROUPS):
        standings = get_actual_standings(g)
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"**Group {g}**")
                for j, row in enumerate(standings):
                    t = TEAMS[row["id"]]
                    prob = base_probs.get(row["id"], 0)
                    pct = round(prob * 100)
                    col = "#2d6a0f" if pct >= 70 else "#185FA5" if pct >= 40 else "#a32d2d"
                    bg = "rgba(29,158,117,0.07)" if j < 2 else "transparent"
                    st.markdown(
                        f'<div style="display:flex;justify-content:space-between;'
                        f'align-items:center;padding:3px 6px;border-radius:6px;'
                        f'background:{bg};margin:2px 0;font-size:13px">'
                        f'<span>{t["flag"]} {t["name"]}</span>'
                        f'<span style="color:{col};font-weight:600">{pct}%</span></div>',
                        unsafe_allow_html=True
                    )

    st.markdown("---")
    st.caption("Probabilities from 8,000 Monte Carlo runs using a Poisson model with team-specific attack/defense ratings. Green = top 2 qualifying spots.")

with tab2:
    g = st.selectbox("Select group", GROUPS, key="group_select")
    standings = get_actual_standings(g)
    group_fixtures = [f for f in FIXTURES if f["g"] == g]
    completed = [f for f in group_fixtures if f["status"] == "FINISHED"]
    remaining = [f for f in group_fixtures if f["status"] == "SCHEDULED"]

    rows = []
    for i, row in enumerate(standings):
        t = TEAMS[row["id"]]
        prob = base_probs.get(row["id"], 0)
        status, _ = get_status(prob)
        gd = row["gf"] - row["ga"]
        rows.append({
            "Rank": i + 1,
            "Team": f'{t["flag"]} {t["name"]}',
            "P": row["mp"],
            "W": row["w"],
            "D": row["d"],
            "L": row["l"],
            "GF": row["gf"],
            "GA": row["ga"],
            "GD": f'+{gd}' if gd > 0 else str(gd),
            "Pts": row["pts"],
            "Qual %": f'{round(prob * 100)}%',
            "Status": status,
        })

    df = pd.DataFrame(rows)

    def highlight_rows(row):
        rank = row["Rank"]
        if rank == 1:
            return ["background-color: rgba(29,158,117,0.10)"] * len(row)
        if rank == 2:
            return ["background-color: rgba(55,138,221,0.07)"] * len(row)
        return [""] * len(row)

    st.dataframe(
        df.style.apply(highlight_rows, axis=1),
        use_container_width=True,
        hide_index=True,
    )

    col1, col2 = st.columns(2)

    if completed:
        with col1:
            st.markdown("#### Results")
            for f in completed:
                h, a = TEAMS[f["h"]], TEAMS[f["a"]]
                st.markdown(
                    f'<div style="border:0.5px solid #dee2e6;border-radius:10px;padding:10px 14px;margin:6px 0">'
                    f'<div style="font-size:11px;color:#6c757d;margin-bottom:6px">Matchday {f["md"]} · {f["date"]}</div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<span style="font-weight:500;font-size:13px">{h["flag"]} {h["name"]}</span>'
                    f'<span style="font-size:16px;font-weight:700;padding:0 12px">{f["hs"]} – {f["as"]}</span>'
                    f'<span style="font-weight:500;font-size:13px">{a["name"]} {a["flag"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

    if remaining:
        with col2:
            st.markdown("#### Upcoming")
            for f in remaining:
                h, a = TEAMS[f["h"]], TEAMS[f["a"]]
                st.markdown(
                    f'<div style="border:0.5px solid #dee2e6;border-radius:10px;padding:10px 14px;margin:6px 0">'
                    f'<div style="font-size:11px;color:#6c757d;margin-bottom:6px">Matchday {f["md"]} · {f["date"]}</div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<span style="font-weight:500;font-size:13px">{h["flag"]} {h["name"]}</span>'
                    f'<span style="font-size:12px;color:#adb5bd;padding:0 12px">vs</span>'
                    f'<span style="font-weight:500;font-size:13px">{a["name"]} {a["flag"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

    st.markdown("#### Team stories")
    for row in standings:
        t = TEAMS[row["id"]]
        prob = base_probs.get(row["id"], 0)
        story = story_text(row["id"], standings, prob)
        st.markdown(
            f'<div class="story-box"><strong>{t["flag"]} {t["name"]}:</strong> {story}</div>',
            unsafe_allow_html=True
        )

with tab3:
    st.markdown("### What-if simulator")
    st.caption("Fix specific match scores, then run the simulation to see how qualification probabilities change for the group.")

    wi_group = st.selectbox("Select group", GROUPS, key="wi_group")
    wi_remaining = [f for f in FIXTURES if f["g"] == wi_group and f["status"] == "SCHEDULED"]

    if not wi_remaining:
        st.info(f"All Group {wi_group} matches have been played.")
    else:
        overrides = {}
        st.markdown("**Set match results**")
        for f in wi_remaining:
            h, a = TEAMS[f["h"]], TEAMS[f["a"]]
            fix_col, home_col, sep_col, away_col = st.columns([0.3, 0.3, 0.05, 0.35])
            with fix_col:
                fix = st.checkbox(
                    f'Fix: {h["name"]} vs {a["name"]}',
                    key=f'fix_{f["id"]}'
                )
            if fix:
                with home_col:
                    hg = st.number_input(
                        f'{h["flag"]} {h["name"]}',
                        min_value=0, max_value=15, value=1,
                        key=f'hg_{f["id"]}'
                    )
                with sep_col:
                    st.markdown("<div style='padding-top:32px;text-align:center'>–</div>", unsafe_allow_html=True)
                with away_col:
                    ag = st.number_input(
                        f'{a["flag"]} {a["name"]}',
                        min_value=0, max_value=15, value=0,
                        key=f'ag_{f["id"]}'
                    )
                overrides[f["id"]] = (int(hg), int(ag))

        run = st.button("Run simulation ▶", type="primary")

        if run and overrides:
            with st.spinner("Running 8,000 simulations with your what-if results..."):
                ov_tuple = tuple(sorted((k, v) for k, v in overrides.items()))
                wi_probs = run_simulation(overrides_tuple=ov_tuple, n=8000)

            st.markdown(f"#### Probability comparison — Group {wi_group}")
            wi_standings = get_actual_standings(wi_group)
            comp_rows = []
            for row in wi_standings:
                t = TEAMS[row["id"]]
                before = round(base_probs.get(row["id"], 0) * 100)
                after = round(wi_probs.get(row["id"], 0) * 100)
                delta = after - before
                comp_rows.append({
                    "Team": f'{t["flag"]} {t["name"]}',
                    "Before": f"{before}%",
                    "After (what-if)": f"{after}%",
                    "Change": f"+{delta}%" if delta > 0 else f"{delta}%" if delta < 0 else "no change",
                })

            comp_df = pd.DataFrame(comp_rows)

            def colour_delta(val):
                if val.startswith("+"):
                    return "color: #2d6a0f; font-weight: 600"
                if val.startswith("-"):
                    return "color: #a32d2d; font-weight: 600"
                return "color: #6c757d"

            st.dataframe(
                comp_df.style.map(colour_delta, subset=["Change"]),
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("#### Updated stories")
            for row in wi_standings:
                t = TEAMS[row["id"]]
                prob = wi_probs.get(row["id"], 0)
                story = story_text(row["id"], wi_standings, prob)
                st.markdown(
                    f'<div class="story-box"><strong>{t["flag"]} {t["name"]}:</strong> {story}</div>',
                    unsafe_allow_html=True
                )
        elif run and not overrides:
            st.warning("Check at least one match to fix before running.")

with tab4:
    st.markdown("### All 48 teams ranked by qualification probability")

    conf_filter = st.selectbox(
        "Filter by confederation",
        ["All", "UEFA", "CONMEBOL", "CONCACAF", "CAF", "AFC", "OFC"],
        key="conf_filter"
    )

    all_rows = []
    for tid, t in TEAMS.items():
        standings = get_actual_standings(t["group"])
        row = next((r for r in standings if r["id"] == tid), None)
        pts = row["pts"] if row else 0
        prob = base_probs.get(tid, 0)
        status, _ = get_status(prob)
        all_rows.append({
            "Team": f'{t["flag"]} {t["name"]}',
            "Group": t["group"],
            "Confederation": t.get("conf", ""),
            "Pts": pts,
            "Qual %": round(prob * 100),
            "Status": status,
            "_prob": prob,
            "_tid": tid,
        })

    all_rows.sort(key=lambda r: r["_prob"], reverse=True)

    if conf_filter != "All":
        all_rows = [r for r in all_rows if r["Confederation"] == conf_filter]

    display_rows = []
    for i, r in enumerate(all_rows):
        display_rows.append({
            "#": i + 1,
            "Team": r["Team"],
            "Group": r["Group"],
            "Pts": r["Pts"],
            "Qual %": f'{r["Qual %"]}%',
            "Status": r["Status"],
        })

    def highlight_status(row):
        s = row["Status"]
        if s == "QUALIFIED":
            return ["background-color: rgba(29,158,117,0.08)"] * len(row)
        if s == "ELIMINATED":
            return ["background-color: rgba(163,45,45,0.05)"] * len(row)
        return [""] * len(row)

    st.dataframe(
        pd.DataFrame(display_rows).style.apply(highlight_status, axis=1),
        use_container_width=True,
        hide_index=True,
        height=900,
    )
    st.caption("Ranked by Monte Carlo qualification probability. Green = qualified, Red = eliminated, White = still in contention.")

st.markdown("---")
st.caption("Built by **Abhi Salunke** · Senior Data Engineer · [LinkedIn](https://linkedin.com/in/abhisheksalunke12) · [Medium](https://medium.com/@abhisheksalunke) · Data: football-data.org · Model: Poisson + Monte Carlo")
