
from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from databaze import DBManager
import requests


app = Flask(__name__)

#### Funkce pro získání cviků z WGER API
def get_exercise_images(limit=5):
    url = f"https://wger.de/api/v2/exerciseimage/?limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['results']
        exercises = []
        for item in data:
            exercises.append({
                "name": item.get("exercise", "Cvik"),
                "description": item.get("comment", ""),
                "image": item.get("image", None)
            })
        return exercises
    return []

@app.route("/")
def index():
    db = DBManager()

    ###### DATA PRO GRAF
    strength = db.get_strength_by_exercise("bench")
    strength_img = None

    if strength:
        dates = [row[0] for row in strength]
        weights = [row[1] for row in strength]

        plt.figure()
        plt.plot(dates, weights, marker='o')
        plt.xlabel("Datum")
        plt.ylabel("Váha (kg)")
        plt.title("Bench press – progres")
        plt.xticks(rotation=45)
        plt.tight_layout()

        ###### Uložení grafu do paměti (Base64) pro vložení přímo do HTML
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        strength_img = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()

    ####### DATA PRO TABULKU
    workouts = db.get_all_workouts()

    ###### CVIKY Z WGER API
    exercises = get_exercise_images(limit=5)

    db.close()

    return render_template(
        "index.html",
        workouts=workouts,
        exercises=exercises,
        strength_img=strength_img
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
