import streamlit as st
import requests
from datetime import datetime
import pytz

# ====================== CONFIGURATION ======================
tz = pytz.timezone("Africa/Bujumbura")
date_str = datetime.now(tz).strftime("%Y-%m-%d")

# Tes Clés
API_KEY_RAPID = "80da65258a3809f6c7ad2c74930ceb90"
FOOTBALL_DATA_KEY = "A6ef05d939bb4da9acae3d8de8c47c8c"

st.set_page_config(page_title="AI-BET MULTI-SPORTS", layout="wide")

# ====================== FONCTIONS DE RÉCUPÉRATION ======================

def fetch_sports_data(sport_type):
    """Récupère Basket ou Tennis via RapidAPI"""
    endpoints = {
        "basket": "https://v1.basketball.api-sports.io/games",
        "tennis": "https://v1.tennis.api-sports.io/fixtures"
    }
    url = endpoints[sport_type]
    headers = {"x-rapidapi-key": API_KEY_RAPID, "x-rapidapi-host": url.split("//")[1].split("/")[0]}
    params = {"date": date_str}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=7).json()
        return r.get("response", [])
    except: return []

def fetch_foot_api_sports():
    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
    headers = {"x-rapidapi-key": API_KEY_RAPID, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        r = requests.get(url, headers=headers, timeout=5).json()
        return r.get("response", [])
    except: return None

def fetch_foot_data_org():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": FOOTBALL_DATA_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=5).json()
        return r.get("matches", [])
    except: return None

# ====================== INTERFACE ======================
st.title("🏆 AI-BET : Multi-Sports Live")

tabs = st.tabs(["⚽ Football", "🏀 Basketball", "🎾 Tennis", "📺 Vidéos"])

# --- ONGLET FOOTBALL ---
with tabs[0]:
    data = fetch_foot_api_sports()
    source = "API-Football"
    if not data:
        data = fetch_foot_data_org()
        source = "Football-Data.org"
    
    if data:
        st.write(f"🟢 Source: {source}")
        for m in data[:15]:
            if source == "API-Football":
                h, a = m['teams']['home']['name'], m['teams']['away']['name']
                score = f"{m['goals']['home'] or 0} - {m['goals']['away'] or 0}"
            else:
                h, a = m['homeTeam']['name'], m['awayTeam']['name']
                score = f"{m['score']['fullTime']['home'] or 0} - {m['score']['fullTime']['away'] or 0}"
            st.write(f"**{h}** `{score}` **{a}**")

# --- ONGLET BASKETBALL ---
with tabs[1]:
    st.subheader("🏀 Matchs de Basket")
    basket_data = fetch_sports_data("basket")
    if basket_data:
        for g in basket_data[:15]:
            h, a = g['teams']['home']['name'], g['teams']['away']['name']
            sh, sa = g['scores']['home']['total'] or 0, g['scores']['away']['total'] or 0
            st.write(f"🏀 **{h}** `{sh} - {sa}` **{a}**")
    else: st.info("Aucun match de basket trouvé ou quota atteint.")

# --- ONGLET TENNIS ---
with tabs[2]:
    st.subheader("🎾 Matchs de Tennis")
    tennis_data = fetch_sports_data("tennis")
    if tennis_data:
        for t in tennis_data[:15]:
            h, a = t['teams']['home']['name'], t['teams']['away']['name']
            st.write(f"🎾 **{h}** vs **{a}**")
    else: st.info("Aucun match de tennis trouvé.")

# --- ONGLET VIDÉOS ---
with tabs[3]:
    st.subheader("📺 Vidéos ScoreBat")
    try:
        videos = requests.get("https://www.scorebat.com/video-api/v3/").json().get("response", [])
        for v in videos[:5]:
            with st.expander(v['title']):
                st.video(v['matchviewUrl'])
    except: st.write("Vidéos indisponibles.")
