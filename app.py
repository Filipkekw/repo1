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
import platform  # Import modułu platform, który pozwala sprawdzić system operacyjny.
import darkdetect  # Import biblioteki darkdetect do wykrywania, czy system używa trybu ciemnego.
import subprocess  # Import modułu subprocess, który umożliwia wykonywanie poleceń systemowych.

# Ścieżka do pliku czcionki "Aller_Lt.ttf" znajdującego się w katalogu "fonts" obok skryptu.
font_path = os.path.join(os.path.dirname(__file__), "fonts", "Aller_Lt.ttf")
# Rejestracja czcionki "Aller_Lt" w bibliotece ReportLab, aby można jej było używać w plikach PDF.
pdfmetrics.registerFont(TTFont('Aller_Lt', font_path))

# Definicje nazw plików używanych do przechowywania danych aplikacji.
DATA_FILE = "tasks.json"  # Plik JSON przechowujący zadania użytkownika.
DAY_VARIATIONS_FILE = "day_variations.json"  # Plik JSON z wariantami planów dnia.
SETTINGS_FILE = "settings.json"  # Plik JSON przechowujący ustawienia aplikacji (np. preferowany motyw).

def get_linux_appearance():
    try:
        # Wykonanie komendy systemowej, która pobiera aktywny motyw GTK.
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],  # Komenda odczytująca nazwę aktywnego motywu GTK.
            capture_output=True, text=True, check=True  # Przechwycenie wyniku jako tekst.
        )
        theme = result.stdout.strip().strip("'").lower()  # Usunięcie zbędnych znaków i zamiana na małe litery.

        # Sprawdzenie, czy nazwa motywu zawiera "dark", co oznacza tryb ciemny.
        if "dark" in theme:
            return "dark"  # Zwrócenie wartości "dark", jeśli użytkownik używa ciemnego motywu.
        return "light"  # W przeciwnym razie zwrócenie wartości "light".
    except Exception:
        return "light"  # W razie błędu domyślnie zwracany jest jasny motyw.


# Funkcja zapisująca domyślne warianty planów dnia.
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

def load_day_variations():
    # Sprawdza, czy plik z wariantami planów dnia istnieje
    if os.path.exists(DAY_VARIATIONS_FILE):
        with open(DAY_VARIATIONS_FILE, "r", encoding="utf-8") as file:
            try:
                # Próbuje wczytać dane z pliku JSON
                return json.load(file)
            except json.JSONDecodeError:
                # Jeśli plik JSON jest uszkodzony lub niepoprawny, zwraca pusty słownik
                return {}
    # Jeśli plik nie istnieje, zwraca pusty słownik
    return {}

