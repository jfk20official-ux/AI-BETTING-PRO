import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np
from scipy.stats import poisson
import os

# ====================== CONFIGURATION SECRETS ======================
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Tunga25721204301")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "80da65258a3809f6c7ad2c74930ceb90")

tz = pytz.timezone("Africa/Bujumbura")

# ====================== MULTI-LANGUAGE SUPPORT ======================
languages = {
    "English": "English",
    "Mandarin": "中文",
    "Hindi": "हिंदी",
    "Spanish": "Español",
    "French": "Français",
    "Arabic": "العربية",
    "Bengali": "বাংলা",
    "Portuguese": "Português",
    "Swahili": "Kiswahili"
}

translations = {
    "English": {
        "title": "AI-BET LIVESCORE & PRONOS",
        "live": "Live",
        "upcoming": "Upcoming",
        "finished": "Finished",
        "admin_mode": "Admin Mode",
        "password": "Password",
        "save": "Save",
        "no_match": "No match or API problem ({date_str})",
        "BTTS": "BTTS",
        "Over2.5": "Over 2.5",
        "Under2.5": "Under 2.5",
        "1X2": "1X2",
        "livescore_tab": "Livescore",
        "predictions_tab": "Predictions",
        "statistics_tab": "Statistics"
    },
    "Mandarin": {
        "title": "AI-BET 实时比分 & 预测",
        "live": "现场",
        "upcoming": "即将到来",
        "finished": "完成",
        "admin_mode": "管理员模式",
        "password": "密码",
        "save": "保存",
        "no_match": "无比赛或 API 问题 ({date_str})",
        "BTTS": "双方得分",
        "Over2.5": "超过 2.5",
        "Under2.5": "低于 2.5",
        "1X2": "1X2",
        "livescore_tab": "实时比分",
        "predictions_tab": "预测",
        "statistics_tab": "统计数据"
    },
    "Hindi": {
        "title": "AI-BET लाइवस्कोर & प्रोनोस",
        "live": "लाइव",
        "upcoming": "आगामी",
        "finished": "समाप्त",
        "admin_mode": "एडमिन मोड",
        "password": "पासवर्ड",
        "save": "सहेजें",
        "no_match": "कोई मैच नहीं या API समस्या ({date_str})",
        "BTTS": "बीटीटीएस",
        "Over2.5": "ओवर 2.5",
        "Under2.5": "अंडर 2.5",
        "1X2": "1X2",
        "livescore_tab": "लाइवस्कोर",
        "predictions_tab": "भविष्यवाणियां",
        "statistics_tab": "सांख्यिकी"
    },
    "Spanish": {
        "title": "AI-BET LIVESCORE & PRONOS",
        "live": "En directo",
        "upcoming": "Próximos",
        "finished": "Terminados",
        "admin_mode": "Modo Admin",
        "password": "Contraseña",
        "save": "Guardar",
        "no_match": "No hay partido o problema API ({date_str})",
        "BTTS": "BTTS",
        "Over2.5": "Más de 2.5",
        "Under2.5": "Menos de 2.5",
        "1X2": "1X2",
        "livescore_tab": "Livescore",
        "predictions_tab": "Predicciones",
        "statistics_tab": "Estadísticas"
    },
    "French": {
        "title": "AI-BET LIVESCORE & PRONOS",
        "live": "En direct",
        "upcoming": "À venir",
        "finished": "Terminés",
        "admin_mode": "Mode Admin",
        "password": "Mot de passe",
        "save": "Enregistrer",
        "no_match": "Aucun match ou problème API ({date_str})",
        "BTTS": "BTTS",
        "Over2.5": "Plus de 2.5",
        "Under2.5": "Moins de 2.5",
        "1X2": "1X2",
        "livescore_tab": "Livescore",
        "predictions_tab": "Prédictions",
        "statistics_tab": "Statistiques"
    },
    "Arabic": {
        "title": "AI-BET نتيجة مباشرة & تنبؤات",
        "live": "مباشر",
        "upcoming": "قادم",
        "finished": "منتهي",
        "admin_mode": "وضع المسؤول",
        "password": "كلمة المرور",
        "save": "تسجيل",
        "no_match": "لا مباراة أو مشكلة API ({date_str})",
        "BTTS": "BTTS",
        "Over2.5": "أكثر من 2.5",
        "Under2.5": "أقل من 2.5",
        "1X2": "1X2",
        "livescore_tab": "نتيجة مباشرة",
        "predictions_tab": "تنبؤات",
        "statistics_tab": "إحصاءات"
    },
    "Bengali": {
        "title": "AI-BET লাইভস্কোর & প্রোনোস",
        "live": "লাইভ",
        "upcoming": "আসন্ন",
        "finished": "শেষ",
        "admin_mode": "অ্যাডমিন মোড",
        "password": "পাসওয়ার্ড",
        "save": "সংরক্ষণ",
        "no_match": "কোনও ম্যাচ নেই বা API সমস্যা ({date_str})",
        "BTTS": "BTTS",
        "Over2.5": "ওভার 2.5",
        "Under2.5": "আন্ডার 2.5",
        "1X2": "1X2",
        "livescore_tab": "লাইভস্কোর",
        "predictions_tab": "ভবিষ্যদ্বাণী",
        "statistics_tab": "পরিসংখ্যান"
    },
    "Portuguese": {
        "title": "AI-BET LIVESCORE & PRONOS",
        "live": "Ao vivo",
        "upcoming": "A vir",
        "finished": "Terminados",
        "admin_mode": "Modo Admin",
        "password": "Senha",
        "save": "Salvar",
        "no_match": "Nenhum jogo ou problema API ({date_str})",
        "BTTS": "BTTS",
        "Over2.5": "Mais de 2.5",
        "Under2.5": "Menos de 2.5",
        "1X2": "1X2",
        "livescore_tab": "Livescore",
        "predictions_tab": "Previsões",
        "statistics_tab": "Estatísticas"
    },
    "Swahili": {
        "title": "AI-BET LIVESCORE & PRONOS",
        "live": "Moja kwa moja",
        "upcoming": "Kuja",
        "finished": "Iliyokamilishwa",
        "admin_mode": "Hali ya Admin",
        "password": "Neno la siri",
        "save": "Hifadhi",
        "no_match": "Hakuna mechi au tatizo API ({date_str})",
        "BTTS": "BTTS",
        "Over2.5": "Zaidi ya 2.5",
        "Under2.5": "Chini ya 2.5",
        "1X2": "1X2",
        "livescore_tab": "Livescore",
        "predictions_tab": "Tabiri",
        "statistics_tab": "Takwimu"
    }
}

