import tkinter as tk  # Importuje bibliotekę tkinter do tworzenia GUI
from tkinter import messagebox, ttk  # Importuje moduły do okien dialogowych i stylów
import json  # Importuje moduł JSON do zapisu i odczytu danych
import os  # Importuje moduł os do operacji na plikach
import random  # Importuje moduł random do losowego generowania planów dnia
import datetime  # Importuje moduł datetime do obsługi dat i godzin

DATA_FILE = "tasks.json"  # Ścieżka do pliku z zapisanymi zadaniami
DAY_VARIATIONS_FILE = "day_variations.json"  # Ścieżka do pliku z wariantami harmonogramów dnia

def save_default_day_variations():
    default_variations = {
        "Dzień roboczy": [
            [("07:00", "Pobudka i śniadanie"), ("08:00", "Dojazd do pracy"), ("09:00", "Spotkanie zespołowe"), ("11:00", "Praca nad projektem"), ("13:00", "Lunch"), ("14:00", "Kodowanie i testowanie"), ("16:00", "Podsumowanie dnia"), ("17:00", "Powrót do domu"), ("18:00", "Obiad"), ("19:00", "Relaks lub hobby"), ("22:00", "Przygotowanie do snu")],
            [("06:30", "Poranny jogging"), ("07:30", "Śniadanie"), ("08:00", "Dojazd do pracy"), ("09:30", "Prezentacja dla klienta"), ("12:00", "Lunch"), ("13:30", "Analiza raportów"), ("15:00", "Kodowanie nowej funkcji"), ("17:30", "Powrót do domu"), ("19:00", "Czas dla rodziny"), ("21:00", "Wieczorny film"), ("23:00", "Sen")],
            [("07:00", "Pobudka i szybka kawa"), ("07:30", "Przygotowanie do pracy"), ("08:00", "Dojazd do biura"), ("09:00", "Poranne spotkanie zespołu"), ("10:30", "Kodowanie i debugging"), ("12:30", "Lunch"), ("14:00", "Spotkanie projektowe"), ("16:30", "Dokumentacja i raportowanie"), ("18:00", "Powrót do domu"), ("19:00", "Kolacja"), ("20:00", "Wieczorny spacer"), ("22:30", "Przygotowanie do snu")],
        ],
        "Dzień wolny": [
            [("09:00", "Długi sen"), ("10:30", "Śniadanie na mieście"), ("12:00", "Zakupy"), ("14:00", "Spacer w parku"), ("16:00", "Obiad z rodziną"), ("18:00", "Czytanie książki"), ("20:00", "Wieczór filmowy"), ("22:00", "Przygotowanie do snu")],
            [("07:00", "Poranne bieganie"), ("08:30", "Kawa z książką"), ("10:00", "Wizyta u znajomych"), ("12:30", "Obiad domowy"), ("15:00", "Gra w planszówki"), ("18:00", "Kolacja w restauracji"), ("20:00", "Wieczorny spacer"), ("22:30", "Serial przed snem")],
            [("10:00", "Lenistwo w łóżku"), ("11:00", "Brunch"), ("13:00", "Oglądanie ulubionego serialu"), ("15:00", "Sprzątanie mieszkania"), ("17:00", "Wyjście na kolację"), ("19:00", "Spotkanie ze znajomymi"), ("22:00", "Wieczorne czytanie"), ("23:30", "Sen")],
        ],
        "Praca zdalna": [
            [("07:30", "Poranna gimnastyka"), ("08:00", "Sprawdzenie wiadomości"), ("09:00", "Planowanie zadań"), ("10:30", "Wideo-konferencja"), ("12:00", "Lunch"), ("14:00", "Kodowanie modułu"), ("16:00", "Testowanie aplikacji"), ("18:00", "Odpoczynek wieczorny"), ("20:00", "Relaks przy muzyce"), ("22:30", "Przygotowanie do snu")],
            [("07:00", "Poranne ćwiczenia"), ("08:00", "Przygotowanie do pracy"), ("09:00", "Pisanie dokumentacji"), ("11:00", "Spotkanie online"), ("13:00", "Lunch"), ("14:30", "Analiza raportów"), ("16:30", "Kodowanie nowej funkcji"), ("18:30", "Wieczorna joga"), ("20:00", "Serial"), ("22:30", "Sen")],
            [("08:00", "Poranne raporty"), ("09:30", "Tworzenie prezentacji"), ("11:00", "Planowanie sprintu"), ("13:00", "Lunch"), ("15:00", "Dokończenie zadań"), ("17:00", "Gotowanie obiadu"), ("19:00", "Spacer z psem"), ("21:00", "Wieczorna lektura"), ("23:00", "Przygotowanie do snu")],
        ]
    }
    
    if not os.path.exists(DAY_VARIATIONS_FILE):
        with open(DAY_VARIATIONS_FILE, "w", encoding="utf-8") as file:
            json.dump(default_variations, file, ensure_ascii=False, indent=4)

