import streamlit as st
import requests
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURATION DE LA PAGE (INDISPENSABLE EN 1ER)
# ==========================================
st.set_page_config(
    page_title="AI-BETTING-PRO", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CACHER L'INTERFACE STREAMLIT (MODE PRO)
# ==========================================
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            #stDecoration {display:none;}
            [data-testid="stHeader"] {display:none;}
            /* Force le style sur mobile */
            .stApp { margin-top: -60px; } 
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# 3. CONFIGURATION PRIVÉE
# ==========================================
API_KEY = "80da65258a3809f6c7ad2c74930ceb90" 
ADMIN_PASSWORD = "Tunga25721204301"
WHATSAPP_LINK = "https://wa.me/TON_NUMERO"
PROMO_CODE_ACTIF = "JFK20" 

# Simulation de base de données interne
if 'matchs_valides' not in st.session_state:
    st.session_state['matchs_valides'] = [
        {"sport": "⚽ Foot", "equipes": "Real Madrid vs Man City", "predic": "Win 1", "confiance": 97},
        {"sport": "🏀 Basket", "equipes": "Lakers vs Celtics", "predic": "Win 2 (Total +220)", "confiance": 94}
    ]

# ==========================================
# 4. STYLE PERSONNALISÉ (DORÉ ET NOIR)
# ==========================================
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI'; font-size: 14px; color: #e0e0e0; background-color: #0e1117; }
    .gold-glow { color: #D4AF37; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.6); font-weight: bold; }
    .vip-card { border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; margin-bottom:10px; background: rgba(212, 175, 55, 0.05); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background: rgba(14,17,23,0.9); color: #555; text-align: center; padding: 10px; font-size: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 5. NAVIGATION & CONTENU
# ==========================================
st.sidebar.markdown("<h1 class='gold-glow'>L'ORACLE AI</h1>", unsafe_allow_html=True)
menu = ["🏠 Accueil", "💎 ESPACE VIP (95%)", "🎁 Promo", "📩 Contact", "🔐 Admin"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- ACCUEIL ---
if choice == "🏠 Accueil":
    st.markdown("<h1 class='gold-glow'>🔮 AI-BETTING-PRO</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?q=80&w=500")
    st.markdown("<h2 class='gold-glow'>Système de Prédiction Mondial</h2>", unsafe_allow_html=True)
    st.write("Bienvenue sur l'interface officielle. Nos algorithmes analysent des milliers de données pour extraire les meilleures opportunités.")
    st.info("Utilisez le menu à gauche pour accéder à la zone VIP.")

# --- ESPACE VIP ---
elif choice == "💎 ESPACE VIP (95%)":
    st.markdown("<h2 class='gold-glow'>💎 Zone Premium</h2>", unsafe_allow_html=True)
    code_vip = st.sidebar.text_input("Entrez votre Clé VIP", type="password")
    
    if code_vip:
        # Tu peux changer '1234' par ta vraie clé client
        if code_vip == "1234" or code_vip == PROMO_CODE_ACTIF:
            st.success("✅ Accès VIP Certifié")
            for m in st.session_state['matchs_valides']:
                st.markdown(f"""
                <div class='vip-card'>
                    <h4>{m['sport']} : {m['equipes']}</h4>
                    <p>🎯 Pronostic : <b>{m['predic']}</b></p>
                    <p style='color:#D4AF37;'>⭐ Fiabilité : <b>Certification 95% +</b></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Clé invalide.")
    else:
        st.warning("🔒 Cette zone est réservée aux membres VIP. Veuillez entrer votre clé dans la barre latérale.")

# --- PROMO ---
elif choice == "🎁 Promo":
    st.markdown("<h2 class='gold-glow'>🎁 Offre Spéciale</h2>", unsafe_allow_html=True)
    cp = st.text_input("Entrez votre Code Promo", type="password").upper()
    if cp == PROMO_CODE_ACTIF:
        st.balloons()
        st.success(f"Félicitations ! Le code {PROMO_CODE_ACTIF} est valide.")
        st.write("Accès temporaire débloqué. Contactez l'Oracle pour votre clé définitive.")

# --- ADMIN ---
elif choice == "🔐 Admin":
    psw = st.text_input("Code Maître", type="password")
    if psw == ADMIN_PASSWORD:
        st.success("Accès Maître activé.")
        
        # Gestion des matchs
        for i, m in enumerate(st.session_state['matchs_valides']):
            col1, col2, col3 = st.columns([2, 2, 1])
            col1.write(f"**{m['equipes']}**")
            col2.write(f"📊 Réel : **{m['confiance']}%**")
            if col3.button(f"Supprimer", key=f"del_{i}"):
                st.session_state['matchs_valides'].pop(i)
                st.rerun()
        
        st.divider()
        with st.form("new_match"):
            s = st.selectbox("Sport", ["⚽ Foot", "🏀 Basket"])
            eq = st.text_input("Équipes")
            pr = st.text_input("Prono")
            conf = st.slider("Confiance réelle (%)", 90, 100, 95)
            if st.form_submit_button("Publier"):
                st.session_state['matchs_valides'].append({"sport": s, "equipes": eq, "predic": pr, "confiance": conf})
                st.rerun()

# --- FOOTER ---
st.markdown(f"""<div class="footer">AI-BETTING-PRO v2.8 | © 2026 | <a href="{WHATSAPP_LINK}" style="color:#D4AF37;text-decoration:none;">Support WhatsApp</a></div>""", unsafe_allow_html=True)
