import streamlit as st
import requests
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title="AI SCORECAST PRO MAX", layout="wide")

API_KEY = st.secrets.get("API_FOOTBALL_KEY", "")
ODDS_KEY = st.secrets.get("ODDS_API_KEY", "")

# ─────────────────────────────
# UI STYLE
# ─────────────────────────────
st.markdown("""
<style>
.title{font-size:34px;text-align:center;font-weight:900;color:#1DB954}
.card{background:white;padding:15px;margin:10px;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
.badge{padding:5px 8px;border-radius:6px;font-weight:700;margin-right:4px}
.green{background:#d4edda;color:#155724}
.red{background:#f8d7da;color:#721c24}
.blue{background:#d9ecff;color:#0b4f8a}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>⚽ AI SCORECAST PRO MAX ENGINE</div>", unsafe_allow_html=True)

# ─────────────────────────────
# API MATCHES
# ─────────────────────────────
def get_matches():

    if not API_KEY:
        return fallback()

    url = "https://v3.football.api-sports.io/fixtures?next=10"
    headers = {"x-apisports-key": API_KEY}

    try:
        r = requests.get(url, headers=headers, timeout=10).json()
        return r.get("response", [])
    except:
        return fallback()

def fallback():
    return [
        {"teams":{"home":{"name":"FC Alpha"},"away":{"name":"FC Beta"}}},
        {"teams":{"home":{"name":"Real Test"},"away":{"name":"AI United"}}}
    ]

# ─────────────────────────────
# FEATURE ENGINE (ELO + FORM SIMULÉ)
# ─────────────────────────────
def features(home, away):

    seed = abs(hash(home)) % 1000
    np.random.seed(seed)

    h_attack = np.random.uniform(1.2, 2.5)
    h_def = np.random.uniform(0.8, 2.0)

    a_attack = np.random.uniform(1.0, 2.3)
    a_def = np.random.uniform(0.8, 2.1)

    elo_diff = np.random.uniform(-50, 50)

    form = np.random.uniform(-1, 1)

    return [h_attack, h_def, a_attack, a_def, elo_diff, form]

# ─────────────────────────────
# DATASET TRAINING (SIMULÉ MAIS STRUCTURÉ)
# ─────────────────────────────
def train_model():

    data = []

    for _ in range(3000):

        h = np.random.uniform(1,2.5)
        a = np.random.uniform(1,2.3)

        elo = np.random.uniform(-50,50)
        form = np.random.uniform(-1,1)

        label = np.random.choice([0,1,2])

        data.append([h,a,elo,form,label])

    df = pd.DataFrame(data, columns=["h","a","elo","form","res"])

    X = df[["h","a","elo","form"]]
    y = df["res"]

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05
    )

    model.fit(X, y)

    return model

model = train_model()

# ─────────────────────────────
# ODDS API
# ─────────────────────────────
def get_odds():
    if not ODDS_KEY:
        return None

    try:
        url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={ODDS_KEY}&regions=eu&markets=h2h"
        r = requests.get(url, timeout=10).json()
        return r
    except:
        return None

# ─────────────────────────────
# VALUE BET ENGINE 💰
# ─────────────────────────────
def value_bet(prob, odds):

    ev = (prob/100) * odds

    return ev, ev > 1.05

# ─────────────────────────────
# PREDICT ENGINE
# ─────────────────────────────
def predict(match):

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    f = features(home, away)

    probs = model.predict_proba([f])[0]

    p_draw = probs[0] * 100
    p_away = probs[1] * 100
    p_home = probs[2] * 100

    score = f"{int(f[0])}-{int(f[2])}"

    confidence = max(probs) * 100

    trend = "Balanced"
    if p_home > 50:
        trend = "Home strong"
    elif p_away > 50:
        trend = "Away strong"

    value = ""
    ev, ok = value_bet(p_home, 2.0)
    if ok:
        value = "💰 VALUE BET DETECTED"

    return home, away, p_home, p_draw, p_away, score, confidence, trend, value

# ─────────────────────────────
# UI
# ─────────────────────────────
matches = get_matches()

for m in matches[:8]:

    h, a, ph, pd, pa, score, conf, trend, value = predict(m)

    st.markdown(f"""
    <div class="card">

        <h3>{h} vs {a}</h3>

        <h2>{score}</h2>

        <p>{trend} • Confidence {round(conf,1)}%</p>

        <div>
            <span class="badge green">1: {round(ph,1)}%</span>
            <span class="badge blue">X: {round(pd,1)}%</span>
            <span class="badge red">2: {round(pa,1)}%</span>
        </div>

        <h4 style="color:green;">{value}</h4>

    </div>
    """, unsafe_allow_html=True)
