import streamlit as st

# 1. CONFIGURATION (DOIT ÊTRE EN HAUT)
st.set_page_config(page_title="AI-BETTING-PRO", layout="wide")

# 2. CACHER L'INTERFACE POUR LE LOOK "APP MOBILE"
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stHeader"] {display:none;}
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DES DONNÉES (Pour éviter l'erreur 500)
if 'matchs_valides' not in st.session_state:
    st.session_state['matchs_valides'] = [
        {"sport": "⚽ Foot", "equipes": "Real Madrid vs Man City", "predic": "Win 1", "confiance": 97},
        {"sport": "🏀 Basket", "equipes": "Lakers vs Celtics", "predic": "Win 2", "confiance": 94}
    ]

# 4. VARIABLES DE SÉCURITÉ
ADMIN_PASSWORD = "Tunga25721204301"  # Change-le ici
PROMO_CODE = "JFK20"

# 5. DESIGN GLOBAL
st.markdown("<h1 style='color: #D4AF37; text-align: center;'>🔮 AI-BETTING-PRO</h1>", unsafe_allow_html=True)

# 6. NAVIGATION LATÉRALE
menu = ["🏠 Accueil", "💎 ESPACE VIP", "🔐 Admin"]
choice = st.sidebar.selectbox("Menu", menu)

# --- PAGE ACCUEIL ---
if choice == "🏠 Accueil":
    st.write("### Bienvenue dans l'Oracle")
    st.image("https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?q=80&w=500")
    st.info("Utilisez le menu à gauche pour accéder aux pronostics VIP.")

# --- PAGE VIP ---
elif choice == "💎 ESPACE VIP":
    st.subheader("💎 Accès Premium")
    code_entre = st.text_input("Entrez votre clé VIP ou Code Promo", type="password")
    
    if code_entre == "1234" or code_entre.upper() == PROMO_CODE:
        st.success("Accès Autorisé")
        for m in st.session_state['matchs_valides']:
            st.markdown(f"""
            <div style="border: 1px solid #D4AF37; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                <h4>{m['sport']} : {m['equipes']}</h4>
                <p>🎯 Prono : <b>{m['predic']}</b></p>
                <p style="color: #D4AF37;">⭐ Confiance : {m['confiance']}%</p>
            </div>
            """, unsafe_allow_html=True)
    elif code_entre:
        st.error("Clé invalide")

# --- PAGE ADMIN ---
elif choice == "🔐 Admin":
    pwd = st.text_input("Mot de passe Maître", type="password")
    if pwd == ADMIN_PASSWORD:
        st.write("### Interface de Gestion")
        
        # Ajouter un match
        with st.form("ajout"):
            sp = st.selectbox("Sport", ["⚽ Foot", "🏀 Basket"])
            eq = st.text_input("Match")
            pr = st.text_input("Prono")
            cf = st.slider("Confiance", 90, 100, 95)
            if st.form_submit_button("Publier"):
                st.session_state['matchs_valides'].append({"sport": sp, "equipes": eq, "predic": pr, "confiance": cf})
                st.rerun()

# 7. FOOTER
st.markdown("<br><hr><center style='color: gray; font-size: 10px;'>AI-BETTING-PRO © 2026</center>", unsafe_allow_html=True)
