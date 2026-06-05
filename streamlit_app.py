import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np
from scipy.stats import poisson
import os

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title="AI-BET • Livescore & Pronos", layout="wide")

tz = pytz.timezone("Africa/Bujumbura")

ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD",
    st.secrets.get("ADMIN_PASSWORD", "CHANGE_ME")
)

API_KEY = os.getenv(
    "API_FOOTBALL_KEY",
    st.secrets.get("API_FOOTBALL_KEY", "")
)

# ─────────────────────────────
# AUTO REFRESH
# ─────────────────────────────
if "mode" not in st.session_state:
    st.session_state.mode = "Client"

if st.session_state.mode == "Client":
    st_autorefresh(interval=90 * 1000, key="refresh")

# ─────────────────────────────
# STYLE
# ─────────────────────────────
st.markdown("""
<style>
.stApp { background: #f8f9fa; }
.match-card { background: white; border-radius: 8px; padding: 12px; margin-bottom: 12px;
box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; gap: 12px; }

.time-col { min-width: 70px; text-align: center; font-weight: bold; }
.time { font-size: 1.1rem; }

.status-live { color: #dc3545; font-weight: 900; }
.status-fin { color: #6c757d; }

.teams { flex-grow: 1; }

.team-row { display: flex; justify-content: space-between; }

.score { font-weight: 900; }

.proba-box {
background: #e9f5ff;
border-radius: 6px;
padding: 4px 8px;
font-weight: bold;
font-size: 0.85rem;
}

.win-border { border-left: 5px solid #28a745; }
.loss-border { border-left: 5px solid #dc3545; }
.wait-border { border-left: 5px solid #ffc107; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# SIDEBAR
# ─────────────────────────────
with st.sidebar:
    st.header("AI-BET")

    toggle = st.toggle("Mode Admin")

    if toggle:
        pwd = st.text_input("Mot de passe", type="password")

        if pwd == ADMIN_PASSWORD:
            st.session_state.mode = "Admin"
            st.success("Admin activé")
        else:
            st.session_state.mode = "Client"
            if pwd:
                st.error("Mot de passe incorrect")
    else:
        st.session_state.mode = "Client"

    show_tomorrow = st.checkbox("Voir demain", value=False)

# ─────────────────────────────
# POISSON MODEL (AMÉLIORABLE)
# ─────────────────────────────
def get_poisson_proba(home, away):
    # VERSION SIMPLIFIÉE (sera améliorée avec données réelles ensuite)

    lambda_home = 1.6
    lambda_away = 1.2

    max_goals = 6

    home_probs = poisson.pmf(np.arange(max_goals), lambda_home)
    away_probs = poisson.pmf(np.arange(max_goals), lambda_away)

    matrix = np.outer(home_probs, away_probs)

    p_home = np.sum(np.tril(matrix, -1)) * 100
    p_draw = np.sum(np.diag(matrix)) * 100
    p_away = np.sum(np.triu(matrix, 1)) * 100

    over25 = (1 - np.sum(matrix[:3, :3])) * 100

    return {
        "1": round(p_home, 1),
        "X": round(p_draw, 1),
        "2": round(p_away, 1),
        "Over2.5": round(over25, 1)
    }

# ─────────────────────────────
# API FETCH
# ─────────────────────────────
@st.cache_data(ttl=120)
def fetch_fixtures(date_str):
    if not API_KEY:
        return []

    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        if "response" in data:
            return data["response"]

        return []
    except:
        return []

# ─────────────────────────────
# ADMIN MODE
# ─────────────────────────────
if st.session_state.mode == "Admin":
    st.subheader("Admin Panel")

    mid = st.text_input("Match ID")
    prono = st.selectbox("Prono", ["1", "X", "2"])

    if st.button("Save"):
        if mid:
            if "pronos" not in st.session_state:
                st.session_state.pronos = {}

            st.session_state.pronos[mid] = prono
            st.success("Prono enregistré")

# ─────────────────────────────
# CLIENT VIEW
# ─────────────────────────────
else:
    st.markdown("<h2 style='text-align:center;'>AI-BET LIVESCORE</h2>", unsafe_allow_html=True)

    date = datetime.now(tz).date()

    if show_tomorrow:
        date += timedelta(days=1)

    date_str = date.strftime("%Y-%m-%d")

    fixtures = fetch_fixtures(date_str)

    if not fixtures:
        st.warning("Aucun match ou quota API atteint")
    else:

        live = []
        upcoming = []
        finished = []

        for m in fixtures:
            status = m["fixture"]["status"]["short"]

            if status in ["1H", "HT", "2H"]:
                live.append(m)
            elif status == "NS":
                upcoming.append(m)
            else:
                finished.append(m)

        for group, title in [(live, "LIVE"), (upcoming, "UPCOMING"), (finished, "FINISHED")]:

            if group:
                st.subheader(title)

                for m in group:

                    fid = str(m["fixture"]["id"])

                    home = m["teams"]["home"]["name"]
                    away = m["teams"]["away"]["name"]

                    hg = m["goals"]["home"]
                    ag = m["goals"]["away"]

                    status = m["fixture"]["status"]["short"]

                    dt = datetime.fromisoformat(
                        m["fixture"]["date"].replace("Z", "+00:00")
                    ).astimezone(tz)

                    time = dt.strftime("%H:%M")

                    border = "wait-border"

                    prono_html = ""

                    if "pronos" in st.session_state and fid in st.session_state["pronos"]:
                        p = st.session_state["pronos"][fid]

                        prono_html = f"<div class='proba-box'>{p}</div>"

                        if status == "FT":
                            result = "1" if hg > ag else ("2" if ag > hg else "X")
                            border = "win-border" if p == result else "loss-border"

                    proba_html = ""

                    if status == "NS":
                        proba = get_poisson_proba(home, away)

                        proba_html = f"""
                        <div style="display:flex; gap:5px; margin-top:5px;">
                            <div class='proba-box'>{proba['1']}%</div>
                            <div class='proba-box'>{proba['X']}%</div>
                            <div class='proba-box'>{proba['2']}%</div>
                            <div class='proba-box'>O2.5 {proba['Over2.5']}%</div>
                        </div>
                        """

                    st.markdown(f"""
                    <div class="match-card {border}">
                        <div class="time-col">
                            <div class="time">{time}</div>
                        </div>

                        <div class="teams">
                            <div class="team-row">
                                <span>{home}</span><span class="score">{hg}</span>
                            </div>
                            <div class="team-row">
                                <span>{away}</span><span class="score">{ag}</span>
                            </div>
                            {proba_html}
                        </div>

                        {prono_html}
                    </div>
                    """, unsafe_allow_html=True)
