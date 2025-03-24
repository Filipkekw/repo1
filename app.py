import customtkinter as ctk  # Importowanie biblioteki CustomTkinter do tworzenia nowoczesnych interfejsów graficznych.
import json  # Import modułu json, który umożliwia zapis i odczyt danych w formacie JSON.
import os  # Import modułu os, który pozwala na operacje na plikach i ścieżkach.
import random  # Import modułu random, który umożliwia losowy wybór elementów.
import datetime  # Import modułu datetime do obsługi dat i godzin.
import reportlab  # Import biblioteki ReportLab do generowania plików PDF.
from reportlab.lib.pagesizes import A4  # Import stałej A4 określającej rozmiar strony PDF.
from reportlab.pdfgen import canvas  # Import narzędzia canvas do rysowania zawartości na stronach PDF.
from tkinter import filedialog  # Import modułu filedialog z Tkinter do wyświetlania okien zapisu/otwarcia plików.
from reportlab.pdfbase import pdfmetrics  # Import modułu pdfmetrics z ReportLab do rejestracji czcionek.
from reportlab.pdfbase.ttfonts import TTFont  # Import klasy TTFont do obsługi czcionek TrueType.

font_path = os.path.join(os.path.dirname(__file__), "fonts", "Aller_Lt.ttf")  # Buduje ścieżkę do pliku czcionki "Aller_Lt.ttf" znajdującego się w folderze "fonts" obok pliku skryptu.
pdfmetrics.registerFont(TTFont('Aller_Lt', font_path))  # Rejestracja czcionki "Aller_Lt" w ReportLab, dzięki czemu będzie można jej używać przy generowaniu PDF.

DATA_FILE = "tasks.json"  # Stała określająca nazwę pliku JSON, w którym przechowywane są zadania oraz wybrany plan dnia.
DAY_VARIATIONS_FILE = "day_variations.json"  # Stała określająca nazwę pliku JSON z wariantami planów dnia.

class CustomMessageBox(ctk.CTkToplevel):  # Definicja klasy CustomMessageBox dziedziczącej po CTkToplevel – tworzy niestandardowe okno dialogowe.
    def __init__(self, parent, title, message, callback):  # Konstruktor klasy, przyjmuje rodzica, tytuł, wiadomość i funkcję callback.
        super().__init__(parent)  # Inicjalizacja klasy nadrzędnej (CTkToplevel) z rodzicem.
        self.title(title)  # Ustawia tytuł okna dialogowego.
        self.geometry("300x150")  # Ustawia rozmiar okna dialogowego na 300x150 pikseli.
        self.callback = callback  # Przechowuje funkcję callback, która zostanie wywołana po wyborze użytkownika.
        self.grab_set()  # Ustawia okno jako modalne, blokując interakcję z głównym oknem.

        ctk.CTkLabel(self, text=message, font=("Arial", 14)).pack(pady=10)  # Tworzy etykietę z przekazaną wiadomością i ustawia margines pionowy 10 pikseli.

        button_frame = ctk.CTkFrame(self)  # Tworzy ramkę, która będzie zawierała przyciski.
        button_frame.pack(pady=10)  # Umieszcza ramkę z marginesem pionowym 10 pikseli.

        ctk.CTkButton(button_frame, text="Tak", fg_color="green", command=lambda: self.answer(True)).pack(side="left", padx=10)  
        # Tworzy przycisk "Tak" z zielonym tłem, który po kliknięciu wywoła metodę answer z argumentem True; przycisk jest umieszczony po lewej stronie z marginesem poziomym 10 pikseli.
        ctk.CTkButton(button_frame, text="Nie", fg_color="red", command=lambda: self.answer(False)).pack(side="right", padx=10)  
        # Tworzy przycisk "Nie" z czerwonym tłem, który wywoła metodę answer z argumentem False; przycisk jest umieszczony po prawej stronie z marginesem poziomym 10 pikseli.

    def answer(self, response):  # Metoda obsługująca wybór użytkownika.
        self.callback(response)  # Wywołuje przekazaną funkcję callback z odpowiedzią (True/False).
        self.destroy()  # Zamyka okno dialogowe.

