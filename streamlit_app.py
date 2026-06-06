import streamlit as st
import numpy as np
from scipy.stats import poisson
import random
from streamlit_autorefresh import st_autorefresh

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title="AI SCORECAST VALUE BETS", layout="wide")
st_autorefresh(interval=120000, key="refresh")

# ─────────────────────────────
# STYLE
# ─────────────────────────────
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:34px;
    font-weight:900;
    color:#1DB954;
    margin-bottom:20px;
}

.card {
    background:white;
    padding:14px;
    margin:10px 0;
    border-radius:12px;
    box-shadow:0 2px 10px rgba(0,0,0,0.1);
    border-left:6px solid #1DB954;
}

.match {
    font-weight:800;
    font-size:18px;
}

.score {
    font-size:22px;
    font-weight:900;
    margin-top:5px;
}

.trend {
    font-size:13px;
    color:#444;
    font-style:italic;
    margin-top:5px;
}

.badge {
    padding:5px 8px;
    border-radius:6px;
    font-size:12px;
    font-weight:700;
    margin-right:4px;
}

.green { background:#d4edda; color:#155724; }
.orange { background:#fff3cd; color:#856404; }
.red { background:#f8d7da; color:#721c24; }
.blue { background:#d9ecff; color:#0b4f8a; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>⚽ AI SCORECAST PRO • VALUE BET ENGINE 💰</div>", unsafe_allow_html=True)

# ─────────────────────────────
# FIXTURES
# ─────────────────────────────
def get_fixtures():
    return [
        {"home":"FC Alpha","away":"FC Beta"},
        {"home":"Real Test","away":"AI United"},
        {"home":"Green FC","away":"Future Stars"},
        {"home":"Burundi Stars","away":"City FC"},
    ]

# ─────────────────────────────
# TEAM STRENGTH (REALISTIC + NOISE CONTROLLED)
# ─────────────────────────────
def team_stats(team):
    seed = abs(hash(team)) % 1000
    random.seed(seed)

    attack = random.uniform(1.0, 2.2)
    defense = random.uniform(0.8, 2.0)
    form = random.uniform(0.85, 1.15)

    return attack * form, defense

# ─────────────────────────────
# PROBABILITY CALIBRATION (IMPORTANT)
# ─────────────────────────────
def calibrate(prob):
    # ajuste type real betting market
    return max(5, min(95, prob * random.uniform(0.92, 1.08)))

# ─────────────────────────────
# MODEL CORE
# ─────────────────────────────
def predict(home, away):

    h_attack, h_def = team_stats(home)
    a_attack, a_def = team_stats(away)

    home_lambda = (h_attack * 1.2 + a_def * 0.3)
    away_lambda = (a_attack * 1.0 + h_def * 0.35)

    max_g = 6

    h = poisson.pmf(np.arange(max_g), home_lambda)
    a = poisson.pmf(np.arange(max_g), away_lambda)

    matrix = np.outer(h, a)

    p1 = calibrate(np.sum(np.tril(matrix, -1)) * 100)
    px = calibrate(np.sum(np.diag(matrix)) * 100)
    p2 = calibrate(np.sum(np.triu(matrix, 1)) * 100)
    over25 = calibrate((1 - np.sum(matrix[:3, :3])) * 100)

    score_h = np.argmax(h)
    score_a = np.argmax(a)

    # confidence score
    confidence = (max(p1, p2) - px) + random.uniform(0, 5)

    if confidence > 40:
        conf_label = "HIGH"
    elif confidence > 25:
        conf_label = "MEDIUM"
    else:
        conf_label = "LOW"

    # trend engine
    if p1 > 50:
        trend = "Home dominance"
    elif p2 > 50:
        trend = "Away dominance"
    elif over25 > 60:
        trend = "High scoring match"
    else:
        trend = "Balanced match"

    # VALUE BET LOGIC 💰
    value_bet = None

    # simple betting market simulation
    market_odds = {
        "1": 2.10,
        "X": 3.20,
        "2": 3.80,
        "O2.5": 1.95
    }

    # detect value bets
    if p1/100 * market_odds["1"] > 1.05:
        value_bet = "VALUE BET: HOME WIN 💰"
    elif p2/100 * market_odds["2"] > 1.05:
        value_bet = "VALUE BET: AWAY WIN 💰"
    elif over25/100 * market_odds["O2.5"] > 1.05:
        value_bet = "VALUE BET: OVER 2.5 💰"

    return {
        "1": round(p1,1),
        "X": round(px,1),
        "2": round(p2,1),
        "O2.5": round(over25,1),
        "score": f"{score_h}-{score_a}",
        "trend": trend,
        "confidence": conf_label,
        "value": value_bet
    }

# ─────────────────────────────
# DISPLAY
# ─────────────────────────────
for m in get_fixtures():

    p = predict(m["home"], m["away"])

    st.markdown(f"""
    <div class="card">

        <div class="match">{m['home']} vs {m['away']}</div>

        <div class="score">Predicted Score: {p['score']}</div>

        <div class="trend">{p['trend']} • Confidence: {p['confidence']}</div>

        <div style="margin-top:8px;">
            <span class="badge green">1: {p['1']}%</span>
            <span class="badge orange">X: {p['X']}%</span>
            <span class="badge red">2: {p['2']}%</span>
            <span class="badge blue">O2.5: {p['O2.5']}%</span>
        </div>

        <div style="margin-top:8px; font-weight:900; color:#1DB954;">
            {p['value'] if p['value'] else ""}
        </div>

    </div>
    """, unsafe_allow_html=True)