# Wczytuje warianty planów dnia z pliku JSON
day_variations = load_day_variations()
# Tworzy listę nazw dostępnych wariantów planów dnia
day_types = list(day_variations.keys())

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, master, title, message, on_confirm):
        super().__init__(master)  # Inicjalizuje okno dialogowe jako `Toplevel`

        self.title(title)  # Ustawia tytuł okna dialogowego
        self.geometry("300x175")  # Ustawia rozmiar okna na 300x175 pikseli
        self.on_confirm = on_confirm  # Przechowuje funkcję wywoływaną po wyborze

        # Tworzy etykietę (label) z wiadomością dla użytkownika
        self.label = ctk.CTkLabel(self, text=message)
        self.label.pack(pady=20)  # Dodaje odstęp pionowy (20 pikseli)

        # Tworzy przycisk "Tak", który potwierdza akcję
        self.confirm_button = ctk.CTkButton(self, text="Tak", command=self.confirm, fg_color="green")
        self.confirm_button.pack(pady=10)  # Dodaje odstęp pionowy (10 pikseli)

        # Tworzy przycisk "Nie", który anuluje akcję
        self.cancel_button = ctk.CTkButton(self, text="Nie", command=self.cancel, fg_color="red")
        self.cancel_button.pack(pady=5)  # Dodaje odstęp pionowy (5 pikseli)

        self.update_idletasks()  # Aktualizuje interfejs, aby poprawnie wyświetlić elementy
        self.wait_visibility()  # Czeka, aż okno stanie się widoczne
        self.grab_set()  # Blokuje interakcję z głównym oknem aplikacji, dopóki użytkownik nie zamknie tego okna

    def confirm(self):
        self.on_confirm(True)  # Wywołuje funkcję zwrotną `on_confirm`, przekazując wartość `True`
        self.destroy()  # Zamknięcie okna dialogowego

    def cancel(self):
        self.on_confirm(False)  # Wywołuje funkcję zwrotną `on_confirm`, przekazując wartość `False`
        self.destroy()  # Zamknięcie okna dialogowego

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()  # Inicjalizacja klasy nadrzędnej `CTk` (główne okno aplikacji)

        # Wykrywanie systemowego motywu – uwzględnienie systemu Linux
        if platform.system() == "Linux":
            actual_theme = get_linux_appearance()  # Pobiera motyw systemowy dla Linuxa
            ctk.set_appearance_mode("dark" if actual_theme == "dark" else "light")  # Ustawia motyw na ciemny lub jasny
        else:
            # Dla systemów Windows i macOS sprawdza, czy system używa ciemnego motywu
            if darkdetect.isDark():
                ctk.set_appearance_mode("dark")  # Ustawia ciemny motyw
            else:
                ctk.set_appearance_mode("light")  # Ustawia jasny motyw

        self.system_theme = ctk.get_appearance_mode()  # Pobiera aktualnie ustawiony motyw

        self.title("To-Do List")  # Ustawia tytuł okna aplikacji
        self.geometry("600x900")  # Ustawia rozmiar okna aplikacji na 600x900 pikseli

        # Tworzy górny pasek interfejsu
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(side="top", fill="x")  # Umieszcza pasek na górze okna, rozciągając go na całą szerokość

        # Ustalanie opcji motywu w zależności od systemu operacyjnego
        if platform.system() == "Linux":
            theme_options = ["Jasny", "Ciemny"]  # Na Linuxie dostępne są tylko dwa tryby
            self.theme_var = ctk.StringVar(value="Ciemny")  # Domyślnie ustawiony tryb ciemny
        else:
            theme_options = ["System", "Jasny", "Ciemny"]  # Na Windowsie i macOS dodana opcja "System"
            self.theme_var = ctk.StringVar(value="System")  # Domyślnie ustawiony tryb systemowy

        self.task_manager = TaskManager(self)  # Inicjalizacja menedżera zadań

        # Tworzy rozwijane menu do wyboru motywu aplikacji
        self.theme_menu = ctk.CTkComboBox(
            master=top_bar,
            values=theme_options,  # Lista dostępnych opcji motywu
            variable=self.theme_var,  # Powiązanie wyboru z `self.theme_var`
            command=self.change_theme,  # Wywołanie metody zmieniającej motyw po wyborze
            width=120,  # Szerokość rozwijanego menu
            state="readonly"  # Opcja `readonly` uniemożliwia ręczne wpisywanie wartości
        )
        self.theme_menu.pack(side="right", padx=10, pady=10)  # Umieszcza menu po prawej stronie paska

        self.load_settings()  # Wczytuje zapisane ustawienia aplikacji (np. ostatnio używany motyw)
        self.change_theme(self.theme_var.get())  # Ustawia motyw na podstawie zapisanych ustawień
        self.update_task_text_color()  # Aktualizuje kolor tekstu zadań w zależności od motywu

        self.day_type_var = ctk.StringVar(value="Plan dnia")  # Zmienna przechowująca aktualnie wybrany typ dnia
        self.task_generator = TaskGenerator(self.task_manager, self.day_type_var, day_variations)  # Generator zadań

        # Tworzy nagłówek aplikacji
        ctk.CTkLabel(self, text="Twoja Lista Zadań", font=("Arial", 16, "bold")).pack(pady=10)

        # Tworzy główny kontener dla elementów interfejsu
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(pady=5, fill="x")  # Dodaje odstęp i wypełnia szerokość okna

        # Lewa część interfejsu (pole do wpisywania zadań)
        left_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Prawa część interfejsu (wybór planu dnia i generowanie zadań)
        right_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)

        # Pole tekstowe do wpisania treści zadania
        self.task_entry = ctk.CTkEntry(left_frame, width=250, placeholder_text="Treść zadania")
        self.task_entry.pack(pady=5)

        # Pole do wpisania godziny zadania (format HH:MM)
        self.time_entry = ctk.CTkEntry(left_frame, width=60, placeholder_text="HH:MM")
        self.time_entry.pack(pady=5)
        self.time_entry.bind("<KeyRelease>", self.format_time_entry)  # Formatowanie tekstu podczas wpisywania

        # Przycisk dodawania nowego zadania
        self.add_button = ctk.CTkButton(left_frame, text="Dodaj zadanie", fg_color="green", hover_color="darkgreen", command=self.add_task)
        self.add_button.pack(pady=5)

        # Rozwijane menu do wyboru planu dnia
        self.day_menu = ctk.CTkComboBox(right_frame, values=day_types, variable=self.day_type_var, state="readonly")
        self.day_menu.pack(pady=5)

        # Przycisk generowania planu dnia
        self.generate_button = ctk.CTkButton(right_frame, text="Wygeneruj plan dnia", fg_color="blue", hover_color="darkblue", command=self.generate_sorted_plan)
        self.generate_button.pack(pady=5)

        # Przycisk eksportowania planu dnia do pliku PDF
        self.export_button = ctk.CTkButton(right_frame, text="Eksportuj do PDF", fg_color="purple", hover_color="darkviolet", command=self.export_to_pdf)
        self.export_button.pack(pady=5)

        # Główne okno na listę zadań
        self.task_container = ctk.CTkFrame(self, fg_color="transparent")
        self.task_container.pack(pady=10, fill="both", expand=True)

        self.summary_button = ctk.CTkButton(self, text="Podsumowanie dnia", fg_color="purple", hover_color="darkviolet", command=self.daily_summary)
        self.summary_button.pack(pady=10)

        self.task_manager.load_tasks()  # Wczytuje zapisane zadania
        self.update_task_text_color()  # Aktualizuje kolory tekstu w zależności od motywu

    def format_time_entry(self, event):
        # Pobiera tekst z pola do wpisywania godziny
        text = self.time_entry.get()
        # Jeśli wpisano dokładnie dwa znaki i nie zawierają dwukropka, dodaje ":"
        if len(text) == 2 and ":" not in text:
            self.time_entry.insert(2, ":")

    def validate_time(self, time_text):
        try:
            # Jeśli użytkownik nie wpisał godziny, zwracamy True (pole może być puste)
            if time_text == "HH:MM":
                return True
            # Sprawdza, czy tekst pasuje do formatu godziny HH:MM
            datetime.datetime.strptime(time_text, "%H:%M").time()
            return True
        except ValueError:
            return False  # Jeśli wystąpił błąd, oznacza to niepoprawny format godziny

    def add_task(self):
        task_text = self.task_entry.get().strip()  # Pobiera i usuwa zbędne spacje z tekstu zadania
        time_text = self.time_entry.get().strip()  # Pobiera i usuwa zbędne spacje z pola czasu

        # Jeśli pole zadania jest puste, nie dodaje nic
        if not task_text:
            return

        # Jeśli użytkownik wpisał godzinę, sprawdza jej poprawność
        if time_text and time_text != "HH:MM" and not self.validate_time(time_text):
            return  # Jeśli godzina jest niepoprawna, nie dodaje zadania

        # Jeśli użytkownik wpisał godzinę, dodaje ją przed treścią zadania
        if time_text and time_text != "HH:MM":
            task_text = f"{time_text} - {task_text}"

        self.task_manager.add_task(task_text)  # Dodaje zadanie do listy
        self.task_entry.delete(0, "end")  # Czyści pole tekstowe zadania
        self.time_entry.delete(0, "end")  # Czyści pole wpisywania godziny
        self.update_task_text_color()  # Aktualizuje kolor tekstu zadania w zależności od motywu

    def generate_sorted_plan(self):
        if any("[AUTO]" in task.text for task in self.task_manager.tasks):
            # Jeśli istnieją zadania automatycznie wygenerowane, pyta użytkownika o potwierdzenie
            CustomMessageBox(self, "Potwierdzenie", "Czy chcesz nadpisać istniejący plan dnia?", self.handle_confirmation)
        else:
            self.execute_generation()  # Jeśli nie ma automatycznych zadań, od razu generuje plan dnia

    def handle_confirmation(self, response):
        if response:  # Jeśli użytkownik potwierdził, wykonuje generowanie planu
            self.execute_generation()

    def execute_generation(self):
        self.task_manager.remove_auto_tasks()  # Usuwa stare automatyczne zadania
        self.task_generator.generate_day_plan()  # Generuje nowy plan dnia
        self.task_manager.sort_tasks()  # Sortuje zadania według godzin

    def export_to_pdf(self):
        # Generuje domyślną nazwę pliku na podstawie aktualnej daty
        default_filename = f"harmonogram_{datetime.datetime.now().strftime('%Y_%m_%d')}.pdf"
        
        # Otwiera okno zapisu pliku
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,  # Domyślna nazwa pliku
            defaultextension=".pdf",  # Domyślne rozszerzenie pliku
            filetypes=[("Pliki PDF", "*.pdf")],  # Filtr plików
            title="Zapisz harmonogram jako PDF"  # Tytuł okna dialogowego
        )
        
        # Jeśli użytkownik nie podał nazwy pliku, anulujemy zapis
        if not file_path:
            return

        # Tworzenie nowego pliku PDF
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y_position = height - 50  # Pozycja początkowa tekstu

        # Pobranie aktualnej daty i wybranego planu dnia
        generation_date = datetime.datetime.now().strftime("%Y-%m-%d")
        selected_plan = self.day_type_var.get()

        # Nagłówek pliku PDF
        c.setFont("Aller_Lt", 16)
        c.drawString(50, y_position, "Harmonogram dnia")
        y_position -= 30

        # Dodanie daty i nazwy planu dnia
        c.setFont("Aller_Lt", 12)
        c.drawString(50, y_position, f"Data: {generation_date}")
        y_position -= 20
        c.drawString(50, y_position, f"Plan dnia: {selected_plan}")
        y_position -= 30

        # Wypisywanie zadań w pliku PDF
        c.setFont("Aller_Lt", 12)
        for task in self.task_manager.tasks:
            c.drawString(50, y_position, f"- {task.text}")
            y_position -= 20
            # Jeśli miejsce na stronie się skończy, tworzy nową stronę
            if y_position < 50:
                c.showPage()
                c.setFont("Aller_Lt", 12)
                y_position = height - 50

        c.save()  # Zapisuje plik PDF

    def change_theme(self, new_theme: str):
        if new_theme == "System":
            actual_theme = self.system_theme  # Używa wykrytego motywu systemowego
        else:
            # Mapa konwertująca nazwy z rozwijanego menu na wartości CustomTkinter
            mapping = {"Jasny": "Light", "Ciemny": "Dark"}
            actual_theme = mapping.get(new_theme, "Light")  # Domyślnie "Light", jeśli nieznana wartość

        ctk.set_appearance_mode(actual_theme)  # Ustawia nowy motyw

        # Jeśli menedżer zadań istnieje, aktualizuje kolory tekstu w zadaniach
        if hasattr(self, "task_manager") and self.task_manager:
            self.update_task_text_color()

        self.save_settings()  # Zapisuje nowe ustawienie motywu

    def update_task_text_color(self):
        if not hasattr(self, "task_manager") or not self.task_manager:
            return  # Jeśli menedżer zadań nie istnieje, kończy funkcję
        
        # Pobiera aktualnie ustawiony motyw
        current_theme = ctk.get_appearance_mode()
        text_color = "black" if current_theme == "Light" else "white"

        # Przechodzi przez wszystkie zadania i aktualizuje ich kolor tekstu
        for task in self.task_manager.tasks:
            if hasattr(task, "label"):
                task.label.configure(text_color=text_color)

    def save_settings(self):
        settings = {"theme": self.theme_var.get()}
        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file, indent=4)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                try:
                    settings = json.load(file)
                    if "theme" in settings:
                        self.theme_var.set(settings["theme"])
                        self.system_theme = ctk.get_appearance_mode()
                except json.JSONDecodeError:
                    pass  # Jeśli plik JSON jest uszkodzony, ignoruje błąd
    
    def daily_summary(self):  # Zliczenie zadań wykonanych oraz niewykonanych
        total_tasks = len(self.task_manager.tasks)  # Pobiera całkowitą liczbę zadań
        done_tasks = sum(1 for task in self.task_manager.tasks if task.done)  # Liczy wykonane zadania
        undone_tasks = total_tasks - done_tasks  # Oblicza liczbę niewykonanych zadań

        # Przygotowanie tekstu raportu
        report = (
            f"Wykonane zadania: {done_tasks}\n"
            f"Niewykonane zadania: {undone_tasks}\n"
        )

        # Tworzy okno popup do wyświetlenia podsumowania dnia
        popup = CustomMessageBox(self, "Podsumowanie dnia", report, self.handle_summary_response)
        popup.geometry("300x225")  # Ustawia rozmiar popupu na 300x225 pikseli

        # Konfiguracja przycisków w popupie
        popup.confirm_button.configure(text="Zapisz jako plik .txt", hover_color="darkgreen")  # Zmienia tekst i kolor podświetlenia przycisku
        popup.cancel_button.configure(text="Zamknij", hover_color="darkred")  # Zmienia tekst i kolor podświetlenia przycisku "Zamknij"
        popup.confirm_button.pack(pady=5)  # Dodaje odstęp pionowy dla przycisku "Zapisz jako TXT"
        popup.cancel_button.pack(pady=5)  # Dodaje odstęp pionowy dla przycisku "Zamknij"

        # Dodaje nowy przycisk "Zapisz jako plik .pdf" do popupu
        pdf_button = ctk.CTkButton(
            popup, text="Zapisz jako plik .pdf", fg_color="purple", hover_color="darkviolet",
            command=lambda: self.save_summary_pdf(report, popup)  # Przekazuje raport i popup do funkcji zapisującej PDF
        )
        pdf_button.pack(pady=5)  # Wyświetla przycisk w popupie z odstępem pionowym

    def save_summary_pdf(self, report, popup):
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Pobiera aktualną datę w formacie YYYY-MM-DD

        # Otwiera okno dialogowe do wyboru nazwy pliku i lokalizacji
        file_path = filedialog.asksaveasfilename(
            initialfile=f"podsumowanie_{today_date}.pdf",  # Domyślna nazwa pliku
            defaultextension=".pdf",  # Automatyczne dodanie rozszerzenia .pdf
            filetypes=[("Pliki PDF", "*.pdf")],  # Określenie obsługiwanych formatów plików
            title="Zapisz raport jako PDF"  # Tytuł okna dialogowego
        )

        if file_path:
            c = canvas.Canvas(file_path, pagesize=A4)  # Tworzy nowy dokument PDF o rozmiarze A4
            width, height = A4  # Pobiera szerokość i wysokość strony A4
            y_position = height - 50  # Ustawia początkową pozycję tekstu na stronie

            c.setFont("Aller_Lt", 16)  # Ustawia czcionkę nagłówka
            c.drawString(50, y_position, f"Podsumowanie dnia - {today_date}")  # Dodaje nagłówek z datą
            y_position -= 30  # Przesuwa pozycję tekstu w dół

            c.setFont("Aller_Lt", 12)  # Ustawia czcionkę dla treści raportu
            for line in report.split("\n"):  # Iteruje przez każdą linię raportu
                c.drawString(50, y_position, line)  # Rysuje tekst raportu w pliku PDF
                y_position -= 20  # Przesuwa pozycję w dół
                if y_position < 50:  # Jeśli brakuje miejsca na stronie
                    c.showPage()  # Tworzy nową stronę
                    c.setFont("Aller_Lt", 12)  # Ponownie ustawia czcionkę
                    y_position = height - 50  # Resetuje pozycję tekstu

            c.save()  # Zapisuje plik PDF
        popup.destroy()  # Zamyka popup po zapisaniu pliku

    def handle_summary_response(self, response):
        if response:
            # Jeśli użytkownik wybrał "Tak", zapisujemy raport
            total_tasks = len(self.task_manager.tasks)  # Pobiera liczbę wszystkich zadań
            done_tasks = sum(1 for task in self.task_manager.tasks if task.done)  # Liczy wykonane zadania
            undone_tasks = total_tasks - done_tasks  # Oblicza liczbę niewykonanych zadań
            today_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Pobiera aktualną datę

            # Tworzy tekst raportu zawierający datę
            report = (
                f"Podsumowanie dnia {today_date}:\n"
                f"Wykonane zadania: {done_tasks}\n"
                f"Niewykonane zadania: {undone_tasks}\n"
            )
            self.save_summary_txt(report)  # Wywołuje funkcję zapisującą raport jako plik TXT
        else:
            return  # Jeśli użytkownik anulował, funkcja nie wykonuje żadnych akcji

    def save_summary_txt(self, report): # Otwiera okno dialogowe do wyboru nazwy pliku i lokalizacji
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",  # Automatyczne dodanie rozszerzenia .txt
            filetypes=[("Pliki TXT", "*.txt")],  # Określenie obsługiwanych formatów plików
            title="Zapisz raport jako TXT"  # Tytuł okna dialogowego
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:  # Otwiera plik w trybie zapisu z kodowaniem UTF-8
                file.write(report)  # Zapisuje treść raportu do pliku

