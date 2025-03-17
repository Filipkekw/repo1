import tkinter as tk
from tkinter import messagebox

# Funkcja dodająca zadanie do listy wraz z przyciskiem usuwania
def add_to_list():
    text = task_entry.get()  # Pobiera tekst z pola tekstowego
    if text != "":  # Jeżeli tekst nie jest pusty
        add_task(text)  # Wywołuje funkcję dodającą zadanie
        task_entry.delete(0, tk.END)  # Czyści pole tekstowe
    else:
        messagebox.showwarning("Uwaga!", "Nie można dodać pustego zadania!")

# Funkcja usuwająca określone zadanie
def remove_task(frame):
    frame.destroy()  # Usuwa ramkę zawierającą zadanie i przycisk

# Funkcja oznaczania zadania jako zrobione
def mark_done(task_label, check_var):
    if check_var.get():
        task_label.config(fg="gray", underline=True)  # Oznacza jako zrobione
    else:
        task_label.config(fg="black", underline=False)  # Przywraca normalny wygląd

# Funkcja dodająca nowe zadanie do interfejsu
def add_task(text):
    # Tworzy ramkę na zadanie i przycisk
    task_frame = tk.Frame(task_container)
    task_frame.pack(fill="x", pady=2)

    # Zmienna kontrolująca stan checkboxa
    check_var = tk.BooleanVar()

    # Checkbox do oznaczania zadania jako zrobione
    check_button = tk.Checkbutton(task_frame, variable=check_var, command=lambda: mark_done(task_label, check_var))
    check_button.pack(side="left")

    # Dodaje etykietę z treścią zadania
    task_label = tk.Label(task_frame, text=text, anchor="w")
    task_label.pack(side="left", fill="x", expand=True)

    # Przycisk do usuwania konkretnego zadania
    delete_button = tk.Button(task_frame, text="Usuń", command=lambda: remove_task(task_frame))
    delete_button.pack(side="right")

# Tworzenie głównego okna
root = tk.Tk()
root.title("To-Do List")
root.geometry("450x600")

# Pole do wpisywania zadań
task_entry = tk.Entry(root, width=50)
task_entry.pack(pady=10)

# Przycisk do dodawania zadań
add_button = tk.Button(root, text="Dodaj zadanie", width=12, command=add_to_list)
add_button.pack(pady=5)

# Kontener na listę zadań
task_container = tk.Frame(root)
task_container.pack(pady=10, fill="both", expand=True)

# Uruchamianie aplikacji
root.mainloop()
