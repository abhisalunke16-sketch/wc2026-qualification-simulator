# FIFA World Cup 2026 Group Qualification Simulator 🏆⚽

A Python-based simulator that models FIFA World Cup 2026
group stage qualification scenarios.

Run thousands of simulations to predict which teams advance
based on real group fixtures, current standings, and
probabilistic match outcomes.

🌐 **Live Demo:** https://paultheoctopus-fifa2026.streamlit.app/

---

## What It Does

- Simulates all 48 group stage matches across 12 groups
- Models match outcomes using probability distributions
- Runs Monte Carlo simulations to predict qualification likelihood
- Outputs qualification probability for every team in the tournament
- Identifies which teams are mathematically eliminated or qualified

---

## How It Works

Each match result is simulated based on:
- Current FIFA world rankings
- Historical head-to-head performance
- Home/away advantage factors
- Group stage point standings

Thousands of simulations are run to produce statistically
robust qualification probabilities for every team.

---

## Run Locally

```bash
git clone https://github.com/abhisalunke16-sketch/wc2026-qualification-simulator.git
cd wc2026-qualification-simulator
pip install -r requirements.txt
streamlit run app.py
```

---

## Tech Stack

- Python 3.11
- Streamlit (live interactive demo)
- NumPy (probability distributions)
- Pandas (standings and fixtures management)
- Matplotlib (results visualization)

---

## The Data Engineering Angle

This project applies core data engineering principles to
sports analytics: structured data ingestion, transformation
pipelines, simulation at scale, and output visualization.

The same Monte Carlo simulation logic used here applies
directly to satellite anomaly prediction and space mission
risk modeling, which is what I'm building next.

→ Satellite Telemetry Pipeline coming July 2026.

---

## About the Author

Senior Data Engineer specializing in data infrastructure.
Based in Ottawa, Canada.

🔗 [LinkedIn](https://linkedin.com/in/abhisheksalunke12) ·
✍️ [Medium](https://medium.com/@abhisheksalunke) ·
🛰️ [Known Space Explorer](https://abhisalunke16-sketch.github.io/space_simulator/)

---

## License

© 2026 Abhishek Salunke. Licensed under CC BY-NC 4.0.
Non-commercial use only. See LICENSE for details.