class TaskManager:
    def __init__(self, parent): # Menedżer zadań przechowujący i zarządzający listą zadań.
        self.parent = parent  # Referencja do głównej aplikacji
        self.tasks = []  # Lista przechowująca obiekty zadań

    def add_task(self, text, done=False): # Dodaje nowe zadanie do listy.
        # Tworzy nowy obiekt zadania i dodaje go do listy
        task = Task(self.parent.task_container, text, done, self.remove_task, self.save_tasks)
        self.tasks.append(task)
        self.save_tasks()  # Zapisuje listę zadań do pliku JSON
        self.sort_tasks()  # Sortuje zadania według czasu

    def remove_task(self, task): # Usuwa zadanie z listy i interfejsu.
        if task in self.tasks:  # Sprawdza, czy zadanie istnieje na liście
            self.tasks.remove(task)  # Usuwa zadanie z listy
            task.frame.destroy()  # Usuwa widżet zadania z interfejsu
            self.save_tasks()  # Zapisuje zaktualizowaną listę zadań

    def save_tasks(self): # Zapisuje aktualną listę zadań do pliku JSON.
        tasks_data = {
            "plan": self.parent.day_type_var.get(),  # Pobiera aktualnie wybrany plan dnia
            "tasks": [{"text": task.text, "done": task.done} for task in self.tasks]  # Lista zadań jako słownik
        }
        with open(DATA_FILE, "w") as file:  # Otwiera plik w trybie zapisu
            json.dump(tasks_data, file, indent=4)  # Zapisuje dane w formacie JSON

    def load_tasks(self): # Wczytuje listę zadań z pliku JSON.
        if os.path.exists(DATA_FILE):  # Sprawdza, czy plik istnieje
            with open(DATA_FILE, "r") as file:  # Otwiera plik w trybie odczytu
                try:
                    data = json.load(file)  # Wczytuje dane JSON
                    if isinstance(data, dict):  # Sprawdza, czy dane mają poprawny format
                        plan = data.get("plan", None)  # Pobiera nazwę zapisanego planu dnia
                        if plan:
                            self.parent.day_type_var.set(plan)  # Ustawia plan dnia w interfejsie
                        tasks_data = data.get("tasks", [])  # Pobiera listę zapisanych zadań
                        for task_data in tasks_data:
                            self.add_task(task_data["text"], task_data.get("done", False))  # Dodaje każde zadanie do listy
                    else:
                        # Obsługuje starszy format zapisu (gdy JSON zawierał tylko listę zadań)
                        for task_data in data:
                            self.add_task(task_data["text"], task_data.get("done", False))
                except json.JSONDecodeError:  # Obsługuje błąd w przypadku uszkodzonego pliku JSON
                    pass

    def remove_auto_tasks(self): # Usuwa zadania oznaczone jako automatycznie wygenerowane ([AUTO]).
        # Filtruje listę, wybierając tylko zadania z tagiem "[AUTO]"
        tasks_to_remove = [task for task in self.tasks if "[AUTO]" in task.text]
        for task in tasks_to_remove:
            task.frame.destroy()  # Usuwa widżet zadania
            self.tasks.remove(task)  # Usuwa zadanie z listy
        self.refresh_tasks()  # Aktualizuje interfejs
        self.sort_tasks()  # Sortuje zadania

    def sort_tasks(self): # Sortuje zadania według godziny (jeśli godzina jest podana w treści zadania).
        def extract_time(task):
            # Rozdziela tekst zadania, próbując wydobyć godzinę z formatu "HH:MM - Treść zadania"
            parts = task.text.split(" - ", 1)
            if len(parts) > 1 and ":" in parts[0]:  # Sprawdza, czy pierwszy fragment tekstu zawiera godzinę
                try:
                    return datetime.datetime.strptime(parts[0], "%H:%M").time()  # Konwertuje na obiekt czasu
                except ValueError:
                    return datetime.time(23, 59)  # Jeśli format godziny jest niepoprawny, ustawia na koniec dnia
            return datetime.time(23, 59)  # Jeśli brak godziny, zadanie trafia na koniec listy

        # Sortuje zadania na podstawie godziny
        self.tasks.sort(key=lambda task: extract_time(task))
        self.refresh_tasks()  # Odświeża interfejs

    def refresh_tasks(self): # Odświeża interfejs, aby zadania były wyświetlane w poprawnej kolejności.
        for task in self.tasks:
            task.frame.pack_forget()  # Ukrywa wszystkie zadania
        for task in self.tasks:
            task.frame.pack(fill="x", padx=5, pady=5)  # Ponownie wyświetla zadania w posortowanej kolejności

