import streamlit as st
import requests
from datetime import datetime
import numpy as np
from scipy.stats import poisson
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BET GLOBAL", layout="wide")
tz = pytz.timezone("Africa/Bujumbura")

# --- GESTION DES LANGUES ---
LANGUAGES = {
    "Français": {"title": "PRONOSTICS IA", "live": "EN DIRECT", "advice": "Conseil", "minutes": "Min", "admin": "Admin"},
    "English": {"title": "AI PREDICTIONS", "live": "LIVE", "advice": "Advice", "minutes": "Min", "admin": "Admin"},
    "Español": {"title": "PREDICCIONES IA", "live": "EN VIVO", "advice": "Consejo", "minutes": "Min", "admin": "Admin"},
    "Português": {"title": "PREVISÕES IA", "live": "AO VIVO", "advice": "Conselho", "minutes": "Min", "admin": "Admin"},
    "Deutsch": {"title": "KI-PROGNOSEN", "live": "LIVE", "advice": "Rat", "minutes": "Min", "admin": "Admin"},
    "中文 (Chinois)": {"title": "人工智能预测", "live": "直播", "advice": "建议", "minutes": "分", "admin": "管理"},
    "العربية (Arabe)": {"title": "توقعات الذكاء الاصطناعي", "live": "مباشر", "advice": "نصيحة", "minutes": "دقيقة", "admin": "إشراف"},
    "हिन्दी (Hindi)": {"title": "AI भविष्यवाणियाँ", "live": "लाइव", "advice": "सलाह", "minutes": "मिनट", "admin": "प्रशासन"},
    "Kiswahili": {"title": "UTABIRI WA AI", "live": "MUBASHARA", "advice": "Ushauri", "minutes": "Dakika", "admin": "Usimamizi"}
}

# Sélection de la langue dans la sidebar
selected_lang = st.sidebar.selectbox("🌐 Language / Lugha", list(LANGUAGES.keys()))
L = LANGUAGES[selected_lang]

# --- STYLE CSS (Rectangles 75% et Design Compact) ---
st.markdown(f"""
<style>
    .match-container {{
        width: 75%; /* Rectangle réduit à 3/4 */
        margin: auto;
        background: #1a1c23;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 8px;
        border-left: 4px solid #00ff88;
    }}
    .time-badge {{
        background: #ff4b4b;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: bold;
    }}
    .score-live {{ color: #00ff88; font-size: 1.2rem; font-weight: bold; }}
    .prediction-row {{ font-size: 0.8rem; color: #888; margin-top: 5px; }}
</style>
""", unsafe_allow_html=True)

# --- FONCTION PRÉDICTION ---
def calculate_ai_probs():
    return {"1X2": ["45%", "25%", "30%"], "O25": "62%", "Advice": "1X & Over 1.5"}

# --- ONGLET ADMIN ---
def admin_panel():
    st.subheader(f"🔐 {L['admin']} Panel")
    pwd = st.text_input("Password", type="password")
    if pwd == "Tunga257": # Ton mot de passe
        st.success("Accès autorisé")
        st.write("Statistiques des clés API :")
        st.progress(85, text="Quota API-Football (85/100)")
        st.button("Forcer rafraîchissement des scores")
    elif pwd != "":
        st.error("Mot de passe incorrect")

# --- MAIN APP ---
tab1, tab2, tab3, tab4 = st.tabs(["⚽ Football", "🏀 Basket", "📺 Vidéos", f"⚙️ {L['admin']}"])

with tab1:
    st.title(L['title'])
    
    # Simulation de données (à remplacer par ton fetch_all_football)
    matches = [
        {"h": "Arsenal", "a": "Chelsea", "sh": 2, "sa": 1, "min": "72'", "league": "Premier League"},
        {"h": "Real Madrid", "a": "Barcelone", "sh": 0, "sa": 0, "min": "15'", "league": "La Liga"}
    ]

    for m in matches:
        p = calculate_ai_probs()
        st.markdown(f"""
        <div class="match-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.7rem; color: #666;">{m['league']}</span>
                <span class="time-badge">{m['min']} {L['minutes']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top:5px;">
                <div style="flex:1; text-align:right; font-weight:bold;">{m['h']}</div>
                <div style="flex:0.4; text-align:center;" class="score-live">{m['sh']} - {m['sa']}</div>
                <div style="flex:1; text-align:left; font-weight:bold;">{m['a']}</div>
            </div>
            <div class="prediction-row">
                📊 1X2: {p['1X2'][0]} | {p['1X2'][1]} | {p['1X2'][2]} • Over 2.5: {p['O25']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"💡 {L['advice']}"):
            st.write(f"**Analyse IA:** {p['Advice']}")

with tab4:
    admin_panel()
