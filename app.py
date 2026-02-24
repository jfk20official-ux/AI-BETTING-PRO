import streamlit as st
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BETTING-PRO", layout="centered")

# --- TES CODES ICI (COLLE À L'INTÉRIEUR DES GUILLEMETS) ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90" 
MDP_ADMIN = "Tunga25721204301"
CODE_VIP = "COLLE_TON_CODE_CLIENT_VIP_ICI"

# --- STYLE CSS (OR ET NOIR) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .match-card { 
        background-color: #1A1C24; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #D4AF37; 
        margin-bottom: 15px;
    }
    h1, h2, h3 { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
st.sidebar.title("💎 MENU")
page = st.sidebar.radio("Navigation", ["Accueil", "Espace VIP", "Admin"])

# --- FONCTION API ---
def get_live_data():
    if "COLLE" in API_KEY or API_KEY == "":
        return None
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.json().get('response', [])
    except:
        return None

# --- LOGIQUE ---
if page == "Accueil":
    st.title("🔮 AI-BETTING-PRO")
    st.write("---")
    st.subheader("Bienvenue dans l'Oracle")
    st.write("Utilisez le menu à gauche pour accéder aux pronostics.")

elif page == "Espace VIP":
    st.title("🏆 PRONOSTICS VIP")
    entree_code = st.text_input("Code d'accès", type="password")
    if entree_code == CODE_VIP:
        st.success("Accès autorisé")
        data = get_live_data()
        if data:
            for m in data:
                st.markdown(f"<div class='match-card'><h4>⚽ {m['teams']['home']['name']} vs {m['teams']['away']['name']}</h4><p>Analyse IA en cours...</p></div>", unsafe_allow_html=True)
        else:
            st.warning("Aucun match en direct pour le moment ou clé API non configurée.")

elif page == "Admin":
    st.title("🔐 ADMINISTRATION")
    pwd = st.text_input("Mot de passe Maître", type="password")
    if pwd == MDP_ADMIN:
        st.success("Connecté")
        st.write("Votre système est opérationnel.")

st.sidebar.write("---")
st.sidebar.caption("AI-BETTING-PRO v2.2")
