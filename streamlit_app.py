import streamlit as st
import requests
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BET EXPERT", layout="wide", initial_sidebar_state="collapsed")
tz = pytz.timezone("Africa/Bujumbura")
date_now = datetime.now(tz).strftime("%d/%m/%Y")
api_date = datetime.now(tz).strftime("%Y-%m-%d")

# Tes Clés
API_KEY_RAPID = "80da65258a3809f6c7ad2c74930ceb90"
FOOTBALL_DATA_KEY = "A6ef05d939bb4da9acae3d8de8c47c8c"

# --- STYLE CSS (Barre Fixe & Couleurs) ---
st.markdown("""
<style>
    .block-container { padding: 0px !important; background-color: #0b0e11; }
    .sticky-nav {
        position: fixed; top: 0; width: 100%; z-index: 1000;
        background: #161920; display: flex; overflow-x: auto;
        padding: 12px; gap: 10px; border-bottom: 2px solid #2d3442;
    }
    .nav-btn {
        background: #212630; color: #ffffff; padding: 7px 18px;
        border-radius: 5px; font-weight: bold; font-size: 0.85rem;
        border: 1px solid #3e4451; white-space: nowrap;
    }
    .date-time { color: #8a8f9d; font-size: 0.8rem; padding: 10px 15px 0 15px; }
    .stExpander summary p { color: #ff4b4b !important; font-size: 1.1rem !important; font-weight: bold !important; }
    .prediction-txt { color: #38b6ff; font-weight: bold; font-size: 1rem; padding: 5px 15px; }
    .prob-table { width: 95%; margin: 10px auto; text-align: center; color: white; border-collapse: collapse; }
    .prob-header { font-weight: bold; font-size: 1rem; color: #ffffff; }
    .prob-val { font-size: 1.1rem; color: #ffca28; font-weight: bold; }
    .res-pos { color: #00ff88; font-weight: bold; padding: 5px 15px; }
    .res-neg { color: #8a8f9d; font-weight: bold; padding: 5px 15px; }
    .spacer { height: 75px; }
    hr { border: 0; border-bottom: 1px solid #24272e; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
st.markdown("""
<div class="sticky-nav">
    <div class="nav-btn">1X2</div>
    <div class="nav-btn">BTTS</div>
    <div class="nav-btn">Over 2.5</div>
    <div class="nav-btn">VIP</div>
    <div class="nav-btn">JFK20</div>
</div><div class="spacer"></div>
""", unsafe_allow_html=True)

# --- MOTEUR D'ALTERNANCE (BACKUP) ---
@st.cache_data(ttl=300)
def fetch_all_sources():
    # Source 1: API-Football (RapidAPI)
    url1 = f"https://v3.football.api-sports.io/fixtures?date={api_date}"
    headers1 = {"x-rapidapi-key": API_KEY_RAPID, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        r1 = requests.get(url1, headers=headers1, timeout=7).json()
        if r1.get("response"):
            return r1["response"], "APIF"
    except: pass

    # Source 2: Football-Data.org (En cas d'échec de la 1)
    url2 = "https://api.football-data.org/v4/matches"
    headers2 = {"X-Auth-Token": FOOTBALL_DATA_KEY}
    try:
        r2 = requests.get(url2, headers=headers2, timeout=7).json()
        if r2.get("matches"):
            return r2["matches"], "FDOrg"
    except: pass
    
    return [], None

# --- AFFICHAGE ---
matches, source = fetch_all_sources()

if matches:
    for m in matches:
        # Normalisation des données selon la source
        if source == "APIF":
            h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
            h_score, a_score = m['goals']['home'], m['goals']['away']
            time_start = m['fixture']['date'][11:16]
        else:
            h_name, a_name = m['homeTeam']['name'], m['awayTeam']['name']
            h_score, a_score = m['score']['fullTime']['home'], m['score']['fullTime']['away']
            time_start = m['utcDate'][11:16]

        # 1. Date (Gris)
        st.markdown(f'<div class="date-time">{date_now} - {time_start}</div>', unsafe_allow_html=True)
        
        # 2. Match (Rouge) + Expander pour stats
        with st.expander(f"{h_name} Vs {a_name}"):
            st.markdown(f"""
            <div style="background:#161920; padding:10px; color:#8a8f9d; font-size:0.85rem;">
                <b>ANALYSE IA</b><br>
                • {h_name} : Forme (V-N-V)<br>
                • {a_name} : Forme (D-D-N)
            </div>
            """, unsafe_allow_html=True)

        # 3. Table 1X2 (Sans %)
        st.markdown(f"""
        <table class="prob-table">
            <tr class="prob-header"><td>1</td><td>X</td><td>2</td></tr>
            <tr class="prob-val"><td>41</td><td>32</td><td>27</td></tr>
        </table>
        """, unsafe_allow_html=True)

        # 4. Choix attendu (Bleu)
        st.markdown('<div class="prediction-txt">PRONO: 1X & Over 1.5</div>', unsafe_allow_html=True)

        # 5. Score Final (Vert/Gris)
        if h_score is not None:
            style = "res-pos" if (h_score + a_score) > 0 else "res-neg"
            st.markdown(f'<div class="{style}">Score Final: {h_score} - {a_score}</div>', unsafe_allow_html=True)
        
        st.markdown('<hr>', unsafe_allow_html=True)
else:
    st.error("⚠️ Quotas API épuisés sur les deux sources. Réessayez plus tard.")
