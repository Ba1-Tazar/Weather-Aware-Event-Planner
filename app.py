import sqlite3
import requests
from typing import List, Optional

class Event:
    def __init__(self, id: int, title: str, city: str):
        self.id = id
        self.title = title
        self.city = city

    def __eq__(self, other): # Required for object comparison
        return isinstance(other, Event) and self.id == other.id

class EventRepository:
    def __init__(self, db_path=":memory:"): # Using in-memory database for speed/testing
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS events (id INT PRIMARY KEY, title TEXT, city TEXT)")

    def add_or_update(self, event: Event):
        self.conn.execute("INSERT OR REPLACE INTO events VALUES (?, ?, ?)", 
                          (event.id, event.title, event.city))
        self.conn.commit()

    def get_all(self) -> List[Event]:
        cursor = self.conn.execute("SELECT id, title, city FROM events")
        return [Event(*row) for row in cursor.fetchall()]

    def get_by_id(self, event_id: int) -> Optional[Event]:
        """Fetch a single event by ID directly from the database."""
        cursor = self.conn.execute("SELECT id, title, city FROM events WHERE id = ?", (event_id,))
        row = cursor.fetchone()
        return Event(*row) if row else None
    
    def delete_by_id(self, event_id: int) -> bool:
        """Remove an event from the database. Returns True if a row was deleted."""
        cursor = self.conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self.conn.commit()
        return cursor.rowcount > 0

class WeatherService:
    def get_weather(self, city: str) -> str:
        # Simulation of an external weather API
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude=52.23&longitude=21.01&current_weather=true"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return "Słonecznie (API OK)"
            return "No data from API"
        except requests.exceptions.RequestException:
            return "Connection error"