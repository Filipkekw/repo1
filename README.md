# Aplikacja Lista Zadań z generatorem planu dnia (To-Do List)

Jest to prosta aplikacja lista zadań stworzona przy użyciu biblioteki `customtkinter` w Pythonie. Aplikacja pozwala użytkownikowi dodawać zadania do listy, wyświetlać je w interfejsie graficznym i eksportować listę zadań do pliku w formacie PDF. Posiada również funkcję generowania planu dnia roboczego, wolnego od pracy lub na pracy zdalej w zależności od wyboru użytkownika. 

## Funkcje:
- Dodawanie zadań do listy.
- Wyświetlanie dodanych zadań w polu listy.
- Pole do wpisywania zadań.
- Przycisk do dodawania i usuwania zadań, eksportu do pliku PDF i generowania planu dnia.
- Oznaczenie zadania jako wykonane.
- Zapis danych do pliku JSON, automatycznie wczytywanych przy uruchomieniu aplikacji.
- Możliwość wygenerowania planu dnia roboczego, wolnego od pracy lub pracy zdalnej.
- Możliwość eksportu wszystkich aktualnych zadań z listy do pliku w formacie PDF.
- Zmiana czcionki w plikach pdf aby polskie znaki specjlane były normalnie pokazywane.
- Automatyczne nazywanie plików .pdf z datą ich wygenerowania.
- Podsumowywanie dnia i eksport podsumowania do pliku .txt lub .pdf.
- Eksport zadań z całego tygodnia do pliku .pdf z podsumowaniem

## Wymagania:
- Python 3.11
- Biblioteka tkinter
- Biblioteka customtkinter w wersji conajmniej 5.2.2
- Podfolder "fonts" z plikiem Aller_Lt.ttf

# Instrukcje
## Jak uruchomić:
1. Upewnij się, że masz zainstalowanego Pythona 3.11 na swoim systemie.
2. Skopiuj kod do pliku `.py` (np. `todo_list.py`).
3. Uruchom plik używając interpretera Pythona:
   ```bash
   python todo_list.py
## Jak wyeksportować aktualną listę zadań do formatu PDF?
1. Zapisz zadania na liście lub wygeneruj plan dnia.
2. Kliknij przycisk "Eksportuj do PDF".
3. Zapisz plik pod automatyczną lub zmienioną nazwą.