# Wywołanie funkcji, aby upewnić się, że plik z predefiniowanymi zadaniami istnieje
save_default_day_variations()


def load_day_variations():
    if os.path.exists(DAY_VARIATIONS_FILE):  # Sprawdza, czy plik istnieje
        with open(DAY_VARIATIONS_FILE, "r", encoding="utf-8") as file:  # Otwiera plik w trybie odczytu
            try:
                return json.load(file)  # Próbuje załadować dane JSON
            except json.JSONDecodeError:  # Obsługuje błąd w przypadku uszkodzonego pliku JSON
                messagebox.showerror("Błąd", "Nie można odczytać pliku z harmonogramami dni.")  # Wyświetla komunikat o błędzie
    return {}  # Zwraca pusty słownik, jeśli plik nie istnieje lub nie można go odczytać

day_variations = load_day_variations()  # Ładuje dostępne warianty planów dnia
day_types = list(day_variations.keys())  # Tworzy listę nazw wariantów dnia

class ToDoApp:
    def __init__(self, root):
        self.root = root  # Główne okno aplikacji
        self.root.title("To-Do List")  # Ustawia tytuł okna
        self.root.geometry("600x900")  # Ustawia rozmiar okna
        self.root.configure(bg="#f7f7f7")  # Ustawia kolor tła

        self.task_container = ttk.Frame(root)  # Tworzy kontener na zadania
        self.task_manager = TaskManager(self.task_container)  # Tworzy obiekt do zarządzania zadaniami
        self.day_type_var = tk.StringVar(value="Plan dnia")  # Tworzy zmienną przechowującą typ dnia
        self.task_generator = TaskGenerator(self.task_manager, self.day_type_var, day_variations)  # Tworzy generator planu dnia

        self.style = ttk.Style()  # Tworzy styl dla elementów interfejsu
        self.style.configure("TButton", font=("Arial", 12), padding=5)  # Ustawia styl przycisków
        self.style.configure("TLabel", font=("Arial", 12))  # Ustawia styl etykiet
        self.style.configure("TEntry", font=("Arial", 12), padding=5)  # Ustawia styl pól tekstowych
        self.style.configure("TCheckbutton", font=("Arial", 12))  # Ustawia styl pól wyboru
        self.style.configure("AddButton.TButton", foreground="green", background="green")  # Styl dla przycisku dodawania
        self.style.configure("DeleteButton.TButton", foreground="red", background="red")  # Styl dla przycisku usuwania
        self.style.configure("GenerateButton.TButton", foreground="blue", background="blue")  # Styl dla przycisku generowania planu

        header_frame = tk.Frame(root, bg="#f7f7f7")  # Tworzy ramkę nagłówka
        header_frame.pack(pady=20)  # Ustawia margines pionowy
        header_label = tk.Label(header_frame, text="Twoja Lista Zadań", bg="#f7f7f7", fg="#333333", font=("Helvetica", 16, "bold"))  # Tworzy nagłówek
        header_label.pack()  # Wyświetla nagłówek

        self.task_entry = ttk.Entry(root, width=50, foreground="gray")
        self.task_entry.pack(pady=10)
        self.task_entry.insert(0, "Treść zadania")  # Ustawiamy placeholder na start
        self.task_entry.bind("<FocusIn>", self.clear_task_placeholder)
        self.task_entry.bind("<FocusOut>", self.restore_task_placeholder)

        self.time_entry = ttk.Entry(root, width=7, foreground="gray")  # Tworzy pole do wpisywania godziny z domyślnym kolorem tekstu
        self.time_entry.pack(pady=5)  # Ustawia margines
        self.time_entry.insert(0, "HH:MM")  # Wstawia domyślną wartość placeholdera
        self.time_entry.bind("<FocusIn>", self.clear_placeholder)  # Usuwa placeholder po kliknięciu
        self.time_entry.bind("<FocusOut>", self.restore_placeholder)  # Przywraca placeholder po opuszczeniu pola
        self.time_entry.bind("<KeyRelease>", self.format_time_entry)  # Automatycznie dodaje ":" po dwóch cyfrach

        self.add_button = ttk.Button(root, text="Dodaj zadanie", command=self.add_task, style="AddButton.TButton")  # Tworzy przycisk dodawania zadania
        self.add_button.pack(pady=5)  # Ustawia margines

        self.day_menu = ttk.OptionMenu(root, self.day_type_var, "Plan dnia", *day_types)  # Tworzy rozwijane menu wyboru typu dnia
        self.day_menu.pack(pady=5)  # Ustawia margines

        self.generate_button = ttk.Button(root, text="Wygeneruj plan dnia", command=self.generate_sorted_plan, style="GenerateButton.TButton")  # Tworzy przycisk generowania planu dnia
        self.generate_button.pack(pady=5)  # Ustawia margines

        self.task_container.pack(pady=10, fill="both", expand=True)  # Wyświetla kontener na zadania
        self.task_manager.load_tasks()  # Wczytuje wcześniej zapisane zadania

    def clear_placeholder(self, event):
        if self.time_entry.get() == "HH:MM":  # Sprawdza, czy w polu jest placeholder
            self.time_entry.delete(0, tk.END)  # Usuwa placeholder
            self.time_entry.config(foreground="black")  # Zmienia kolor tekstu na czarny

    def restore_placeholder(self, event):
        if not self.time_entry.get():  # Sprawdza, czy pole jest puste
            self.time_entry.insert(0, "HH:MM")  # Wstawia placeholder
            self.time_entry.config(foreground="gray")  # Zmienia kolor tekstu na szary
    
    def clear_task_placeholder(self, event):
        if self.task_entry.get() == "Treść zadania":
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(foreground="black")

    def restore_task_placeholder(self, event):
        """Sprawdza, czy pole zadania jest puste i przywraca placeholder."""
        self.root.after(10, lambda: self._check_task_placeholder())

    def _check_task_placeholder(self):
        """Przywraca placeholder 'Treść zadania', jeśli pole jest puste."""
        if self.task_entry.get().strip() == "":
            self.task_entry.insert(0, "Treść zadania")
            self.task_entry.config(foreground="gray")

    def format_time_entry(self, event):
        text = self.time_entry.get()

        # Zezwalamy tylko na cyfry i ":"
        if not all(c.isdigit() or c == ":" for c in text):
            self.time_entry.delete(len(text) - 1, tk.END)
            return

        # Automatyczne wstawianie ":"
        if len(text) == 2 and ":" not in text:
            self.time_entry.insert(2, ":")

        # Dodatkowe sprawdzenie poprawności formatu
        if len(text) > 5:
            self.time_entry.delete(5, tk.END)
    
    def validate_time(self, time_text):
        try:
            if time_text == "HH:MM":  # Jeśli domyślny placeholder, zwracamy True
                return True
            time_obj = datetime.datetime.strptime(time_text, "%H:%M").time()
            return 0 <= time_obj.hour < 24 and 0 <= time_obj.minute < 60
        except ValueError:
            return False

    def add_task(self):
        task_text = self.task_entry.get().strip()  # Pobiera i usuwa zbędne spacje z wpisanego zadania
        time_text = self.time_entry.get().strip()  # Pobiera i usuwa zbędne spacje z wpisanej godziny

        if not task_text or task_text == "Treść zadania":  # Sprawdza, czy pole zadania nie jest puste
            messagebox.showwarning("Błąd", "Nie można dodać pustego zadania.")  # Wyświetla ostrzeżenie
            return  # Kończy działanie funkcji

        if time_text and time_text != "HH:MM":  # Sprawdza, czy użytkownik wpisał godzinę
            if not self.validate_time(time_text):
                messagebox.showerror("Błąd", "Niepoprawny format godziny! Podaj godzinę w zakresie 00:00 - 23:59!")
                self.task_entry.delete(0, tk.END)  # Czyści pole wpisywania zadania
                self.time_entry.delete(0,tk.END) # Czyści pole godziny
                self.restore_placeholder(None)  # Przywraca placeholder w polu godziny
                self.restore_task_placeholder(None)
                return
            task_text = f"{time_text} - {task_text}"  # Dodaje godzinę do treści zadania

        self.task_manager.add_task(task_text)  # Dodaje zadanie do listy

        self.task_entry.delete(0, tk.END)  # Czyści pole wpisywania zadania
        self.time_entry.delete(0,tk.END) # Czyści pole godziny
        self.restore_placeholder(None)  # Przywraca placeholder w polu godziny
        self.restore_task_placeholder(None) # Przywraca placeholder w polu zadania
    
    def sort_tasks(self):
        self.task_listbox.delete(0, tk.END)  # Czyszczenie listy
        self.task_manager.tasks.sort(key=lambda task: task.time)  # Sortowanie po czasie
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, task.title)  # Ponowne dodanie do listy

    def generate_sorted_plan(self):
        if any("[AUTO]" in task.text for task in self.task_manager.tasks):  # Sprawdza, czy istnieją automatycznie wygenerowane zadania
            response = messagebox.askyesno("Potwierdzenie", "Czy chcesz nadpisać istn=iejący plan dnia?")  # Pyta użytkownika o potwierdzenie
            if not response:  # Jeśli użytkownik nie chce nadpisać
                return  # Kończy działanie funkcji

        self.task_manager.remove_auto_tasks()  # Usuwa automatycznie wygenerowane zadania
        self.task_generator.generate_day_plan()  # Generuje nowy plan dnia
        self.task_manager.sort_tasks()  # Sortuje zadania według godziny

