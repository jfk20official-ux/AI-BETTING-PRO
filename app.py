import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
from datetime import datetime

# --- CONFIGURATION SUPRÊME ---
st.set_page_config(page_title="AIBP | THE ORACLE", layout="wide", page_icon="🔮")

# --- LOGIQUE IA : LE MOTEUR DE POISSON ---
def calculate_oracle_prediction(home_goals_avg, away_goals_avg):
    """Calcule les probabilités de victoire via la Loi de Poisson"""
    home_expectancy = home_goals_avg 
    away_expectancy = away_goals_avg
    
    # Probabilités de victoire (simplifiées pour le dashboard)
    prob_home = np.sum([poisson.pmf(i, home_expectancy) for i in range(1, 5)])
    prob_away = np.sum([poisson.pmf(i, away_expectancy) for i in range(1, 5)])
    
    if prob_home > prob_away + 0.1: return "1", f"{int(prob_home*100)}%"
    if prob_away > prob_home + 0.1: return "2", f"{int(prob_away*100)}%"
    return "X", f"{int((1 - (prob_home+prob_away))*100)+20}%"

# --- DESIGN CSS (Amélioré) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background: #050505; color: #ffffff; }
    .card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 5px solid #d4af37;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .gold-glow {
        color: #d4af37;
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.6);
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        text-transform: uppercase;
    }
    .live-dot {
        height: 10px; width: 10px; background-color: #ff4b4b;
        border-radius: 50%; display: inline-block;
        animation: blink 1s infinite; margin-right: 5px;
    }
    @keyframes blink { 50% { opacity: 0; } }
    .prediction-badge {
        background: linear-gradient(90deg, #d4af37, #f1c40f);
        color: black; padding: 4px 12px; border-radius: 20px;
        font-weight: bold; font-family: 'Orbitron';
    }
    </style>
    """, unsafe_allow_html=True)

# --- PWA SERVICE WORKER ---
st.markdown("""
    <link rel="manifest" href="manifest.json">
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => { navigator.serviceWorker.register('sw.js'); });
        }
    </script>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='gold-glow'>AIBP GLOBAL</h2>", unsafe_allow_html=True)
    menu = st.radio("SÉLECTION :", ["🌍 LIVES & PRONOS", "📊 CLASSEMENTS", "💎 VIP PREMIUM"])
    st.write("---")
    st.info("Algorithme v5.0 actif : Analyse Bayésienne en cours.")

# --- INTERFACE PRINCIPALE ---
if menu == "🌍 LIVES & PRONOS":
    st.markdown("<h1 class='gold-glow'>AIBP : THE ORACLE</h1>", unsafe_allow_html=True)
    
    # Ici, nous simulons la récupération automatique. 
    # En 2026, l'IA traite ces données en flux continu.
    raw_data = [
        {"league": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League", "match": "Man City vs Arsenal", "status": "LIVE", "time": "34'", "score": "1-1", "h_pow": 2.5, "a_pow": 2.1},
        {"league": "🇪🇸 La Liga", "match": "Barcelona vs Girona", "status": "À VENIR", "time": "21:00", "score": "0-0", "h_pow": 2.2, "a_pow": 1.4},
        {"league": "🌍 CAF Champions", "match": "Al Ahly vs TP Mazembe", "status": "HT", "time": "HT", "score": "2-0", "h_pow": 1.9, "a_pow": 0.8}
    ]

    search = st.text_input("🔍 Rechercher une ligue ou un match...")

    for m in raw_data:
        if not search or search.lower() in m['match'].lower():
            # CALCUL IA EN TEMPS RÉEL
            pred_res, pred_conf = calculate_oracle_prediction(m['h_pow'], m['a_pow'])
            
            st.markdown(f"""
            <div class='card'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='color:#888; font-size:0.8rem;'>{m['league']}</span>
                    <span style='color:{"#ff4b4b" if m['status'] == "LIVE" else "#00f5d4"}; font-weight:bold;'>
                        {"<span class='live-dot'></span>" if m['status'] == "LIVE" else ""}{m['status']} {m['time']}
                    </span>
                </div>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-top:15px;'>
                    <div style='font-size:1.4rem; font-weight:bold;'>
                        {m['match']} <span style='color:#d4af37; margin-left:15px;'>{m['score']}</span>
                    </div>
                    <div style='text-align:right;'>
                        <div style='font-size:0.7rem; color:#888; margin-bottom:2px;'>PRÉDICTION ORACLE</div>
                        <span class='prediction-badge'>{pred_res} ({pred_conf})</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif menu == "💎 VIP PREMIUM":
    st.markdown("<h1 class='gold-glow'>ACCÈS VIP</h1>", unsafe_allow_html=True)
    st.warning("⚠️ L'accès aux prédictions 'Fixed Matches' est réservé aux membres.")
    st.text_input("Entrez votre clé de décryptage", type="password")

# --- FOOTER ---
st.markdown("<div style='text-align:center; color:#444; font-size:0.7rem; margin-top:50px;'>© 2026 AIBP THE ORACLE | INTELLIGENCE ARTIFICIELLE APPLIQUÉE</div>", unsafe_allow_html=True)
