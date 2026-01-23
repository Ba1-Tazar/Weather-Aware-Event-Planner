from app import Event, EventRepository, WeatherService

def run_command(repo: EventRepository, weather_svc: WeatherService, cmd: str) -> bool:
    parts = cmd.split()
    if not parts: return True
    
    action = parts[0].lower()
    
    if action == "exit":
        return False
    elif action == "help":
        print("Available commands:")
        print("  add <id> <title> <city> - Adds a new event")
        print("  list                    - Displays list of events")
        print("  weather <id>            - Checks weather for an event")
        print("  delete <id>             - Removes an event by ID") # Dodano tę linię
        print("  help                    - Displays this help")
        print("  exit                    - Closes the program")
    elif action == "add" and len(parts) == 4:
        try:
            event_id = int(parts[1])
            # Optimized check: look up by ID instead of loading all events
            if repo.get_by_id(event_id):
                print(f"Error: Event with ID {event_id} already exists!")
            else:
                repo.add_or_update(Event(event_id, parts[2], parts[3]))
                print("Event added.")
        except ValueError:
            print("Error: ID must be a number.")
    elif action == "delete" and len(parts) == 2:
        try:
            event_id = int(parts[1])
            if repo.delete_by_id(event_id):
                print(f"Event {event_id} deleted successfully.")
            else:
                print(f"Error: Event {event_id} not found.")
        except ValueError:
            print("Error: ID must be a number.")
    elif action == "list":
        events = repo.get_all()
        if not events:
            print("Database is empty.")
        for e in events:
            print(f"ID: {e.id} | {e.title} ({e.city})")
    elif action == "weather" and len(parts) == 2:
        try:
            event_id = int(parts[1])
            event = repo.get_by_id(event_id)
            if event:
                print(f"Weather for {event.city}: {weather_svc.get_weather(event.city)}")
            else:
                print("Event with that ID not found.")
        except ValueError:
            print("Error: ID must be a number.")
    else:
        print("Unknown command. Type 'help' to see the list of commands.")
    return True

if __name__ == "__main__":
    repo = EventRepository("events.db")
    weather_svc = WeatherService()
    print("Weather Planner CLI. Type 'help' for commands.")
    while True:
        try:
            if not run_command(repo, weather_svc, input("> ")):
                break
        except EOFError:
            break