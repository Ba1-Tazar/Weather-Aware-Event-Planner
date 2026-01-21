import sqlite3
import requests
from typing import List

class Event:
    def __init__(self, id: int, title: str, city: str):
        self.id = id
        self.title = title
        self.city = city

    def __eq__(self, other): # Wymóg porównywania obiektów
        return isinstance(other, Event) and self.id == other.id

class EventRepository:
    def __init__(self, db_path=":memory:"): # Technika 1: Baza w pamięci
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS events (id INT PRIMARY KEY, title TEXT, city TEXT)")

    def add_or_update(self, event: Event):

        self.conn.execute("INSERT OR REPLACE INTO events VALUES (?, ?, ?)", 

                          (event.id, event.title, event.city))
        self.conn.commit()

    def get_all(self) -> List[Event]:
        cursor = self.conn.execute("SELECT id, title, city FROM events")
        return [Event(*row) for row in cursor.fetchall()]


class WeatherService:
    def get_weather(self, city: str) -> str:
        # Symulacja zewnętrznego API pogodowego 
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude=52.23&longitude=21.01&current_weather=true"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return "Słonecznie (API OK)"
            return "Brak danych z API"
        except requests.exceptions.RequestException:

            return "Błąd połączenia"
