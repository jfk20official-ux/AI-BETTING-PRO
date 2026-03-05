import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np
from scipy.stats import poisson
import os

# ====================== CONFIGURATION ======================
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Tunga25721204301")
API_FOOTBALL_KEY = "80da65258a3809f6c7ad2c74930ceb90"
FOOTBALL_DATA_KEY = "A6ef05d939bb4da9acae3d8de8c47c8c"

tz = pytz.timezone("Africa/Bujumbura")

if 'mode' not in st.session_state:
    st.session_state.mode = "Client"
if st.session_state.mode == "Client":
    st_autorefresh(interval=90 * 1000, key="refresh")

st.set_page_config(page_title="AI-BET EXPERT", layout="wide", initial_sidebar_state="collapsed")

# ====================== STYLE MODERNE ======================
st.markdown("""
<style>
    .block-container { padding: 0 !important; background: #0b0e11; }
    .sticky-nav { position: fixed; top: 0; width: 100%; z-index: 1000; background: #161920; 
                  display: flex; overflow-x: auto; padding: 12px; gap: 10px; border-bottom: 2px solid #2d3442; }
    .nav-btn { background: #212630; color: white; padding: 8px 20px; border-radius: 6px; 
               font-weight: bold; white-space: nowrap; border: 1px solid #3e4451; }
    .match-card { background: #161920; border-radius: 10px; padding: 15px; margin: 12px 0; color: white; }
    .prob-table { width: 100%; border-collapse: collapse; margin: 10px 0; }
    .prob-header { background: #212630; color: #ffca28; font-weight: bold; }
    .prob-val { font-size: 1.2rem; font-weight: bold; }
    .res-pos { color: #00ff88; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ====================== NAVIGATION TABS ======================
tab1, tab2, tab3, tab4 = st.tabs(["🏟️ Livescore", "🔮 1X2 Pronos", "⚽ BTTS & Over 2.5", "📊 Statistiques"])

# ====================== POISSON AVEC BTTS & OVER ======================
def get_poisson_proba(home, away):
    λh = 1.8
    λa = 1.3
    MAX = 6
    matrix = np.outer(poisson.pmf(np.arange(MAX+1), λh), poisson.pmf(np.arange(MAX+1), λa))
    p1 = np.sum(np.tril(matrix, -1)) * 100
    px = np.sum(np.diag(matrix)) * 100
    p2 = np.sum(np.triu(matrix, 1)) * 100
    over25 = (1 - sum(np.diag(matrix, k).sum() for k in range(-2,3))) * 100
    btts = (1 - matrix[0,0] - sum(matrix[i,0] for i in range(1,MAX+1)) - sum(matrix[0,j] for j in range(1,MAX+1))) * 100

    return {"1": round(p1,1), "X": round(px,1), "2": round(p2,1),
            "Over2.5": round(over25,1), "BTTS": round(btts,1)}

# ====================== FETCH 3 SOURCES ======================
@st.cache_data(ttl=300)
def fetch_all_sources():
    date_str = datetime.now(tz).strftime("%Y-%m-%d")

    # 1. TheSportsDB (priorité)
    try:
        r = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={date_str}", timeout=8).json()
        events = r.get("events", [])
        if events:
            return [{"fixture": {"id": e.get("idEvent"), "date": e.get("dateEvent")+"T"+e.get("strTime","00:00:00"),
                                 "status": {"short": "NS"}},
                     "teams": {"home": {"name": e.get("strHomeTeam")}, "away": {"name": e.get("strAwayTeam")}},
                     "goals": {"home": e.get("intHomeScore"), "away": e.get("intAwayScore")}} for e in events]
    except: pass

    # 2. Football-Data.org
    try:
        r = requests.get("https://api.football-data.org/v4/matches", 
                         headers={"X-Auth-Token": FOOTBALL_DATA_KEY}, timeout=8).json()
        if r.get("matches"):
            return r["matches"]
    except: pass

    # 3. API-Football (dernier recours)
    try:
        r = requests.get(f"https://v3.football.api-sports.io/fixtures?date={date_str}",
                         headers={"x-rapidapi-key": API_FOOTBALL_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}, timeout=8).json()
        if r.get("response"):
            return r["response"]
    except: pass

    return []

matches = fetch_all_sources()

# ====================== AFFICHAGE ======================
with tab1:  # Livescore
    st.markdown("<h2 style='text-align:center; color:#38b6ff;'>🏟️ LIVE & À VENIR</h2>", unsafe_allow_html=True)
    if not matches:
        st.error("⚠️ Aucune donnée disponible pour le moment")
    else:
        for m in matches[:15]:  # limite pour éviter surcharge
            h = m.get('teams', {}).get('home', {}).get('name') or m.get('homeTeam', {}).get('name', '???')
            a = m.get('teams', {}).get('away', {}).get('name') or m.get('awayTeam', {}).get('name', '???')
            hs = m.get('goals', {}).get('home') or m.get('score', {}).get('fullTime', {}).get('home', '-')
            as_ = m.get('goals', {}).get('away') or m.get('score', {}).get('fullTime', {}).get('away', '-')
            
            with st.expander(f"⚽ {h} vs {a}"):
                st.markdown(f"**Score :** {hs} - {as_}")
                proba = get_poisson_proba(h, a)
                st.table({
                    "1X2": [proba["1"], proba["X"], proba["2"]],
                    "BTTS": [proba["BTTS"], "-", "-"],
                    "Over 2.5": [proba["Over2.5"], "-", "-"]
                })

with tab2:  # 1X2 Pronos
    st.markdown("<h2 style='text-align:center; color:#ffca28;'>🔮 1X2 & PRONOS IA</h2>", unsafe_allow_html=True)
    for m in matches:
        h = m.get('teams', {}).get('home', {}).get('name') or m.get('homeTeam', {}).get('name', '???')
        a = m.get('teams', {}).get('away', {}).get('name') or m.get('awayTeam', {}).get('name', '???')
        proba = get_poisson_proba(h, a)
        st.success(f"{h} vs {a} → **1** {proba['1']}% | **X** {proba['X']}% | **2** {proba['2']}%")

with tab3:  # BTTS & Over 2.5
    st.markdown("<h2 style='text-align:center; color:#00ff88;'>⚽ BTTS & OVER / UNDER</h2>", unsafe_allow_html=True)
    for m in matches:
        h = m.get('teams', {}).get('home', {}).get('name') or m.get('homeTeam', {}).get('name', '???')
        a = m.get('teams', {}).get('away', {}).get('name') or m.get('awayTeam', {}).get('name', '???')
        proba = get_poisson_proba(h, a)
        st.info(f"{h} vs {a} → BTTS **{proba['BTTS']}%** | Over 2.5 **{proba['Over2.5']}%**")

with tab4:  # Statistiques
    st.markdown("<h2 style='text-align:center; color:#ff4b4b;'>📊 STATISTIQUES IA</h2>", unsafe_allow_html=True)
    st.write("Statistiques détaillées en cours de développement...")

# Admin Mode
if st.sidebar.checkbox("Mode Admin"):
    pwd = st.sidebar.text_input("Mot de passe Admin", type="password")
    if pwd == ADMIN_PASSWORD:
        st.sidebar.success("Admin activé")
        # Tu peux ajouter ici la logique d'enregistrement de pronos
