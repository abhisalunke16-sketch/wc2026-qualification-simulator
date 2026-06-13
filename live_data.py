"""
live_data.py
Single source of truth for all match and team data.

Fetches from openfootball/worldcup.json — free, no API key.
URL: https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json

On success:  builds TEAMS (with live names/groups) + FIXTURES from the feed.
On failure:  falls back to static data.py.

Team display names and group assignments come entirely from the live feed.
Only Poisson attack/defense ratings (not in the feed) are kept in data.py.
"""

import requests
import streamlit as st
from datetime import datetime, timezone
from data import RATINGS, FALLBACK_FIXTURES, FALLBACK_TEAMS

API_URL = (
    "https://raw.githubusercontent.com/openfootball/"
    "worldcup.json/master/2026/worldcup.json"
)

# ---------------------------------------------------------------------------
# Name → internal ID mapping (openfootball name strings → our ID keys)
# IDs are stable even if the display name changes in the feed.
# ---------------------------------------------------------------------------
NAME_TO_ID = {
    "Mexico":                           "MEX",
    "South Africa":                     "ZAF",
    "South Korea":                      "KOR",
    "Czech Republic":                   "CZE",
    "Canada":                           "CAN",
    "Bosnia and Herzegovina":           "UEFA_A",
    "Bosnia & Herzegovina":             "UEFA_A",
    "Qatar":                            "QAT",
    "Switzerland":                      "SUI",
    "Brazil":                           "BRA",
    "Morocco":                          "MAR",
    "Haiti":                            "HTI",
    "Scotland":                         "SCO",
    "USA":                              "USA",
    "United States":                    "USA",
    "Paraguay":                         "PAR",
    "Australia":                        "AUS",
    "Türkiye":                          "UEFA_C",
    "Turkey":                           "UEFA_C",
    "Germany":                          "GER",
    "Curaçao":                          "CUW",
    "Curacao":                          "CUW",
    "Ivory Coast":                      "CIV",
    "Côte d'Ivoire":                    "CIV",
    "Ecuador":                          "ECU",
    "Netherlands":                      "NED",
    "Japan":                            "JPN",
    "Sweden":                           "UEFA_B",
    "Tunisia":                          "TUN",
    "Belgium":                          "BEL",
    "Egypt":                            "EGY",
    "Iran":                             "IRN",
    "New Zealand":                      "NZL",
    "Spain":                            "ESP",
    "Cape Verde":                       "CPV",
    "Saudi Arabia":                     "KSA",
    "Uruguay":                          "URU",
    "France":                           "FRA",
    "Senegal":                          "SEN",
    "Iraq":                             "IC2",
    "Norway":                           "NOR",
    "Argentina":                        "ARG",
    "Algeria":                          "ALG",
    "Austria":                          "AUT",
    "Jordan":                           "JOR",
    "Portugal":                         "POR",
    "DR Congo":                         "IC1",
    "Congo DR":                         "IC1",
    "Democratic Republic of Congo":     "IC1",
    "Uzbekistan":                       "UZB",
    "Colombia":                         "COL",
    "England":                          "ENG",
    "Croatia":                          "CRO",
    "Ghana":                            "GHA",
    "Panama":                           "PAN",
    # Unresolved placeholder strings the feed may still use
    "UEFA Path A winner":               "UEFA_A",
    "UEFA Path B winner":               "UEFA_B",
    "UEFA Path C winner":               "UEFA_C",
    "UEFA Path D winner":               "CZE",
    "IC Path 1 winner":                 "IC1",
    "IC Path 2 winner":                 "IC2",
}

