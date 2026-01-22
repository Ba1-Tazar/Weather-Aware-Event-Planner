# Weather-Aware Event Planner

## 1. Opis projektu
Weather-Aware Event Planner to aplikacja do zarządzania wydarzeniami zintegrowana z prognozą pogody. System pozwala na przechowywanie planowanych wydarzeń w lokalnej bazie danych oraz dynamiczne sprawdzanie warunków atmosferycznych dla wybranych lokalizacji. 

Projekt realizuje wymagania zaliczeniowe poprzez połączenie logiki biznesowej z dwoma zewnętrznymi usługami oraz kompleksowym zestawem testów.

## 2. Architektura i Serwisy Zewnętrzne
Aplikacja korzysta z dwóch zewnętrznych systemów, z których każdy jest testowany inną techniką:

* **Serwis 1: Baza danych SQLite** – Przechowuje informacje o wydarzeniach (`id`, `title`, `city`).
    * *Technika testowania*: **In-memory database**. Testy integracyjne używają bazy w pamięci (`:memory:`), co gwarantuje szybkość i brak efektów ubocznych w systemie plików.
* **Serwis 2: API Open-Meteo** – Dostarcza rzeczywiste dane pogodowe.
    * *Technika testowania*: **Mockowanie (unittest.mock)**. W testach symulujemy odpowiedzi serwera (success/failure), co pozwala na testowanie logiki bez połączenia z internetem.

## 3. Instrukcja uruchomienia

### Wymagania
* Python 3.8+
* Biblioteki: `requests`

### Instalacja
1. Sklonuj repozytorium.
2. Zainstaluj wymagane biblioteki:
   ```bash
   pip install requests