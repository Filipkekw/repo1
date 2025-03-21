import customtkinter as ctk  # Importowanie biblioteki CustomTkinter do tworzenia interfejsów użytkownika.
import json  # Importowanie modułu do obsługi plików JSON.
import os  # Importowanie modułu do operacji na plikach i katalogach.
import random  # Importowanie modułu do losowego wyboru elementów.
import datetime  # Importowanie modułu do obsługi dat i czasu.
import reportlab  # Importowanie biblioteki do generowania plików PDF.
from reportlab.lib.pagesizes import A4  # Importowanie stałej określającej rozmiar strony A4.
from reportlab.pdfgen import canvas  # Importowanie narzędzia do rysowania na stronach PDF.
from tkinter import filedialog  # Importowanie modułu do obsługi okien dialogowych do wyboru plików.

# Stałe dla plików danych
DATA_FILE = "tasks.json"  # Nazwa pliku, w którym przechowywane są zadania.
DAY_VARIATIONS_FILE = "day_variations.json"  # Nazwa pliku przechowującego różne warianty dni.

class CustomMessageBox(ctk.CTkToplevel):  # Klasa definiująca niestandardowe okno dialogowe (potwierdzenia).
    def __init__(self, parent, title, message, callback):  # Konstruktor klasy, inicjalizuje okno dialogowe.
        super().__init__(parent)  # Wywołanie konstruktora klasy nadrzędnej (CTkToplevel).
        self.title(title)  # Ustawienie tytułu okna.
        self.geometry("300x150")  # Ustawienie rozmiaru okna na 300x150 pikseli.
        self.callback = callback  # Przypisanie funkcji zwrotnej do zmiennej instancji.
        self.grab_set()  # Ustawienie okna jako modalnego (blokuje interakcję z głównym oknem).

        ctk.CTkLabel(self, text=message, font=("Arial", 14)).pack(pady=10)  
        # Dodanie etykiety z podanym komunikatem i czcionką Arial o rozmiarze 14.

        button_frame = ctk.CTkFrame(self)  # Tworzenie ramki do umieszczenia przycisków.
        button_frame.pack(pady=10)  # Wyświetlenie ramki z marginesem pionowym 10 pikseli.

        ctk.CTkButton(button_frame, text="Tak", fg_color="green", command=lambda: self.answer(True)).pack(side="left", padx=10)  
        # Dodanie zielonego przycisku "Tak", który po kliknięciu wywołuje metodę answer(True).

        ctk.CTkButton(button_frame, text="Nie", fg_color="red", command=lambda: self.answer(False)).pack(side="right", padx=10)  
        # Dodanie czerwonego przycisku "Nie", który po kliknięciu wywołuje metodę answer(False).

    def answer(self, response):  # Metoda obsługująca odpowiedź użytkownika.
        self.callback(response)  # Wywołanie funkcji zwrotnej z odpowiedzią użytkownika (True lub False).
        self.destroy()  # Zamknięcie okna dialogowego.

# Zapisuje domyślne warianty harmonogramów dnia
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

save_default_day_variations()

