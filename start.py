import json
import os
from datetime import date

DATA_FILE = "data/my_workouts.json"


def _load_data():
    """Načte všechna data z JSON souboru."""
    if not os.path.exists(DATA_FILE):
        print("Zatím nemáš žádné záznamy.")
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)
    
def _save_data(data):
    """Uloží všechna data zpět do JSON souboru."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_strength(exercise, weight, sets, reps,  workout_type="strength"):
    data = _load_data()
    data.append({
        "date": date.today().isoformat(),
        "workout_type": workout_type,
        "exercise": exercise,
        "weight": weight,
        "sets": sets,
        "reps": reps
    })
    _save_data(data)
    print(f"Záznam přidán: {exercise} {weight}kg x{sets}x{reps}")

def add_cardio(exercise, duration, distance=0):
    data = _load_data()
    data.append({
        "date": date.today().isoformat(),
        "workout_type": "cardio",
        "exercise": exercise,
        "duration": duration,
        "distance": distance
    })
    _save_data(data)
    print(f"Záznam přidán: {exercise} {duration}min {distance}km")

def add_flexibility(exercise, duration):
    data = _load_data()
    data.append({
        "date": date.today().isoformat(),
        "workout_type": "flexibility",
        "exercise": exercise,
        "duration": duration
    })
    _save_data(data)
    print(f"Záznam přidán: {exercise} {duration}min")


def plot_strength_progress(exercise):
    """Vypíše progres daného cviku (bench, dřep atd.)"""

    data = _load_data()

    ##### vyberu jen záznamy o síle + konkrétní cvik #####
    filtered = [
        w for w in data
        if w["workout_type"] == "strength"
        and w["exercise"].lower() == exercise.lower()
    ]

    if not filtered:
        print(f"\nŽádné záznamy pro cvik: {exercise}")
        return

    print(f"\n=== PROGRES CVIKU: {exercise.upper()} ===")
    for w in filtered:
        print(f"{w['date']} — {w['weight']} kg  |  {w['sets']}×{w['reps']}")


def plot_cardio_progress():
    """Vypíše progres kardia (běh, kolo, eliptical)"""
    data = _load_data()

    filtered = [
        w for w in data
        if w["workout_type"] == "cardio"
    ]

    if not filtered:
        print("\nZatím nemáš žádné kardio záznamy.")
        return

    print("\n=== PROGRES KARDIA ===")
    for w in filtered:
        print(f"{w['date']} — {w['exercise']}  |  {w['duration']} min  |  {w.get('distance', 0)} km")
