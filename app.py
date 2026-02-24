import streamlit as st
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BETTING-PRO", layout="centered")

# --- PARAMÈTRES DE SÉCURITÉ ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90" # Remplace par ta clé
MDP_ADMIN = "Tunga25721204301"
CODE_VIP = "Jfk20"

# --- SYSTÈME DE LANGUES ---
languages = {
    "Français": {
        "welcome": "Bienvenue dans l'Oracle",
        "desc": "L'IA au service de vos paris.",
        "menu": "MENU PRINCIPAL",
        "home": "Accueil",
        "vip": "Espace VIP",
        "admin": "Admin",
        "enter_code": "Entrez votre code d'accès",
        "access_ok": "Accès autorisé",
        "no_match": "Aucun match pour le moment.",
        "pwd_admin": "Mot de passe Maître"
    },
    "English": {
        "welcome": "Welcome to the Oracle",
        "desc": "AI at the service of your bets.",
        "menu": "MAIN MENU",
        "home": "Home",
        "vip": "VIP Space",
        "admin": "Admin",
        "enter_code": "Enter your access code",
        "access_ok": "Access granted",
        "no_match": "No matches at the moment.",
        "pwd_admin": "Master Password"
    },
    "Swahili": {
        "welcome": "Karibu kwenye Oracle",
        "desc": "AI kwa ajili ya ushindi wako.",
        "menu": "MENU KUU",
        "home": "Nyumbani",
        "vip": "Eneo la VIP",
        "admin": "Admin",
        "enter_code": "Weka nambari yako ya siri",
        "access_ok": "Umewezeshwa kuingia",
        "no_match": "Hakuna mechi kwa sasa.",
        "pwd_admin": "Nenosiri la Admin"
    }
}

# Sélecteur de langue dans la barre latérale
lang_choice = st.sidebar.selectbox("🌐 Language / Lugha", ["Français", "English", "Swahili"])
texts = languages[lang_choice]

# --- STYLE CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #FFFFFF; }}
    .match-card {{ background-color: #1A1C24; padding: 20px; border-radius: 15px; border-left: 5px solid #D4AF37; margin-bottom: 15px; }}
    h1, h2, h3 {{ color: #D4AF37 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
st.sidebar.title(f"💎 {texts['menu']}")
page = st.sidebar.radio("", [texts['home'], texts['vip'], texts['admin']])

# --- LOGIQUE ---
if page == texts['home']:
    st.title(f"🔮 AI-BETTING-PRO")
    st.write("---")
    st.subheader(texts['welcome'])
    st.write(texts['desc'])
    
    # Photo de Raphinha et Mbappé
    st.image("https://img.asmedia.epimg.net/resizer/v2/GHSMLRNR75IBFCHWEY4Y73QO2E.jpg?auth=76384f5d52069c944f8087265886915152504620f5c1a704686419062363162b&width=1200&height=675&smart=true", caption="Raphinha & Mbappé - The New Era")

elif page == texts['vip']:
    st.title(f"🏆 {texts['vip']}")
    code = st.text_input(texts['enter_code'], type="password")
    if code == CODE_VIP:
        st.success(texts['access_ok'])
        st.info(texts['no_match'])

elif page == texts['admin']:
    st.title(f"🔐 {texts['admin']}")
    pwd = st.text_input(texts['pwd_admin'], type="password")
    if pwd == MDP_ADMIN:
        st.success("OK")

st.sidebar.write("---")
st.sidebar.caption(f"AI-BETTING-PRO v3.0")
