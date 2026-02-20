import streamlit as st
import pandas as pd
import math
import hashlib
import sqlite3

# --- CONFIGURATION DE L'APPLICATION ---
st.set_page_config(page_title="IA Betting Pro 2026", layout="wide")

# --- STYLE VISUEL ÉPURÉ ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    th { background-color: #2e3136 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- TRADUCTIONS (Français, English, Kirundi, Kiswahili) ---
LANGS = {
    "Français": {"m1": "WIN / VICTOIRE", "m4": "💰 PREMIUM (PAYANT)", "m5": "🎫 COUPON JKJ20", "id_txt": "Pourquoi votre ID?"},
    "English": {"m1": "WIN / VICTORY", "m4": "💰 PREMIUM (PAID)", "m5": "🎫 JKJ20 COUPON", "id_txt": "Why your ID?"},
    "Kirundi": {"m1": "GUTSINDA (1X2)", "m4": "💰 VIP (KURIHA)", "m5": "🎫 COUPON YA JKJ20", "id_txt": "Kuki dushaka ID?"},
    "Kiswahili": {"m1": "USHINDI (1X2)", "m4": "💰 VIP (MALIPO)", "m5": "🎫 KUPONI YA JKJ20", "id_txt": "Kwa nini ID?"}
}

sel_lang = st.sidebar.selectbox("Language / Lugha", list(LANGS.keys()))
t = LANGS[sel_lang]

# --- INTERFACE DE CONNEXION ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("⚽ IA Betting Pro 2026")
    menu = ["Connexion", "Inscription"]
    choix = st.radio("Menu", menu)
    
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    
    if choix == "Inscription":
        u_id = st.text_input("ID 1xbet")
        u_promo = st.text_input("Code Promo", value="JKJ20")
        if st.button("Créer mon compte"):
            st.success("Compte créé ! Connectez-vous.")
    else:
        if st.button("Se connecter"):
            if email == "JFK20" and password == "admin123": # Admin par défaut
                st.session_state['user'] = "JFK20"
            else:
                st.session_state['user'] = email
            st.session_state['auth'] = True
            st.rerun()

# --- CONTENU PRINCIPAL (UNE FOIS CONNECTÉ) ---
else:
    user = st.session_state['user']
    st.title(f"🎯 IA Predictions - {user}")

    # --- CHAPITRE 1 : WIN / VICTOIRE (Style Forebet) ---
    with st.expander(t["m1"], expanded=True):
        st.write("**PRONOSTICS 1X2**")
        data = {
            "Match": ["Arsenal - Man City", "Real Madrid - Barca", "Inter - Juve", "Bayern - BVB"],
            "1": [45, 38, 52, 60],
            "X": [25, 30, 24, 20],
            "2": [30, 32, 24, 20],
            "Côte": [2.10, 2.45, 1.85, 1.55]
        }
        st.table(pd.DataFrame(data))

    # --- CHAPITRE 2 : OVER / UNDER ---
    with st.expander("⚽ OVER / UNDER (2.5)"):
        data_ou = {
            "Match": ["Arsenal - Man City", "Real Madrid - Barca"],
            "Over 2.5": [62, 58],
            "Under 2.5": [38, 42],
            "Côte": [1.75, 1.80]
        }
        st.table(pd.DataFrame(data_ou))

    # --- CHAPITRE 3 : BTTS ---
    with st.expander("🔄 BTTS (OUI/NON)"):
        st.write("Les deux équipes marquent : Analyse en cours...")

    # --- CHAPITRE 4 : PREMIUM (PAYANT) ---
    with st.expander(t["m4"]):
        st.warning("🔒 Section réservée aux abonnés VIP. Contactez JFK20 pour activer votre accès.")

    # --- CHAPITRE 5 : COUPON JKJ20 (AFFILIATION) ---
    with st.expander(t["m5"]):
        st.info("Utilisez le code promo **JKJ20** sur 1xbet pour débloquer ce coupon.")
        st.code("CODE COUPON : [VERROUILLÉ]", language="text")

    # --- PANNEAU ADMIN JFK20 ---
    if user == "JFK20":
        st.divider()
        st.header("🛠️ Administration JFK20")
        
        # Messagerie avec Traduction
        st.subheader("📩 Messages clients")
        msg_brut = st.text_area("Message reçu (ex: Kirundi)", "Ndashaka kumenya uburyo bwo kwinjira muri VIP.")
        col1, col2 = st.columns(2)
        if col1.button("Traduire en Français"):
            st.info("Traduction : 'Je veux savoir comment rejoindre le VIP.'")
        if col2.button("Traduire en Anglais"):
            st.info("Translation: 'I want to know how to join the VIP.'")

        # Gestion des membres
        st.subheader("👥 Validation des membres")
        st.write("Liste des IDs en attente de vérification...")
