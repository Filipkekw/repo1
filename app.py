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
import platform
import darkdetect
import subprocess

font_path = os.path.join(os.path.dirname(__file__), "fonts", "Aller_Lt.ttf")  # Buduje ścieżkę do pliku czcionki "Aller_Lt.ttf"
pdfmetrics.registerFont(TTFont('Aller_Lt', font_path))  # Rejestracja czcionki "Aller_Lt" w ReportLab

DATA_FILE = "tasks.json"  # Nazwa pliku JSON z zadaniami i planem dnia.
DAY_VARIATIONS_FILE = "day_variations.json"  # Nazwa pliku JSON z wariantami planów dnia.
SETTINGS_FILE = "settings.json"
 
def get_linux_appearance():
    try:
        # Pobierz aktywny motyw GTK
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
            capture_output=True, text=True, check=True
        )
        theme = result.stdout.strip().strip("'").lower()

        # Jeśli motyw zawiera "dark", to ustaw ciemny motyw
        if "dark" in theme:
            return "dark"
        return "light"
    except Exception:
        return "light"  # Domyślnie jasny, jeśli nie uda się odczytać

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
    if os.path.exists(DAY_VARIATIONS_FILE):
        with open(DAY_VARIATIONS_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

day_variations = load_day_variations()
day_types = list(day_variations.keys())

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, master, title, message, on_confirm):
        super().__init__(master)
        self.title(title)
        self.geometry("300x175")
        self.on_confirm = on_confirm

        self.label = ctk.CTkLabel(self, text=message)
        self.label.pack(pady=20)

        self.confirm_button = ctk.CTkButton(self, text="Tak", command=self.confirm, fg_color="green")
        self.confirm_button.pack(pady=10)

        self.cancel_button = ctk.CTkButton(self, text="Nie", command=self.cancel, fg_color="red")
        self.cancel_button.pack(pady=5)

        self.update_idletasks()
        self.wait_visibility()
        self.grab_set()

    def confirm(self):
        self.on_confirm(True)
        self.destroy()

    def cancel(self):
        self.on_confirm(False)
        self.destroy()

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Wykrywanie systemowego motywu – uwzględnienie systemu Linux
        if platform.system() == "Linux":
            actual_theme = get_linux_appearance()
            ctk.set_appearance_mode("dark" if actual_theme == "dark" else "light")
        else:
            if darkdetect.isDark():
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")

        self.system_theme = ctk.get_appearance_mode()

        self.title("To-Do List")
        self.geometry("600x900")

        # Wewnątrz __init__ klasy ToDoApp:
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(side="top", fill="x")

        # Ustalanie opcji motywu w zależności od systemu operacyjnego
        if platform.system() == "Linux":
            theme_options = ["Jasny", "Ciemny"]
            self.theme_var = ctk.StringVar(value="Ciemny")
        else:
            theme_options = ["System", "Jasny", "Ciemny"]
            self.theme_var = ctk.StringVar(value="System")

        self.task_manager = TaskManager(self)

        self.theme_menu = ctk.CTkComboBox(
            master=top_bar,
            values=theme_options,
            variable=self.theme_var,
            command=self.change_theme,
            width=120,
            state="readonly"
        )
        self.theme_menu.pack(side="right", padx=10, pady=10)


        self.load_settings()
        self.change_theme(self.theme_var.get())
        self.update_task_text_color()

        self.day_type_var = ctk.StringVar(value="Plan dnia")
        self.task_generator = TaskGenerator(self.task_manager, self.day_type_var, day_variations)

        ctk.CTkLabel(self, text="Twoja Lista Zadań", font=("Arial", 16, "bold")).pack(pady=10)

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(pady=5, fill="x")

        left_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        right_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)

        self.task_entry = ctk.CTkEntry(left_frame, width=250, placeholder_text="Treść zadania")
        self.task_entry.pack(pady=5)

        self.time_entry = ctk.CTkEntry(left_frame, width=60, placeholder_text="HH:MM")
        self.time_entry.pack(pady=5)
        self.time_entry.bind("<KeyRelease>", self.format_time_entry)

        self.add_button = ctk.CTkButton(left_frame, text="Dodaj zadanie", fg_color="green", hover_color="darkgreen", command=self.add_task)
        self.add_button.pack(pady=5)

        self.day_menu = ctk.CTkComboBox(right_frame, values=day_types, variable=self.day_type_var, state="readonly")
        self.day_menu.pack(pady=5)

        self.generate_button = ctk.CTkButton(right_frame, text="Wygeneruj plan dnia", fg_color="blue", hover_color="darkblue", command=self.generate_sorted_plan)
        self.generate_button.pack(pady=5)

        self.export_button = ctk.CTkButton(right_frame, text="Eksportuj do PDF", fg_color="purple", hover_color="darkviolet", command=self.export_to_pdf)
        self.export_button.pack(pady=5)

        self.task_container = ctk.CTkFrame(self, fg_color="transparent")
        self.task_container.pack(pady=10, fill="both", expand=True)

        self.task_manager.load_tasks()
        self.update_task_text_color()

    def format_time_entry(self, event):
        text = self.time_entry.get()
        if len(text) == 2 and ":" not in text:
            self.time_entry.insert(2, ":")

    def validate_time(self, time_text):
        try:
            if time_text == "HH:MM":
                return True
            datetime.datetime.strptime(time_text, "%H:%M").time()
            return True
        except ValueError:
            return False

    def add_task(self):
        task_text = self.task_entry.get().strip()
        time_text = self.time_entry.get().strip()

        if not task_text:
            return

        if time_text and time_text != "HH:MM" and not self.validate_time(time_text):
            return

        if time_text and time_text != "HH:MM":
            task_text = f"{time_text} - {task_text}"

        self.task_manager.add_task(task_text)
        self.task_entry.delete(0, "end")
        self.time_entry.delete(0, "end")
        self.update_task_text_color()

    def generate_sorted_plan(self):
        if any("[AUTO]" in task.text for task in self.task_manager.tasks):
            CustomMessageBox(self, "Potwierdzenie", "Czy chcesz nadpisać istniejący plan dnia?", self.handle_confirmation)
        else:
            self.execute_generation()

    def handle_confirmation(self, response):
        if response:
            self.execute_generation()

    def execute_generation(self):
        self.task_manager.remove_auto_tasks()
        self.task_generator.generate_day_plan()
        self.task_manager.sort_tasks()

    def export_to_pdf(self):
        default_filename = f"harmonogram_{datetime.datetime.now().strftime('%Y_%m_%d')}.pdf"
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
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

    def change_theme(self, new_theme: str):
        if new_theme == "System":
            actual_theme = self.system_theme  # Używamy wykrytego motywu systemowego
        else:
            mapping = {"Jasny": "Light", "Ciemny": "Dark"}
            actual_theme = mapping.get(new_theme, "Light")

        ctk.set_appearance_mode(actual_theme)

        if hasattr(self, "task_manager") and self.task_manager:
            self.update_task_text_color()

        self.save_settings()

    def update_task_text_color(self):
        if not hasattr(self, "task_manager") or not self.task_manager:
            return
        
        current_theme = ctk.get_appearance_mode()
        text_color = "black" if current_theme == "Light" else "White"

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
                    pass

