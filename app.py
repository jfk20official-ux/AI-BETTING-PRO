
import streamlit as st
import requests
import random
import string
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURATION (Stabilité maximale) ---
st.set_page_config(page_title="AI-BETTING-PRO", layout="wide")

# --- ACTUALISATION SILENCIEUSE (15 sec) ---
# Rafraîchit les scores sans faire clignoter toute la page
st_autorefresh(interval=15 * 1000, key="livescore_silent")

# --- PARAMÈTRES RÉSEAU & SÉCURITÉ ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
PWD_ADMIN = "Tunga25721204301"

# --- MÉMOIRE INTERNE (Session) ---
if 'pronos' not in st.session_state:
    st.session_state.pronos = {"gratuit": {}, "vip": {}, "promo": {}}
if 'gen_code' not in st.session_state:
    st.session_state.gen_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
if 'auth_vip' not in st.session_state:
    st.session_state.auth_vip = False

# --- STYLE CSS (Inspiration Forebet / Anti-Flicker) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    .match-row { 
        background: white; padding: 12px; border-radius: 8px;
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 5px; border: 1px solid #EEE;
        color: #333 !important;
    }
    .time-col { color: #FF4B4B; font-weight: bold; width: 45px; font-size: 14px; }
    .team-name { font-weight: 500; color: #111 !important; width: 38%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .score-box { background: #222; color: #D4AF37; padding: 4px 12px; border-radius: 4px; font-weight: bold; min-width: 60px; text-align: center; }
    .vip-card { background: #D4AF37; color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px; }
    .prono-item { background: #E8F5E9; border-left: 5px solid #2E7D32; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: #111 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- RÉCUPÉRATION DES SCORES (Mise en cache 10s pour fluidité) ---
@st.cache_data(ttl=10)
def get_live_scores():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        res = requests.get(url, headers=headers, timeout=5).json().get('response', [])
        # Classer par temps (les plus avancés en haut)
        return sorted(res, key=lambda x: x['fixture']['status']['elapsed'] or 0, reverse=True)
    except: return []

# --- BARRE LATÉRALE ---
st.sidebar.title("💎 AI-BETTING-PRO")
menu = st.sidebar.radio("Navigation", ["⚽ DIRECT & GRATUIT", "🏆 ESPACE PRIVÉ", "⚙️ ADMIN"])

# --- 1. PAGE DIRECT (LIVESCORE + GRATUIT) ---
if menu == "⚽ DIRECT & GRATUIT":
    st.markdown("<h2 style='color:#111;'>📊 Scores & Pronos Gratuits</h2>", unsafe_allow_html=True)
    
    # Affichage des pronos gratuits ajoutés par l'Admin
    if st.session_state.pronos['gratuit']:
        for k, p in st.session_state.pronos['gratuit'].items():
            st.markdown(f"""<div class="prono-item">💡 <b>{p['match']}</b> | PRONO : {p['prono']} | Cote : {p['cote']}</div>""", unsafe_allow_html=True)

    st.write("---")
    
    # Affichage Livescore
    data = get_live_scores()
    if data:
        for m in data:
            st.markdown(f"""
            <div class="match-row">
                <div class="time-col">{m['fixture']['status']['elapsed']}'</div>
                <div class="team-name" style="text-align:right;">{m['teams']['home']['name']}</div>
                <div class="score-box">{m['goals']['home']} - {m['goals']['away']}</div>
                <div class="team-name">{m['teams']['away']['name']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucun match en direct pour le moment. Actualisation automatique active...")

# --- 2. ESPACE PRIVÉ (VIP / PROMO) ---
elif menu == "🏆 ESPACE PRIVÉ":
    if not st.session_state.auth_vip:
        st.markdown(f'<div class="vip-card"><h3>🔒 ACCÈS RÉSERVÉ</h3>Code d\'accès actuel : <b>{st.session_state.gen_code}</b></div>', unsafe_allow_html=True)
        code_in = st.text_input("Entrez le code pour voir les pronostics VIP :", type="default")
        if code_in.strip() == st.session_state.gen_code:
            st.session_state.auth_vip = True
            st.rerun()
    else:
        st.title("💎 Salon de l'Oracle")
        if st.button("🚪 Se déconnecter de la zone VIP"):
            st.session_state.auth_vip = False
            st.rerun()
            
        t1, t2 = st.tabs(["🔥 PRONOS VIP", "💰 SECTION 1XBET (Jfk20)"])
        with t1:
            if not st.session_state.pronos['vip']: st.write("Analyse en cours...")
            for k, v in st.session_state.pronos['vip'].items():
                st.markdown(f"<div class='prono-item' style='background:#FFF9C4; border-color:#FBC02D;'>⚽ <b>{v['match']}</b><br>PRONO : {v['prono']} | Cote : {v['cote']}</div>", unsafe_allow_html=True)
        with t2:
            st.info("Utilisez le code promo Jfk20 pour vos dépôts 1xBet")
            for k, v in st.session_state.pronos['promo'].items():
                st.write(f"✅ {v['match']} | {v['prono']}")

# --- 3. ADMIN (PANNEAU DE GESTION) ---
elif menu == "⚙️ ADMIN":
    pwd = st.text_input("Mot de passe Maître", type="password")
    if pwd == PWD_ADMIN:
        st.success("Bienvenue Tunga. Gérez vos codes et matchs ici.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🆕 GÉNÉRER NOUVEAU CODE VIP"):
                st.session_state.gen_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                st.rerun()
        with col2:
            if st.button("🗑️ EFFACER TOUS LES MATCHS"):
                st.session_state.pronos = {"gratuit": {}, "vip": {}, "promo": {}}
                st.rerun()
        
        st.write("---")
        with st.form("add_match"):
            c = st.selectbox("Catégorie", ["gratuit", "vip", "promo"])
            m = st.text_input("Nom du Match (ex: Real vs Barça)")
            p = st.text_input("Ton Pronostic")
            co = st.text_input("Cote")
            if st.form_submit_button("PUBLIER LE PRONOSTIC"):
                st.session_state.pronos[c][m] = {"match": m, "prono": p, "cote": co}
                st.success(f"Match ajouté avec succès dans {c} !")

st.sidebar.write("---")
st.sidebar.caption("AI-BETTING-PRO v7.0")
