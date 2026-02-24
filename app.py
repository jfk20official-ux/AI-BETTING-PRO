import streamlit as st
import requests

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="AI-BETTING-PRO", layout="wide")

# --- PARAMÈTRES ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
PWD_ADMIN = "Tunga25721204301"
CODE_VIP = "Jfk20"

# --- MÉMOIRE DE CONNEXION (Évite de retaper le code) ---
if 'auth_admin' not in st.session_state: st.session_state.auth_admin = False
if 'auth_vip' not in st.session_state: st.session_state.auth_vip = False
if 'pronos_publies' not in st.session_state: st.session_state.pronos_publies = []

# --- STYLE TYPE "FOREBET" (Clair et Léger) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #F0F2F5; color: #333; }}
    .main-header {{ background-color: #D4AF37; padding: 10px; border-radius: 5px; color: white; text-align: center; margin-bottom: 20px; }}
    .card {{ background-color: white; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
    .btn-refresh {{ background-color: #ffffff; border: 1px solid #D4AF37; color: #D4AF37; border-radius: 20px; padding: 5px 15px; cursor: pointer; }}
    h1, h2, h3 {{ color: #1a1a1a; }}
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
st.sidebar.markdown("<h2 style='color: #D4AF37;'>AI-BETTING-PRO</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("Navigation", ["🏠 Accueil", "💎 Espace VIP", "🔐 Admin", "🎁 Bonus 1xBet"])

# --- FONCTION API ---
def get_live():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        return requests.get(url, headers=headers, timeout=10).json().get('response', [])
    except: return []

# --- PAGE ACCUEIL ---
if menu == "🏠 Accueil":
    st.markdown("<div class='main-header'><h1>⚽ SCORES EN DIRECT</h1></div>", unsafe_allow_html=True)
    if st.button("🔄 Actualiser les scores"): st.rerun()
    
    live_matches = get_live()
    if live_matches:
        for m in live_matches[:10]:
            with st.container():
                st.markdown(f"""
                <div class='card'>
                    <span style='color:red; font-weight:bold;'>• LIVE</span> | 
                    <b>{m['teams']['home']['name']}</b> {m['goals']['home']} - {m['goals']['away']} <b>{m['teams']['away']['name']}</b>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("Pas de matchs en cours. Revenez plus tard.")

# --- PAGE VIP ---
elif menu == "💎 Espace VIP":
    st.title("🏆 Espace Pronostics VIP")
    if not st.session_state.auth_vip:
        code = st.text_input("Entrez votre code d'accès :", type="password")
        if code == CODE_VIP:
            st.session_state.auth_vip = True
            st.rerun()
    
    if st.session_state.auth_vip:
        st.success("Accès Client VIP Actif")
        if not st.session_state.pronos_publies:
            st.info("L'Oracle analyse les matchs...")
        for p in st.session_state.pronos_publies:
            st.markdown(f"<div class='card'><h3>{p['match']}</h3><p style='color:green;'><b>Prono : {p['prono']}</b></p><p>Cote: {p['cote']} | Confiance: {p['fiab']}%</p></div>", unsafe_allow_html=True)

# --- PAGE BONUS 1XBET (NOUVEAU) ---
elif menu == "🎁 Bonus 1xBet":
    st.title("🎁 Bonus & Vérification ID")
    st.markdown("""
    <div class='card'>
        <h4>Utilisez le code promo : <b style='color: #D4AF37;'>Jfk20</b></h4>
        <p>Pour débloquer les services VIP, créez votre compte 1xBet avec ce code.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("id_verify"):
        user_id = st.text_input("Entrez votre ID 1xBet pour vérification")
        if st.form_submit_button("Envoyer mon ID"):
            st.success(f"ID {user_id} envoyé ! L'admin va vérifier votre inscription sous Jfk20.")

# --- PAGE ADMIN ---
elif menu == "🔐 Admin":
    st.title("🔐 Administration")
    if not st.session_state.auth_admin:
        pwd = st.text_input("Mot de passe Maître :", type="password")
        if pwd == PWD_ADMIN:
            st.session_state.auth_admin = True
            st.rerun()
            
    if st.session_state.auth_admin:
        st.success("Connecté en tant que Tunga")
        if st.button("Déconnexion"):
            st.session_state.auth_admin = False
            st.rerun()
            
        with st.form("prono_form"):
            m = st.text_input("Match")
            p = st.text_input("Prono")
            c = st.text_input("Cote")
            f = st.slider("Fiabilité", 0, 100, 95)
            if st.form_submit_button("Publier"):
                st.session_state.pronos_publies.append({"match": m, "prono": p, "cote": c, "fiab": f})
                st.success("Publié !")

st.sidebar.write("---")
st.sidebar.write("AI-BETTING-PRO v4.0")
