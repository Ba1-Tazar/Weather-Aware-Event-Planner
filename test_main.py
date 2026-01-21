import requests
import pytest
from unittest.mock import MagicMock, patch
from app import Event, EventRepository, WeatherService
from main import run_command

# --- UNIT TESTS --- 

def test_event_equality():
    """Verify that eq and hash methods work correctly based on ID"""
    assert Event(1, "Concert", "Warsaw") == Event(1, "Other", "Other")
    assert Event(1, "A", "C") != Event(2, "A", "C")

@patch('app.requests.get')
def test_weather_service_error_handling(mock_get):
    """Edge case: API connection error handling"""
    # Simulate a RequestException being raised
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")
    svc = WeatherService()
    
    # Verify the method returns a string error message instead of crashing
    result = svc.get_weather("Warsaw")
    assert result == "Connection error"

# --- INTEGRATION TESTS --- 

def test_repo_add_and_get_all():
    """Test adding events and retrieving the full list"""
    repo = EventRepository(":memory:") 
    repo.add_or_update(Event(1, "Test", "Warsaw"))
    repo.add_or_update(Event(2, "Match", "Krakow"))
    assert len(repo.get_all()) == 2

def test_repo_get_by_id():
    """Test fetching a single specific event by ID directly from the database"""
    repo = EventRepository(":memory:")
    repo.add_or_update(Event(10, "Meeting", "Berlin"))
    
    event = repo.get_by_id(10)
    assert event is not None
    assert event.title == "Meeting"
    
    # Test for non-existent ID
    assert repo.get_by_id(999) is None

def test_repo_delete():
    """Verify that events can be removed by ID"""
    repo = EventRepository(":memory:")
    repo.add_or_update(Event(1, "Delete Me", "City"))
    
    # Check that it exists first
    assert repo.get_by_id(1) is not None
    
    # Delete and verify
    assert repo.delete_by_id(1) is True
    assert repo.get_by_id(1) is None
    
    # Try deleting something that isn't there
    assert repo.delete_by_id(999) is False

def test_repo_duplicate_overwrite():
    """Adding the same ID twice should overwrite the existing entry"""
    repo = EventRepository(":memory:")
    repo.add_or_update(Event(1, "First", "City1"))
    repo.add_or_update(Event(1, "Second", "City2"))
    all_events = repo.get_all()
    assert len(all_events) == 1
    assert all_events[0].title == "Second"

# --- CLI LOGIC TESTS ---

def test_run_command_help(capsys):
    """Test help command output"""
    repo = EventRepository(":memory:")
    svc = WeatherService()
    run_command(repo, svc, "help")
    captured = capsys.readouterr()
    assert "Available commands:" in captured.out

def test_run_command_add_duplicate(capsys):
    """Edge case: attempt to add an ID that already exists"""
    repo = EventRepository(":memory:")
    svc = WeatherService()
    run_command(repo, svc, "add 1 Test Warsaw")
    run_command(repo, svc, "add 1 Other Krakow")
    captured = capsys.readouterr()
    assert "Error: Event with ID 1 already exists!" in captured.out

# --- MOCKING TESTS --- 

@patch('app.requests.get')
def test_weather_mock_success(mock_get):
    """Verify weather service behavior when API returns success"""
    mock_get.return_value.status_code = 200
    svc = WeatherService()
    assert "API OK" in svc.get_weather("Warsaw")

# --- E2E TEST --- 

"""
E2E SCENARIO:
1. Initialize in-memory repository and weather service.
2. Add event ID 5 via 'add' command.
3. Verify event appears in 'list'.
4. Check weather for event 5 using a mocked API.
5. Close program via 'exit'.
"""
def test_full_e2e_flow(capsys):
    repo = EventRepository(":memory:")
    svc = WeatherService()
    
    # 2. Add
    run_command(repo, svc, "add 5 Match Berlin")
    
    # 3. List
    run_command(repo, svc, "list")
    captured = capsys.readouterr()
    assert "ID: 5 | Match (Berlin)" in captured.out
    
    # 4. Weather (Mocked)
    with patch('app.requests.get') as mock_api:
        mock_api.return_value.status_code = 200
        run_command(repo, svc, "weather 5")
        captured = capsys.readouterr()
        assert "Słonecznie (API OK)" in captured.out
    
    # 5. Exit
    assert run_command(repo, svc, "exit") is False