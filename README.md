# Weather-Aware Event Planner

## 1. Opis projektu
Weather-Aware Event Planner to aplikacja konsolowa (CLI) służąca do zarządzania nadchodzącymi wydarzeniami z uwzględnieniem prognozy pogody. System pozwala na zapisywanie wydarzeń w bazie danych oraz automatyczne sprawdzanie warunków atmosferycznych dla wybranych lokalizacji przy użyciu zewnętrznego API. 

Projekt został przygotowany jako praca zaliczeniowa, łącząca funkcjonalności zarządzania obiektami (zgodnie z Mini Projektem 1) oraz integrację z systemami rozproszonymi i bazami danych (zgodnie z Mini Projektem 2).

## 2. Funkcjonalności
* **Repozytorium Wydarzeń**: Dodawanie, aktualizowanie oraz przeglądanie listy wydarzeń.
* **Integracja Pogodowa**: Pobieranie rzeczywistych danych pogodowych dla miast przy użyciu API Open-Meteo.
* **Trwałość danych**: Wykorzystanie bazy danych SQLite do przechowywania informacji.

## 3. Serwisy zewnętrzne i techniki testowania
Zgodnie z wymaganiami projekt wykorzystuje:
* **Serwis 1: Baza danych SQLite** – wykorzystywana do przechowywania obiektów `Event`.
    * *Technika testowania*: **Baza danych w pamięci (in-memory)**. Testy integracyjne nie modyfikują plików na dysku, co zapewnia izolację środowiska.
* **Serwis 2: API Open-Meteo** – zewnętrzne API pogodowe.
    * *Technika testowania*: **Mockowanie (unittest.mock)**. Komunikacja sieciowa jest zastępowana przez obiekty pozorowane, co pozwala na testowanie aplikacji w trybie offline i zapewnia determinizm testów.

## 4. Instrukcja uruchomienia

### Wymagania
* Python 3.8+
* Biblioteki: `requests`, `pytest`, `pytest-cov`, `pytest-html`

### Instalacja zależności
```bash
pip install requests pytest pytest-cov pytest-html
