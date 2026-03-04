import streamlit as st
import requests
from datetime import datetime
import pytz

# ====================== CONFIGURATION ======================
tz = pytz.timezone("Africa/Bujumbura")
date_str = datetime.now(tz).strftime("%Y-%m-%d")

# Tes Clés API
API_FOOTBALL_KEY = "80da65258a3809f6c7ad2c74930ceb90"
FOOTBALL_DATA_KEY = "A6ef05d939bb4da9acae3d8de8c47c8c"

st.set_page_config(page_title="AI-BET MULTI-SPORTS", layout="wide")

# ====================== FONCTIONS DE RÉCUPÉRATION ======================

def fetch_foot_api_sports():
    """Source 1: API-Football (RapidAPI)"""
    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
    headers = {"x-rapidapi-key": API_FOOTBALL_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        r = requests.get(url, headers=headers, timeout=5).json()
        return r.get("response", [])
    except: return None

def fetch_foot_data_org():
    """Source 2: Football-Data.org (Clé A6ef05...)"""
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": FOOTBALL_DATA_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=5).json()
        return r.get("matches", [])
    except: return None

def fetch_scorebat_videos():
    """Source Vidéo: ScoreBat (Gratuit)"""
    try:
        return requests.get("https://www.scorebat.com/video-api/v3/", timeout=5).json().get("response", [])
    except: return []

# ====================== INTERFACE UTILISATEUR ======================

st.title("⚽ AI-BET Premium : Foot, Basket & Tennis")

# Création des onglets
tabs = st.tabs(["⚽ Football", "🏀 Basketball", "🎾 Tennis", "📺 Résumés Vidéo"])

# --- ONGLET 1 : FOOTBALL (AVEC FALLBACK) ---
with tabs[0]:
    st.subheader("Matchs de Football")
    
    # Stratégie de cascade
    data = fetch_foot_api_sports()
    source = "API-Football"
    
    if not data:
        st.warning("API-Football saturée... Passage sur Football-Data.org")
        data = fetch_foot_data_org()
        source = "Football-Data.org"
        
    if data:
        st.caption(f"Données fournies par : {source}")
        for m in data[:20]:
            if source == "API-Football":
                h, a = m['teams']['home']['name'], m['teams']['away']['name']
                score = f"{m['goals']['home'] or 0} - {m['goals']['away'] or 0}"
                status = m['fixture']['status']['short']
            else:
                h, a = m['homeTeam']['name'], m['awayTeam']['name']
                score = f"{m['score']['fullTime']['home'] or 0} - {m['score']['fullTime']['away'] or 0}"
                status = m['status']
            
            st.markdown(f"**{h}** `{score}`  **{a}** *({status})*")
    else:
        st.error("Aucune donnée disponible. Vérifiez vos quotas API.")

# --- ONGLET 2 : BASKETBALL (PRÉPARATION) ---
with tabs[1]:
    st.subheader("🏀 Basketball (NBA, Euroleague)")
    st.info("Configuration de l'API Basketball en cours... Utilisez votre clé RapidAPI pour ce module.")
    # Ici, tu pourras copier la structure fetch_foot_api_sports avec l'URL basket

# --- ONGLET 3 : TENNIS (PRÉPARATION) ---
with tabs[2]:
    st.subheader("🎾 Tennis (ATP, WTA)")
    st.info("Le module Tennis sera activé après validation du module Football.")

# --- ONGLET 4 : VIDÉOS ---
with tabs[3]:
    st.subheader("📺 Derniers buts en vidéo")
    videos = fetch_scorebat_videos()
    if videos:
        for v in videos[:10]:
            with st.expander(f"🎥 {v['title']}"):
                st.video(v['matchviewUrl'])
    else:
        st.write("Pas de vidéos disponibles pour le moment.")

# ====================== DESIGN SIDEBAR ======================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3588/3588658.png", width=100)
    st.header("Paramètres")
    st.write(f"📅 Date : {date_str}")
    st.write(f"🌍 Zone : {tz.zone}")
    st.divider()
    st.write("💡 *L'application bascule automatiquement entre les sources en cas de saturation.*")
