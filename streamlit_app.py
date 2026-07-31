import streamlit as st
import requests
import os
import numpy as np
import pandas as pd
import pytz

from datetime import datetime, timedelta
from scipy.stats import poisson
from streamlit_autorefresh import st_autorefresh


# ==========================================================
# CONFIGURATION APPLICATION
# ==========================================================

st.set_page_config(
    page_title="AI-BET PRO",
    page_icon="⚽",
    layout="wide"
)


# ==========================================================
# SECRETS
# ==========================================================

try:
    API_KEY = os.getenv(
        "API_FOOTBALL_KEY",
        st.secrets["API_FOOTBALL_KEY"]
    )
except:
    API_KEY = ""

try:
    ADMIN_PASSWORD = os.getenv(
        "ADMIN_PASSWORD",
        st.secrets["ADMIN_PASSWORD"]
    )
except:
    ADMIN_PASSWORD = "CHANGE_ME"


TZ = pytz.timezone("Africa/Bujumbura")


# ==========================================================
# SESSION
# ==========================================================

if "mode" not in st.session_state:
    st.session_state.mode = "Client"

if "pronos" not in st.session_state:
    st.session_state.pronos = {}

if "history" not in st.session_state:
    st.session_state.history = []


# Refresh automatique client

if st.session_state.mode == "Client":
    st_autorefresh(
        interval=90000,
        key="aibet_refresh"
    )


# ==========================================================
# DESIGN AI-BET
# ==========================================================

st.markdown("""
<style>

body {
    background:#f5f7fa;
}

.main-title {
    text-align:center;
    color:#00A651;
    font-size:38px;
    font-weight:900;
}

.subtitle {
    text-align:center;
    color:#555;
    font-size:18px;
}


.match-card {

background:white;
border-radius:15px;
padding:18px;
margin-bottom:15px;
box-shadow:0 4px 15px rgba(0,0,0,0.08);

}


.team {

font-weight:700;
font-size:18px;

}


.score {

font-size:25px;
font-weight:900;
color:#00A651;

}


.badge {

padding:8px;
border-radius:10px;
font-weight:bold;
margin:3px;
display:inline-block;

}


.home {

background:#d4edda;
color:#155724;

}


.draw {

background:#fff3cd;
color:#856404;

}


.away {

background:#f8d7da;
color:#721c24;

}


.safe {

background:#00A651;
color:white;
padding:8px;
border-radius:10px;

}


.risk {

background:#dc3545;
color:white;
padding:8px;
border-radius:10px;

}


.value {

background:#111;
color:#00ff88;
padding:10px;
border-radius:10px;
font-weight:bold;

}


</style>
""", unsafe_allow_html=True)



# ==========================================================
# TITRE
# ==========================================================

st.markdown(
"""
<div class="main-title">
⚽ AI-BET PRO
</div>

<div class="subtitle">
Smarter Predictions. Better Decisions. 📊
</div>
""",
unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR ADMIN
# ==========================================================

with st.sidebar:

    st.header("⚽ AI-BET CONTROL")

    admin = st.toggle("Mode Admin")

    if admin:

        password = st.text_input(
            "Mot de passe",
            type="password"
        )

        if password == ADMIN_PASSWORD:

            st.session_state.mode="Admin"

            st.success(
                "Administrateur connecté"
            )

        elif password:

            st.error(
                "Mot de passe incorrect"
            )

    else:

        st.session_state.mode="Client"



    tomorrow = st.checkbox(
        "Afficher demain"
    )



# ==========================================================
# API FOOTBALL
# ==========================================================

@st.cache_data(ttl=120)
def fetch_fixtures(date_value):

    if not API_KEY:
        return []

    url = (
        "https://v3.football.api-sports.io/"
        f"fixtures?date={date_value}"
    )

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host":
        "v3.football.api-sports.io"
    }


    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        data = response.json()

        if "response" in data:
            return data["response"]

        return []


    except Exception:

        return []



# ==========================================================
# AI TEAM STRENGTH ENGINE
# ==========================================================

