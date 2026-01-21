from app import Event, EventRepository, WeatherService

def run_command(repo: EventRepository, weather_svc: WeatherService, cmd: str) -> bool:

    parts = cmd.split()
    if not parts: return True
    
    action = parts[0].lower()
    
    if action == "exit":
        return False
    elif action == "add" and len(parts) == 4:
        repo.add_or_update(Event(int(parts[1]), parts[2], parts[3]))
        print("Dodano wydarzenie.")
    elif action == "list":
        for e in repo.get_all():
            print(f"ID: {e.id} | {e.title} ({e.city})")
    elif action == "weather" and len(parts) == 2:
        # Pobieranie pogody dla miasta z wydarzenia
        events = [e for e in repo.get_all() if str(e.id) == parts[1]]
        if events:
            print(f"Pogoda dla {events[0].city}: {weather_svc.get_weather(events[0].city)}")
    else:
        print("Nieznana komenda lub złe parametry (add/list/weather/exit).")
    return True


if __name__ == "__main__":

    repo = EventRepository("events.db")
    weather_svc = WeatherService()
    print("Weather Planner CLI. Wpisz 'help' lub komendę.")
    while True:
        if not run_command(repo, weather_svc, input("> ")):
            break
