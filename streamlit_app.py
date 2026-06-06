import streamlit as st
from datetime import datetime
import pytz
import numpy as np
from scipy.stats import poisson
from streamlit_autorefresh import st_autorefresh
import random

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title="AI SCORECAST FOREBET", layout="wide")
tz = pytz.timezone("Africa/Bujumbura")

st_autorefresh(interval=120 * 1000, key="refresh")

# ─────────────────────────────
# STYLE (VERT PRO)
# ─────────────────────────────
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:32px;
    font-weight:900;
    color:#1DB954;
    margin-bottom:25px;
}

.card {
    background:white;
    padding:14px;
    margin:12px 0;
    border-radius:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
    border-left:6px solid #1DB954;
}

.team { font-weight:800; font-size:18px; }
.score { font-weight:900; font-size:22px; margin-top:5px; }

.box {
    display:inline-block;
    padding:6px 10px;
    margin:4px 3px;
    background:#e9fff0;
    border-radius:8px;
    font-weight:bold;
    font-size:12px;
    color:#0b6b2f;
}

.trend {
    margin-top:6px;
    font-size:13px;
    color:#444;
    font-style:italic;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# TITLE
# ─────────────────────────────
st.markdown("<div class='title'>⚽ AI SCORECAST PRO • FOREBET ENGINE</div>", unsafe_allow_html=True)

# ─────────────────────────────
# FIXTURES (SANS API = STABLE)
# ─────────────────────────────
def get_fixtures(date_str):
    return [
        {"id":"1","home":"FC Alpha","away":"FC Beta"},
        {"id":"2","home":"Real Test","away":"AI United"},
        {"id":"3","home":"Green FC","away":"Future Stars"},
        {"id":"4","home":"Burundi Stars","away":"City FC"},
        {"id":"5","home":"River FC","away":"Mountain FC"}
    ]

# ─────────────────────────────
# TEAM STRENGTH (SIMULATION FOREBET STYLE)
# ─────────────────────────────
def team_strength(team):
    seed = abs(hash(team)) % 1000
    random.seed(seed)

    attack = random.uniform(1.0, 2.2)
    defense = random.uniform(0.8, 2.0)

    form = random.uniform(0.8, 1.2)  # forme récente simulée

    return attack * form, defense

# ─────────────────────────────
# FOREBET-STYLE ENGINE
# ─────────────────────────────
def predict_match(home, away):

    h_attack, h_def = team_strength(home)
    a_attack, a_def = team_strength(away)

    # home advantage (important)
    home_lambda = (h_attack * 1.15 + a_def * 0.25)
    away_lambda = (a_attack * 0.95 + h_def * 0.30)

    max_goals = 6

    h = poisson.pmf(np.arange(max_goals), home_lambda)
    a = poisson.pmf(np.arange(max_goals), away_lambda)

    matrix = np.outer(h, a)

    p1 = np.sum(np.tril(matrix, -1)) * 100
    px = np.sum(np.diag(matrix)) * 100
    p2 = np.sum(np.triu(matrix, 1)) * 100
    over25 = (1 - np.sum(matrix[:3, :3])) * 100

    score_home = np.argmax(h)
    score_away = np.argmax(a)

    # FOREBET STYLE TREND ENGINE
    if p1 > 47:
        trend = "Strong home dominance expected"
    elif p2 > 47:
        trend = "Strong away performance expected"
    elif over25 > 55:
        trend = "High scoring match expected"
    else:
        trend = "Balanced match"

    return {
        "1": round(p1,1),
        "X": round(px,1),
        "2": round(p2,1),
        "O2.5": round(over25,1),
        "score": f"{score_home}-{score_away}",
        "trend": trend
    }

# ─────────────────────────────
# LOAD DATA
# ─────────────────────────────
date_str = datetime.now(tz).strftime("%Y-%m-%d")
fixtures = get_fixtures(date_str)

# ─────────────────────────────
# DISPLAY ENGINE
# ─────────────────────────────
for m in fixtures:

    p = predict_match(m["home"], m["away"])

    st.markdown(f"""
    <div class="card">
        <div class="team">{m['home']} vs {m['away']}</div>

        <div class="score">Predicted Score: {p['score']}</div>

        <div class="trend">{p['trend']}</div>

        <div>
            <span class="box">1 {p['1']}%</span>
            <span class="box">X {p['X']}%</span>
            <span class="box">2 {p['2']}%</span>
            <span class="box">O2.5 {p['O2.5']}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