def team_strength(team_name):

    """
    Simulation intelligente temporaire.
    Prête à recevoir:
    - classement
    - forme
    - H2H
    - statistiques API
    """

    seed = sum(
        ord(c)
        for c in team_name
    )

    np.random.seed(seed)

    attack = np.random.uniform(
        0.8,
        2.4
    )

    defense = np.random.uniform(
        0.7,
        1.8
    )

    return attack, defense



# ==========================================================
# POISSON AI MODEL
# ==========================================================

def poisson_prediction(home, away):


    home_attack, home_defense = (
        team_strength(home)
    )

    away_attack, away_defense = (
        team_strength(away)
    )


    # Buts attendus

    lambda_home = (
        home_attack *
        (2 - away_defense/2)
    )


    lambda_away = (
        away_attack *
        (2 - home_defense/2)
    )


    lambda_home = max(
        0.3,
        min(lambda_home,4)
    )

    lambda_away = max(
        0.3,
        min(lambda_away,4)
    )



    max_goals = 6


    matrix = np.outer(
        poisson.pmf(
            np.arange(max_goals+1),
            lambda_home
        ),

        poisson.pmf(
            np.arange(max_goals+1),
            lambda_away
        )
    )



    # Probabilités résultat


    home_win = (
        np.tril(matrix,-1).sum()
        *100
    )


    draw = (
        np.diag(matrix).sum()
        *100
    )


    away_win = (
        np.triu(matrix,1).sum()
        *100
    )


    # Score exact

    index = np.unravel_index(
        np.argmax(matrix),
        matrix.shape
    )


    score = (
        f"{index[0]}-{index[1]}"
    )



    # Over 2.5


    under25 = 0

    for h in range(3):
        for a in range(3-h):
            under25 += matrix[h][a]


    over25 = (
        1-under25
    )*100



    # BTTS


    btts = (
        1 -
        matrix[0,:].sum()
        -
        matrix[:,0].sum()
        +
        matrix[0,0]
    )*100



    confidence = max(
        home_win,
        draw,
        away_win
    )


    return {

        "score":score,

        "1":round(
            home_win,
            1
        ),

        "X":round(
            draw,
            1
        ),

        "2":round(
            away_win,
            1
        ),

        "over25":round(
            over25,
            1
        ),

        "btts":round(
            btts,
            1
        ),

        "confidence":round(
            confidence,
            1
        )

    }



# ==========================================================
# VALUE BET ENGINE
# ==========================================================

def value_engine(probability, odd=None):


    if not odd:

        return {
            "value":False,
            "message":
            "Cote non disponible"
        }



    expected = (
        probability/100
    )*odd



    if expected > 1.05:

        return {

            "value":True,

            "message":
            "💰 VALUE BET DETECTED"

        }


    return {

        "value":False,

        "message":
        "Pas de value"

    }



# ==========================================================
# TOP PICK ENGINE
# ==========================================================

def ai_signal(data):


    conf = data["confidence"]


    if conf >=70:

        return (
            "🔥 SAFE PICK",
            "safe"
        )


    elif conf >=55:

        return (
            "⚠️ MEDIUM RISK",
            "safe"
        )


    else:

        return (
            "❌ HIGH RISK",
            "risk"
        )




# ==========================================================
# ADMIN PANEL
# ==========================================================

if st.session_state.mode == "Admin":


    st.subheader(
        "🛠️ AI-BET ADMIN PANEL"
    )


    match_id = st.text_input(
        "ID du match"
    )


    prediction = st.selectbox(
        "Pronostic manuel",
        [
            "1",
            "X",
            "2"
        ]
    )


    if st.button(
        "Enregistrer le pronostic"
    ):

        if match_id:

            st.session_state.pronos[
                match_id
            ] = prediction


            st.success(
                "Pronostic enregistré"
            )



# ==========================================================
# CLIENT DASHBOARD
# ==========================================================

