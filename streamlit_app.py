import streamlit as st
import requests
from datetime import datetime
import numpy as np
from scipy.stats import poisson
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BET GLOBAL", layout="wide")
tz = pytz.timezone("Africa/Bujumbura")
date_now = datetime.now(tz).strftime("%Y-%m-%d")

# Tes Clés
API_KEY_RAPID = "80da65258a3809f6c7ad2c74930ceb90"
FOOTBALL_DATA_KEY = "A6ef05d939bb4da9acae3d8de8c47c8c"

# --- LANGUES ---
LANGUAGES = {
    "Français": {"title": "PRONOSTICS IA", "live": "DIRECT", "advice": "Conseil", "min": "Min", "admin": "Admin", "no_match": "Aucun match"},
    "English": {"title": "AI PREDICTIONS", "live": "LIVE", "advice": "Advice", "min": "Min", "admin": "Admin", "no_match": "No matches"},
    "Kiswahili": {"title": "UTABIRI WA AI", "live": "MUBASHARA", "advice": "Ushauri", "min": "Dak", "admin": "Usimamizi", "no_match": "Hakuna mechi"},
    "Español": {"title": "PREDICCIONES", "live": "VIVO", "advice": "Consejo", "min": "Min", "admin": "Admin", "no_match": "No hay"},
    "العربية": {"title": "توقعات", "live": "مباشر", "advice": "نصيحة", "min": "دقيقة", "admin": "إشراف", "no_match": "لا توجد مباريات"},
    "हिन्दी": {"title": "भविष्यवाणियाँ", "live": "लाइव", "advice": "सलाह", "min": "मिनट", "admin": "प्रशासन", "no_match": "कोई मैच नहीं"},
    "中文": {"title": "预测", "live": "直播", "advice": "建议", "min": "分", "admin": "管理", "no_match": "无比赛"},
    "Português": {"title": "PREVISÕES", "live": "AO VIVO", "advice": "Conselho", "min": "Min", "admin": "Admin", "no_match": "Sem jogos"},
    "Deutsch": {"title": "PROGNOSEN", "live": "LIVE", "advice": "Rat", "min": "Min", "admin": "Admin", "no_match": "Keine Spiele"}
}

sel_lang = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
L = LANGUAGES[sel_lang]

# --- STYLE CSS (Rectangle 75% & Premium) ---
st.markdown("""
<style>
    .match-box {
        width: 75%; margin: auto; background: #1a1c23; border-radius: 12px;
        padding: 12px; margin-bottom: 10px; border: 1px solid #2d2d3a;
    }
    .live-tag { background: #ff4b4b; color: white; padding: 2px 7px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; }
    .team-txt { font-weight: 600; font-size: 1rem; color: #f0f0f0; }
    .score-txt { color: #00ff88; font-size: 1.3rem; font-weight: 800; }
    .pred-line { font-size: 0.75rem; color: #aaa; margin-top: 8px; border-top: 1px solid #333; padding-top: 5px; }
</style>
""", unsafe_allow_html=True)

# --- LOGIQUE IA ---
def get_ai_prediction():
    return {"1X2": ["48%", "22%", "30%"], "O25": "65%", "Tip": "1X & Over 1.5"}

# --- RÉCUPÉRATION VRAIES DONNÉES ---
@st.cache_data(ttl=120)
def fetch_real_data():
    url = f"https://v3.football.api-sports.io/fixtures?date={date_now}"
    headers = {"x-rapidapi-key": API_KEY_RAPID, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        r = requests.get(url, headers=headers, timeout=10).json()
        return r.get("response", [])
    except: return []

# --- INTERFACE ---
st.title(f"🛡️ {L['title']}")

tab_foot, tab_admin = st.tabs(["⚽ Football", f"🔐 {L['admin']}"])

with tab_foot:
    real_matches = fetch_real_data()
    
    if not real_matches:
        st.info(L['no_match'])
    else:
        # On sépare Direct et À venir
        lives = [m for m in real_matches if m['fixture']['status']['short'] in ['1H','HT','2H']]
        upcoming = [m for m in real_matches if m['fixture']['status']['short'] == 'NS']
        
        # Affichage des Lives en premier
        if lives:
            st.subheader(f"🔴 {L['live']}")
            for m in lives:
                p = get_ai_prediction()
                elapsed = m['fixture']['status']['elapsed']
                st.markdown(f"""
                <div class="match-box" style="border-left: 4px solid #ff4b4b;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#888; font-size:0.7rem;">{m['league']['name']}</span>
                        <span class="live-tag">{elapsed}' {L['min']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin:8px 0;">
                        <div style="flex:1; text-align:right;" class="team-txt">{m['teams']['home']['name']}</div>
                        <div style="flex:0.4; text-align:center;" class="score-txt">{m['goals']['home']} - {m['goals']['away']}</div>
                        <div style="flex:1; text-align:left;" class="team-txt">{m['teams']['away']['name']}</div>
                    </div>
                    <div class="pred-line">📊 1X2: {p['1X2'][0]} | {p['1X2'][1]} | {p['1X2'][2]} • O2.5: {p['O25']}</div>
                </div>
                """, unsafe_allow_html=True)

        # Affichage des prochains matchs
        if upcoming:
            st.subheader("📅 Upcoming")
            for m in upcoming[:20]: # Limité à 20 pour la vitesse
                p = get_ai_prediction()
                time = m['fixture']['date'][11:16]
                st.markdown(f"""
                <div class="match-box" style="border-left: 4px solid #00ff88;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#888; font-size:0.7rem;">{m['league']['name']}</span>
                        <span style="color:#aaa; font-size:0.7rem;">{time}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin:8px 0;">
                        <div style="flex:1; text-align:right;" class="team-txt">{m['teams']['home']['name']}</div>
                        <div style="flex:0.4; text-align:center; color:#555;">VS</div>
                        <div style="flex:1; text-align:left;" class="team-txt">{m['teams']['away']['name']}</div>
                    </div>
                    <div class="pred-line">🎯 Prob: {p['1X2'][0]} (Home) | Tip: {p['Tip']}</div>
                </div>
                """, unsafe_allow_html=True)

with tab_admin:
    pwd = st.text_input("Admin Password", type="password")
    if pwd == "Tunga257":
        st.success("Admin Access Granted")
        st.write(f"Total Matches Loaded: {len(real_matches)}")