# ====================== LANGUAGE SELECTION ======================
selected_lang = st.sidebar.selectbox("Language", list(languages.keys()))
tr = translations[selected_lang]

# Sidebar
with st.sidebar:
    st.header("AI-BET")
    toggle = st.toggle(tr["admin_mode"])
    if toggle:
        pwd = st.text_input(tr["password"], type="password")
        if pwd == ADMIN_PASSWORD:
            st.session_state.mode = "Admin"
            st.success("Admin OK")
        else:
            st.session_state.mode = "Client"
            if pwd: st.error("Incorrect")
    else:
        st.session_state.mode = "Client"

    show_tomorrow = st.checkbox("Demain", value=False)

# Poisson with BTTS, Over/Under 2.5
def get_poisson_proba(home, away):
    lambda_home = 1.8
    lambda_away = 1.3

    MAX_GOALS = 6
    matrix = np.outer(poisson.pmf(np.arange(MAX_GOALS+1), lambda_home),
                      poisson.pmf(np.arange(MAX_GOALS+1), lambda_away))

    p1 = np.sum(np.tril(matrix, -1)) * 100
    px = np.sum(np.diag(matrix)) * 100
    p2 = np.sum(np.triu(matrix, 1)) * 100
    over25 = (1 - sum(np.diag(matrix, k).sum() for k in range(-2, 3))) * 100
    under25 = 100 - over25
    btts = (1 - matrix[0,0] - sum(matrix[i,0] for i in range(1, MAX_GOALS+1)) - sum(matrix[0,j] for j in range(1, MAX_GOALS+1))) * 100

    return {
        "1X2": {
            "1": round(p1, 1),
            "X": round(px, 1),
            "2": round(p2, 1)
        },
        "Over2.5": round(over25, 1),
        "Under2.5": round(under25, 1),
        "BTTS": round(btts, 1)
    }

# Fetch fixtures (your current function, or replace with mixed if needed)
@st.cache_data(ttl=60)
def fetch_fixtures(date_str):
    if not API_KEY:
        return []
    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        r = requests.get(url, headers=headers, timeout=8).json()
        return r.get("response", []) if not r.get("errors") else []
    except:
        return []

# ====================== AFFICHAGE AVEC TABS ======================
tabs = st.tabs([tr["livescore_tab"], tr["predictions_tab"], tr["statistics_tab"]])