else:


    st.subheader(
        "⚽ Matchs & Prédictions IA"
    )


    today = datetime.now(
        TZ
    ).date()


    if tomorrow:

        today += timedelta(
            days=1
        )


    date_api = today.strftime(
        "%Y-%m-%d"
    )


    fixtures = fetch_fixtures(
        date_api
    )



    if not fixtures:


        st.warning(
            "Aucun match trouvé ou API indisponible"
        )


    else:


        predictions_today = []



        # ===============================
        # CALCUL DES PRONOSTICS
        # ===============================


        for match in fixtures:


            status = (
                match["fixture"]
                ["status"]
                ["short"]
            )


            if status != "NS":

                continue



            home = (
                match["teams"]
                ["home"]
                ["name"]
            )


            away = (
                match["teams"]
                ["away"]
                ["name"]
            )



            prediction = poisson_prediction(
                home,
                away
            )


            signal, css = ai_signal(
                prediction
            )


            predictions_today.append({

                "home":home,

                "away":away,

                "data":prediction,

                "signal":signal

            })



        # ===============================
        # TOP PICKS
        # ===============================


        if predictions_today:


            st.markdown(
                "## 🔥 AI-BET TOP PICKS"
            )


            top = sorted(
                predictions_today,
                key=lambda x:
                x["data"]["confidence"],
                reverse=True
            )[:5]



            for item in top:


                st.info(

                    f"""
                    ⚽ {item['home']}
                    vs
                    {item['away']}

                    Score:
                    {item['data']['score']}

                    Confiance:
                    {item['data']['confidence']}%

                    {item['signal']}
                    """

                )



        st.divider()



        # ===============================
        # MATCH CARDS
        # ===============================


        st.markdown(
            "## 📊 ANALYSE DES MATCHS"
        )


        for item in predictions_today:


            home = item["home"]

            away = item["away"]

            data = item["data"]


            signal, css = ai_signal(
                data
            )



            st.markdown(

            f"""

            <div class="match-card">


            <div class="team">

            ⚽ {home}
            <br>
            🆚
            <br>
            ⚽ {away}

            </div>


            <hr>


            <div class="score">

            Prediction:
            {data['score']}

            </div>


            <br>


            <span class="badge home">
            1:
            {data['1']}%
            </span>


            <span class="badge draw">
            X:
            {data['X']}%
            </span>


            <span class="badge away">
            2:
            {data['2']}%
            </span>


            <br><br>


            <span class="badge">
            Over 2.5:
            {data['over25']}%
            </span>


            <span class="badge">
            BTTS:
            {data['btts']}%
            </span>


            <br><br>


            <span class="{css}">
            {signal}
            </span>


            </div>


            """,

            unsafe_allow_html=True

            )



            # Sauvegarde historique

            st.session_state.history.append({

                "match":
                f"{home}-{away}",

                "score":
                data["score"],

                "confidence":
                data["confidence"]

            })


# ==========================================================
# PARTIE 4/4
# BACKTESTING + STATISTICS + FINALIZATION
# ==========================================================


# ==========================================================
# PERFORMANCE DASHBOARD
# ==========================================================

st.divider()


st.subheader(
    "📈 AI-BET PERFORMANCE"
)


total_predictions = len(
    st.session_state.history
)


if total_predictions > 0:


    df = pd.DataFrame(
        st.session_state.history
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Prédictions",
            total_predictions
        )


    with col2:

        avg_conf = round(
            df["confidence"]
            .mean(),
            1
        )

        st.metric(
            "Confiance moyenne",
            f"{avg_conf}%"
        )


    with col3:

        st.metric(
            "Moteur",
            "Poisson AI"
        )


    with st.expander(
        "Voir historique"
    ):

        st.dataframe(
            df,
            use_container_width=True
        )


else:


    st.info(
        "Pas encore d'historique disponible"
    )



# ==========================================================
# FOOTER AI-BET
# ==========================================================


st.markdown(
"""
<br><br>

<div style="
text-align:center;
color:#777;
font-size:14px;
">

⚽ AI-BET PRO ENGINE V2  
<br>
Smarter Predictions. Better Decisions.

<br>

Powered by:
Poisson Model • AI Engine • Football Data

</div>

""",
unsafe_allow_html=True
)

