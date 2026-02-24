import streamlit as st
import requests
import random
import string
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BETTING-PRO", layout="wide")

# --- ACTUALISATION AUTO (15 secondes) ---
st_autorefresh(interval=15 * 1000, key="livescore_update")

# --- PARAMÈTRES ET CLÉS ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
PWD_ADMIN = "Tunga25721204301"

# --- INITIALISATION DE LA MÉMOIRE ---
if 'pronos' not in st.session_state:
    st.session_state.pronos = {"gratuit": {}, "vip": {}, "promo": {}}
if 'gen_code' not in st.session_state:
    st.session_state.gen_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
if 'auth_vip' not in st.session_state:
    st.session_state.auth_vip = False

# --- STYLE TYPE "LIVESCORE" & "FOREBET" ---
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F8; color: #333; }
    .match-row { 
        background: white; padding: 12px; border-bottom: 1px solid #eee; 
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 2px;
    }
    .time-col { color: #E74C3C; font-weight: bold; width: 60px; font-size: 14px; text-align: center; }
    .team-name { font-weight: 500; color: #111; width: 35%; }
    .score-box { background: #333; color: #D4AF37; padding: 5px 12px; border-radius: 5px; font-weight: bold; font-size: 18px; }
    .vip-banner { background: #D4AF37; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; font-weight: bold; font-size: 20px; cursor: pointer; }
    .prono-card { background: white; border-left: 5px solid #28a745; padding: 10px; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTION API ---
def fetch_live_data():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        res = requests.get(url, headers=headers, timeout=5).json().get('response', [])
        # Trier par temps écoulé
        return sorted(res, key=lambda x: x['fixture']['status']['elapsed'] or 0, reverse=True)
    except: return []

# --- NAVIGATION ---
st.sidebar.title("💎 AI-BETTING-PRO")
menu = st.sidebar.radio("Navigation", ["⚽ LiveScore & Gratuit", "🔐 Espace VIP / Promo", "🛠️ Administration"])

# --- 1. PAGE ACCUEIL : LIVESCORE & GRATUIT ---
if menu == "⚽ LiveScore & Gratuit":
    st.title("🔴 LiveScore - En Direct")
    
    # Section Pronostics Gratuits (En haut pour la visibilité)
    if st.session_state.pronos['gratuit']:
        st.subheader("💡 Pronos Gratuits de l'Oracle")
        for k, p in st.session_state.pronos['gratuit'].items():
            st.markdown(f"<div class='prono-card'><b>{p['match']}</b> | Pronostic : <span style='color:green;'>{p['prono']}</span> | Cote: {p['cote']}</div>", unsafe_allow_html=True)

    st.write("---")
    
    # Affichage des scores live (Style ligne par ligne)
    lives = fetch_live_data()
    if lives:
        for m in lives:
            time = m['fixture']['status']['elapsed']
            home = m['teams']['home']['name']
            away = m['teams']['away']['name']
            sh = m['goals']['home']
            sa = m['goals']['away']
            st.markdown(f"""
            <div class="match-row">
                <div class="time-col">{time}'</div>
                <div class="team-name" style="text-align:right;">{home}</div>
                <div class="score-box">{sh} - {sa}</div>
                <div class="team-name">{away}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucun match en direct pour le moment. Revenez lors des prochains coups d'envoi !")

# --- 2. ESPACE VIP / PROMO ---
elif menu == "🔐 Espace VIP / Promo":
    st.title("💎 Zone Privée")
    
    if not st.session_state.auth_vip:
        st.markdown(f"""<div class="vip-banner">CODE D'ACCÈS ACTUEL : {st.session_state.gen_code}</div>""", unsafe_allow_html=True)
        st.info("Copiez le code ci-dessus et validez pour entrer.")
        input_code = st.text_input("Saisissez le code :")
        if input_code == st.session_state.gen_code:
            st.session_state.auth_vip = True
            st.rerun()
    else:
        tab1, tab2 = st.tabs(["🏆 PRONOSTICS VIP", "🎁 BONUS CODE Jfk20"])
        with tab1:
            if not st.session_state.pronos['vip']: st.write("Analyse en cours par l'Oracle...")
            for k, v in st.session_state.pronos['vip'].items():
                st.markdown(f"<div class='prono-card' style='border-left-color: gold;'><h3>{v['match']}</h3><b>PRONO : {v['prono']}</b><br>Cote : {v['cote']}</div>", unsafe_allow_html=True)
        with tab2:
            st.write("Section réservée aux affiliés **1xBet** avec le code promo **Jfk20**.")
            for k, v in st.session_state.pronos['promo'].items():
                st.markdown(f"<div class='prono-card' style='border-left-color: blue;'><h3>{v['match']}</h3><b>PRONO : {v['prono']}</b></div>", unsafe_allow_html=True)

# --- 3. ADMINISTRATION ---
elif menu == "🛠️ Administration":
    pwd = st.text_input("Mot de passe Maître", type="password")
    if pwd == PWD_ADMIN:
        st.success("Accès Admin Accordé")
        
        # Bouton pour générer un nouveau code IA
        if st.button("🔄 GÉNÉRER UN NOUVEAU CODE VIP"):
            st.session_state.gen_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            st.success(f"Nouveau code généré : {st.session_state.gen_code}")
            st.rerun()
            
        with st.form("add_prono"):
            cat = st.selectbox("Choisir la Catégorie", ["gratuit", "vip", "promo"])
            m_nom = st.text_input("Nom du Match")
            m_prono = st.text_input("Pronostic")
            m_cote = st.text_input("Cote")
            if st.form_submit_button("PUBLIER LE MATCH"):
                st.session_state.pronos[cat][m_nom] = {"match": m_nom, "prono": m_prono, "cote": m_cote}
                st.success(f"Match ajouté dans {cat}")

        if st.button("🗑️ TOUT EFFACER"):
            st.session_state.pronos = {"gratuit": {}, "vip": {}, "promo": {}}
            st.rerun()

st.sidebar.write("---")
st.sidebar.caption("AI-BETTING-PRO v6.0")
