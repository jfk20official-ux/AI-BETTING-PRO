import sys
import random
import string
from datetime import datetime

# ================================================
# CONFIGURATION JFK20 - Édition par l'utilisateur
# ================================================

# Code promo généré par Grok AI (changeable à volonté)
def generate_jfk20_code(length=8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

JFK20_PROMO_CODE = generate_jfk20_code()   # ← Change ici si tu veux un code fixe (ex: "JFK2025X")

# ================================================
# COULEURS EXACTEMENT COMME FOREBET (vert/jaune/rouge + bold)
# ================================================
class ForebetColors:
    GREEN = '\033[92m'   # Prob > 65% → très probable
    YELLOW = '\033[93m'  # 50% à 65%
    RED = '\033[91m'     # < 50%
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def color_prob(p):
    if p >= 65:
        return ForebetColors.GREEN + f"{p}%" + ForebetColors.END
    elif p >= 50:
        return ForebetColors.YELLOW + f"{p}%" + ForebetColors.END
    else:
        return ForebetColors.RED + f"{p}%" + ForebetColors.END

# ================================================
# DONNÉES DES MATCHS (remplace par ton API plus tard)
# ================================================
finished = [
    {"time": "Terminé", "home": "Real Madrid", "away": "FC Barcelona", "pred": "1", "prob": 72, "score": "3-1"},
    {"time": "Terminé", "home": "Liverpool", "away": "Manchester City", "pred": "X", "prob": 48, "score": "1-1"},
]

in_progress = [
    {"time": "67'", "home": "PSG", "away": "Olympique Marseille", "pred": "1", "prob": 81, "score": "2-0"},
    {"time": "23'", "home": "Bayern München", "away": "Borussia Dortmund", "pred": "Over 2.5", "prob": 77, "score": "1-1"},
]

upcoming = [
    {"time": "Aujourd'hui 21:00", "home": "Chelsea", "away": "Arsenal", "pred": "BTTS", "prob": 58, "score": "-"},
    {"time": "Demain 18:30", "home": "Juventus", "away": "Inter Milan", "pred": "1X", "prob": 69, "score": "-"},
]

# ================================================
# SECTION JFK20 ÉDITABLE - Matches classés par type
# ================================================
jfk20_matches = {
    "1x2": [
        {"time": "21:00", "home": "AC Milan", "away": "AS Roma", "pred": "1", "prob": 68, "score": "-"},
        {"time": "20:45", "home": "Ajax", "away": "Feyenoord", "pred": "X", "prob": 52, "score": "-"},
    ],
    "BTTS": [
        {"time": "19:00", "home": "Tottenham", "away": "Newcastle", "pred": "BTTS Oui", "prob": 74, "score": "-"},
    ],
    "Over 2.5": [
        {"time": "22:00", "home": "Atalanta", "away": "Napoli", "pred": "Over 2.5", "prob": 79, "score": "-"},
        {"time": "18:00", "home": "Leipzig", "away": "Wolfsburg", "pred": "Over 2.5", "prob": 83, "score": "-"},
    ],
    "Over 1.5": [
        {"time": "20:30", "home": "Bayer Leverkusen", "away": "Stuttgart", "pred": "Over 1.5", "prob": 88, "score": "-"},
    ],
    "1X": [
        {"time": "21:00", "home": "Benfica", "away": "Porto", "pred": "1X", "prob": 71, "score": "-"},
    ],
    "12": [
        {"time": "19:45", "home": "Galatasaray", "away": "Fenerbahce", "pred": "12", "prob": 66, "score": "-"},
    ],
    "2X": [
        {"time": "18:30", "home": "Lille", "away": "Lyon", "pred": "2X", "prob": 64, "score": "-"},
    ],
}

# ================================================
# AFFICHAGE IDENTIQUE AU STYLE FOREBET
# ================================================
def print_header(title):
    print("\n" + "="*90)
    print(f"{ForebetColors.BOLD}{ForebetColors.UNDERLINE}{title.center(90)}{ForebetColors.END}")
    print("="*90)

def display_match_row(m):
    print(f"{m['time']:12} │ {m['home']:18} - {m['away']:18} │ {m['pred']:8} │ {color_prob(m['prob']):10} │ {m['score']:6}")

def show_section(section_name, matches_list):
    print_header(section_name)
    print(f"{'Heure':12} │ {'Équipes':38} │ {'Prédiction':8} │ {'Probabilité':10} │ {'Score'}")
    print("-"*90)
    for m in matches_list:
        display_match_row(m)
    print("-"*90)

# ================================================
# PROGRAMME PRINCIPAL
# ================================================
def main():
    print(f"\n{ForebetColors.BOLD}🚀 CODE PROMO JFK20 GÉNÉRÉ PAR GROK AI : {JFK20_PROMO_CODE}{ForebetColors.END}\n")
    
    # Matches terminés
    show_section("✅ MATCHES TERMINÉS", finished)
    
    # Matches en cours
    show_section("🔴 MATCHES EN COURS", in_progress)
    
    # Matches à venir
    show_section("⏳ MATCHES À VENIR", upcoming)
    
    # ====================== SECTION JFK20 ÉDITABLE ======================
    print_header("🔑 JFK20 ÉDITABLE - Accès réservé")
    code = input(f"{ForebetColors.BOLD}Entrez le code promo JFK20 : {ForebetColors.END}").strip().upper()
    
    if code == JFK20_PROMO_CODE:
        print(f"{ForebetColors.GREEN}✅ Accès autorisé ! Bienvenue dans la section JFK20{ForebetColors.END}\n")
        
        for cat in ["1x2", "BTTS", "Over 2.5", "Over 1.5", "1X", "12", "2X"]:
            if jfk20_matches[cat]:
                show_section(f"📌 {cat.upper()}", jfk20_matches[cat])
    else:
        print(f"{ForebetColors.RED}❌ Code promo incorrect. Accès refusé.{ForebetColors.END}")

if __name__ == "__main__":
    main()