def save_default_day_variations():
    default_variations = {  # Definicja słownika zawierającego domyślne warianty planów dnia.
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
    
    if not os.path.exists(DAY_VARIATIONS_FILE):  # Jeśli plik z wariantami dni nie istnieje, zapisz domyślne dane.
        with open(DAY_VARIATIONS_FILE, "w", encoding="utf-8") as file:
            json.dump(default_variations, file, ensure_ascii=False, indent=4)  # Zapisuje dane do pliku w formacie JSON.

save_default_day_variations()  # Wywołanie funkcji zapisującej domyślne warianty planów dnia.

def load_day_variations():  # Funkcja do wczytywania wariantów planów dnia z pliku JSON.
    if os.path.exists(DAY_VARIATIONS_FILE):  # Sprawdza, czy plik istnieje.
        with open(DAY_VARIATIONS_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)  # Próbuje wczytać dane z pliku.
            except json.JSONDecodeError:
                return {}  # W przypadku błędu zwraca pusty słownik.
    return {}  # Jeśli plik nie istnieje, zwraca pusty słownik.

day_variations = load_day_variations()  # Przechowuje warianty planów dnia.
day_types = list(day_variations.keys())  # Tworzy listę nazw planów (kluczy ze słownika).

class ToDoApp(ctk.CTk):  # Główna klasa aplikacji, dziedziczy po CTk (okno główne CustomTkinter).
    def __init__(self):
        super().__init__()  # Inicjalizacja klasy nadrzędnej.
        self.title("To-Do List")  # Ustawia tytuł głównego okna.
        self.geometry("600x900")  # Ustawia rozmiar okna.

        self.task_manager = TaskManager(self)  # Tworzy instancję menedżera zadań.
        self.day_type_var = ctk.StringVar(value="Plan dnia")  # Inicjalizuje zmienną przechowującą wybrany plan dnia (domyślnie "Plan dnia").
        self.task_generator = TaskGenerator(self.task_manager, self.day_type_var, day_variations)  # Tworzy instancję generatora planu dnia.

        ctk.CTkLabel(self, text="Twoja Lista Zadań", font=("Arial", 16, "bold")).pack(pady=10)  # Dodaje etykietę tytułową na górze okna.

        top_frame = ctk.CTkFrame(self)  # Tworzy ramkę umieszczoną u góry, która podzieli przestrzeń na dwie kolumny.
        top_frame.pack(pady=5, fill="x")  # Umieszcza ramkę z marginesem pionowym 5 pikseli i wypełnia całą szerokość.

        left_frame = ctk.CTkFrame(top_frame)  # Tworzy lewą kolumnę wewnątrz ramki top_frame – przeznaczoną do dodawania zadań.
        left_frame.pack(side="left", fill="both", expand=True, padx=5)  # Umieszcza lewą kolumnę po lewej stronie z marginesem poziomym 5 pikseli.

        right_frame = ctk.CTkFrame(top_frame)  # Tworzy prawą kolumnę wewnątrz top_frame – przeznaczoną do wyboru planu dnia i generowania planu.
        right_frame.pack(side="right", fill="both", expand=True, padx=5)  # Umieszcza prawą kolumnę po prawej stronie z marginesem poziomym 5 pikseli.

        self.task_entry = ctk.CTkEntry(left_frame, width=250, placeholder_text="Treść zadania")  # Tworzy pole tekstowe do wpisywania treści zadania.
        self.task_entry.pack(pady=5)  # Umieszcza pole w lewej kolumnie z marginesem pionowym 5 pikseli.

        self.time_entry = ctk.CTkEntry(left_frame, width=60, placeholder_text="HH:MM")  # Tworzy pole tekstowe do wpisywania godziny zadania.
        self.time_entry.pack(pady=5)  # Umieszcza pole w lewej kolumnie.
        self.time_entry.bind("<KeyRelease>", self.format_time_entry)  # Podłącza zdarzenie formatowania wpisywanego czasu po każdej zwolnionej klawiszu.

        self.add_button = ctk.CTkButton(left_frame, text="Dodaj zadanie", fg_color="green", hover_color="darkgreen", command=self.add_task)  
        # Tworzy przycisk "Dodaj zadanie" z zielonym tłem, który wywołuje metodę add_task.
        self.add_button.pack(pady=5)  # Umieszcza przycisk z marginesem pionowym 5 pikseli.

        self.day_menu = ctk.CTkComboBox(right_frame, values=day_types, variable=self.day_type_var, state="readonly")  
        # Tworzy rozwijaną listę (ComboBox) w prawej kolumnie, zawierającą dostępne plany dnia; wartość jest przechowywana w day_type_var.
        self.day_menu.pack(pady=5)  # Umieszcza ComboBox z marginesem pionowym 5 pikseli.

        self.generate_button = ctk.CTkButton(right_frame, text="Wygeneruj plan dnia", fg_color="blue", hover_color="darkblue", command=self.generate_sorted_plan)  
        # Tworzy przycisk do generowania planu dnia, wywołujący metodę generate_sorted_plan.
        self.generate_button.pack(pady=5)  # Umieszcza przycisk z marginesem pionowym 5 pikseli.

        self.export_button = ctk.CTkButton(right_frame, text="Eksportuj do PDF", fg_color="purple", hover_color="darkviolet", command=self.export_to_pdf)  
        # Tworzy przycisk do eksportowania planu do pliku PDF, wywołujący metodę export_to_pdf.
        self.export_button.pack(pady=5)  # Umieszcza przycisk z marginesem pionowym 5 pikseli.

        self.task_container = ctk.CTkFrame(self)  # Tworzy główną ramkę, w której będą wyświetlane zadania.
        self.task_container.pack(pady=10, fill="both", expand=True)  # Umieszcza ramkę z marginesem pionowym 10 pikseli, rozciągając ją na całą przestrzeń.

        self.task_manager.load_tasks()  # Wywołuje metodę load_tasks menedżera zadań, która wczytuje zadania oraz zapisany plan dnia z pliku.

    def format_time_entry(self, event):  # Metoda formatująca wpisaną wartość w polu czasu.
        text = self.time_entry.get()  # Pobiera aktualny tekst z pola czasu.
        if len(text) == 2 and ":" not in text:  # Jeśli wpisano dwie cyfry i nie ma dwukropka,
            self.time_entry.insert(2, ":")  # wstawia dwukropek po drugiej cyfrze.

    def validate_time(self, time_text):  # Metoda walidująca poprawność formatu wpisanego czasu.
        try:
            if time_text == "HH:MM":  # Jeśli wpisana wartość to domyślny placeholder,
                return True  # uznajemy ją za poprawną.
            datetime.datetime.strptime(time_text, "%H:%M").time()  # Próbuje sparsować wpisany czas do formatu HH:MM.
            return True  # Jeśli parsowanie się powiedzie, zwraca True.
        except ValueError:
            return False  # W przypadku błędu zwraca False.

    def add_task(self):  # Metoda dodająca nowe zadanie.
        task_text = self.task_entry.get().strip()  # Pobiera treść zadania z pola tekstowego i usuwa białe znaki.
        time_text = self.time_entry.get().strip()  # Pobiera wpisaną godzinę i usuwa białe znaki.

        if not task_text:  # Jeśli treść zadania jest pusta,
            return  # przerywa wykonywanie metody.

        if time_text and time_text != "HH:MM" and not self.validate_time(time_text):  
            # Jeśli wpisano czas (różny od placeholdera) ale nie przechodzi walidacji,
            return  # przerywa dodawanie zadania.

        if time_text and time_text != "HH:MM":  
            task_text = f"{time_text} - {task_text}"  # Jeśli wpisano poprawny czas, łączy go z treścią zadania.

        self.task_manager.add_task(task_text)  # Dodaje zadanie do listy poprzez TaskManager.
        self.task_entry.delete(0, "end")  # Czyści pole wpisywania treści zadania.
        self.time_entry.delete(0, "end")  # Czyści pole wpisywania czasu.

    def generate_sorted_plan(self):  # Metoda generująca plan dnia z wariantów.
        if any("[AUTO]" in task.text for task in self.task_manager.tasks):  
            # Sprawdza, czy w liście zadań istnieje zadanie wygenerowane automatycznie (z markerem [AUTO]).
            CustomMessageBox(self, "Potwierdzenie", "Czy chcesz nadpisać istniejący plan dnia?", self.handle_confirmation)  
            # Jeśli tak, wyświetla okno potwierdzenia.
        else:
            self.execute_generation()  # Jeśli nie, bezpośrednio wywołuje metodę generującą plan.

    def handle_confirmation(self, response):  # Metoda obsługująca odpowiedź z okna potwierdzenia.
        if response:  # Jeśli użytkownik potwierdzi (True),
            self.execute_generation()  # wywołuje generowanie planu.

    def execute_generation(self):  # Metoda wykonująca generowanie planu dnia.
        self.task_manager.remove_auto_tasks()  # Usuwa wcześniej wygenerowane zadania (te z markerem [AUTO]).
        self.task_generator.generate_day_plan()  # Wywołuje metodę generatora, która generuje nowy plan dnia.
        self.task_manager.sort_tasks()  # Sortuje zadania (np. według czasu).

    def export_to_pdf(self):
        # Tworzymy domyślną nazwę pliku na podstawie aktualnej daty.
        default_filename = f"harmonogram_{datetime.datetime.now().strftime('%Y_%m_%d')}.pdf"
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,  # Domyślna nazwa pliku.
            defaultextension=".pdf",
            filetypes=[("Pliki PDF", "*.pdf")],
            title="Zapisz harmonogram jako PDF"
        )
        if not file_path:
            return

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y_position = height - 50

        generation_date = datetime.datetime.now().strftime("%Y-%m-%d")
        selected_plan = self.day_type_var.get()

        c.setFont("Aller_Lt", 16)
        c.drawString(50, y_position, "Harmonogram dnia")
        y_position -= 30

        c.setFont("Aller_Lt", 12)
        c.drawString(50, y_position, f"Data: {generation_date}")
        y_position -= 20

        c.drawString(50, y_position, f"Plan dnia: {selected_plan}")
        y_position -= 30

        c.setFont("Aller_Lt", 12)
        for task in self.task_manager.tasks:
            c.drawString(50, y_position, f"- {task.text}")
            y_position -= 20
            if y_position < 50:
                c.showPage()
                c.setFont("Aller_Lt", 12)
                y_position = height - 50

        c.save()