class TaskManager:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []

    def add_task(self, text, done=False):
        task = Task(self.parent.task_container, text, done, self.remove_task, self.save_tasks)
        self.tasks.append(task)
        self.save_tasks()
        self.sort_tasks()

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            task.frame.destroy()
            self.save_tasks()

    def save_tasks(self):
        tasks_data = {
            "plan": self.parent.day_type_var.get(),
            "tasks": [{"text": task.text, "done": task.done} for task in self.tasks]
        }
        with open(DATA_FILE, "w") as file:
            json.dump(tasks_data, file, indent=4)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                try:
                    data = json.load(file)
                    if isinstance(data, dict):
                        plan = data.get("plan", None)
                        if plan:
                            self.parent.day_type_var.set(plan)
                        tasks_data = data.get("tasks", [])
                        for task_data in tasks_data:
                            self.add_task(task_data["text"], task_data.get("done", False))
                    else:
                        for task_data in data:
                            self.add_task(task_data["text"], task_data.get("done", False))
                except json.JSONDecodeError:
                    pass

    def remove_auto_tasks(self):
        tasks_to_remove = [task for task in self.tasks if "[AUTO]" in task.text]
        for task in tasks_to_remove:
            task.frame.destroy()
            self.tasks.remove(task)
        self.refresh_tasks()
        self.sort_tasks()

    def sort_tasks(self):
        def extract_time(task):
            parts = task.text.split(" - ", 1)
            if len(parts) > 1 and ":" in parts[0]:
                try:
                    return datetime.datetime.strptime(parts[0], "%H:%M").time()
                except ValueError:
                    return datetime.time(23, 59)
            return datetime.time(23, 59)
        self.tasks.sort(key=lambda task: extract_time(task))
        self.refresh_tasks()

    def refresh_tasks(self):
        for task in self.tasks:
            task.frame.pack_forget()
        for task in self.tasks:
            task.frame.pack(fill="x", padx=5, pady=5)

class Task:
    def __init__(self, parent, text, done, remove_callback, update_callback):
        self.parent = parent
        self.text = text
        self.done = done
        self.remove_callback = remove_callback
        self.update_callback = update_callback

        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame.pack(fill="x", padx=5, pady=3)

        self.check_var = ctk.BooleanVar(value=self.done)
        self.checkbox = ctk.CTkCheckBox(
            self.frame, text="", variable=self.check_var, command=self.toggle_done,
            checkmark_color="white", fg_color="green", border_color="green"
        )
        self.checkbox.pack(side="left", padx=5)

        self.label = ctk.CTkLabel(self.frame, text=self.text)
        self.label.pack(side="left", expand=True, padx=5)

        self.delete_button = ctk.CTkButton(self.frame, text="Usuń", fg_color="red", command=self.remove, width=5, hover_color="darkred")
        self.delete_button.pack(side="right", padx=5)
        self.update_style()

    def toggle_done(self):
        self.done = self.check_var.get()
        self.update_style()
        self.update_callback()

    def update_style(self):
        current_theme = ctk.get_appearance_mode()
        if self.done:
            text_color = "green"
        else:
            text_color = "black" if current_theme == "Light" else "white"
        self.label.configure(text_color=text_color)

    def remove(self):
        self.frame.destroy()
        self.remove_callback(self)

class TaskGenerator:
    def __init__(self, task_manager, day_type_var, day_variations):
        self.task_manager = task_manager
        self.day_type_var = day_type_var
        self.day_variations = day_variations

    def generate_day_plan(self):
        day_type = self.day_type_var.get()
        if day_type in self.day_variations:
            tasks = random.choice(self.day_variations[day_type])
            for time, task in tasks:
                self.task_manager.add_task(f"{time} - {task} [AUTO]")
            self.task_manager.sort_tasks()

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
