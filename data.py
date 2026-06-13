# data.py — ground truth team/group data + static fallback fixtures
# Groups sourced from openfootball/worldcup.json (github.com/openfootball/worldcup.json)
# Real draw: Dec 5 2025, Kennedy Center, Washington DC

GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

# UEFA playoff winners are TBD — we label them with placeholders and use
# average Poisson params until the real team is known.
TEAMS = {
    # Group A
    "MEX": {"name": "Mexico",           "group": "A", "conf": "CONCACAF", "atk": 1.25, "def": 0.88},
    "ZAF": {"name": "South Africa",     "group": "A", "conf": "CAF",      "atk": 0.82, "def": 1.18},
    "KOR": {"name": "South Korea",      "group": "A", "conf": "AFC",      "atk": 1.10, "def": 0.95},
    "CZE": {"name": "Czech Republic",   "group": "A", "conf": "UEFA",     "atk": 1.05, "def": 1.02},
    # Group B
    "CAN": {"name": "Canada",           "group": "B", "conf": "CONCACAF", "atk": 0.98, "def": 1.05},
    "UEFA_A": {"name": "UEFA Path A",   "group": "B", "conf": "UEFA",     "atk": 0.95, "def": 1.05},
    "QAT": {"name": "Qatar",            "group": "B", "conf": "AFC",      "atk": 0.88, "def": 1.15},
    "SUI": {"name": "Switzerland",      "group": "B", "conf": "UEFA",     "atk": 1.08, "def": 0.92},
    # Group C
    "BRA": {"name": "Brazil",           "group": "C", "conf": "CONMEBOL", "atk": 1.42, "def": 0.80},
    "MAR": {"name": "Morocco",          "group": "C", "conf": "CAF",      "atk": 1.05, "def": 0.95},
    "HTI": {"name": "Haiti",            "group": "C", "conf": "CONCACAF", "atk": 0.72, "def": 1.30},
    "SCO": {"name": "Scotland",         "group": "C", "conf": "UEFA",     "atk": 0.92, "def": 1.08},
    # Group D
    "USA": {"name": "USA",              "group": "D", "conf": "CONCACAF", "atk": 1.12, "def": 0.95},
    "PAR": {"name": "Paraguay",         "group": "D", "conf": "CONMEBOL", "atk": 0.95, "def": 1.05},
    "AUS": {"name": "Australia",        "group": "D", "conf": "AFC",      "atk": 0.98, "def": 1.05},
    "UEFA_C": {"name": "UEFA Path C",   "group": "D", "conf": "UEFA",     "atk": 0.95, "def": 1.05},
    # Group E
    "GER": {"name": "Germany",          "group": "E", "conf": "UEFA",     "atk": 1.38, "def": 0.82},
    "CUW": {"name": "Curacao",          "group": "E", "conf": "CONCACAF", "atk": 0.72, "def": 1.35},
    "CIV": {"name": "Ivory Coast",      "group": "E", "conf": "CAF",      "atk": 1.05, "def": 1.05},
    "ECU": {"name": "Ecuador",          "group": "E", "conf": "CONMEBOL", "atk": 0.95, "def": 1.02},
    # Group F
    "NED": {"name": "Netherlands",      "group": "F", "conf": "UEFA",     "atk": 1.30, "def": 0.85},
    "JPN": {"name": "Japan",            "group": "F", "conf": "AFC",      "atk": 1.08, "def": 0.95},
    "UEFA_B": {"name": "UEFA Path B",   "group": "F", "conf": "UEFA",     "atk": 0.95, "def": 1.05},
    "TUN": {"name": "Tunisia",          "group": "F", "conf": "CAF",      "atk": 0.85, "def": 1.12},
    # Group G
    "BEL": {"name": "Belgium",          "group": "G", "conf": "UEFA",     "atk": 1.22, "def": 0.88},
    "EGY": {"name": "Egypt",            "group": "G", "conf": "CAF",      "atk": 0.92, "def": 1.05},
    "IRN": {"name": "Iran",             "group": "G", "conf": "AFC",      "atk": 0.88, "def": 1.08},
    "NZL": {"name": "New Zealand",      "group": "G", "conf": "OFC",      "atk": 0.72, "def": 1.30},
    # Group H
    "ESP": {"name": "Spain",            "group": "H", "conf": "UEFA",     "atk": 1.42, "def": 0.78},
    "CPV": {"name": "Cape Verde",       "group": "H", "conf": "CAF",      "atk": 0.78, "def": 1.25},
    "KSA": {"name": "Saudi Arabia",     "group": "H", "conf": "AFC",      "atk": 0.92, "def": 1.10},
    "URU": {"name": "Uruguay",          "group": "H", "conf": "CONMEBOL", "atk": 1.18, "def": 0.90},
    # Group I
    "FRA": {"name": "France",           "group": "I", "conf": "UEFA",     "atk": 1.45, "def": 0.78},
    "SEN": {"name": "Senegal",          "group": "I", "conf": "CAF",      "atk": 1.05, "def": 1.00},
    "IC2": {"name": "IC Path 2",        "group": "I", "conf": "OTHER",    "atk": 0.85, "def": 1.15},
    "NOR": {"name": "Norway",           "group": "I", "conf": "UEFA",     "atk": 1.15, "def": 0.95},
    # Group J
    "ARG": {"name": "Argentina",        "group": "J", "conf": "CONMEBOL", "atk": 1.45, "def": 0.80},
    "ALG": {"name": "Algeria",          "group": "J", "conf": "CAF",      "atk": 0.95, "def": 1.10},
    "AUT": {"name": "Austria",          "group": "J", "conf": "UEFA",     "atk": 1.12, "def": 0.95},
    "JOR": {"name": "Jordan",           "group": "J", "conf": "AFC",      "atk": 0.85, "def": 1.15},
    # Group K
    "POR": {"name": "Portugal",         "group": "K", "conf": "UEFA",     "atk": 1.38, "def": 0.82},
    "IC1": {"name": "IC Path 1",        "group": "K", "conf": "OTHER",    "atk": 0.85, "def": 1.15},
    "UZB": {"name": "Uzbekistan",       "group": "K", "conf": "AFC",      "atk": 0.82, "def": 1.20},
    "COL": {"name": "Colombia",         "group": "K", "conf": "CONMEBOL", "atk": 1.18, "def": 0.92},
    # Group L
    "ENG": {"name": "England",          "group": "L", "conf": "UEFA",     "atk": 1.30, "def": 0.85},
    "CRO": {"name": "Croatia",          "group": "L", "conf": "UEFA",     "atk": 1.15, "def": 0.92},
    "GHA": {"name": "Ghana",            "group": "L", "conf": "CAF",      "atk": 0.95, "def": 1.08},
    "PAN": {"name": "Panama",           "group": "L", "conf": "CONCACAF", "atk": 0.80, "def": 1.20},
}

