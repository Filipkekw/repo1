import tkinter as tk
from tkinter import messagebox
import json
import os

# Ścieżka do pliku z danymi
DATA_FILE = "tasks.json"  # Plik, w którym przechowywane są zadania w formacie JSON

class Task: # Klasa obsługująca interakcje z zadaniem i usuwanie go
    def __init__(self, parent, text, done, remove_callback, update_callback):
        self.parent = parent  # Kontener, w którym zostanie umieszczone zadanie
        self.text = text  # Tekst zadania
        self.done = done  # Status ukończenia zadania (True/False)
        self.remove_callback = remove_callback  # Funkcja do usunięcia zadania
        self.update_callback = update_callback  # Funkcja do zapisu zmian

        self.frame = tk.Frame(self.parent)  # Tworzy ramkę dla zadania
        self.frame.pack(fill="x", pady=2)  # Umieszcza ramkę w kontenerze

        self.check_var = tk.BooleanVar(value=self.done)  # Przechowuje stan checkboxa

        # Checkbox do oznaczania zadania jako ukończone
        self.checkbox = tk.Checkbutton(self.frame, variable=self.check_var, command=self.toggle_done)
        self.checkbox.pack(side="left")

        # Etykieta z tekstem zadania
        self.label = tk.Label(self.frame, text=self.text, anchor="w")
        self.label.pack(side="left", fill="x", expand=True)

        # Przycisk do usuwania zadania
        self.delete_button = tk.Button(self.frame, text="Usuń", command=self.remove)
        self.delete_button.pack(side="right")

        self.update_style()  # Aktualizacja wyglądu zadania

    def toggle_done(self):
        self.done = self.check_var.get()  # Aktualizuje status ukończenia
        self.update_style()  # Zmienia wygląd w zależności od statusu
        self.update_callback()  # Zapisuje zmiany do pliku

    def update_style(self):
        if self.done:
            self.label.config(fg="gray", underline=True)  # Zadanie ukończone - szare i podkreślone
        else:
            self.label.config(fg="black", underline=False)  # Zadanie nieukończone - czarne i bez podkreślenia

    def remove(self):
        self.frame.destroy()  # Usuwa ramkę z interfejsu
        self.remove_callback(self)  # Informuje menedżera o usunięciu zadania


class TaskManager: # Klasa do zarządzania listą zadań (dodawanie, usuwanie, zapis/odczyt pliku JSON)
    def __init__(self, container):
        self.container = container  # Kontener, w którym przechowywane są wszystkie zadania
        self.tasks = []  # Lista zadań

    def add_task(self, text, done=False):
        # Tworzy nowe zadanie i dodaje je do listy
        task = Task(self.container, text, done, self.remove_task, self.save_tasks)
        self.tasks.append(task)
        self.save_tasks()  # Zapisuje zadania do pliku

    def remove_task(self, task):
        self.tasks.remove(task)  # Usuwa zadanie z listy
        self.save_tasks()  # Zapisuje zmiany do pliku

    def save_tasks(self):
        # Zapisuje wszystkie zadania do pliku JSON
        tasks_data = [{"text": task.text, "done": task.done} for task in self.tasks]
        with open(DATA_FILE, "w") as file:
            json.dump(tasks_data, file)

    def load_tasks(self):
        # Wczytuje zadania z pliku JSON
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                try:
                    tasks_data = json.load(file)
                    for task in tasks_data:
                        self.add_task(task["text"], task["done"])  # Dodaje każde zadanie z pliku
                except json.JSONDecodeError:
                    messagebox.showerror("Błąd", "Nie można odczytać pliku z zadaniami.")


class ToDoApp: # Klasa zarządzająca GUI
    def __init__(self, root):
        self.root = root  # Główne okno aplikacji
        self.root.title("To-Do List")  # Ustawia tytuł okna
        self.root.geometry("600x400")  # Ustawia rozmiar okna

        # Pole do wprowadzania nowego zadania
        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.pack(pady=10)

        # Przycisk do dodawania nowego zadania
        self.add_button = tk.Button(root, text="Dodaj zadanie", width=12, command=self.add_task)
        self.add_button.pack(pady=5)

        # Kontener na listę zadań
        self.task_container = tk.Frame(root)
        self.task_container.pack(pady=10, fill="both", expand=True)

        # Inicjalizacja menedżera zadań
        self.task_manager = TaskManager(self.task_container)

        # Wczytanie zadań z pliku przy starcie aplikacji
        self.task_manager.load_tasks()

    def add_task(self):
        # Dodaje nowe zadanie do listy
        text = self.task_entry.get()  # Pobiera tekst z pola
        if text.strip():  # Sprawdza, czy tekst nie jest pusty
            self.task_manager.add_task(text)  # Dodaje zadanie do menedżera
            self.task_entry.delete(0, tk.END)  # Czyści pole tekstowe
        else:
            messagebox.showwarning("Uwaga!", "Nie można dodać pustego zadania!")  # Ostrzeżenie o pustym zadaniu

# Tworzenie głównego okna
root = tk.Tk()
app = ToDoApp(root)  # Inicjalizacja aplikacji

# Uruchamianie aplikacji
root.mainloop()  # Rozpoczyna główną pętlę zdarzeń
