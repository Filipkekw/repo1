import tkinter as tk  # Moduł do tworzenia interfejsu graficznego
from tkinter import messagebox  # Moduł do obsługi komunikatów
import json  # Obsługa zapisu i odczytu danych w formacie JSON
import os  # Moduł do operacji na plikach
import random  # Moduł do losowego wybierania danych

DATA_FILE = "tasks.json"  # Plik, w którym przechowywane są zadania

# Zdefiniowane harmonogramy dla różnych typów dni
day_variations = {
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
        self.container = container  # Kontener dla zadań
        self.tasks = []  # Lista przechowywanych zadań

    def add_task(self, text, done=False):
        task = Task(self.container, text, done, self.remove_task, self.save_tasks)  # Tworzenie zadania
        self.tasks.append(task)  # Dodanie zadania do listy
        self.save_tasks()  # Zapisanie zmian

    def remove_task(self, task):
        self.tasks.remove(task)  # Usunięcie zadania z listy
        self.save_tasks()  # Zapisanie stanu listy

    def save_tasks(self):
        tasks_data = [{"text": task.text, "done": task.done} for task in self.tasks]  # Konwersja na JSON
        with open(DATA_FILE, "w") as file:
            json.dump(tasks_data, file)  # Zapis do pliku

    def load_tasks(self):
        if os.path.exists(DATA_FILE):  # Sprawdzenie, czy plik istnieje
            with open(DATA_FILE, "r") as file:
                try:
                    tasks_data = json.load(file)  # Odczyt danych
                    for task in tasks_data:
                        self.add_task(task["text"], task["done"])  # Przywrócenie zadań
                except json.JSONDecodeError:
                    messagebox.showerror("Błąd", "Nie można odczytać pliku.")  # Obsługa błędu JSON

class ToDoApp:
    def __init__(self, root):
        self.root = root  # Główne okno aplikacji
        self.root.title("To-Do List")  # Ustawienie tytułu okna
        self.root.geometry("600x800")  # Rozmiar okna

        self.task_entry = tk.Entry(root, width=50)  # Pole tekstowe do wpisywania zadań
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Dodaj zadanie", command=self.add_task)  # Przycisk dodawania zadania
        self.add_button.pack(pady=5)

        self.task_container = tk.Frame(root)  # Kontener na listę zadań
        self.task_container.pack(pady=10, fill="both", expand=True)

        self.task_manager = TaskManager(self.task_container)  # Inicjalizacja menedżera zadań
        self.task_manager.load_tasks()  # Wczytanie zapisanych zadań

        self.generator_label = tk.Label(root, text="Wybierz rodzaj dnia:")  # Etykieta do wyboru trybu dnia
        self.generator_label.pack()

        self.day_type_var = tk.StringVar(value="Plan na dzień")  # Zmienna przechowująca wybór trybu dnia
        self.day_options = ["Dzień roboczy", "Praca zdalna", "Dzień wolny"]  # Możliwe tryby dnia
        self.day_menu = tk.OptionMenu(root, self.day_type_var, *self.day_options)  # Menu wyboru
        self.day_menu.pack()
        self.generate_button = tk.Button(root, text="Wygeneruj plan dnia", command=self.generate_day_plan)  # Przycisk generowania planu
        self.generate_button.pack(pady=5)

    def add_task(self):
        text = self.task_entry.get()  # Pobranie tekstu zadania
        if text.strip():  # Sprawdzenie, czy wpis nie jest pusty
            self.task_manager.add_task(text)  # Dodanie zadania
            self.task_entry.delete(0, tk.END)  # Wyczyszczenie pola tekstowego
        else:
            messagebox.showwarning("Uwaga!", "Nie można dodać pustego zadania!")  # Komunikat ostrzegawczy

    def generate_day_plan(self):
        day_type = self.day_type_var.get()  # Pobranie wybranego trybu dnia
        tasks = random.choice(day_variations[day_type])  # Losowy wybór harmonogramu
        for time, task in tasks:
            self.task_manager.add_task(f"{time} - {task}")  # Dodanie zadań do listy

root = tk.Tk()
app = ToDoApp(root)
root.mainloop()  # Uruchomienie aplikacji
