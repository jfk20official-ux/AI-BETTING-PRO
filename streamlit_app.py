import streamlit as st
import requests
from datetime import datetime
import pytz

# --- SETUP ---
st.set_page_config(page_title="AI-BET PREMIUM", layout="wide", initial_sidebar_state="collapsed")
tz = pytz.timezone("Africa/Bujumbura")
date_now = datetime.now(tz).strftime("%Y-%m-%d")
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"

# --- STYLE INTERFACE (SofaScore Style) ---
st.markdown("""
<style>
    .block-container { padding: 0rem !important; background-color: #0b0e11; }
    .match-card {
        background: #161920;
        border-bottom: 1px solid #24272e;
        padding: 12px 15px;
        color: white;
    }
    .league-header {
        background: #1f232d;
        padding: 5px 15px;
        font-size: 0.7rem;
        color: #8a8f9d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .team-row { display: flex; align-items: center; margin: 5px 0; justify-content: space-between; }
    .team-info { display: flex; align-items: center; gap: 12px; }
    .team-logo { width: 22px; height: 22px; object-fit: contain; }
    .team-name { font-size: 0.95rem; font-weight: 500; }
    .score { font-size: 1.1rem; font-weight: 700; color: #00ff88; }
    .time-badge { color: #ff4b4b; font-size: 0.8rem; font-weight: bold; margin-right: 10px; }
    
    .bet-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 12px; }
    .bet-box {
        background: #212630;
        border-radius: 6px;
        padding: 8px;
        text-align: center;
        border: 1px solid #2d3442;
    }
    .bet-label { font-size: 0.6rem; color: #8a8f9d; display: block; margin-bottom: 3px; }
    .bet-val { font-size: 0.85rem; font-weight: 700; color: #ffca28; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_data():
    url = f"https://v3.football.api-sports.io/fixtures?date={date_now}"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        return requests.get(url, headers=headers, timeout=10).json().get("response", [])
    except: return []

# --- RENDER ---
data = get_data()

if data:
    current_league = ""
    for m in data:
        # Header de Ligue
        league_name = f"{m['league']['name']} ({m['league']['country']})"
        if league_name != current_league:
            st.markdown(f'<div class="league-header">{league_name}</div>', unsafe_allow_html=True)
            current_league = league_name

        # Data Match
        status = m['fixture']['status']['short']
        elapsed = m['fixture']['status']['elapsed']
        time_ui = f"● {elapsed}'" if status in ['1H','2H'] else status
        
        # Match Card
        st.markdown(f"""
        <div class="match-card">
            <div class="team-row">
                <div class="team-info">
                    <img src="{m['teams']['home']['logo']}" class="team-logo">
                    <span class="team-name">{m['teams']['home']['name']}</span>
                </div>
                <span class="score">{m['goals']['home'] if m['goals']['home'] is not None else ""}</span>
            </div>
            <div class="team-row">
                <div class="team-info">
                    <img src="{m['teams']['away']['logo']}" class="team-logo">
                    <span class="team-name">{m['teams']['away']['name']}</span>
                </div>
                <span class="score">{m['goals']['away'] if m['goals']['away'] is not None else ""}</span>
            </div>
            <div style="margin-top:5px; font-size:0.75rem;">
                <span class="time-badge">{time_ui}</span>
                <span style="color:#585e6a;">{m['fixture']['date'][11:16]}</span>
            </div>
            <div class="bet-grid">
                <div class="bet-box"><span class="bet-label">WIN</span><span class="bet-val">1X</span></div>
                <div class="bet-box"><span class="bet-label">OVER 1.5</span><span class="bet-val">78%</span></div>
                <div class="bet-box"><span class="bet-label">OVER 2.5</span><span class="bet-val">54%</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No live matches available.")




