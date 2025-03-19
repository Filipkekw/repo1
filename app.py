import tkinter as tk  # Importowanie biblioteki Tkinter do tworzenia GUI
from tkinter import messagebox  # Importowanie modułu do wyświetlania komunikatów
import json  # Importowanie modułu do obsługi plików JSON
import os  # Importowanie modułu do operacji na plikach
import random  # Importowanie modułu do losowego wyboru danych

DATA_FILE = "tasks.json"  # Nazwa pliku przechowującego zadania
DAY_VARIATIONS_FILE = "day_variations.json"  # Plik JSON z harmonogramami dni

# Predefiniowane harmonogramy dni
def save_default_day_variations():
    default_variations = {
    "Dzień roboczy": [
        [("07:00", "Pobudka i śniadanie"), ("08:00", "Dojazd do pracy"), ("09:00", "Spotkanie zespołowe"), ("11:00", "Praca nad projektem"), ("13:00", "Lunch"), ("14:00", "Kodowanie i testowanie"), ("16:00", "Podsumowanie dnia"), ("17:00", "Powrót do domu"), ("18:00", "Obiad"), ("19:00", "Relaks lub hobby"), ("22:00", "Przygotowanie do snu")],
        [("06:30", "Poranny jogging"), ("07:30", "Śniadanie"), ("08:00", "Dojazd do pracy"), ("09:30", "Prezentacja dla klienta"), ("12:00", "Lunch"), ("13:30", "Analiza raportów"), ("15:00", "Kodowanie nowej funkcji"), ("17:30", "Powrót do domu"), ("19:00", "Czas dla rodziny"), ("21:00", "Wieczorny film"), ("23:00", "Sen")],
        [("07:00", "Pobudka i szybka kawa"), ("07:30", "Przygotowanie do pracy"), ("08:00", "Dojazd do biura"), ("09:00", "Poranne spotkanie zespołu"), ("10:30", "Kodowanie i debugging"), ("12:30", "Lunch"), ("14:00", "Spotkanie projektowe"), ("16:30", "Dokumentacja i raportowanie"), ("18:00", "Powrót do domu"), ("19:00", "Kolacja"), ("20:00", "Wieczorny spacer"), ("22:30", "Przygotowanie do snu")]
    ],
    "Dzień wolny": [
        [("09:00", "Długi sen"), ("10:30", "Śniadanie na mieście"), ("12:00", "Zakupy"), ("14:00", "Spacer w parku"), ("16:00", "Obiad z rodziną"), ("18:00", "Czytanie książki"), ("20:00", "Wieczór filmowy"), ("22:00", "Przygotowanie do snu")],
        [("07:00", "Poranne bieganie"), ("08:30", "Kawa z książką"), ("10:00", "Wizyta u znajomych"), ("12:30", "Obiad domowy"), ("15:00", "Gra w planszówki"), ("18:00", "Kolacja w restauracji"), ("20:00", "Wieczorny spacer"), ("22:30", "Serial przed snem")],
        [("10:00", "Lenistwo w łóżku"), ("11:00", "Brunch"), ("13:00", "Oglądanie ulubionego serialu"), ("15:00", "Sprzątanie mieszkania"), ("17:00", "Wyjście na kolację"), ("19:00", "Spotkanie ze znajomymi"), ("22:00", "Wieczorne czytanie"), ("23:30", "Sen")]
    ],
    "Praca zdalna": [
        [("07:30", "Poranna gimnastyka"), ("08:00", "Sprawdzenie wiadomości"), ("09:00", "Planowanie zadań"), ("10:30", "Wideo-konferencja"), ("12:00", "Lunch"), ("14:00", "Kodowanie modułu"), ("16:00", "Testowanie aplikacji"), ("18:00", "Odpoczynek wieczorny"), ("20:00", "Relaks przy muzyce"), ("22:30", "Przygotowanie do snu")],
        [("07:00", "Poranne ćwiczenia"), ("08:00", "Przygotowanie do pracy"), ("09:00", "Pisanie dokumentacji"), ("11:00", "Spotkanie online"), ("13:00", "Lunch"), ("14:30", "Analiza raportów"), ("16:30", "Kodowanie nowej funkcji"), ("18:30", "Wieczorna joga"), ("20:00", "Serial"), ("22:30", "Sen")],
        [("08:00", "Poranne raporty"), ("09:30", "Tworzenie prezentacji"), ("11:00", "Planowanie sprintu"), ("13:00", "Lunch"), ("15:00", "Dokończenie zadań"), ("17:00", "Gotowanie obiadu"), ("19:00", "Spacer z psem"), ("21:00", "Wieczorna lektura"), ("23:00", "Przygotowanie do snu")]
    ]
}
    if not os.path.exists(DAY_VARIATIONS_FILE):
        with open(DAY_VARIATIONS_FILE, "w", encoding="utf-8") as file:
            json.dump(default_variations, file, ensure_ascii=False, indent=4)