# Confederation lookup by ID (not in live feed)
CONF = {
    "MEX":"CONCACAF","ZAF":"CAF","KOR":"AFC","CZE":"UEFA",
    "CAN":"CONCACAF","UEFA_A":"UEFA","QAT":"AFC","SUI":"UEFA",
    "BRA":"CONMEBOL","MAR":"CAF","HTI":"CONCACAF","SCO":"UEFA",
    "USA":"CONCACAF","PAR":"CONMEBOL","AUS":"AFC","UEFA_C":"UEFA",
    "GER":"UEFA","CUW":"CONCACAF","CIV":"CAF","ECU":"CONMEBOL",
    "NED":"UEFA","JPN":"AFC","UEFA_B":"UEFA","TUN":"CAF",
    "BEL":"UEFA","EGY":"CAF","IRN":"AFC","NZL":"OFC",
    "ESP":"UEFA","CPV":"CAF","KSA":"AFC","URU":"CONMEBOL",
    "FRA":"UEFA","SEN":"CAF","IC2":"OTHER","NOR":"UEFA",
    "ARG":"CONMEBOL","ALG":"CAF","AUT":"UEFA","JOR":"AFC",
    "POR":"UEFA","IC1":"OTHER","UZB":"AFC","COL":"CONMEBOL",
    "ENG":"UEFA","CRO":"UEFA","GHA":"CAF","PAN":"CONCACAF",
}


def _parse_date(date_str):
    """Convert '2026-06-14' → 'Jun 14'."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("Jun %d").replace(" 0", " ")
    except Exception:
        return date_str


@st.cache_data(ttl=600, show_spinner=False)
def _fetch_raw():
    """Download and return raw JSON, or None on failure. Cached 10 min."""
    try:
        resp = requests.get(API_URL, timeout=8)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def _build_from_live(data):
    """
    Parse openfootball JSON into:
      - teams dict  {id: {name, group, conf, atk, def}}
      - fixtures list  [{id, g, h, a, md, status, hs, as, date}]

    Team names and group assignments come entirely from the feed.
    Ratings come from RATINGS in data.py (keyed by our internal ID).
    """
    teams   = {}   # id -> {name, group, conf, atk, def}
    fixtures = []
    match_counters = {}  # group -> match index within group (for id generation)

    for m in data.get("matches", []):
        group_raw = m.get("group", "")
        if not group_raw or not group_raw.startswith("Group "):
            continue  # skip knockout rounds

        group_id = group_raw.replace("Group ", "").strip()
        t1_name  = m.get("team1", "")
        t2_name  = m.get("team2", "")
        h_id = NAME_TO_ID.get(t1_name)
        a_id = NAME_TO_ID.get(t2_name)

        if not h_id or not a_id:
            continue  # unknown team, skip

        # Register teams with their live name and group
        for tid, tname in [(h_id, t1_name), (a_id, t2_name)]:
            if tid not in teams:
                ratings = RATINGS.get(tid, {"atk": 0.90, "def": 1.10})
                teams[tid] = {
                    "name":  tname,
                    "group": group_id,
                    "conf":  CONF.get(tid, "OTHER"),
                    "atk":   ratings["atk"],
                    "def":   ratings["def"],
                }

        # Build fixture
        match_counters[group_id] = match_counters.get(group_id, 0) + 1
        fix_id = f"{group_id}{match_counters[group_id]}"
        round_num = m.get("round", match_counters[group_id])

        score = m.get("score", {})
        ft    = score.get("ft") if score else None
        if ft and len(ft) == 2:
            status, hs, as_ = "FINISHED", int(ft[0]), int(ft[1])
        else:
            status, hs, as_ = "SCHEDULED", None, None

        fixtures.append({
            "id":     fix_id,
            "g":      group_id,
            "h":      h_id,
            "a":      a_id,
            "md":     round_num,
            "status": status,
            "hs":     hs,
            "as":     as_,
            "date":   _parse_date(m.get("date", "")),
        })

    return teams, fixtures


def get_all_data():
    """
    Main entry point called by app.py.
    Returns (teams, fixtures, source, status_msg).

    source is "live" or "static".
    teams and fixtures have the same shape regardless of source.
    """
    raw = _fetch_raw()

    if raw:
        teams, fixtures = _build_from_live(raw)
        if teams and fixtures:
            done  = sum(1 for f in fixtures if f["status"] == "FINISHED")
            total = len(fixtures)
            ts    = datetime.now(timezone.utc).strftime("%H:%M UTC")
            msg   = (
                f"Live data via openfootball/worldcup.json "
                f"· {done}/{total} group matches played · Updated {ts}"
            )
            return teams, fixtures, "live", msg

    # Fallback
    return FALLBACK_TEAMS, list(FALLBACK_FIXTURES), "static", None