# Static fixtures — used as fallback when live API is unavailable.
# Source: openfootball/worldcup.json master (fetched Jun 13 2026)
# Scores filled in for completed matches; rest are SCHEDULED.
FIXTURES = [
    # ── Group A ──────────────────────────────────────────────────
    {"id":"A1", "g":"A","h":"MEX","a":"ZAF","md":1,"status":"FINISHED","hs":2,"as":0,"date":"Jun 11"},
    {"id":"A2", "g":"A","h":"KOR","a":"CZE","md":1,"status":"FINISHED","hs":2,"as":1,"date":"Jun 11"},
    {"id":"A3", "g":"A","h":"CZE","a":"ZAF","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 18"},
    {"id":"A4", "g":"A","h":"MEX","a":"KOR","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 18"},
    {"id":"A5", "g":"A","h":"CZE","a":"MEX","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 24"},
    {"id":"A6", "g":"A","h":"ZAF","a":"KOR","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 24"},
    # ── Group B ──────────────────────────────────────────────────
    {"id":"B1", "g":"B","h":"CAN","a":"UEFA_A","md":1,"status":"FINISHED","hs":1,"as":1,"date":"Jun 12"},
    {"id":"B2", "g":"B","h":"QAT","a":"SUI",   "md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 13"},
    {"id":"B3", "g":"B","h":"SUI","a":"UEFA_A","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 18"},
    {"id":"B4", "g":"B","h":"CAN","a":"QAT",   "md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 18"},
    {"id":"B5", "g":"B","h":"SUI","a":"CAN",   "md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 24"},
    {"id":"B6", "g":"B","h":"UEFA_A","a":"QAT","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 24"},
    # ── Group C ──────────────────────────────────────────────────
    {"id":"C1", "g":"C","h":"BRA","a":"MAR","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 13"},
    {"id":"C2", "g":"C","h":"HTI","a":"SCO","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 13"},
    {"id":"C3", "g":"C","h":"SCO","a":"MAR","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 19"},
    {"id":"C4", "g":"C","h":"BRA","a":"HTI","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 19"},
    {"id":"C5", "g":"C","h":"SCO","a":"BRA","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 24"},
    {"id":"C6", "g":"C","h":"MAR","a":"HTI","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 24"},
    # ── Group D ──────────────────────────────────────────────────
    {"id":"D1", "g":"D","h":"USA","a":"PAR",   "md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 12"},
    {"id":"D2", "g":"D","h":"AUS","a":"UEFA_C","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 13"},
    {"id":"D3", "g":"D","h":"USA","a":"AUS",   "md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 19"},
    {"id":"D4", "g":"D","h":"UEFA_C","a":"PAR","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 19"},
    {"id":"D5", "g":"D","h":"UEFA_C","a":"USA","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 25"},
    {"id":"D6", "g":"D","h":"PAR","a":"AUS",   "md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 25"},
    # ── Group E ──────────────────────────────────────────────────
    {"id":"E1", "g":"E","h":"GER","a":"CUW","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 14"},
    {"id":"E2", "g":"E","h":"CIV","a":"ECU","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 14"},
    {"id":"E3", "g":"E","h":"GER","a":"CIV","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 20"},
    {"id":"E4", "g":"E","h":"ECU","a":"CUW","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 20"},
    {"id":"E5", "g":"E","h":"CUW","a":"CIV","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 25"},
    {"id":"E6", "g":"E","h":"ECU","a":"GER","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 25"},
    # ── Group F ──────────────────────────────────────────────────
    {"id":"F1", "g":"F","h":"NED","a":"JPN",   "md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 14"},
    {"id":"F2", "g":"F","h":"UEFA_B","a":"TUN","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 14"},
    {"id":"F3", "g":"F","h":"NED","a":"UEFA_B","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 20"},
    {"id":"F4", "g":"F","h":"TUN","a":"JPN",   "md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 20"},
    {"id":"F5", "g":"F","h":"JPN","a":"UEFA_B","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 25"},
    {"id":"F6", "g":"F","h":"TUN","a":"NED",   "md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 25"},
    # ── Group G ──────────────────────────────────────────────────
    {"id":"G1", "g":"G","h":"BEL","a":"EGY","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 15"},
    {"id":"G2", "g":"G","h":"IRN","a":"NZL","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 15"},
    {"id":"G3", "g":"G","h":"BEL","a":"IRN","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 21"},
    {"id":"G4", "g":"G","h":"NZL","a":"EGY","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 21"},
    {"id":"G5", "g":"G","h":"EGY","a":"IRN","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 26"},
    {"id":"G6", "g":"G","h":"NZL","a":"BEL","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 26"},
    # ── Group H ──────────────────────────────────────────────────
    {"id":"H1", "g":"H","h":"ESP","a":"CPV","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 15"},
    {"id":"H2", "g":"H","h":"KSA","a":"URU","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 15"},
    {"id":"H3", "g":"H","h":"ESP","a":"KSA","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 21"},
    {"id":"H4", "g":"H","h":"URU","a":"CPV","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 21"},
    {"id":"H5", "g":"H","h":"CPV","a":"KSA","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 26"},
    {"id":"H6", "g":"H","h":"URU","a":"ESP","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 26"},
    # ── Group I ──────────────────────────────────────────────────
    {"id":"I1", "g":"I","h":"FRA","a":"SEN","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 16"},
    {"id":"I2", "g":"I","h":"IC2","a":"NOR","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 16"},
    {"id":"I3", "g":"I","h":"FRA","a":"IC2","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 22"},
    {"id":"I4", "g":"I","h":"NOR","a":"SEN","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 22"},
    {"id":"I5", "g":"I","h":"NOR","a":"FRA","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 26"},
    {"id":"I6", "g":"I","h":"SEN","a":"IC2","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 26"},
    # ── Group J ──────────────────────────────────────────────────
    {"id":"J1", "g":"J","h":"ARG","a":"ALG","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 16"},
    {"id":"J2", "g":"J","h":"AUT","a":"JOR","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 16"},
    {"id":"J3", "g":"J","h":"ARG","a":"AUT","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 22"},
    {"id":"J4", "g":"J","h":"JOR","a":"ALG","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 22"},
    {"id":"J5", "g":"J","h":"ALG","a":"AUT","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 27"},
    {"id":"J6", "g":"J","h":"JOR","a":"ARG","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 27"},
    # ── Group K ──────────────────────────────────────────────────
    {"id":"K1", "g":"K","h":"POR","a":"IC1","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 17"},
    {"id":"K2", "g":"K","h":"UZB","a":"COL","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 17"},
    {"id":"K3", "g":"K","h":"POR","a":"UZB","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 23"},
    {"id":"K4", "g":"K","h":"COL","a":"IC1","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 23"},
    {"id":"K5", "g":"K","h":"COL","a":"POR","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 27"},
    {"id":"K6", "g":"K","h":"IC1","a":"UZB","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 27"},
    # ── Group L ──────────────────────────────────────────────────
    {"id":"L1", "g":"L","h":"ENG","a":"CRO","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 17"},
    {"id":"L2", "g":"L","h":"GHA","a":"PAN","md":1,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 17"},
    {"id":"L3", "g":"L","h":"ENG","a":"GHA","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 23"},
    {"id":"L4", "g":"L","h":"PAN","a":"CRO","md":2,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 23"},
    {"id":"L5", "g":"L","h":"PAN","a":"ENG","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 27"},
    {"id":"L6", "g":"L","h":"CRO","a":"GHA","md":3,"status":"SCHEDULED","hs":None,"as":None,"date":"Jun 27"},
]