# Funkcja wczytująca harmonogramy dni z pliku JSON
def load_day_variations():
    if os.path.exists(DAY_VARIATIONS_FILE):  # Sprawdzenie, czy plik istnieje
        with open(DAY_VARIATIONS_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)  # Wczytanie danych z pliku JSON
            except json.JSONDecodeError:
                messagebox.showerror("Błąd", "Nie można odczytać pliku z harmonogramami dni.")
    return {}  # Zwrócenie pustego słownika, jeśli plik nie istnieje lub jest uszkodzony

# Zapisanie domyślnych harmonogramów, jeśli plik nie istnieje
save_default_day_variations()

# Wczytanie harmonogramów dni
day_variations = load_day_variations()

class Task:
    def __init__(self, parent, text, done, remove_callback, update_callback):
        self.parent = parent  # Kontener nadrzędny
        self.text = text  # Treść zadania
        self.done = done  # Status wykonania
        self.remove_callback = remove_callback  # Funkcja usuwająca zadanie
        self.update_callback = update_callback  # Funkcja zapisująca stan

        self.frame = tk.Frame(self.parent)  # Kontener dla zadania
        self.frame.pack(fill="x", pady=2)

        self.check_var = tk.BooleanVar(value=self.done)  # Przechowywanie stanu checkboxa
        self.checkbox = tk.Checkbutton(self.frame, variable=self.check_var, command=self.toggle_done)
        self.checkbox.pack(side="left")

        self.label = tk.Label(self.frame, text=self.text, anchor="w")  # Etykieta z treścią zadania
        self.label.pack(side="left", fill="x", expand=True)

        self.delete_button = tk.Button(self.frame, text="Usuń", command=self.remove)  # Przycisk usuwania
        self.delete_button.pack(side="right")

        self.update_style()  # Aktualizacja wyglądu

    def toggle_done(self):
        self.done = self.check_var.get()  # Zmiana statusu zadania
        self.update_style()  # Aktualizacja stylu tekstu
        self.update_callback()  # Zapisanie zmian

    def update_style(self):
        if self.done:
            self.label.config(fg="gray", underline=True)  # Oznaczenie zadania jako ukończone
        else:
            self.label.config(fg="black", underline=False)  # Normalny styl dla aktywnego zadania
    
    def remove(self):
        self.frame.destroy()  # Usunięcie elementu GUI
        self.remove_callback(self)  # Wywołanie funkcji usuwania zadania

class TaskManager:
    def __init__(self, container):
        self.container = container  # Kontener, w którym będą umieszczone zadania
        self.tasks = []  # Lista przechowująca wszystkie zadania

    def add_task(self, text, done=False):
        # Tworzy nowe zadanie, dodaje je do listy zadań i zapisuje do pliku
        task = Task(self.container, text, done, self.remove_task, self.save_tasks)  # Inicjalizuje obiekt Task
        self.tasks.append(task)  # Dodaje zadanie do listy
        self.save_tasks()  # Zapisuje zaktualizowaną listę zadań do pliku

    def remove_task(self, task):
        # Usuwa zadanie z listy i aktualizuje plik z zapisanymi zadaniami
        self.tasks.remove(task)  # Usuwa wskazane zadanie z listy
        self.save_tasks()  # Zapisuje zaktualizowaną listę zadań do pliku

    def save_tasks(self):
        # Zapisuje wszystkie zadania do pliku JSON
        tasks_data = [{"text": task.text, "done": task.done} for task in self.tasks]  # Tworzy listę słowników z danymi zadań
        with open(DATA_FILE, "w") as file:  # Otwiera plik do zapisu
            json.dump(tasks_data, file)  # Zapisuje dane zadań w formacie JSON

    def load_tasks(self):
        # Wczytuje zadania z pliku JSON, jeśli plik istnieje
        if os.path.exists(DATA_FILE):  # Sprawdza, czy plik z zapisanymi zadaniami istnieje
            with open(DATA_FILE, "r") as file:  # Otwiera plik do odczytu
                try:
                    tasks_data = json.load(file)  # Wczytuje dane z pliku JSON
                    for task in tasks_data:  # Iteruje po wszystkich wczytanych zadaniach
                        self.add_task(task["text"], task["done"])  # Dodaje każde zadanie do listy
                except json.JSONDecodeError:  # Obsługuje błąd w przypadku uszkodzonego pliku JSON
                    messagebox.showerror("Błąd", "Nie można odczytać pliku z zadaniami.")  # Wyświetla komunikat o błędzie


