import streamlit as st
import requests
import random
import string
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BETTING-PRO", layout="centered")
st_autorefresh(interval=15 * 1000, key="silent_refresh")

# --- PARAMÈTRES ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
PWD_ADMIN = "Tunga25721204301"

if 'pronos' not in st.session_state: st.session_state.pronos = {"gratuit": {}, "vip": {}, "promo": {}}
if 'gen_code' not in st.session_state: st.session_state.gen_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
if 'auth_vip' not in st.session_state: st.session_state.auth_vip = False

# --- STYLE CSS (PRO & VERTICAL) ---
st.markdown("""
    <style>
    .stApp { background-color: #F2F2F2; }
    .match-card { 
        background: white; padding: 10px; border-radius: 8px; margin-bottom: 8px;
        border-left: 5px solid #D4AF37; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .team-row { display: flex; justify-content: space-between; align-items: center; font-weight: bold; font-size: 16px; margin: 2px 0; }
    .score-val { background: #333; color: #D4AF37; padding: 2px 8px; border-radius: 4px; min-width: 30px; text-align: center; }
    .time-val { color: red; font-size: 12px; font-weight: bold; }
    .odds-row { display: flex; gap: 10px; margin-top: 5px; border-top: 1px solid #eee; padding-top: 5px; font-size: 12px; }
    .odd-box { background: #f8f8f8; padding: 2px 8px; border-radius: 3px; border: 1px solid #ddd; flex: 1; text-align: center; }
    .vip-lock { text-align: center; padding: 20px; background: white; border-radius: 10px; border: 2px dashed #D4AF37; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# --- API ---
def get_live():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try: return requests.get(url, headers=headers, timeout=5).json().get('response', [])
    except: return []

# --- NAVIGATION ---
menu = st.sidebar.radio("MENU", ["⚽ LIVE", "💎 VIP 🔒", "🎁 Jfk20 🔒", "⚙️ ADMIN"])

# --- 1. PAGE LIVE (STYLE VERTICAL) ---
if menu == "⚽ LIVE":
    data = get_live()
    if data:
        for m in data:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-size:10px; color:gray;">{m['league']['name']}</span>
                    <span class="time-val">{m['fixture']['status']['elapsed']}'</span>
                </div>
                <div class="team-row"><span>{m['teams']['home']['name']}</span><span class="score-val">{m['goals']['home']}</span></div>
                <div class="team-row"><span>{m['teams']['away']['name']}</span><span class="score-val">{m['goals']['away']}</span></div>
                <div class="odds-row">
                    <div class="odd-box">1: <b>--</b></div>
                    <div class="odd-box">X: <b>--</b></div>
                    <div class="odd-box">2: <b>--</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Pronos Gratuits
    for k, p in st.session_state.pronos['gratuit'].items():
        st.success(f"💡 {p['match']} | PRONO: {p['prono']} | @{p['cote']}")

# --- 2. ESPACE VIP ---
elif menu == "💎 VIP 🔒":
    if not st.session_state.auth_vip:
        st.markdown(f'<div class="vip-lock"><h3>💎 ACCÈS VIP 🔒</h3>Code actuel : <b>{st.session_state.gen_code}</b><br><small>Cliquez pour entrer le code</small></div>', unsafe_allow_html=True)
        code_in = st.text_input("Code :")
        if code_in == st.session_state.gen_code:
            st.session_state.auth_vip = True
            st.rerun()
    else:
        st.title("🏆 VIP")
        for k, v in st.session_state.pronos['vip'].items():
            st.info(f"⚽ {v['match']} -> {v['prono']} (@{v['cote']})")

# --- 3. SECTION PROMO ---
elif menu == "🎁 Jfk20 🔒":
    st.markdown('<div class="vip-lock"><h3>🎁 CODE PROMO Jfk20 🔒</h3>Vérification ID 1xBet requise.</div>', unsafe_allow_html=True)
    for k, v in st.session_state.pronos['promo'].items():
        st.warning(f"💎 {v['match']} | {v['prono']}")

# --- 4. ADMIN ---
elif menu == "⚙️ ADMIN":
    pwd = st.text_input("Password", type="password")
    if pwd == PWD_ADMIN:
        st.success("ADMIN")
        if st.button("👁️ VUE CLIENT"):
            st.session_state.auth_vip = True
            st.info("Mode Client activé. Allez sur l'onglet VIP.")
        
        if st.button("🆕 NOUVEAU CODE"):
            st.session_state.gen_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            st.rerun()
            
        with st.form("add"):
            c = st.selectbox("Zone", ["gratuit", "vip", "promo"])
            m = st.text_input("Match")
            p = st.text_input("Prono")
            co = st.text_input("Cote")
            if st.form_submit_button("PUBLIER"):
                st.session_state.pronos[c][m] = {"match": m, "prono": p, "cote": co}
                st.success("OK")