# Ładuje harmonogramy dnia
def load_day_variations():
    if os.path.exists(DAY_VARIATIONS_FILE):
        with open(DAY_VARIATIONS_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

day_variations = load_day_variations()
day_types = list(day_variations.keys())

class ToDoApp(ctk.CTk):  # Klasa głównego okna aplikacji To-Do List, dziedziczy po CTk.
    def __init__(self):  # Konstruktor klasy.
        super().__init__()  # Wywołanie konstruktora klasy nadrzędnej.
        self.title("To-Do List")  # Ustawienie tytułu okna aplikacji.
        self.geometry("600x900")  # Ustawienie rozmiaru okna na 600x900 pikseli.

        self.task_manager = TaskManager(self)  # Tworzenie obiektu menedżera zadań.
        self.day_type_var = ctk.StringVar(value="Plan dnia")  # Tworzenie zmiennej przechowującej typ dnia.
        self.task_generator = TaskGenerator(self.task_manager, self.day_type_var, day_variations)  
        # Tworzenie obiektu generatora zadań.

        ctk.CTkLabel(self, text="Twoja Lista Zadań", font=("Arial", 16, "bold")).pack(pady=10)  
        # Etykieta tytułowa aplikacji.

         # Tworzymy ramkę górną, w której będą dwie kolumny: left_frame i right_frame
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=5, fill="x")

        # Kolumna lewa
        left_frame = ctk.CTkFrame(top_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Kolumna prawa
        right_frame = ctk.CTkFrame(top_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5)

        # --- LEWA KOLUMNA ---
        self.task_entry = ctk.CTkEntry(left_frame, width=250, placeholder_text="Treść zadania")
        self.task_entry.pack(pady=5)

        self.time_entry = ctk.CTkEntry(left_frame, width=60, placeholder_text="HH:MM")
        self.time_entry.pack(pady=5)
        self.time_entry.bind("<KeyRelease>", self.format_time_entry)

        self.add_button = ctk.CTkButton(left_frame, text="Dodaj zadanie", fg_color="green", hover_color="darkgreen", command=self.add_task)
        self.add_button.pack(pady=5)

        # --- PRAWA KOLUMNA ---
        self.day_menu = ctk.CTkComboBox(right_frame, values=day_types, variable=self.day_type_var, state="readonly")
        self.day_menu.pack(pady=5)

        self.generate_button = ctk.CTkButton(right_frame, text="Wygeneruj plan dnia", fg_color="blue", hover_color="darkblue", command=self.generate_sorted_plan)
        self.generate_button.pack(pady=5)

        self.export_button = ctk.CTkButton(right_frame, text="Eksportuj do PDF", fg_color="purple", hover_color="darkviolet", command=self.export_to_pdf)
        self.export_button.pack(pady=5)

        self.task_container = ctk.CTkFrame(self)  # Kontener dla listy zadań.
        self.task_container.pack(pady=10, fill="both", expand=True)

        self.task_manager.load_tasks()  # Załadowanie zadań z pliku.

    def format_time_entry(self, event):  # Funkcja automatycznie formatująca wpisaną godzinę.
        text = self.time_entry.get()
        if len(text) == 2 and ":" not in text:  # Jeśli wpisano dwie cyfry, dodaj dwukropek.
            self.time_entry.insert(2, ":")

    def validate_time(self, time_text):  # Funkcja sprawdzająca poprawność formatu czasu.
        try:
            if time_text == "HH:MM":  
                return True  # Domyślna wartość jest poprawna.
            datetime.datetime.strptime(time_text, "%H:%M").time()  
            # Próba przekształcenia tekstu na czas (jeśli niepoprawny, wywoła wyjątek).
            return True
        except ValueError:
            return False  # Jeśli format jest błędny, zwróć False.

    def add_task(self):  # Funkcja dodająca zadanie do listy.
        task_text = self.task_entry.get().strip()  # Pobranie i usunięcie spacji z początku i końca wpisu.
        time_text = self.time_entry.get().strip()

        if not task_text:  # Jeśli nie wpisano tekstu zadania, zakończ funkcję.
            return

        if time_text and time_text != "HH:MM" and not self.validate_time(time_text):  
            return  # Jeśli czas jest podany, ale niepoprawny, zakończ funkcję.

        if time_text and time_text != "HH:MM":  
            task_text = f"{time_text} - {task_text}"  # Dodanie godziny do tekstu zadania.

        self.task_manager.add_task(task_text)  # Dodanie zadania do menedżera.
        self.task_entry.delete(0, "end")  # Wyczyść pole wpisywania zadania.
        self.time_entry.delete(0, "end")  # Wyczyść pole wpisywania czasu.

    def generate_sorted_plan(self):  # Funkcja generowania posortowanego planu dnia.
        if any("[AUTO]" in task.text for task in self.task_manager.tasks):  
            # Sprawdzenie, czy istnieją wcześniej wygenerowane zadania.
            CustomMessageBox(self, "Potwierdzenie", "Czy chcesz nadpisać istniejący plan dnia?", self.handle_confirmation)  
            # Wyświetlenie okna potwierdzenia.
        else:
            self.execute_generation()  # Jeśli nie ma wcześniejszych zadań, wykonaj generowanie.

    def handle_confirmation(self, response):  # Obsługa odpowiedzi użytkownika w oknie potwierdzenia.
        if response:  
            self.execute_generation()  # Jeśli użytkownik potwierdził, wygeneruj plan.

    def execute_generation(self):  # Właściwe generowanie planu dnia.
        self.task_manager.remove_auto_tasks()  # Usunięcie wcześniej wygenerowanych zadań.
        self.task_generator.generate_day_plan()  # Wygenerowanie nowego planu.
        self.task_manager.sort_tasks()  # Posortowanie zadań.

    def export_to_pdf(self):  # Eksportowanie listy zadań do pliku PDF.
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("Pliki PDF", "*.pdf")],
                                             title="Zapisz harmonogram jako PDF")
        if not file_path:
            return  # Jeśli użytkownik anulował zapis, zakończ funkcję.

        c = canvas.Canvas(file_path, pagesize=A4)  # Tworzenie dokumentu PDF w formacie A4.
        width, height = A4  # Pobranie szerokości i wysokości strony.
        y_position = height - 50  # Ustawienie początkowej pozycji tekstu na stronie.

        c.setFont("Helvetica-Bold", 16)  # Ustawienie czcionki nagłówka.
        c.drawString(50, y_position, "Harmonogram dnia")  # Dodanie tytułu w pliku PDF.
        y_position -= 30  # Przesunięcie pozycji w dół.

        c.setFont("Helvetica", 12)  # Ustawienie czcionki dla zadań.
        for task in self.task_manager.tasks:  # Iteracja po zadaniach.
            c.drawString(50, y_position, f"- {task.text}")  # Dodanie zadania do pliku PDF.
            y_position -= 20  # Przesunięcie pozycji w dół.
            if y_position < 50:  # Jeśli brakuje miejsca na stronie, dodaj nową stronę.
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 50

        c.save()  # Zapisanie pliku PDF.

