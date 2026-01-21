import pytest
from unittest.mock import MagicMock, patch
from app import Event, EventRepository, WeatherService

# TEST JEDNOSTKOWY: Logika porównywania [cite: 855]
def test_event_equality():
    assert Event(1, "A", "City") == Event(1, "B", "Other")

# TEST INTEGRACYJNY: Baza danych in-memory [cite: 860, 911]
def test_repo_integration():
    repo = EventRepository(":memory:")
    repo.add_or_update(Event(1, "Test", "Warszawa"))
    assert len(repo.get_all()) == 1


# TEST MOCKOWANIA: Udawanie API pogodowego [cite: 755, 917]
@patch('app.requests.get')
def test_weather_mock(mock_get):
    mock_get.return_value.status_code = 200
    svc = WeatherService()
    assert "API OK" in svc.get_weather("Warszawa")

# TEST E2E: Scenariusz opisany w komentarzu [cite: 753, 872]
"""
SCENARIUSZ E2E:
1. System inicjuje repozytorium i serwis pogodowy.
2. Użytkownik dodaje wydarzenie o ID 5, tytule 'Mecz' w mieście 'Berlin'.
3. System weryfikuje obecność wydarzenia na liście wszystkich rekordów.
4. System sprawdza pogodę dla pobranych danych (zmockowane API).
"""
def test_e2e_flow():
    repo = EventRepository(":memory:")
    svc = WeatherService()
    repo.add_or_update(Event(5, "Mecz", "Berlin"))
    
    all_events = repo.get_all()
    assert any(e.id == 5 for e in all_events)
    
    with patch('app.requests.get') as mock_api:
        mock_api.return_value.status_code = 200
        assert svc.get_weather("Berlin") == "Słonecznie (API OK)"