class TaskManager:
    def __init__(self, container):
        self.container = container  # Kontener, w którym będą wyświetlane zadania
        self.tasks = []  # Lista przechowująca wszystkie zadania

    def add_task(self, text, done=False):
        task = Task(self.container, text, done, self.remove_task, self.save_tasks)  # Tworzy nowy obiekt zadania
        self.tasks.append(task)  # Dodaje zadanie do listy
        self.save_tasks()  # Zapisuje zadania do pliku
        self.sort_tasks() # Sortuje zadania po dodaniu nowego
        self.refresh_tasks()  # Odświeża listę zadań

    def remove_task(self, task):
        if task in self.tasks:  # Sprawdza, czy zadanie istnieje w liście
            self.tasks.remove(task)  # Usuwa zadanie z listy
            task.frame.destroy()  # Usuwa graficzną reprezentację zadania
            self.save_tasks()  # Zapisuje zmiany

    def save_tasks(self):
        tasks_data = [{"text": task.text, "done": task.done} for task in self.tasks]  # Tworzy listę słowników z danymi zadań
        with open(DATA_FILE, "w") as file:  # Otwiera plik w trybie zapisu
            json.dump(tasks_data, file)  # Zapisuje dane w formacie JSON

    def load_tasks(self):
        if os.path.exists(DATA_FILE):  # Sprawdza, czy plik z danymi istnieje
            with open(DATA_FILE, "r") as file:  # Otwiera plik w trybie odczytu
                try:
                    tasks_data = json.load(file)  # Wczytuje dane JSON
                    for task_data in tasks_data:  # Iteruje po zadaniach z pliku
                        self.add_task(task_data["text"], task_data.get("done", False))  # Dodaje zadania do listy
                except json.JSONDecodeError:  # Obsługuje błąd w przypadku niepoprawnego pliku JSON
                    messagebox.showerror("Błąd", "Nie można odczytać pliku z zadaniami.")  # Wyświetla komunikat o błędzie

    def remove_auto_tasks(self):
        auto_tasks = [task for task in self.tasks if "[AUTO]" in task.text]  # Wyszukuje zadania oznaczone jako automatyczne
        if auto_tasks:  # Sprawdza, czy istnieją automatyczne zadania
            confirm = messagebox.askyesno("Potwierdzenie", "Czy chcesz nadpisać istniejący plan dnia?")  # Pyta użytkownika o potwierdzenie
            if not confirm:  # Jeśli użytkownik odmówi
                return  # Przerywa działanie funkcji

        for task in auto_tasks:  # Iteruje po automatycznych zadaniach
            task.frame.destroy()  # Usuwa graficzną reprezentację zadania
            self.tasks.remove(task)  # Usuwa zadanie z listy
        self.save_tasks()  # Zapisuje zmiany

    def sort_tasks(self):
        try:
            def extract_time(task):
                parts = task.text.split(" - ", 1)  # Rozdziela tekst po pierwszym myślniku
                if len(parts) > 1 and ":" in parts[0]:  # Sprawdza, czy pierwsza część wygląda na godzinę
                    try:
                        return datetime.datetime.strptime(parts[0], "%H:%M").time()  # Konwertuje na obiekt time
                    except ValueError:  # Obsługuje błąd konwersji
                        return datetime.time(23, 59)  # Zadania z błędnym formatem godziny trafiają na koniec listy
                return datetime.time(23, 59)  # Zadania bez godziny również idą na koniec

            self.tasks.sort(key=lambda task: extract_time(task))  # Sortuje zadania według wyciągniętej godziny
            self.refresh_tasks()  # Odświeża listę zadań po sortowaniu

        except Exception as e:  # Obsługuje błędy podczas sortowania
            messagebox.showerror("Błąd", f"Nie udało się posortować zadań:\n{str(e)}")  # Wyświetla komunikat o błędzie

    def refresh_tasks(self):
        for task in self.tasks:  # Iteruje po wszystkich zadaniach
            task.frame.pack_forget()  # Ukrywa wszystkie zadania
        for task in self.tasks:  # Ponownie iteruje po zadaniach
            task.frame.pack(fill="x", padx=5, pady=5)  # Wyświetla posortowane zadania

