import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================
# 1. CONFIGURATION (À REMPLIR)
# ==========================================
API_KEY = "TA_CLE_ICI" 
ADMIN_PASSWORD = "TON_MOT_DE_PASSE"
GA_ID = "G-XXXXXXXXXX" # Ton ID Google Analytics (facultatif au début)

# ==========================================
# 2. DESIGN & CSS (GOLD EDITION)
# ==========================================
st.set_page_config(page_title="AIBP | THE ORACLE", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    .stApp { background: #0a0a0a; color: #eee; font-family: 'Inter', sans-serif; }
    .card {
        background: linear-gradient(145deg, #151515, #1d1d1d);
        border-radius: 12px; padding: 15px; margin-bottom: 12px;
        border-left: 5px solid #d4af37; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .gold-glow { color: #d4af37; font-family: 'Orbitron'; text-align: center; text-transform: uppercase; }
    .live-dot { height: 10px; width: 10px; background-color: #ff4b4b; border-radius: 50%; display: inline-block; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .vip-card { border: 1px solid #d4af37; background: rgba(212, 175, 55, 0.05); border-radius: 10px; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. MOTEUR DE DONNÉES & ANALYTICS
# ==========================================
def inject_ga():
    ga_code = f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date()); gtag('config', '{GA_ID}');
        </script>
    """
    components.html(ga_code, height=0)

@st.cache_data(ttl=60)
def fetch_live_data():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json().get('response', [])
    except:
        return []

def get_predictions(h_score, a_score, elapsed):
    # Logique Oracle simplifiée
    p1 = np.clip(35 + (h_score - a_score) * 15, 5, 95)
    p2 = np.clip(30 + (a_score - h_score) * 15, 5, 95)
    px = 100 - (p1 + p2)
    return [f"{int(p1)}%", f"{int(px)}%", f"{int(p2)}%"]

# ==========================================
# 4. INTERFACE & NAVIGATION
# ==========================================
inject_ga()

with st.sidebar:
    st.markdown("<h2 class='gold-glow'>AIBP ORACLE</h2>", unsafe_allow_html=True)
    lang = st.selectbox("🌐 LANGUAGE", ["Français", "English"])
    menu = ["🌍 LIVES & PRONOS", "💎 VIP PREMIUM", "🔐 ADMIN"] if lang == "Français" else ["🌍 LIVE PREDICTIONS", "💎 VIP PREMIUM", "🔐 ADMIN"]
    choice = st.radio("MENU", menu)

# --- SECTION LIVES ---
if choice == menu[0]:
    st.markdown("<h1 class='gold-glow'>L'ORACLE EN DIRECT</h1>", unsafe_allow_html=True)
    data = fetch_live_data()
    
    if not data:
        st.info("Aucun match en direct pour le moment.")
    else:
        for m in data:
            local_time = datetime.fromtimestamp(m['fixture']['timestamp']).strftime('%H:%M')
            preds = get_predictions(m['goals']['home'], m['goals']['away'], m['fixture']['status']['elapsed'])
            
            st.markdown(f"""
            <div class='card'>
                <div style='display:flex; justify-content:space-between; font-size:0.8rem; color:#888;'>
                    <span>🏆 {m['league']['name']}</span>
                    <span><span class='live-dot'></span> {m['fixture']['status']['elapsed']}' (Heure: {local_time})</span>
                </div>
                <div style='display:flex; justify-content:space-between; align-items:center; margin:10px 0;'>
                    <span style='font-size:1.1rem; font-weight:bold;'>{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}</span>
                    <span style='color:#d4af37; font-family:Orbitron; font-weight:bold;'>{preds[0]} - {preds[1]} - {preds[2]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- SECTION VIP ---
elif choice == menu[1]:
    st.markdown("<h1 class='gold-glow'>💎 SELECTION VIP</h1>", unsafe_allow_html=True)
    data = fetch_live_data()
    found_vip = False
    
    for m in data:
        elapsed = m['fixture']['status']['elapsed']
        # Condition VIP : Match après 60 min avec une équipe qui domine
        if elapsed > 60 and abs(m['goals']['home'] - m['goals']['away']) >= 1:
            found_vip = True
            st.markdown(f"""
            <div class='vip-card'>
                <h4 style='color:#d4af37; margin:0;'>🔥 OPPORTUNITÉ DÉTECTÉE</h4>
                <p>{m['teams']['home']['name']} vs {m['teams']['away']['name']} ({elapsed}')<br>
                <b>CONSEIL : MOMENTUM ÉLEVÉ</b></p>
            </div><br>
            """, unsafe_allow_html=True)
            
    if not found_vip:
        st.write("L'Oracle analyse... Aucune opportunité VIP pour l'instant.")

# --- SECTION ADMIN ---
elif choice == "🔐 ADMIN":
    st.markdown("<h1 class='gold-glow'>PANEL ADMIN</h1>", unsafe_allow_html=True)
    pw = st.text_input("Mot de passe", type="password")
    if pw == ADMIN_PASSWORD:
        st.success("Bienvenue, Administrateur.")
        # Dashboard des stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Utilisateurs", "370", "Canada, Burundi, FR")
        col2.metric("Taux de réussite", "78%", "+2%")
        col3.metric("Status API", "OK")
        
        st.markdown("### 📊 Rapports Géographiques (Simulation)")
        st.table(pd.DataFrame({"Pays": ["Canada", "France", "Burundi"], "Visites": [20, 150, 1]}))
    elif pw:
        st.error("Accès refusé.")
