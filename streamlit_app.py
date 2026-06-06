import streamlit as st
import numpy as np
from scipy.stats import poisson
import random
from streamlit_autorefresh import st_autorefresh

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title="AI SCORECAST PRO+ (FOREBET)", layout="wide")
st_autorefresh(interval=120000, key="refresh")

# ─────────────────────────────
# STYLE PRO
# ─────────────────────────────
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:36px;
    font-weight:900;
    color:#1DB954;
    margin-bottom:20px;
}

.card {
    background:white;
    padding:14px;
    margin:10px 0;
    border-radius:12px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
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

.trend {
    font-size:13px;
    color:#444;
    margin-top:5px;
    font-style:italic;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>⚽ AI SCORECAST PRO+ • FOREBET ENGINE</div>", unsafe_allow_html=True)

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
# HISTORIQUE SIMULÉ (BASE FUTURE DB)
# ─────────────────────────────
history = {
    "FC Alpha":[2,1,3,1,2],
    "FC Beta":[1,0,2,1,1],
    "Real Test":[3,2,2,1,3],
    "AI United":[0,1,1,0,2],
    "Green FC":[2,2,1,3,2],
    "Future Stars":[1,1,0,1,1],
    "Burundi Stars":[2,1,2,2,1],
    "City FC":[1,2,1,0,1]
}

# ─────────────────────────────
# FEATURE ENGINE PRO
# ─────────────────────────────
def team_strength(team):

    goals = history.get(team, [1,1,1,1,1])

    attack = np.mean(goals) / 2.0
    defense = 1.5 - attack

    form = (goals[-1] + goals[-2]) / 4

    return attack + form, defense

# ─────────────────────────────
# FOREBET PRO MODEL
# ─────────────────────────────
def predict(home, away):

    h_attack, h_def = team_strength(home)
    a_attack, a_def = team_strength(away)

    # home advantage réaliste
    home_lambda = (h_attack * 1.25 + a_def * 0.30)
    away_lambda = (a_attack * 0.95 + h_def * 0.35)

    max_g = 6

    h = poisson.pmf(np.arange(max_g), home_lambda)
    a = poisson.pmf(np.arange(max_g), away_lambda)

    matrix = np.outer(h, a)

    p1 = np.sum(np.tril(matrix, -1)) * 100
    px = np.sum(np.diag(matrix)) * 100
    p2 = np.sum(np.triu(matrix, 1)) * 100
    over25 = (1 - np.sum(matrix[:3, :3])) * 100

    score_h = np.argmax(h)
    score_a = np.argmax(a)

    # trend PRO
    if p1 > 48:
        trend = "Home dominance detected"
    elif p2 > 48:
        trend = "Away dominance detected"
    elif over25 > 60:
        trend = "High scoring match expected"
    else:
        trend = "Balanced tactical match"

    return {
        "1": round(p1,1),
        "X": round(px,1),
        "2": round(p2,1),
        "O2.5": round(over25,1),
        "score": f"{score_h}-{score_a}",
        "trend": trend
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

        <div class="trend">{p['trend']}</div>

        <div style="margin-top:6px;">
            <span class="badge green">1: {p['1']}%</span>
            <span class="badge orange">X: {p['X']}%</span>
            <span class="badge red">2: {p['2']}%</span>
            <span class="badge">O2.5: {p['O2.5']}%</span>
        </div>

    </div>
    """, unsafe_allow_html=True)