class Task:
    def __init__(self, parent, text, done, remove_callback, update_callback):
        self.parent = parent  # Kontener, w którym zadanie będzie umieszczone
        self.text = text  # Treść zadania
        self.done = done  # Status wykonania zadania (True/False)
        self.remove_callback = remove_callback  # Funkcja do usuwania zadania
        self.update_callback = update_callback  # Funkcja do aktualizacji statusu zadania

        # Główna ramka zadania z użyciem ttk
        self.frame = ttk.Frame(self.parent)  # Tworzy ramkę dla zadania
        self.frame.pack(fill="x", padx=5, pady=5)  # Umieszcza ramkę w kontenerze
        self.frame.columnconfigure(1, weight=1)  # Pozwala etykiecie zajmować dostępne miejsce

        self.check_var = tk.BooleanVar(value=self.done)  # Przechowuje status zaznaczenia checkboxa
        self.checkbox = ttk.Checkbutton(self.frame, variable=self.check_var, command=self.toggle_done)  # Tworzy checkbox do oznaczania wykonania zadania
        self.checkbox.grid(row=0, column=0, padx=(0, 8), sticky="w")  # Ustawia checkbox w ramce

        self.label = ttk.Label(self.frame, text=self.text, anchor="w")  # Tworzy etykietę z treścią zadania
        self.label.grid(row=0, column=1, sticky="w")  # Ustawia etykietę obok checkboxa

        self.delete_button = ttk.Button(self.frame, text="Usuń", command=self.remove, style="DeleteButton.TButton")  # Tworzy przycisk do usuwania zadania
        self.delete_button.grid(row=0, column=2, padx=5, sticky="e")  # Umieszcza przycisk po prawej stronie

        self.update_style()  # Aktualizuje styl na podstawie statusu zadania

    def toggle_done(self):
        self.done = self.check_var.get()  # Pobiera nowy status z checkboxa
        self.update_style()  # Aktualizuje wygląd etykiety
        self.update_callback()  # Wywołuje funkcję aktualizacji

    def update_style(self):
        if self.done:
            self.label.configure(foreground="green")  # Jeśli wykonane, zmienia kolor na szary
        else:
            self.label.configure(foreground="black")  # Jeśli niewykonane, kolor czarny

    def remove(self):
        self.frame.destroy()  # Usuwa ramkę zadania
        self.remove_callback(self)  # Informuje TaskManager o usunięciu zadania

