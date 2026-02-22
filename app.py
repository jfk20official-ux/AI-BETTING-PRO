import streamlit as st
import requests
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURATION PRIVÉE (À REMPLIR)
# ==========================================
API_KEY = "80da65258a3809f6c7ad2c74930ceb90" 
ADMIN_PASSWORD = "Tunga25721204301"
WHATSAPP_LINK = "https://wa.me/TON_NUMERO"

# --- GESTION DU CODE PROMO ---
# Tu peux changer "JFK20" par n'importe quel autre code ici
PROMO_CODE_ACTIF = "JFK20" 

# Délais des Packs (en jours)
DUREE_SILVER = 7
DUREE_GOLD = 30
DUREE_VIP = 90

# ==========================================
# 2. STYLE ET POLICE DISCRÈTE (14px)
# ==========================================
st.set_page_config(page_title="L'Oracle AI", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #e0e0e0;
    }
    .main { background-color: #0e1117; }
    .gold-glow {
        color: #D4AF37;
        text-shadow: 0px 0px 8px rgba(212, 175, 55, 0.4);
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: rgba(14, 17, 23, 0.9);
        color: #555; text-align: center; padding: 5px; font-size: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. LOGIQUE D'EXPIRATION
# ==========================================
def check_expiry(start_date_str, category):
    durations = {"SILVER": DUREE_SILVER, "GOLD": DUREE_GOLD, "VIP": DUREE_VIP}
    days = durations.get(category, 7)
    
    try:
        start_dt = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
        real_start = start_dt + timedelta(hours=5)
        expiry_dt = real_start + timedelta(days=days)
        
        now = datetime.now()
        if now > expiry_dt:
            return False, "00j 00h"
        diff = expiry_dt - now
        return True, f"{diff.days}j {diff.seconds//3600}h"
    except:
        return False, "Erreur Date"

# ==========================================
# 4. NAVIGATION
# ==========================================
st.sidebar.markdown("<h1 class='gold-glow'>L'ORACLE AI</h1>", unsafe_allow_html=True)
menu = ["🏠 Accueil", "📊 Pronostics VIP", "📩 Contact", "🔐 Admin"]
choice = st.sidebar.selectbox("Menu", menu)

# --- ACCUEIL ---
if choice == "🏠 Accueil":
    st.image("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=500")
    st.markdown("<h2 class='gold-glow'>L'Analyseur de Momentum</h2>", unsafe_allow_html=True)
    st.write(f"Bienvenue. Utilisez votre code promo **{PROMO_CODE_ACTIF}** pour activer vos avantages.")

# --- PRONOSTICS VIP (CORRECTION JFK20) ---
elif choice == "📊 Pronostics VIP":
    # Utilisation de .upper() pour que "jfk20" ou "JFK20" fonctionnent tous les deux
    user_code = st.sidebar.text_input("Entrez votre code d'accès ou Promo", type="password").upper()
    
    if user_code == PROMO_CODE_ACTIF.upper():
        # Simulation d'un accès activé maintenant pour le test du code promo
        date_activation_promo = datetime.now().strftime("%Y-%m-%d %H:%M")
        is_active, time_left = check_expiry(date_activation_promo, "SILVER")
        
        st.success(f"✅ Code PROMO {PROMO_CODE_ACTIF} activé !")
        st.info(f"Temps restant avant expiration : {time_left}")
        st.markdown("### 🏆 Pronostics Premium débloqués")
        # Ici tes fonctions de prédictions
        
    elif user_code != "":
        st.error("❌ Code invalide ou expiré.")

# --- ADMIN ---
elif choice == "🔐 Admin":
    passw = st.text_input("Password", type="password")
    if passw == ADMIN_PASSWORD:
        st.success("Accès Maître autorisé.")
        # Dashboard stats Canada/Burundi
