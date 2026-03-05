# ================================================
# JFK20 FOREBET STYLE - VERSION QUI S'AFFICHE À COUP SÛR
# ================================================

import random
import string

def generate_jfk20_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

JFK20_CODE = generate_jfk20_code()

# Données des matchs
finished = [
    {"time": "Terminé", "home": "Real Madrid", "away": "Barcelona", "pred": "1", "prob": "72%", "score": "3-1"},
    {"time": "Terminé", "home": "Liverpool", "away": "Man City", "pred": "X", "prob": "48%", "score": "1-1"},
]

in_progress = [
    {"time": "67'", "home": "PSG", "away": "Marseille", "pred": "1", "prob": "81%", "score": "2-0"},
    {"time": "23'", "home": "Bayern", "away": "Dortmund", "pred": "Over 2.5", "prob": "77%", "score": "1-1"},
]

upcoming = [
    {"time": "21:00", "home": "Chelsea", "away": "Arsenal", "pred": "BTTS", "prob": "58%", "score": "-"},
    {"time": "18:30", "home": "Juventus", "away": "Inter", "pred": "1X", "prob": "69%", "score": "-"},
]

jfk20_matches = {
    "1x2": [{"time": "21:00", "home": "AC Milan", "away": "Roma", "pred": "1", "prob": "68%", "score": "-"}],
    "BTTS": [{"time": "19:00", "home": "Tottenham", "away": "Newcastle", "pred": "BTTS Oui", "prob": "74%", "score": "-"}],
    "Over 2.5": [{"time": "22:00", "home": "Atalanta", "away": "Napoli", "pred": "Over 2.5", "prob": "79%", "score": "-"}],
    "Over 1.5": [{"time": "20:30", "home": "Leverkusen", "away": "Stuttgart", "pred": "Over 1.5", "prob": "88%", "score": "-"}],
    "1X": [{"time": "21:00", "home": "Benfica", "away": "Porto", "pred": "1X", "prob": "71%", "score": "-"}],
    "12": [{"time": "19:45", "home": "Galatasaray", "away": "Fenerbahce", "pred": "12", "prob": "66%", "score": "-"}],
    "2X": [{"time": "18:30", "home": "Lille", "away": "Lyon", "pred": "2X", "prob": "64%", "score": "-"}],
}

def ligne(m):
    print(f"{m['time']:12} | {m['home']:18} - {m['away']:18} | {m['pred']:10} | {m['prob']:6} | {m['score']}")

print("="*95)
print("🚀 JFK20 FOREBET STYLE - CODE PROMO :", JFK20_CODE)
print("="*95)

print("\n✅ MATCHES TERMINÉS")
print("Heure        | Équipes                     | Prédiction | Prob   | Score")
print("-"*95)
for m in finished:
    ligne(m)

print("\n🔴 MATCHES EN COURS")
print("Heure        | Équipes                     | Prédiction | Prob   | Score")
print("-"*95)
for m in in_progress:
    ligne(m)

print("\n⏳ MATCHES À VENIR")
print("Heure        | Équipes                     | Prédiction | Prob   | Score")
print("-"*95)
for m in upcoming:
    ligne(m)

print("\n🔑 SECTION JFK20 ÉDITABLE")
code = input("Entre le code promo JFK20 : ").strip().upper()

if code == JFK20_CODE:
    print("✅ ACCÈS AUTORISÉ ! Bienvenue dans JFK20\n")
    for cat in ["1x2", "BTTS", "Over 2.5", "Over 1.5", "1X", "12", "2X"]:
        if jfk20_matches[cat]:
            print(f"📌 {cat.upper()}")
            print("Heure        | Équipes                     | Prédiction | Prob   | Score")
            print("-"*95)
            for m in jfk20_matches[cat]:
                ligne(m)
            print()
else:
    print("❌ Code incorrect - Accès refusé")

print("\nCode terminé ! Si ça ne s'affiche toujours pas, dis-moi sur quel appareil tu lances (Windows ? Android Termux ? Replit ?)")