class TaskManager:  # Klasa zarządzająca zadaniami w aplikacji.
    def __init__(self, parent):
        self.parent = parent  # Przechowuje referencję do głównego okna aplikacji.
        self.tasks = []  # Inicjalizuje listę zadań jako pustą listę.

    def add_task(self, text, done=False):  # Metoda dodająca nowe zadanie.
        task = Task(self.parent.task_container, text, done, self.remove_task, self.save_tasks)  
        # Tworzy instancję klasy Task przekazując kontener, tekst, stan wykonania, funkcję usuwania i aktualizacji.
        self.tasks.append(task)  # Dodaje nowe zadanie do listy.
        self.save_tasks()  # Zapisuje aktualną listę zadań do pliku.
        self.sort_tasks()  # Sortuje zadania (np. według czasu).

    def remove_task(self, task):  # Metoda usuwająca zadanie.
        if task in self.tasks:  # Sprawdza, czy zadanie istnieje na liście.
            self.tasks.remove(task)  # Usuwa zadanie z listy.
            task.frame.destroy()  # Usuwa graficzny element zadania.
            self.save_tasks()  # Aktualizuje zapisane dane.

    def save_tasks(self):  # Metoda zapisująca zadania do pliku JSON.
        tasks_data = {  # Przygotowuje dane do zapisu w formie słownika.
            "plan": self.parent.day_type_var.get(),  # Zapisuje aktualnie wybrany plan dnia.
            "tasks": [{"text": task.text, "done": task.done} for task in self.tasks]  # Zapisuje listę zadań jako listę słowników.
        }
        with open(DATA_FILE, "w") as file:  # Otwiera plik DATA_FILE w trybie zapisu.
            json.dump(tasks_data, file, indent=4)  # Zapisuje dane w formacie JSON z wcięciami.

    def load_tasks(self):  # Metoda wczytująca zadania z pliku JSON.
        if os.path.exists(DATA_FILE):  # Sprawdza, czy plik istnieje.
            with open(DATA_FILE, "r") as file:  # Otwiera plik w trybie odczytu.
                try:
                    data = json.load(file)  # Próbuje wczytać dane z pliku.
                    if isinstance(data, dict):  # Jeśli dane są w formie słownika (nowy format),
                        plan = data.get("plan", None)  # Pobiera zapisany plan dnia.
                        if plan:
                            self.parent.day_type_var.set(plan)  # Ustawia wybrany plan dnia w interfejsie.
                        tasks_data = data.get("tasks", [])  # Pobiera listę zadań.
                        for task_data in tasks_data:  # Iteruje po liście zadań.
                            self.add_task(task_data["text"], task_data.get("done", False))  # Dodaje każde zadanie do listy.
                    else:  # Jeśli dane są w starszym formacie (lista zadań),
                        for task_data in data:
                            self.add_task(task_data["text"], task_data.get("done", False))  # Dodaje zadania do listy.
                except json.JSONDecodeError:
                    pass  # W przypadku błędu odczytu JSON, pomija wczytywanie.

    def remove_auto_tasks(self):  # Metoda usuwająca automatycznie wygenerowane zadania (z markerem [AUTO]).
        tasks_to_remove = [task for task in self.tasks if "[AUTO]" in task.text]  # Tworzy listę zadań zawierających "[AUTO]".
        for task in tasks_to_remove:  # Iteruje po zadaniach do usunięcia.
            task.frame.destroy()  # Usuwa graficzny element zadania.
            self.tasks.remove(task)  # Usuwa zadanie z listy.
        self.refresh_tasks()  # Odświeża widok zadań.
        self.sort_tasks()  # Sortuje zadania ponownie.

    def sort_tasks(self):  # Metoda sortująca zadania według godziny.
        def extract_time(task):  # Funkcja pomocnicza, która wyciąga godzinę z treści zadania.
            parts = task.text.split(" - ", 1)  # Dzieli tekst zadania przy pierwszym wystąpieniu " - ".
            if len(parts) > 1 and ":" in parts[0]:  # Jeśli pierwsza część zawiera dwukropek (czyli jest godziną),
                try:
                    return datetime.datetime.strptime(parts[0], "%H:%M").time()  # Parsuje godzinę i zwraca obiekt czasu.
                except ValueError:
                    return datetime.time(23, 59)  # W przypadku błędu, przypisuje maksymalny czas 23:59.
            return datetime.time(23, 59)  # Jeśli godziny nie ma, zwraca domyślny czas 23:59.
        self.tasks.sort(key=lambda task: extract_time(task))  # Sortuje listę zadań na podstawie wyekstrahowanego czasu.
        self.refresh_tasks()  # Odświeża wyświetlanie zadań.

    def refresh_tasks(self):  # Metoda odświeżająca wyświetlanie zadań.
        for task in self.tasks:  # Dla każdego zadania,
            task.frame.pack_forget()  # ukrywa ramkę zadania.
        for task in self.tasks:  # Następnie, dla każdego zadania,
            task.frame.pack(fill="x", padx=5, pady=5)  # wyświetla ramkę, rozciągając ją na całą szerokość z marginesami.