class TaskManager:  # Klasa zarządzająca listą zadań.
    def __init__(self, parent):  # Konstruktor klasy.
        self.parent = parent  # Przechowywanie referencji do nadrzędnego obiektu GUI.
        self.tasks = []  # Lista przechowująca zadania.

    def add_task(self, text, done=False):  # Funkcja dodająca nowe zadanie.
        task = Task(self.parent.task_container, text, done, self.remove_task, self.save_tasks)  
        # Tworzenie nowego obiektu Task i przekazanie mu kontenera, tekstu, stanu wykonania oraz funkcji obsługi.
        self.tasks.append(task)  # Dodanie zadania do listy.
        self.save_tasks()  # Zapisanie zadań do pliku.
        self.sort_tasks()  # Posortowanie zadań.

    def remove_task(self, task):  # Funkcja usuwająca zadanie.
        if task in self.tasks:  # Sprawdzenie, czy zadanie istnieje w liście.
            self.tasks.remove(task)  # Usunięcie zadania z listy.
            task.frame.destroy()  # Usunięcie graficznego elementu zadania.
            self.save_tasks()  # Ponowne zapisanie listy zadań.

    def save_tasks(self):  # Funkcja zapisująca zadania do pliku JSON.
        tasks_data = [{"text": task.text, "done": task.done} for task in self.tasks]  
        # Tworzenie listy słowników z informacjami o zadaniach.
        with open(DATA_FILE, "w") as file:  
            # Otwarcie pliku JSON w trybie zapisu.
            json.dump(tasks_data, file)  
            # Zapisanie danych do pliku w formacie JSON.

    def load_tasks(self):  # Funkcja ładująca zadania z pliku JSON.
        if os.path.exists(DATA_FILE):  # Sprawdzenie, czy plik istnieje.
            with open(DATA_FILE, "r") as file:  # Otwarcie pliku w trybie odczytu.
                try:
                    tasks_data = json.load(file)  # Wczytanie danych JSON.
                    for task_data in tasks_data:  # Iteracja po wczytanych zadaniach.
                        self.add_task(task_data["text"], task_data.get("done", False))  
                        # Dodanie zadania do listy.
                except json.JSONDecodeError:  # Obsługa błędu, jeśli plik nie jest poprawnym JSON-em.
                    pass  # Po prostu pomijamy błąd i nie wczytujemy danych.

    def remove_auto_tasks(self):  # Funkcja usuwająca automatycznie wygenerowane zadania.
        tasks_to_remove = [task for task in self.tasks if "[AUTO]" in task.text]  
        # Tworzenie listy zadań, które zawierają znacznik [AUTO].
        for task in tasks_to_remove:  # Iteracja po zadaniach do usunięcia.
            task.frame.destroy()  # Usunięcie elementu graficznego zadania.
            self.tasks.remove(task)  # Usunięcie zadania z listy.
        self.refresh_tasks()  # Odświeżenie wyświetlanej listy zadań.
        self.sort_tasks()  # Ponowne posortowanie zadań.

    def sort_tasks(self):  # Funkcja sortująca zadania według godziny.
        def extract_time(task):  # Funkcja pomocnicza wyciągająca godzinę z tekstu zadania.
            parts = task.text.split(" - ", 1)  # Rozdzielenie tekstu zadania po znaku " - ".
            if len(parts) > 1 and ":" in parts[0]:  # Sprawdzenie, czy pierwsza część zawiera godzinę.
                try:
                    return datetime.datetime.strptime(parts[0], "%H:%M").time()  
                    # Konwersja na obiekt czasu.
                except ValueError:
                    return datetime.time(23, 59)  
                    # Jeśli nie udało się sparsować godziny, przypisz 23:59.
            return datetime.time(23, 59)  # Jeśli brak godziny, przypisz 23:59.

        self.tasks.sort(key=lambda task: extract_time(task))  # Sortowanie listy zadań według czasu.
        self.refresh_tasks()  # Odświeżenie listy po sortowaniu.

    def refresh_tasks(self):  # Funkcja odświeżająca wyświetlaną listę zadań.
        for task in self.tasks:  
            task.frame.pack_forget()  # Ukrycie wszystkich elementów zadań.
        for task in self.tasks:  
            task.frame.pack(fill="x", padx=5, pady=5)  
            # Ponowne wyświetlenie zadań w odpowiedniej kolejności.