class TaskGenerator:
    def __init__(self, task_manager, day_type_var, day_variations):
        self.task_manager = task_manager  # Referencja do menedżera zadań
        self.day_type_var = day_type_var  # Zmienna przechowująca wybrany typ dnia
        self.day_variations = day_variations  # Słownik przechowujący różne harmonogramy dnia

    def generate_day_plan(self):
        day_type = self.day_type_var.get()  # Pobiera aktualnie wybrany typ dnia
        if day_type in self.day_variations:  # Sprawdza, czy istnieje harmonogram dla danego typu dnia
            tasks = random.choice(self.day_variations[day_type])  # Losuje jeden wariant harmonogramu
            for time, task in tasks:  # Iteruje przez zadania w harmonogramie
                self.task_manager.add_task(f"{time} - {task} [AUTO]")  # Dodaje każde zadanie z oznaczeniem [AUTO]
            self.task_manager.sort_tasks()  # Sortuje zadania po czasie
        else:
            messagebox.showerror("Błąd", "Brak harmonogramu dla wybranego typu dnia.")  # Komunikat o błędzie, jeśli brak harmonogramu

if __name__ == "__main__":  # Sprawdza, czy skrypt jest uruchamiany bezpośrednio (a nie importowany jako moduł)
    root = tk.Tk()  # Tworzy główne okno aplikacji Tkinter
    app = ToDoApp(root)  # Inicjalizuje aplikację To-Do List, przekazując główne okno jako parametr
    root.mainloop()  # Uruchamia główną pętlę zdarzeń Tkinter, umożliwiając interakcję z GUI
    
