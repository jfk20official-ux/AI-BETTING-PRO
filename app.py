import streamlit as st
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BETTING-PRO", layout="wide")

# --- PARAMÈTRES DE SÉCURITÉ ET API ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
PWD_ADMIN = "Tunga25721204301"
CODE_VIP = "Jfk20"

# --- STOCKAGE DES PRONOS ---
if 'pronos_publies' not in st.session_state:
    st.session_state.pronos_publies = []

# --- STYLE VISUEL ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .card-client { 
        background: linear-gradient(135deg, #1A1C24 0%, #252833 100%); 
        padding: 20px; border-radius: 15px; 
        border-left: 5px solid #D4AF37; 
        margin-bottom: 20px; 
    }
    .live-indicator { color: #FF4B4B; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTION DE RÉCUPÉRATION API ---
def fetch_live_scores():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json().get('response', [])
    except:
        return []

# --- NAVIGATION ---
st.sidebar.title("💎 AI-BETTING-PRO")
langue = st.sidebar.selectbox("🌐 Langue", ["Français", "English", "Swahili"])
menu = st.sidebar.radio("ALLER VERS :", ["🏠 Accueil", "💎 Espace VIP", "🔐 Admin"])

# --- PAGE ACCUEIL (AVEC SCORES LIVE) ---
if menu == "🏠 Accueil":
    st.title("🔮 AI-BETTING-PRO")
    st.image("https://img.asmedia.epimg.net/resizer/v2/GHSMLRNR75IBFCHWEY4Y73QO2E.jpg?auth=76384f5d52069c944f8087265886915152504620f5c1a704686419062363162b&width=1200", caption="Raphinha vs Mbappé")
    
    st.subheader("🔴 Scores en Direct (API)")
    live_data = fetch_live_scores()
    if live_data:
        for match in live_data[:5]: # Affiche les 5 premiers matchs en direct
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            score_h = match['goals']['home']
            score_a = match['goals']['away']
            st.write(f"⚽ {home} {score_h} - {score_a} {away} (En cours)")
    else:
        st.write("Aucun match en direct pour le moment.")

# --- PAGE VIP ---
elif menu == "💎 Espace VIP":
    st.title("🏆 Zone VIP")
    code = st.text_input("Code Client :", type="password")
    if code == CODE_VIP:
        st.success("Accès Autorisé")
        if not st.session_state.pronos_publies:
            st.info("L'Oracle prépare les prochains gains...")
        else:
            for p in st.session_state.pronos_publies:
                st.markdown(f"""
                <div class="card-client">
                    <h3>⚽ {p['match']}</h3>
                    <p style='color: #D4AF37; font-size: 18px;'><b>PRONO : {p['prono']}</b></p>
                    <p>Cote : {p['cote']} | Confiance : {p['fiab']}%</p>
                </div>
                """, unsafe_allow_html=True)

# --- PAGE ADMIN ---
elif menu == "🔐 Admin":
    st.title("🔐 Panneau de Maître")
    pwd = st.text_input("Mot de passe :", type="password")
    if pwd == PWD_ADMIN:
        st.success(f"Bienvenue, Tunga")
        with st.form("nouveau_prono"):
            m_nom = st.text_input("Match")
            m_prono = st.text_input("Pronostic")
            m_cote = st.text_input("Cote")
            m_fiab = st.slider("Fiabilité %", 0, 100, 95)
            if st.form_submit_button("PUBLIER"):
                st.session_state.pronos_publies.append({"match": m_nom, "prono": m_prono, "cote": m_cote, "fiab": m_fiab})
                st.success("Pronostic envoyé aux clients !")