class Task:  # Klasa reprezentująca pojedyncze zadanie.
    def __init__(self, parent, text, done, remove_callback, update_callback):  # Konstruktor klasy.
        self.parent = parent  # Przechowywanie referencji do nadrzędnego kontenera.
        self.text = text  # Tekst zadania.
        self.done = done  # Status wykonania (True - wykonane, False - niewykonane).
        self.remove_callback = remove_callback  # Funkcja do usunięcia zadania.
        self.update_callback = update_callback  # Funkcja do aktualizacji listy zadań.

        self.frame = ctk.CTkFrame(self.parent)  
        # Tworzenie ramki dla zadania wewnątrz kontenera.
        self.frame.pack(fill="x", padx=5, pady=5)  
        # Wyświetlenie ramki, rozszerzając ją na całą szerokość kontenera.

        self.check_var = ctk.BooleanVar(value=self.done)  
        # Tworzenie zmiennej przechowującej stan zaznaczenia checkboxa.
        self.checkbox = ctk.CTkCheckBox(
            self.frame, text="", variable=self.check_var, command=self.toggle_done,  
            checkmark_color="white", fg_color="green", border_color="green"
        )  
        # Tworzenie przycisku wyboru (checkboxa) do oznaczania wykonania zadania.
        self.checkbox.pack(side="left", padx=5)  
        # Umieszczenie checkboxa po lewej stronie.

        self.label = ctk.CTkLabel(self.frame, text=self.text)  
        # Tworzenie etykiety z tekstem zadania.
        self.label.pack(side="left", expand=True, padx=5)  
        # Umieszczenie etykiety po lewej stronie, pozwalając jej rozszerzać się.

        self.delete_button = ctk.CTkButton(self.frame, text="Usuń", fg_color="red", command=self.remove, width=5)  
        # Tworzenie przycisku "Usuń" do usuwania zadania.
        self.delete_button.pack(side="right", padx=5)  
        # Umieszczenie przycisku po prawej stronie.

        self.update_style()  # Wywołanie funkcji do ustawienia stylu etykiety.

    def toggle_done(self):  # Funkcja obsługująca zmianę stanu wykonania zadania.
        self.done = self.check_var.get()  # Aktualizacja statusu wykonania.
        self.update_style()  # Aktualizacja stylu zadania (koloru tekstu).
        self.update_callback()  # Wywołanie funkcji zapisującej stan zadań.

    def update_style(self):  # Funkcja aktualizująca wygląd zadania.
        self.label.configure(text_color="green" if self.done else "white")  
        # Jeśli zadanie wykonane, kolor tekstu jest zielony, w przeciwnym razie biały.

    def remove(self):  # Funkcja usuwająca zadanie.
        self.frame.destroy()  # Usunięcie elementu graficznego zadania.
        self.remove_callback(self)  # Wywołanie funkcji usuwającej zadanie z listy.

class TaskGenerator:  # Klasa odpowiedzialna za generowanie planu dnia na podstawie wariantów.
    def __init__(self, task_manager, day_type_var, day_variations):  # Konstruktor klasy.
        self.task_manager = task_manager  # Referencja do menedżera zadań.
        self.day_type_var = day_type_var  # Zmienna przechowująca wybrany typ dnia.
        self.day_variations = day_variations  # Słownik przechowujący warianty zadań dla różnych typów dnia.

    def generate_day_plan(self):  # Funkcja generująca plan dnia.
        day_type = self.day_type_var.get()  # Pobranie aktualnie wybranego typu dnia.
        if day_type in self.day_variations:  # Sprawdzenie, czy istnieją warianty dla wybranego dnia.
            tasks = random.choice(self.day_variations[day_type])  
            # Losowy wybór jednej listy zadań z dostępnych wariantów dla danego dnia.
            for time, task in tasks:  # Iteracja przez listę wybranych zadań.
                self.task_manager.add_task(f"{time} - {task} [AUTO]")  
                # Dodanie zadania do menedżera zadań, oznaczonego jako automatycznie wygenerowane.
            self.task_manager.sort_tasks()  # Posortowanie listy zadań po czasie.

if __name__ == "__main__":  # Sprawdzenie, czy skrypt jest uruchamiany bezpośrednio.
    app = ToDoApp()  # Utworzenie instancji aplikacji.
    app.mainloop()  # Uruchomienie głównej pętli aplikacji.