class Task:  # Klasa reprezentująca pojedyncze zadanie.
    def __init__(self, parent, text, done, remove_callback, update_callback):
        self.parent = parent  # Przechowuje referencję do kontenera, w którym zadanie będzie wyświetlone.
        self.text = text  # Przechowuje tekst zadania.
        self.done = done  # Przechowuje stan zadania (wykonane lub nie).
        self.remove_callback = remove_callback  # Przechowuje funkcję, która usunie zadanie.
        self.update_callback = update_callback  # Przechowuje funkcję, która zaktualizuje zapisane zadania.

        self.frame = ctk.CTkFrame(self.parent)  # Tworzy ramkę, która będzie zawierać graficzne elementy zadania.
        self.frame.pack(fill="x", padx=5, pady=5)  # Umieszcza ramkę, rozciągając ją na całą szerokość z marginesami.

        self.check_var = ctk.BooleanVar(value=self.done)  # Tworzy zmienną boolowską przechowującą stan wykonania zadania.
        self.checkbox = ctk.CTkCheckBox(
            self.frame, text="", variable=self.check_var, command=self.toggle_done,
            checkmark_color="white", fg_color="green", border_color="green"
        )  # Tworzy checkbox, który umożliwia zaznaczenie wykonania zadania.
        self.checkbox.pack(side="left", padx=5)  # Umieszcza checkbox po lewej stronie ramki z marginesem.

        self.label = ctk.CTkLabel(self.frame, text=self.text)  # Tworzy etykietę wyświetlającą tekst zadania.
        self.label.pack(side="left", expand=True, padx=5)  # Umieszcza etykietę po lewej stronie, umożliwiając jej rozszerzenie.

        self.delete_button = ctk.CTkButton(self.frame, text="Usuń", fg_color="red", command=self.remove, width=5)  
        # Tworzy przycisk "Usuń", który wywołuje metodę remove, usuwając zadanie.
        self.delete_button.pack(side="right", padx=5)  # Umieszcza przycisk po prawej stronie z marginesem.
        self.update_style()  # Wywołuje metodę update_style, która ustawia styl etykiety w zależności od stanu zadania.

    def toggle_done(self):  # Metoda zmieniająca stan wykonania zadania.
        self.done = self.check_var.get()  # Aktualizuje stan na podstawie wartości checkboxa.
        self.update_style()  # Aktualizuje styl (np. kolor tekstu) zadania.
        self.update_callback()  # Wywołuje funkcję aktualizującą zapisane zadania.

    def update_style(self):  # Metoda aktualizująca wygląd etykiety zadania.
        self.label.configure(text_color="green" if self.done else "white")  # Ustawia kolor tekstu: zielony, jeśli zadanie wykonane, lub biały, jeśli nie.

    def remove(self):  # Metoda usuwająca zadanie.
        self.frame.destroy()  # Usuwa graficzny element zadania.
        self.remove_callback(self)  # Wywołuje funkcję usuwającą zadanie z listy.

