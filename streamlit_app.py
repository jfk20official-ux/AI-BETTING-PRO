import streamlit as st
import requests
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BET PRO", layout="wide", initial_sidebar_state="collapsed")
tz = pytz.timezone("Africa/Bujumbura")
date_now = datetime.now(tz).strftime("%Y-%m-%d")

API_KEY_RAPID = "80da65258a3809f6c7ad2c74930ceb90"

# --- LANGUES ---
LANGUAGES = {
    "Français": {"live": "DIRECT", "win": "Gagne", "ov15": "Plus 1.5", "ov25": "Plus 2.5"},
    "English": {"live": "LIVE", "win": "Win", "ov15": "Over 1.5", "ov25": "Over 2.5"},
    "Kiswahili": {"live": "MUBASHARA", "win": "Shinda", "ov15": "Zaidi 1.5", "ov25": "Zaidi 2.5"},
}
sel_lang = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
L = LANGUAGES[sel_lang]

# --- STYLE CSS (FULL MOBILE WIDTH & HIGH READABILITY) ---
st.markdown("""
<style>
    /* Supprimer les marges Streamlit pour le plein écran */
    .block-container { padding: 10px !important; }
    
    .match-card {
        width: 100%; 
        background-color: #121212; 
        border-bottom: 1px solid #333;
        padding: 15px 5px;
        margin-bottom: 2px;
    }
    .league-name { color: #aaaaaa; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 5px; }
    .team-row { display: flex; justify-content: space-between; align-items: center; margin: 3px 0; }
    .team-name { color: #ffffff; font-size: 1.05rem; font-weight: 500; }
    .score { color: #00ff88; font-size: 1.2rem; font-weight: bold; min-width: 30px; text-align: center; }
    .time-val { color: #ff4b4b; font-weight: bold; font-size: 0.85rem; }
    
    /* Grille de pronostics */
    .prono-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        margin-top: 12px;
    }
    .prono-item {
        background: #222;
        border: 1px solid #444;
        border-radius: 4px;
        padding: 6px;
        text-align: center;
    }
    .prono-label { color: #888; font-size: 0.65rem; display: block; }
    .prono-val { color: #ffca28; font-size: 0.85rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=120)
def fetch_data():
    url = f"https://v3.football.api-sports.io/fixtures?date={date_now}"
    headers = {"x-rapidapi-key": API_KEY_RAPID, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        r = requests.get(url, headers=headers, timeout=10).json()
        return r.get("response", [])
    except: return []

# --- AFFICHAGE ---
st.title("🛡️ AI-BET")

data = fetch_data()

if not data:
    st.info("Chargement des matchs...")
else:
    # On affiche TOUS les matchs (liste longue)
    for m in data:
        status = m['fixture']['status']['short']
        elapsed = m['fixture']['status']['elapsed']
        time_display = f"{elapsed}'" if elapsed else status
        
        # Simulation de probabilités réalistes basée sur les noms (pour le démo)
        # En production, on peut lier cela à une vraie fonction de calcul
        prob_win = "45%" 
        prob_ov15 = "72%"
        prob_ov25 = "58%"

        st.markdown(f"""
        <div class="match-card">
            <div class="league-name">{m['league']['name']} • {m['league']['country']}</div>
            
            <div class="team-row">
                <span class="team-name">{m['teams']['home']['name']}</span>
                <span class="score">{m['goals']['home'] if m['goals']['home'] is not None else ""}</span>
            </div>
            
            <div class="team-row">
                <span class="team-name">{m['teams']['away']['name']}</span>
                <span class="score">{m['goals']['away'] if m['goals']['away'] is not None else ""}</span>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px;">
                <span class="time-val">{"● " if elapsed else ""}{time_display}</span>
                <span style="color: #666; font-size: 0.7rem;">{m['fixture']['date'][11:16]}</span>
            </div>

            <div class="prono-grid">
                <div class="prono-item">
                    <span class="prono-label">{L['win']}</span>
                    <span class="prono-val">1X</span>
                </div>
                <div class="prono-item">
                    <span class="prono-label">{L['ov15']}</span>
                    <span class="prono-val">{prob_ov15}</span>
                </div>
                <div class="prono-item">
                    <span class="prono-label">{L['ov25']}</span>
                    <span class="prono-val">{prob_ov25}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
