"""
live_data.py
Fetches live FIFA World Cup 2026 match results from football-data.org
and merges them into the static FIXTURES list from data.py.

Setup:
  1. Get a free API key at https://www.football-data.org/client/register
  2. In Streamlit Community Cloud → App settings → Secrets, add:
       [api]
       football_data_key = "YOUR_KEY_HERE"
  3. For local dev, create .streamlit/secrets.toml with the same content.

If no key is configured, the app silently falls back to static data.py fixtures.
"""

import requests
import streamlit as st
from datetime import datetime, timezone
from data import FIXTURES, TEAMS

API_BASE = "https://api.football-data.org/v4"
WC_CODE  = "WC"

# Map football-data.org team names → our team IDs
TEAM_NAME_MAP = {
    "Mexico":                  "MEX",
    "South Korea":             "KOR",
    "Korea Republic":          "KOR",
    "Czech Republic":          "CZE",
    "Czechia":                 "CZE",
    "South Africa":            "ZAF",
    "Canada":                  "CAN",
    "Bosnia and Herzegovina":  "BIH",
    "Bosnia & Herzegovina":    "BIH",
    "Switzerland":             "SUI",
    "Qatar":                   "QAT",
    "Germany":                 "GER",
    "Côte d'Ivoire":           "CIV",
    "Ivory Coast":             "CIV",
    "Ecuador":                 "ECU",
    "Curaçao":                 "CUW",
    "Netherlands":             "NED",
    "Japan":                   "JPN",
    "Sweden":                  "SWE",
    "Tunisia":                 "TUN",
    "Belgium":                 "BEL",
    "Egypt":                   "EGY",
    "Iran":                    "IRN",
    "New Zealand":             "NZL",
    "Spain":                   "ESP",
    "Uruguay":                 "URU",
    "Saudi Arabia":            "KSA",
    "Cape Verde":              "CPV",
    "France":                  "FRA",
    "Senegal":                 "SEN",
    "Norway":                  "NOR",
    "Iraq":                    "IRQ",
    "Portugal":                "POR",
    "Argentina":               "ARG",
    "Croatia":                 "CRO",
    "Algeria":                 "ALG",
    "England":                 "ENG",
    "Brazil":                  "BRA",
    "Colombia":                "COL",
    "Morocco":                 "MAR",
    "United States":           "USA",
    "USA":                     "USA",
    "Turkey":                  "TUR",
    "Türkiye":                 "TUR",
    "Ghana":                   "GHA",
    "DR Congo":                "COD",
    "Congo DR":                "COD",
    "Australia":               "AUS",
    "Austria":                 "AUT",
    "Scotland":                "SCO",
    "Uzbekistan":              "UZB",
    "Paraguay":                "PAR",
    "Jordan":                  "JOR",
    "Venezuela":               "VEN",
}

def _get_api_key():
    """Read API key from Streamlit secrets, return None if not configured."""
    try:
        return st.secrets["api"]["football_data_key"]
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_live_fixtures():
    """
    Fetch all WC 2026 matches from the API.
    Returns a list of dicts in the same shape as FIXTURES in data.py,
    or None if the API call fails / no key is set.
    Cached for 10 minutes (ttl=600 seconds).
    """
    key = _get_api_key()
    if not key:
        return None

    try:
        resp = requests.get(
            f"{API_BASE}/competitions/{WC_CODE}/matches",
            headers={"X-Auth-Token": key},
            timeout=8,
        )
        if resp.status_code == 429:
            # Rate limited — return None, use static fallback
            return None
        resp.raise_for_status()
        raw = resp.json().get("matches", [])
    except Exception:
        return None

    live_fixtures = []
    for m in raw:
        # Only group stage matches
        stage = m.get("stage", "")
        if "GROUP" not in stage.upper():
            continue

        home_name = m.get("homeTeam", {}).get("name", "")
        away_name = m.get("awayTeam", {}).get("name", "")
        home_id = TEAM_NAME_MAP.get(home_name)
        away_id = TEAM_NAME_MAP.get(away_name)

        if not home_id or not away_id:
            continue

        status_raw = m.get("status", "SCHEDULED")
        if status_raw in ("FINISHED", "AWARDED"):
            status = "FINISHED"
            score = m.get("score", {}).get("fullTime", {})
            hs = score.get("home") or 0
            as_ = score.get("away") or 0
        elif status_raw in ("IN_PLAY", "PAUSED", "HALFTIME"):
            status = "LIVE"
            score = m.get("score", {}).get("fullTime", {})
            hs = score.get("home") or 0
            as_ = score.get("away") or 0
        else:
            status = "SCHEDULED"
            hs = None
            as_ = None

        # Parse matchday and date
        matchday = m.get("matchday", 1)
        utc_date = m.get("utcDate", "")
        try:
            dt = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
            date_str = dt.strftime("Jun %d").replace(" 0", " ")
        except Exception:
            date_str = ""

        # Derive group from groupName e.g. "GROUP_A" → "A"
        group_raw = m.get("group", "") or ""
        group_id = group_raw.replace("GROUP_", "").strip()
        if not group_id and home_id in TEAMS:
            group_id = TEAMS[home_id]["group"]

        # Build unique ID matching our static fixture IDs format
        fixture_id = f"{group_id}{matchday}_{home_id}_{away_id}"

        live_fixtures.append({
            "id":     fixture_id,
            "g":      group_id,
            "h":      home_id,
            "a":      away_id,
            "md":     matchday,
            "status": status,
            "hs":     hs,
            "as":     as_,
            "date":   date_str,
        })

    return live_fixtures if live_fixtures else None


def get_merged_fixtures():
    """
    Return the best available fixture list:
    - If API succeeds: use live data merged with static fixture IDs
    - If API fails/no key: use static FIXTURES from data.py

    Also returns a status string for display.
    """
    live = fetch_live_fixtures()

    if live is None:
        return list(FIXTURES), "static", None

    # Build lookup by (home_id, away_id) from live data
    live_lookup = {(f["h"], f["a"]): f for f in live}

    merged = []
    for static_f in FIXTURES:
        key = (static_f["h"], static_f["a"])
        if key in live_lookup:
            lf = live_lookup[key]
            merged.append({
                "id":     static_f["id"],   # keep original ID for stability
                "g":      static_f["g"],
                "h":      static_f["h"],
                "a":      static_f["a"],
                "md":     static_f["md"],
                "status": lf["status"],
                "hs":     lf["hs"],
                "as":     lf["as"],
                "date":   static_f["date"],
            })
        else:
            merged.append(dict(static_f))

    # Count live matches for status message
    live_count  = sum(1 for f in merged if f["status"] == "LIVE")
    done_count  = sum(1 for f in merged if f["status"] == "FINISHED")
    last_update = datetime.now(timezone.utc).strftime("%H:%M UTC")

    status_msg = f"Live data · {done_count} matches played"
    if live_count:
        status_msg += f" · {live_count} in progress"
    status_msg += f" · Updated {last_update}"

    return merged, "live", status_msg