class TaskGenerator:  # Klasa odpowiedzialna za generowanie planu dnia z wariantów.
    def __init__(self, task_manager, day_type_var, day_variations):
        self.task_manager = task_manager  # Przechowuje referencję do TaskManager.
        self.day_type_var = day_type_var  # Przechowuje referencję do zmiennej przechowującej wybrany plan dnia.
        self.day_variations = day_variations  # Przechowuje słownik wariantów planów dnia.

    def generate_day_plan(self):  # Metoda generująca plan dnia.
        day_type = self.day_type_var.get()  # Pobiera aktualnie wybrany plan dnia.
        if day_type in self.day_variations:  # Sprawdza, czy dla wybranego planu istnieją warianty.
            tasks = random.choice(self.day_variations[day_type])  # Losowo wybiera jedną listę zadań z dostępnych wariantów.
            for time, task in tasks:  # Dla każdej pary (czas, opis) w wybranym wariancie,
                self.task_manager.add_task(f"{time} - {task} [AUTO]")  # Dodaje zadanie oznaczone jako [AUTO] do listy.
            self.task_manager.sort_tasks()  # Sortuje zadania po dodaniu.

if __name__ == "__main__":  # Punkt wejścia do programu – wykonywany, gdy skrypt jest uruchamiany bezpośrednio.
    app = ToDoApp()  # Tworzy instancję głównej aplikacji.
    app.mainloop()  # Uruchamia główną pętlę aplikacji, dzięki czemu okno pozostaje otwarte.
