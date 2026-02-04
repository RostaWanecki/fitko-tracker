import sqlite3
import os
from datetime import datetime

DB_FILE = "data/fit_tracker.db"

class DBManager:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file

        #### zajistí, že složka data existuje ####
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)

        #### připojení k databázi  ####
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

        self._create_tables()

    def _create_tables(self):
        """Vytvoří tabulku workouts, pokud neexistuje"""
        query = """
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            workout_type TEXT NOT NULL,
            exercise TEXT NOT NULL,
            weight INTEGER,
            sets INTEGER,
            reps INTEGER,
            duration INTEGER,
            distance REAL
        );
        """
        self.cursor.execute(query)
        query_exercises = """
        CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        image TEXT
        );
        """
        self.cursor.execute(query_exercises)
        self.conn.commit()
    
    ### Přidá silový trénink (např. bench press, dřepy, ...) ###
    def add_strength(self, exercise: str, weight: int, sets: int, reps: int, workout_type: str):
        query = """
        INSERT INTO workouts (date, workout_type, exercise, weight, sets, reps)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(
            query,
            (self._today(), workout_type, exercise, weight, sets, reps)
        )
        self.conn.commit()


    
    ### Přidá kardio ###
    def add_cardio(self, exercise: str, duration: int, distance: float = None):
        query = """
        INSERT INTO workouts (date, workout_type, exercise, duration, distance)
        VALUES (?, 'cardio', ?, ?, ?)
        """
        self.cursor.execute(
            query,
            (self._today(), exercise, duration, distance)
        )
        self.conn.commit()

    ### Přidá flexibilitu ###
    def add_flexibility(self, exercise: str, duration: int):
        query = """
        INSERT INTO workouts (date, workout_type, exercise, duration)
        VALUES (?, 'flexibility', ?, ?)
        """
        self.cursor.execute(
            query,
            (self._today(), exercise, duration)
        )
        self.conn.commit()

    def get_all_workouts(self):
        self.cursor.execute("SELECT * FROM workouts ORDER BY date DESC")
        return self.cursor.fetchall()

    ### Vrátí historii jednoho konkrétního silového cviku ###
    def get_strength_by_exercise(self, exercise: str):
        query = """
        SELECT date, weight, sets, reps
        FROM workouts
        WHERE workout_type = 'strength' AND exercise = ?
        ORDER BY date
        """
        self.cursor.execute(query, (exercise,))
        return self.cursor.fetchall()
    

    #### Přidá nový cvik do seznamu cviků ####
    def add_exercise(self, name: str, image: str = None):
        self.cursor.execute(
            "INSERT OR IGNORE INTO exercises (name, image) VALUES (?, ?)",
            (name, image)
         )
        self.conn.commit()
    


    def get_exercises(self):
        self.cursor.execute("SELECT name, image FROM exercises")
        return self.cursor.fetchall()


    def _today(self) -> str:
        return datetime.now().date().isoformat()

    def close(self):
        self.conn.close()
