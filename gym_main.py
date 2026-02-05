import os
from start import plot_strength_progress, plot_cardio_progress
from start import add_strength as json_add_strength
from start import add_cardio as json_add_cardio
from start import add_flexibility as json_add_flexibility
from posilani import send_email_reminder
from dotenv import load_dotenv
from databaze import DBManager
import requests


# Načte proměnné z .env
load_dotenv()

EMAIL = os.getenv("SEZNAM_EMAIL")
PASSWORD = os.getenv("SEZNAM_PASSWORD")




def get_exercise_images(limit=5):
    ###### Načtení cviků #####
    res = requests.get("https://wger.de/api/v2/exercise/?language=2&status=2")
    res.raise_for_status()
    data = res.json()
    exercises = data['results'][:limit]

    exercises_with_images = []

    for ex in exercises:
        ##### Načtení obrázků pro každý cvik #####
        img_res = requests.get(f"https://wger.de/api/v2/exerciseimage/?exercise={ex['id']}")
        img_res.raise_for_status()
        img_data = img_res.json()

        image_url = img_data['results'][0]['image'] if img_data['results'] else None
        exercises_with_images.append({
            "name": ex['name'],
            "description": ex['description'],
            "image": image_url
        })
    return exercises_with_images

def choose_strength_split():
    while True:
        split = input("\nZadej typ tréninku (např. upper, lower, push, pull): ").strip().lower()
        if split:
            return split
        print("Musíš zadat nějaký název.")

class WorkoutTracker:
    ##### classa uklada tréninků do: databáze a JSON souboru ######
    def __init__(self):
        self.db = DBManager()

    def add_strength(self, exercise, weight, sets, reps, workout_type="strength"):
        self.db.add_strength(exercise, weight, sets, reps, workout_type)
        json_add_strength(exercise, weight, sets, reps, workout_type)
        print(f"Záznam přidán: {exercise} {weight}kg x{sets}x{reps}")

    def add_cardio(self, exercise, duration, distance=0):
        self.db.add_cardio(exercise, duration, distance)
        json_add_cardio(exercise, duration, distance)
        print(f"Záznam přidán: {exercise} {duration}min {distance}km")

    def add_flexibility(self, exercise, duration):
        self.db.add_flexibility(exercise, duration)
        json_add_flexibility(exercise, duration)
        print(f"Záznam přidán: {exercise} {duration}min")
        
tracker = WorkoutTracker()

def get_positive_int(text_na_dany_cvik):
    while True:
        value = input(text_na_dany_cvik)
        try:
            value_int = int(value)
            if value_int <= 0:
                print(" Hodnota musí být větší než 0.")
            else:
                return value_int
        except ValueError:
            print(" Zadej celé číslo!")



### hlavní program ####

def main():
    while True:
        print("\n=== Můj Fitko Tracker ===")
        print("1. Přidat cvik (bench, dřepy, mrtvý tah)")
        print("2. Přidat kardio (běh, kolo, eliptical)")
        print("3. Přidat flexibilitu (strečink, mobilita)")
        print("4. Zobrazit graf pokroku")
        print("5. Konec")

        choice = input("Vyber možnost: ")

        match choice:
            case "1":
                workout_type = choose_strength_split()
                exercise = input("Název cviku: ")
                weight = get_positive_int("Váha (kg): ")
                sets = get_positive_int("Počet sérií: ")
                reps = get_positive_int("Počet opakování: ")
                tracker.add_strength(exercise, weight, sets, reps, workout_type)

            case "2":
                exercise = input("Typ kardio: ")
                duration = get_positive_int("Délka (min): ")
                distance = get_positive_int("Vzdálenost (km, pokud není, napiš 0): ")
                tracker.add_cardio(exercise, duration, distance)

            case "3":
                exercise = input("Typ cviku (strečink/mobilita): ")
                duration = get_positive_int("Délka (min): ")
                tracker.add_flexibility(exercise, duration)

            case "4":
                print("Jaký typ cvičení chceš zobrazit?")
                print("a. Síla")
                print("b. Kardio")
                typ = input("Výběr: ")
                
                if typ.lower() == "a":
                        exercise = input("Název cviku (např. bench): ")
                        plot_strength_progress(exercise)
                elif typ.lower() == "b":
                        plot_cardio_progress()
                else:
                        print("Neplatná volba")

            case "5":
                print("Měj skvělý trénink! ")
                break

            case _:
                print("Neplatná volba, zkus to znovu.")



def send_email():
    send_email_reminder(
        to_email=EMAIL,
        subject="Weekly Fit Reminder",
        body="Nezapomeň si zapsat svůj trénink!",
        from_email=EMAIL,
        password=PASSWORD
    )
    print("E-mail odeslán!")


if __name__ == "__main__":
    main()
