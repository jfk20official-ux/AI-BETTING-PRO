import streamlit as st
import requests
import numpy as np
import pandas as pd
from xgboost import XGBClassifier

# ==================================================
# AIBET V2
# ==================================================

st.set_page_config(
    page_title="AiBet",
    page_icon="⚽",
    layout="wide"
)

API_KEY = st.secrets.get("API_FOOTBALL_KEY", "")
ODDS_KEY = st.secrets.get("ODDS_API_KEY", "")

# ==================================================
# STYLE
# ==================================================

st.markdown("""
<style>

.title{
    font-size:42px;
    text-align:center;
    font-weight:900;
    color:#00D26A;
}

.subtitle{
    text-align:center;
    color:#888;
    margin-bottom:25px;
    font-size:16px;
}

.card{
    background:white;
    padding:18px;
    margin:12px 0;
    border-radius:14px;
    box-shadow:0 2px 12px rgba(0,0,0,0.08);
}

.badge{
    padding:6px 10px;
    border-radius:8px;
    font-weight:700;
    margin-right:6px;
}

.green{
    background:#d4edda;
    color:#155724;
}

.red{
    background:#f8d7da;
    color:#721c24;
}

.blue{
    background:#d9ecff;
    color:#0b4f8a;
}

.orange{
    background:#fff3cd;
    color:#856404;
}

.value{
    color:#00A651;
    font-weight:900;
    margin-top:8px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='title'>⚽ AiBet</div>
<div class='subtitle'>
Smarter Predictions. Better Decisions.
</div>
""", unsafe_allow_html=True)

# ==================================================
# FALLBACK MATCHES
# ==================================================

def fallback_matches():
    return [
        {"teams":{"home":{"name":"FC Alpha"},"away":{"name":"FC Beta"}}},
        {"teams":{"home":{"name":"Real Test"},"away":{"name":"AI United"}}},
        {"teams":{"home":{"name":"Green FC"},"away":{"name":"Future Stars"}}},
        {"teams":{"home":{"name":"Burundi Stars"},"away":{"name":"City FC"}}},
        {"teams":{"home":{"name":"River FC"},"away":{"name":"Mountain FC"}}}
    ]

# ==================================================
# API FOOTBALL
# ==================================================

def get_matches():

    if not API_KEY:
        return fallback_matches()

    try:

        url = "https://v3.football.api-sports.io/fixtures?next=10"

        headers = {
            "x-apisports-key": API_KEY
        }

        r = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        data = r.json()

        matches = data.get("response", [])

        if not matches:
            return fallback_matches()

        return matches

    except Exception:
        return fallback_matches()

# ==================================================
# FEATURE ENGINE
# ==================================================

def features(home, away):

    seed = abs(hash(home + away)) % 100000

    rng = np.random.default_rng(seed)

    h_attack = rng.uniform(1.2, 2.5)
    a_attack = rng.uniform(1.0, 2.3)

    elo_diff = rng.uniform(-50, 50)

    form = rng.uniform(-1, 1)

    return [
        h_attack,
        a_attack,
        elo_diff,
        form
    ]

# ==================================================
# TRAIN MODEL
# ==================================================

@st.cache_resource
def train_model():

    data = []

    rng = np.random.default_rng(42)

    for _ in range(3000):

        h = rng.uniform(1.0, 2.5)
        a = rng.uniform(1.0, 2.3)

        elo = rng.uniform(-50, 50)
        form = rng.uniform(-1, 1)

        label = rng.choice([0,1,2])

        data.append([h,a,elo,form,label])

    df = pd.DataFrame(
        data,
        columns=[
            "h_attack",
            "a_attack",
            "elo",
            "form",
            "result"
        ]
    )

    X = df[
        [
            "h_attack",
            "a_attack",
            "elo",
            "form"
        ]
    ]

    y = df["result"]

    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        random_state=42
    )

    model.fit(X, y)

    return model

try:
    model = train_model()

except Exception as e:
    st.error(f"Erreur modèle : {e}")
    st.stop()

# ==================================================
# VALUE BET
# ==================================================

def value_bet(prob, odds=2.0):

    ev = (prob / 100) * odds

    return ev, ev > 1.05

# ==================================================
# PREDICT
# ==================================================

def predict(match):

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    feats = features(home, away)

    probs = model.predict_proba([feats])[0]

    p1 = float(probs[2] * 100)
    px = float(probs[0] * 100)
    p2 = float(probs[1] * 100)

    score_home = max(0, round(feats[0]))
    score_away = max(0, round(feats[1]))

    score = f"{score_home}-{score_away}"

    confidence = max(p1, px, p2)

    trend = "Balanced"

    if p1 > 50:
        trend = "Home strong"

    elif p2 > 50:
        trend = "Away strong"

    value_text = ""

    ev, ok = value_bet(max(p1, p2))

    if ok:

        if p1 > p2:
            value_text = "💰 VALUE BET: HOME WIN"

        else:
            value_text = "💰 VALUE BET: AWAY WIN"

    return (
        home,
        away,
        p1,
        px,
        p2,
        score,
        confidence,
        trend,
        value_text
    )

# ==================================================
# UI
# ==================================================

matches = get_matches()

st.write(f"📊 Matches loaded: {len(matches)}")

for match in matches[:10]:

    try:

        (
            home,
            away,
            p1,
            px,
            p2,
            score,
            confidence,
            trend,
            value
        ) = predict(match)

        st.markdown(f"""
        <div class="card">

            <h3>{home} vs {away}</h3>

            <h2>Predicted Score: {score}</h2>

            <p>
            {trend}
            • Confidence {confidence:.1f}%
            </p>

            <div>
                <span class="badge green">
                1: {p1:.1f}%
                </span>

                <span class="badge orange">
                X: {px:.1f}%
                </span>

                <span class="badge red">
                2: {p2:.1f}%
                </span>
            </div>

            <div class="value">
                {value}
            </div>

        </div>
        """, unsafe_allow_html=True)

    except Exception as e:

        st.error(
            f"Erreur sur un match : {e}"
        )
