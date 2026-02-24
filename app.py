import streamlit as st
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BETTING-PRO", layout="centered")

# --- TA CLÉ API (80da65258a3809f6c7ad2c74930ceb90) ---
API_KEY = "TA_CLE_ICI"  # <--- «Tunga25721204301» 

# --- STYLE CSS (OR ET NOIR) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 10px; }
    .match-card { background-color: #1A1C24; padding: 15px; border-radius: 15px; border-left: 5px solid #D4AF37; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
st.sidebar.title("💎 MENU")
page = st.sidebar.radio("Aller vers :", ["Accueil", "Espace VIP", "Admin"])

# --- FONCTION API ---
def fetch_live_matches():
    if API_KEY == "TA_CLE_ICI":
        return None
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        response = requests.get(url, headers=headers)
        return response.json()['response']
    except:
        return None

# --- PAGES ---
if page == "Accueil":
    st.title("🔮 AI-BETTING-PRO")
    st.write("---")
    st.subheader("L'Oracle des Pronostics")
    st.write("Bienvenue. Utilisez le menu à gauche pour accéder à la zone VIP.")
    st.image("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&q=80&w=500", caption="Analyse en temps réel")

elif page == "Espace VIP":
    st.title("🏆 ZONE VIP")
    code = st.text_input("Code d'accès", type="password")
    
    if code == "JFK20":
        st.success("Accès Maître autorisé")
        
        # Tentative de récupération API
        matches = fetch_live_matches()
        
        if matches:
            for m in matches:
                with st.container():
                    st.markdown(f"""
                    <div class="match-card">
                        <h4>⚽ {m['teams']['home']['name']} vs {m['teams']['away']['name']}</h4>
                        <p>Score : {m['goals']['home']} - {m['goals']['away']}</p>
                        <p style="color: #D4AF37;"><b>PRONO : ANALYSE EN COURS (95%+)</b></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Mode Manuel : En attente de la clé API ou des pronos Admin.")
            if 'manual_matches' in st.session_state:
                for m in st.session_state.manual_matches:
                    st.markdown(f"<div class='match-card'><h4>⚽ {m['match']}</h4><p>Prono: {m['prono']}</p></div>", unsafe_allow_html=True)

elif page == "Admin":
    st.title("🔐 Panneau de Contrôle")
    pwd = st.text_input("Mot de passe Admin", type="password")
    
    if pwd == "ton_mot_de_passe":
        st.write("Ajouter un match manuellement :")
        with st.form("add_match"):
            m_name = st.text_input("Match")
            m_prono = st.text_input("Pronostic")
            if st.form_submit_button("Publier"):
                if 'manual_matches' not in st.session_state:
                    st.session_state.manual_matches = []
                st.session_state.manual_matches.append({"match": m_name, "prono": m_prono})
                st.success("Publié !")

st.sidebar.write("---")
st.sidebar.info("Version 2.0 - API Ready")
