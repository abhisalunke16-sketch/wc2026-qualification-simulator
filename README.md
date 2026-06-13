# ⚽ FIFA World Cup 2026 — Group Qualification Simulator

> **Live app:** [fifa2026qualificationsimulator](https://fifa2026qualificationsimulator.streamlit.app) 

A data engineering + analytics portfolio project built during the **FIFA World Cup 2026 group stage (Jun 11 – Jun 26)**. Calculates real-time qualification probabilities for all 48 teams using Monte Carlo simulation and a Poisson scoring model.

---

## What it does

| Feature | Description |
|---|---|
| **Group standings** | Live W/D/L/GF/GA/GD/Pts for all 12 groups |
| **Qualification probability** | % chance each team advances, from 8,000 Monte Carlo simulations |
| **What-if simulator** | Fix any remaining match result and instantly see how probabilities shift |
| **Team stories** | Auto-generated plain-English narratives for each team's situation |
| **All 48 teams ranked** | Full probability leaderboard filterable by confederation |

---

## Tech stack

| Layer | Tool |
|---|---|
| Data model | Python dataclasses (Bronze/Silver/Gold Medallion pattern) |
| Simulation engine | NumPy Poisson + Monte Carlo (8,000 runs) |
| Frontend | Streamlit |
| Deployment | Streamlit Community Cloud |
| Full pipeline version | Databricks + PySpark + Delta Lake + ADF (see blueprint doc) |

---

## How the model works

**Poisson model:** Each team has an `attack_strength` and `defense_strength` derived from historical World Cup results (2010–2022). For each match:

```
home_lambda = home_atk × away_def × avg_goals_per_match (2.65)
away_lambda = away_atk × home_def × avg_goals_per_match
```

**Monte Carlo:** For each of 8,000 simulation runs, every unplayed match gets a random score drawn from `Poisson(lambda)`. The final group standings are calculated using FIFA tiebreaker rules (points → GD → GF). The proportion of runs in which a team finishes top 2 = their qualification probability.

**What-if override:** User-fixed scores replace the simulated scores for those fixtures in every run. All other matches remain randomized.

---

## Run locally

```bash
git clone https://github.com/yourusername/wc2026-qualification-simulator
cd wc2026-qualification-simulator
pip install -r requirements.txt
streamlit run app.py
```

---

## Deploy to Streamlit Community Cloud (free, public URL)

1. Push this repo to GitHub (public)
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select your repo, branch `main`, file `app.py`
4. Click Deploy — your public URL is ready in ~2 minutes

---

## Update scores as the tournament progresses

Open `data.py` and update the relevant fixture:

```python
{"id":"C1","g":"C","h":"GER","a":"CUW","md":1,"status":"FINISHED","hs":4,"as":0,"date":"Jun 14"},
```

Change `status` from `"SCHEDULED"` to `"FINISHED"` and set `hs` (home score) and `as` (away score). Redeploy or Streamlit Community Cloud will auto-redeploy on push.

---

## Project structure

```
wc2026-qualification-simulator/
├── app.py              # Main Streamlit app (4 tabs)
├── data.py             # All 48 teams, 72 fixtures, group assignments
├── requirements.txt    # streamlit, numpy, pandas
└── README.md
```

---

## Full data engineering blueprint

A complete Databricks + PySpark + Delta Lake + ADF pipeline design for this project (Bronze/Silver/Gold tables, Monte Carlo on Spark, ADF orchestration, Power BI dashboard) is available as a Word document. DM on LinkedIn.

---

## Author

**Abhishek Salunke** — Senior Data Engineer  
[LinkedIn](https://linkedin.com/in/abhisheksalunke12) · [Medium](https://medium.com/@abhisheksalunke)

Built during the FIFA World Cup 2026 group stage as a live portfolio project.
