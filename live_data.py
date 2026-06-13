"""
live_data.py
Fetches live FIFA World Cup 2026 scores from the openfootball/worldcup.json
GitHub repository — completely free, no API key required.

URL: https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json
Updated: manually by the openfootball community ~once per day during the tournament.
Cache: 10 minutes (ttl=600) so repeated page loads don't hammer GitHub.
Fallback: if the fetch fails for any reason, the app uses static data.py fixtures.
"""

import requests
import streamlit as st
from datetime import datetime, timezone
from data import FIXTURES, TEAMS

API_URL = (
    "https://raw.githubusercontent.com/openfootball/"
    "worldcup.json/master/2026/worldcup.json"
)

# Map openfootball team names → our team IDs in data.py
TEAM_NAME_MAP = {
    "Mexico":               "MEX",
    "South Africa":         "ZAF",
    "South Korea":          "KOR",
    "Czech Republic":       "CZE",
    "Canada":               "CAN",
    "Bosnia and Herzegovina": "UEFA_A",   # UEFA Path A winner
    "Qatar":                "QAT",
    "Switzerland":          "SUI",
    "Brazil":               "BRA",
    "Morocco":              "MAR",
    "Haiti":                "HTI",
    "Scotland":             "SCO",
    "USA":                  "USA",
    "United States":        "USA",
    "Paraguay":             "PAR",
    "Australia":            "AUS",
    "Türkiye":              "UEFA_C",    # UEFA Path C winner
    "Turkey":               "UEFA_C",
    "Germany":              "GER",
    "Curaçao":              "CUW",
    "Curacao":              "CUW",
    "Ivory Coast":          "CIV",
    "Côte d'Ivoire":        "CIV",
    "Ecuador":              "ECU",
    "Netherlands":          "NED",
    "Japan":                "JPN",
    "Sweden":               "UEFA_B",    # UEFA Path B winner
    "Tunisia":              "TUN",
    "Belgium":              "BEL",
    "Egypt":                "EGY",
    "Iran":                 "IRN",
    "New Zealand":          "NZL",
    "Spain":                "ESP",
    "Cape Verde":           "CPV",
    "Saudi Arabia":         "KSA",
    "Uruguay":              "URU",
    "France":               "FRA",
    "Senegal":              "SEN",
    "Iraq":                 "IC2",       # IC Path 2 winner
    "Norway":               "NOR",
    "Argentina":            "ARG",
    "Algeria":              "ALG",
    "Austria":              "AUT",
    "Jordan":               "JOR",
    "Portugal":             "POR",
    "DR Congo":             "IC1",       # IC Path 1 winner
    "Congo DR":             "IC1",
    "Democratic Republic of Congo": "IC1",
    "Uzbekistan":           "UZB",
    "Colombia":             "COL",
    "England":              "ENG",
    "Croatia":              "CRO",
    "Ghana":                "GHA",
    "Panama":               "PAN",
    # Placeholder strings from openfootball when qualifiers not yet resolved
    "UEFA Path A winner":   "UEFA_A",
    "UEFA Path B winner":   "UEFA_B",
    "UEFA Path C winner":   "UEFA_C",
    "UEFA Path D winner":   "CZE",
    "IC Path 1 winner":     "IC1",
    "IC Path 2 winner":     "IC2",
}

def _parse_date(date_str):
    """Convert '2026-06-14' → 'Jun 14'."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("Jun %d").replace(" 0", " ")
    except Exception:
        return date_str

@st.cache_data(ttl=600, show_spinner=False)
def fetch_live_fixtures():
    """
    Download worldcup.json and return group-stage matches as a list of
    dicts in the same shape as FIXTURES in data.py, or None on failure.
    Cached for 10 minutes.
    """
    try:
        resp = requests.get(API_URL, timeout=8)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None

    live = []
    for m in data.get("matches", []):
        group_raw = m.get("group", "")
        if not group_raw or not group_raw.startswith("Group "):
            continue  # skip knockout rounds

        group_id = group_raw.replace("Group ", "").strip()
        t1_name  = m.get("team1", "")
        t2_name  = m.get("team2", "")
        h_id = TEAM_NAME_MAP.get(t1_name)
        a_id = TEAM_NAME_MAP.get(t2_name)

        if not h_id or not a_id:
            continue  # unknown team — skip

        score = m.get("score", {})
        ft    = score.get("ft") if score else None

        if ft and len(ft) == 2:
            status = "FINISHED"
            hs, as_ = int(ft[0]), int(ft[1])
        else:
            status = "SCHEDULED"
            hs, as_ = None, None

        live.append({
            "group":  group_id,
            "home":   h_id,
            "away":   a_id,
            "round":  m.get("round", ""),
            "date":   _parse_date(m.get("date", "")),
            "status": status,
            "hs":     hs,
            "as":     as_,
        })

    return live if live else None


def get_merged_fixtures():
    """
    Merge live API data into the static FIXTURES list.
    Returns (fixtures_list, source_string, status_message).
    """
    live = fetch_live_fixtures()

    if live is None:
        return list(FIXTURES), "static", None

    # Build lookup by (home_id, away_id) from live data
    live_lookup = {(f["home"], f["away"]): f for f in live}

    merged = []
    for sf in FIXTURES:
        key = (sf["h"], sf["a"])
        lf  = live_lookup.get(key)
        if lf:
            merged.append({
                "id":     sf["id"],
                "g":      sf["g"],
                "h":      sf["h"],
                "a":      sf["a"],
                "md":     sf["md"],
                "status": lf["status"],
                "hs":     lf["hs"],
                "as":     lf["as"],
                "date":   sf["date"],
            })
        else:
            merged.append(dict(sf))

    done  = sum(1 for f in merged if f["status"] == "FINISHED")
    total = len(merged)
    ts    = datetime.now(timezone.utc).strftime("%H:%M UTC")
    msg   = f"Live data via openfootball/worldcup.json · {done}/{total} group matches played · Updated {ts}"

    return merged, "live", msg