class Task:
    def __init__(self, parent, text, done, remove_callback, update_callback):
        self.parent = parent  # Rodzicielski element GUI, do którego będzie przypisana ramka zadania
        self.text = text  # Tekst opisujący zadanie
        self.done = done  # Flaga wskazująca, czy zadanie jest ukończone (True/False)
        self.remove_callback = remove_callback  # Funkcja wywoływana przy usuwaniu zadania
        self.update_callback = update_callback  # Funkcja wywoływana przy aktualizacji stanu zadania

        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")  # Utworzenie ramki kontenera dla zadania
        self.frame.pack(fill="x", padx=5, pady=3)  # Dodanie ramki do GUI, rozciągnięcie na całą szerokość

        self.check_var = ctk.BooleanVar(value=self.done)  # Zmienna przechowująca stan checkboxa (zaznaczony/odznaczony)
        self.checkbox = ctk.CTkCheckBox(self.frame, text="", variable=self.check_var, command=self.toggle_done, checkmark_color="white", fg_color="green", border_color="green", hover_color="green")  # Utworzenie checkboxa do oznaczania wykonania zadania
        self.checkbox.pack(side="left", padx=5)  # Umieszczenie checkboxa po lewej stronie ramki

        self.label = ctk.CTkLabel(self.frame, text=self.text)  # Utworzenie etykiety wyświetlającej tekst zadania
        self.label.pack(side="left", expand=True, padx=5)  # Umieszczenie etykiety po lewej stronie i rozszerzenie na dostępne miejsce

        self.delete_button = ctk.CTkButton(self.frame, text="Usuń", fg_color="red", command=self.remove, width=5, hover_color="darkred")  # Utworzenie przycisku do usuwania zadania
        self.delete_button.pack(side="right", padx=5)  # Umieszczenie przycisku po prawej stronie ramki
        self.update_style()  # Aktualizacja stylu etykiety w zależności od stanu zadania

    def toggle_done(self):
        self.done = self.check_var.get()  # Aktualizacja stanu zadania na podstawie wartości checkboxa
        self.update_style()  # Aktualizacja stylu etykiety (np. zmiana koloru tekstu) zgodnie z aktualnym stanem
        self.update_callback()  # Wywołanie funkcji aktualizującej (np. zapis zmian w zadaniu)

    def update_style(self):
        current_theme = ctk.get_appearance_mode()  # Pobranie aktualnego trybu wyglądu (Light lub Dark)
        if self.done:
            text_color = "green"  # Jeśli zadanie jest ukończone, ustaw kolor tekstu na zielony
        else:
            text_color = "black" if current_theme == "Light" else "white"  # Dla niedokończonych zadań, ustaw kolor tekstu zależnie od trybu
        self.label.configure(text_color=text_color)  # Zastosowanie wybranego koloru do etykiety zadania

    def remove(self):
        self.frame.destroy()  # Usunięcie ramki zadania z GUI
        self.remove_callback(self)  # Wywołanie funkcji usuwającej zadanie z zarządzania (np. z listy)

class TaskGenerator:
    def __init__(self, task_manager, day_type_var, day_variations):
        self.task_manager = task_manager  # Obiekt zarządzający zadaniami, umożliwiający dodawanie/aktualizację zadań
        self.day_type_var = day_type_var  # Zmienna określająca typ dnia (np. roboczy, wolny)
        self.day_variations = day_variations  # Słownik zawierający różne warianty zadań w zależności od typu dnia

    def generate_day_plan(self):
        day_type = self.day_type_var.get()  # Pobranie aktualnego typu dnia
        if day_type in self.day_variations:
            tasks = random.choice(self.day_variations[day_type])  # Losowe wybranie jednego zestawu zadań dla danego typu dnia
            for time, task in tasks:
                self.task_manager.add_task(f"{time} - {task} [AUTO]")  # Dodanie zadania do menedżera, z informacją o czasie i opisie
            self.task_manager.sort_tasks()  # Posortowanie zadań po dodaniu

if __name__ == "__main__":
    app = ToDoApp()  # Utworzenie instancji aplikacji do zarządzania zadaniami
    app.mainloop()  # Uruchomienie głównej pętli aplikacji, która czeka na zdarzenia użytkownika
