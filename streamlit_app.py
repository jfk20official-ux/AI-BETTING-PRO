import streamlit as st
import requests
from datetime import datetime

# --- CONFIGURATION DES SECRETS ---
# Assure-toi que API_FOOTBALL_KEY est bien dans Settings > Secrets sur Streamlit Cloud
API_KEY = st.secrets["API_FOOTBALL_KEY"]
BASE_URL = "https://v3.football.api-sports.io/fixtures"

def fetch_data(params):
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('response', [])
        else:
            st.error(f"Erreur API {response.status_code}: Vérifiez votre clé.")
            return []
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return []

# --- INTERFACE ---
st.title("⚽ AI ScoreCast Pro")

tab_live, tab_pronos, tab_hist = st.tabs(["🔴 LIVE", "📈 PRONOS", "📚 HISTORIQUE"])

with tab_live:
    # On force la récupération de TOUS les matchs en direct
    lives = fetch_data({'live': 'all'})
    
    if lives:
        for match in lives:
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            status = match['fixture']['status']['elapsed']
            score_home = match['goals']['home']
            score_away = match['goals']['away']
            
            st.markdown(f"""
            <div style="border:1px solid #444; padding:10px; border-radius:10px; margin-bottom:10px;">
                <small style="color:red;">● {status}' LIVE</small><br>
                <b>{home}</b> {score_home} - {score_away} <b>{away}</b>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Aucun match en direct actuellement selon l'API.")
        # Petit bouton pour tester si la clé fonctionne
        if st.button("Vérifier la connexion API"):
            test = fetch_data({'next': '1'})
            if test: st.success("La clé API fonctionne ! C'est juste qu'il n'y a pas de match Live.")

with tab_pronos:
    # Récupère les matchs des prochaines 24h
    next_matches = fetch_data({'next': '10'})
    if next_matches:
        for m in next_matches:
            st.write(f"🔮 {m['teams']['home']['name']} vs {m['teams']['away']['name']}")
    else:
        st.info("Aucun prono disponible.")
