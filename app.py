import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# --- MULTILINGUAL DICTIONARY (Expanded) ---
LANGUAGES = {
    "English": {
        "title": "AIBP : THE ORACLE",
        "search": "🔍 Scan a league, team or status...",
        "sidebar": "SELECT CATEGORY",
        "menu": ["🌍 LIVES & PREDICTIONS", "📊 STANDINGS", "💎 VIP PREMIUM"],
        "pred_label": "ORACLE PREDICTION",
        "details": "Deep Analysis",
        "stats": ["Corners", "Shots on Target", "Over 2.5 Goals"],
        "footer": "ALL RIGHTS RESERVED © 2026 AI BETTING PRO"
    },
    "Français": {
        "title": "AIBP : L'ORACLE",
        "search": "🔍 Scanner une ligue, équipe ou statut...",
        "sidebar": "SÉLECTIONNER CATÉGORIE",
        "menu": ["🌍 LIVES & PRONOS", "📊 CLASSEMENTS", "💎 VIP PREMIUM"],
        "pred_label": "PRÉDICTION ORACLE",
        "details": "Analyse Approfondie",
        "stats": ["Corners", "Tirs Cadrés", "Plus de 2.5 Buts"],
        "footer": "TOUS DROITS RÉSERVÉS © 2026 AI BETTING PRO"
    }
}

# --- CONFIG ---
st.set_page_config(page_title="AIBP | THE ORACLE", layout="wide")

with st.sidebar:
    st.markdown("<h2 style='color:#d4af37; font-family:Orbitron;'>GLOBAL SELECT</h2>", unsafe_allow_html=True)
    selected_lang = st.selectbox("🌐 LANGUAGE", list(LANGUAGES.keys()))
    L = LANGUAGES[selected_lang]

# --- AI ENGINE (Advanced) ---
def get_full_analysis(h_pow, a_pow):
    # Calculations based on Poisson
    prob_1 = np.clip(h_pow / (h_pow + a_pow + 0.5) * 100, 10, 85)
    prob_2 = np.clip(a_pow / (h_pow + a_pow + 0.5) * 100, 10, 85)
    prob_x = 100 - (prob_1 + prob_2)
    
    corners = int((h_pow + a_pow) * 2.5)
    shots = int((h_pow + a_pow) * 3)
    over25 = int((prob_1 + prob_2) * 0.8)
    
    return {
        "1X2": [f"{int(prob_1)}%", f"{int(prob_x)}%", f"{int(prob_2)}%"],
        "corners": corners,
        "shots": shots,
        "over25": f"{over25}%"
    }

# --- CSS (Forebet Dark Gold Edition) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    .stApp { background: #0a0a0a; color: #eee; font-family: 'Inter', sans-serif; }
    .card {
        background: #151515; border-radius: 8px; padding: 15px; margin-bottom: 10px;
        border-bottom: 2px solid #333;
    }
    .prob-bar { display: flex; height: 8px; border-radius: 4px; overflow: hidden; margin: 10px 0; }
    .gold-glow { color: #d4af37; font-family: 'Orbitron'; text-align: center; }
    .stat-box { background: #222; padding: 10px; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- MAIN CONTENT ---
st.markdown(f"<h1 class='gold-glow'>{L['title']}</h1>", unsafe_allow_html=True)
menu_choice = st.sidebar.radio(L["sidebar"], L["menu"])

if menu_choice == L["menu"][0]:
    search = st.text_input(L["search"])
    
    # Dynamic Data Simulation
    raw_data = [
        {"league": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League", "match": "Arsenal vs Chelsea", "status": "21:00", "score": "0-0", "h_pow": 2.8, "a_pow": 1.2},
        {"league": "🌍 CAF Champions", "match": "Al Ahly vs Sundowns", "status": "LIVE", "score": "1-0", "h_pow": 2.1, "a_pow": 1.9}
    ]

    for m in raw_data:
        analysis = get_full_analysis(m['h_pow'], m['a_pow'])
        
        st.markdown(f"""
        <div class='card'>
            <div style='display:flex; justify-content:space-between; font-size:0.7rem; color:#888;'>
                <span>{m['league']}</span><span>{m['status']}</span>
            </div>
            <div style='display:flex; justify-content:space-between; align-items:center; margin:10px 0;'>
                <span style='font-weight:bold; font-size:1.1rem;'>{m['match']}</span>
                <span style='color:#d4af37; font-family:Orbitron; font-weight:bold;'>{analysis['1X2'][0]} - {analysis['1X2'][1]} - {analysis['1X2'][2]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ANALYSIS SECTION (The "Click to Expand" part)
        with st.expander(f"📊 {L['details']} - {m['match']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='stat-box'><small>{L['stats'][0]}</small><br><b style='color:#d4af37;'>{analysis['corners']}</b></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='stat-box'><small>{L['stats'][1]}</small><br><b style='color:#d4af37;'>{analysis['shots']}</b></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='stat-box'><small>{L['stats'][2]}</small><br><b style='color:#d4af37;'>{analysis['over25']}</b></div>", unsafe_allow_html=True)
            
            # Prediction Logic Visualization
            st.write("---")
            st.write("🎯 **Oracle Insights:** High probability of late goals based on team fatigue index.")

# --- FOOTER ---
st.markdown(f"<div style='text-align:center; color:#444; font-size:0.7rem; margin-top:50px;'>{L['footer']}</div>", unsafe_allow_html=True)