class TaskGenerator:
    def __init__(self, task_manager, day_type_var):
        self.task_manager = task_manager  # Przechowuje referencję do obiektu TaskManager, aby dodawać zadania
        self.day_type_var = day_type_var  # Zmienna przechowująca typ dnia (np. roboczy, wolny, zdalny)

    def generate_day_plan(self):
        # Generuje harmonogram dnia na podstawie wybranego typu dnia
        day_type = self.day_type_var.get()  # Pobiera aktualnie wybrany typ dnia z interfejsu
        if day_type in day_variations:  # Sprawdza, czy typ dnia istnieje w predefiniowanych wariantach
            tasks = random.choice(day_variations[day_type])  # Wybiera losowy zestaw zadań dla danego typu dnia
            for time, task in tasks:  # Iteruje przez listę zadań wraz z ich godzinami
                self.task_manager.add_task(f"{time} - {task} [AUTO]")  # Dodaje każde zadanie do TaskManagera z oznaczeniem [AUTO]
        else:
            # Wyświetla komunikat o błędzie, jeśli typ dnia nie jest obsługiwany
            messagebox.showerror("Błąd", "Brak harmonogramu dla wybranego typu dnia.")

class ToDoApp:
    def __init__(self, root):
        self.root = root  # Główne okno aplikacji
        self.root.title("To-Do List")  # Ustawia tytuł okna aplikacji
        self.root.geometry("600x800")  # Ustawia rozmiar okna (szerokość 600, wysokość 800 pikseli)

        # Tworzy pole tekstowe do wprowadzania nowych zadań
        self.task_entry = tk.Entry(root, width=50)  # Pole tekstowe o szerokości 50 znaków
        self.task_entry.pack(pady=10)  # Umieszcza pole w oknie z odstępem 10 pikseli w pionie

        # Tworzy przycisk do dodawania zadań
        self.add_button = tk.Button(root, text="Dodaj zadanie", command=self.add_task)  # Przycisk wywołujący metodę add_task
        self.add_button.pack(pady=5)  # Umieszcza przycisk w oknie z odstępem 5 pikseli w pionie

        # Tworzy kontener na listę zadań
        self.task_container = tk.Frame(root)  # Ramka, w której będą umieszczane zadania
        self.task_container.pack(pady=10, fill="both", expand=True)  # Wypełnia całą szerokość i rozciąga się dynamicznie

        # Inicjalizuje menedżera zadań i wczytuje istniejące zadania
        self.task_manager = TaskManager(self.task_container)  # Tworzy instancję TaskManagera
        self.task_manager.load_tasks()  # Wczytuje zapisane zadania z pliku JSON

        # Tworzy menu wyboru typu dnia (np. roboczy, wolny)
        self.day_type_var = tk.StringVar(value="Plan dnia")  # Zmienna do przechowywania wybranego typu dnia
        self.day_menu = tk.OptionMenu(root, self.day_type_var, *day_variations.keys())  # Menu rozwijane z opcjami z day_variations
        self.day_menu.pack()  # Umieszcza menu w oknie

        # Inicjalizuje generator zadań i przycisk do generowania planu dnia
        self.task_generator = TaskGenerator(self.task_manager, self.day_type_var)  # Tworzy instancję generatora zadań
        self.generate_button = tk.Button(root, text="Wygeneruj plan dnia", command=self.task_generator.generate_day_plan)  # Przycisk do generowania planu
        self.generate_button.pack(pady=5)  # Umieszcza przycisk w oknie z odstępem 5 pikseli w pionie

    def add_task(self):
        # Dodaje nowe zadanie do listy
        text = self.task_entry.get()  # Pobiera tekst wprowadzony przez użytkownika
        if text.strip():  # Sprawdza, czy tekst nie jest pusty (ignorując białe znaki)
            self.task_manager.add_task(text)  # Dodaje zadanie do TaskManagera
            self.task_entry.delete(0, tk.END)  # Czyści pole tekstowe po dodaniu
        else:
            # Wyświetla ostrzeżenie, jeśli użytkownik próbuje dodać puste zadanie
            messagebox.showwarning("Uwaga!", "Nie można dodać pustego zadania!")

root = tk.Tk()
app = ToDoApp(root)
root.mainloop()
