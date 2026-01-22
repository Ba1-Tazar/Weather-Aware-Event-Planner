# Weather-Aware Event Planner

## 1. Opis projektu
Weather-Aware Event Planner to aplikacja do zarządzania wydarzeniami zintegrowana z prognozą pogody. System pozwala na przechowywanie planowanych wydarzeń w lokalnej bazie danych oraz dynamiczne sprawdzanie warunków atmosferycznych dla wybranych lokalizacji. 

Projekt realizuje wymagania zaliczeniowe poprzez połączenie logiki biznesowej z dwoma zewnętrznymi usługami oraz kompleksowym zestawem testów.

## 2. Architektura i Serwisy Zewnętrzne
Aplikacja korzysta z dwóch zewnętrznych systemów, z których każdy jest testowany inną techniką:

* Serwis 1: Baza danych SQLite – Przechowuje informacje o wydarzeniach (id, title, city).
    - Technika testowania: In-memory database. Testy integracyjne używają bazy w pamięci (:memory:), co gwarantuje szybkość i brak efektów ubocznych w systemie plików.
* Serwis 2: API Open-Meteo – Dostarcza rzeczywiste dane pogodowe.
    - Technika testowania: Mockowanie (unittest.mock). W testach symulujemy odpowiedzi serwera (success/failure), co pozwala na testowanie logiki bez połączenia z internetem.

## 3. Instrukcja uruchomienia

### Wymagania
* Python 3.8+
* Biblioteki zewnętrzne wymienione w requirements.txt

### Instalacja
1. Sklonuj repozytorium lub wypakuj pliki projektu.
2. Zainstaluj wymagane zależności komendą:
   pip install -r requirements.txt

### Uruchamianie aplikacji
Aplikacja oferuje dwa niezależne interfejsy:
1. CLI (Linia komend):
   python main.py
2. GUI (Interfejs graficzny):
   python gui_app.py

## 4. Sposób korzystania

### Interfejs CLI (main.py)
Po uruchomieniu programu dostępne są następujące komendy:
* add <id> <title> <city> - dodaje nowe wydarzenie do bazy.
* list - wyświetla wszystkie zapisane wydarzenia.
* weather <id> - sprawdza aktualną pogodę dla miasta przypisanego do wydarzenia.
* delete <id> - usuwa wydarzenie o podanym identyfikatorze.
* help - wyświetla listę dostępnych komend.
* exit - kończy działanie programu.

### Interfejs GUI (gui_app.py)
* Dodawanie: Wprowadź dane w pola ID, Title oraz City, a następnie kliknij "Add Event".
* Pogoda: Zaznacz wydarzenie na liście i kliknij "Check Weather".
* Usuwanie: Zaznacz wydarzenie na liście i kliknij "Delete Selected".

## 5. Testy i Raporty

### Uruchamianie testów
Projekt zawiera testy jednostkowe, integracyjne oraz scenariusz E2E. Aby je uruchomić, użyj komendy:
pytest test_main.py

### Generowanie raportów (Wymóg zaliczeniowy)
1. Raport wykonania testów (HTML):
   pytest --html=report.html --self-contained-html
2. Raport pokrycia kodu (Coverage):
   pytest --cov=app --cov=main --cov-report=term-missing

Scenariusz testu E2E jest zdefiniowany w funkcji test_full_e2e_flow w pliku test_main.py.