with tabs[0]:  # Livescore
    st.markdown("<h3 style='text-align:center; color:#1A73E8;'>"+tr["title"]+"</h3>", unsafe_allow_html=True)

    target = datetime.now(tz).date()
    if show_tomorrow: target += timedelta(days=1)
    date_str = target.strftime("%Y-%m-%d")

    fixtures = fetch_fixtures(date_str)

    if not fixtures:
        st.info(f"Aucun match ou problème API ({date_str})")
    else:
        for group, title in [
            ([m for m in fixtures if m['fixture']['status']['short'] in ['1H','HT','2H']], tr["live"]),
            ([m for m in fixtures if m['fixture']['status']['short'] == 'NS'], tr["upcoming"]),
            ([m for m in fixtures if m['fixture']['status']['short'] == 'FT'], tr["finished"])
        ]:
            if group:
                st.subheader(title)
                for m in sorted(group, key=lambda x: x['fixture']['date']):
                    fid = str(m['fixture']['id'])
                    h = m['teams']['home']['name']
                    a = m['teams']['away']['name']
                    sh = m['goals']['home'] if m['goals']['home'] is not None else "-"
                    sa = m['goals']['away'] if m['goals']['away'] is not None else "-"
                    stt = m['fixture']['status']['short']
                    el = m['fixture']['status']['elapsed'] or ""

                    dt = datetime.fromisoformat(m['fixture']['date'].replace("Z", "+00:00")).astimezone(tz)
                    heure = dt.strftime("%H:%M")
                    jour = dt.strftime("%d/%m")

                    bord = "wait-border"
                    prono_html = ""
                    if fid in st.session_state.get('pronos', {}):
                        pr = st.session_state.pronos[fid]['p']
                        prono_html = f"<div class='proba-box'>{pr}</div>"
                        if stt == "FT":
                            res = "1" if sh > sa else ("2" if sa > sh else "X")
                            bord = "win-border" if pr == res else "loss-border"

                    proba_html = ""
                    if stt == "NS" and not prono_html:
                        proba = get_poisson_proba(h, a)
                        p1 = proba["1X2"]["1"]
                        px = proba["1X2"]["X"]
                        p2 = proba["1X2"]["2"]
                        o25 = proba["Over2.5"]
                        proba_html = f"""
                        <div style="display:flex; gap:6px; margin-top:6px;">
                            <div class='proba-box proba-1'>{p1}%</div>
                            <div class='proba-box proba-x'>{px}%</div>
                            <div class='proba-box proba-2'>{p2}%</div>
                            <div class='proba-box'>O2.5 {o25}%</div>
                        </div>
                        """

                    stat_disp = f"{el}'" if el else stt
                    stat_cls = "status-live" if stt in ['1H','HT','2H'] else "status-fin"

                    st.markdown(f"""
                    <div class="match-card {bord}">
                        <div class="time-col">
                            <div class="time">{heure}</div>
                            <div style="font-size:0.8rem; color:#666;">{jour}</div>
                        </div>
                        <div style="min-width:40px; text-align:center; font-weight:bold;" class="{stat_cls}">
                            {stat_disp}
                        </div>
                        <div class="teams">
                            <div class="team-row"><span class="team-name">{h}</span><span class="score">{sh}</span></div>
                            <div class="team-row"><span class="team-name">{a}</span><span class="score">{sa}</span></div>
                            {proba_html}
                        </div>
                        {prono_html}
                    </div>
                    """, unsafe_allow_html=True)

with tabs[1]:  # Predictions
    st.subheader(tr["predictions_tab"])
    upcoming = [m for m in fixtures if m['fixture']['status']['short'] == 'NS']
    for m in upcoming:
        h = m['teams']['home']['name']
        a = m['teams']['away']['name']
        proba = get_poisson_proba(h, a)
        st.write(f"{h} vs {a}")
        st.write(f"1X2: 1 {proba['1X2']['1']}% | X {proba['1X2']['X']}% | 2 {proba['1X2']['2']}%")
        st.write(f"BTTS: {proba['BTTS']}%")
        st.write(f"Over 2.5: {proba['Over2.5']}% | Under 2.5: {proba['Under2.5']}%")

with tabs[2]:  # Statistics
    st.subheader(tr["statistics_tab"])
    upcoming = [m for m in fixtures if m['fixture']['status']['short'] == 'NS']
    for m in upcoming:
        h = m['teams']['home']['name']
        a = m['teams']['away']['name']
        proba = get_poisson_proba(h, a)
        st.write(f"{h} vs {a}")
        st.write(f"Expected goals home: {1.8} | away: {1.3}")
        st.write(f"Prob of clean sheet home: {round(poisson.pmf(0, lambda_away) * 100, 1)}%")
        st.write(f"Prob of clean sheet away: {round(poisson.pmf(0, lambda_home) * 100, 1)}%")
