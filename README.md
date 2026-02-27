# Weather Aware Event Planner

## 1. Project Description
**Weather-Aware Event Planner** is an event management application integrated with real-time weather forecasting. The system allows users to store planned events in a local database and dynamically check atmospheric conditions for selected locations.

This project fulfills academic requirements by combining business logic with two external services and a comprehensive suite of tests.

## 2. Architecture and External Services
The application utilizes two external systems, each tested using a different methodology:

- **Service 1: SQLite Database** – Stores event information (id, title, city).  
  - Testing technique: In-memory database. Integration tests utilize an in-memory database (`:memory:`), ensuring high performance and preventing side effects within the file system.  

- **Service 2: Open-Meteo API** – Provides real-time weather data.  
  - Testing technique: Mocking (`unittest.mock`). Tests simulate server responses (success/failure), allowing the logic to be verified without an active internet connection.  

## 3. Setup Instructions

### Prerequisites
- Python 3.8+  
- External libraries listed in `requirements.txt`  

### Installation
1. Clone the repository or extract the project files.  
2. Install the required dependencies using `pip install -r requirements.txt`  

### Running the Application
The application offers two independent interfaces:  
1. CLI (Command Line Interface): run `python main.py`  
2. GUI (Graphical User Interface): run `python gui_app.py`  

## 4. Usage

### CLI Interface (main.py)
Once the program is running, the following commands are available:  
- `add [id] [title] [city]` – Adds a new event to the database  
- `list` – Displays all saved events  
- `weather [id]` – Checks the current weather for the city assigned to the event  
- `delete [id]` – Removes the event with the specified ID  
- `help` – Displays a list of available commands  
- `exit` – Terminates the program  

### GUI Interface (gui_app.py)
- **Adding:** Enter data into the ID, Title, and City fields, then click "Add Event"  
- **Weather:** Select an event from the list and click "Check Weather"  
- **Deleting:** Select an event from the list and click "Delete Selected"  

## 5. Testing and Reports

### Running Tests
The project includes unit tests, integration tests, and an E2E (End-to-End) scenario. Run them using `pytest test_main.py`  

### Generating Reports (Academic Requirement)
- Test Execution Report (HTML): `pytest --html=report.html --self-contained-html`  
- Code Coverage Report: `pytest --cov=app --cov=main --cov-report=term-missing`  

The E2E test scenario is defined in the `test_full_e2e_flow` function within the `test_main.py` file.
