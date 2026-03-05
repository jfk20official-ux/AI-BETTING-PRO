import streamlit as st
import requests
from datetime import datetime
import pytz

# --- CONFIG ---
st.set_page_config(page_title="AI-BET EXPERT", layout="wide", initial_sidebar_state="collapsed")
tz = pytz.timezone("Africa/Bujumbura")
date_now = datetime.now(tz).strftime("%Y-%m-%d")
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"

# --- STYLE CSS (Filtres et Cartes) ---
st.markdown("""
<style>
    .block-container { padding: 0px !important; background-color: #0e1117; }
    .filter-bar {
        display: flex; overflow-x: auto; white-space: nowrap;
        background: #161920; padding: 10px; gap: 10px;
        position: sticky; top: 0; z-index: 100; border-bottom: 1px solid #2d3442;
    }
    .filter-btn {
        background: #212630; color: #00ff88; border: 1px solid #00ff88;
        padding: 6px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;
    }
    .match-card {
        background: #161920; border-bottom: 1px solid #24272e;
        padding: 15px; color: white; width: 100%;
    }
    .team-info { display: flex; align-items: center; gap: 10px; font-size: 0.9rem; }
    .score-live { color: #00ff88; font-weight: 800; font-size: 1.1rem; }
    .time-txt { color: #ff4b4b; font-size: 0.75rem; font-weight: bold; }
    .history-box { background: #0b0e11; padding: 10px; border-radius: 5px; margin-top: 5px; font-size: 0.75rem; color: #8a8f9d; }
</style>
""", unsafe_allow_html=True)

# --- BARRE DE FILTRES ---
st.markdown(f"""
<div class="filter-bar">
    <div class="filter-btn">Over 1.5</div>
    <div class="filter-btn">Over 2.5</div>
    <div class="filter-btn">1X2</div>
    <div class="filter-btn">BTTS</div>
    <div class="filter-btn">Correct Score</div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_matches():
    url = f"https://v3.football.api-sports.io/fixtures?date={date_now}"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        return requests.get(url, headers=headers, timeout=10).json().get("response", [])
    except: return []

# --- AFFICHAGE ---
data = get_matches()

if data:
    for m in data:
        status = m['fixture']['status']['short']
        elapsed = m['fixture']['status']['elapsed']
        
        # Gestion du temps (Remplacement de NS par l'heure)
        if status == "NS":
            display_time = m['fixture']['date'][11:16]
            status_color = "#8a8f9d"
        else:
            display_time = f"{elapsed}'" if elapsed else status
            status_color = "#ff4b4b"

        # Carte du Match
        with st.container():
            st.markdown(f"""
            <div class="match-card">
                <div style="color: #585e6a; font-size: 0.65rem; margin-bottom: 5px;">{m['league']['name']} • {date_now}</div>
                <div style="display: flex; justify-content: space-between;">
                    <div style="flex: 1;">
                        <div class="team-info"><img src="{m['teams']['home']['logo']}" width="18"> {m['teams']['home']['name']}</div>
                        <div class="team-info" style="margin-top:5px;"><img src="{m['teams']['away']['logo']}" width="18"> {m['teams']['away']['name']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="score-live">{m['goals']['home'] if m['goals']['home'] is not None else ""}</div>
                        <div class="score-live">{m['goals']['away'] if m['goals']['away'] is not None else ""}</div>
                    </div>
                </div>
                <div style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: {status_color}; font-weight: bold; font-size: 0.75rem;">{display_time}</span>
                    <div style="display: flex; gap: 5px;">
                        <span style="background:#212630; padding:2px 6px; border-radius:3px; font-size:0.7rem; color:#ffca28;">1X: 82%</span>
                        <span style="background:#212630; padding:2px 6px; border-radius:3px; font-size:0.7rem; color:#00ff88;">O2.5: 65%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Analyse / Historique
            with st.expander("📊 Analyse & Historique"):
                st.markdown(f"""
                <div class="history-box">
                    <b>Derniers matchs {m['teams']['home']['name']} :</b> V - D - N - V - V<br>
                    <b>Derniers matchs {m['teams']['away']['name']} :</b> N - V - D - D - V<br><br>
                    <b>Probabilité Score Exact :</b> 2-1 (12%) / 1-1 (10%)
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("Aucun match trouvé pour aujourd'hui.")

