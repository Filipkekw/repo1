import tkinter as tk
from tkinter import messagebox

# Tworzenie głównego okna
root = tk.Tk()
root.title("To-Do List")
root.geometry("600x400")

# Pole do wpisywania zadań
task_entry = tk.Entry(root, width=50)
task_entry.pack(pady=10)

# Przycisk do dodawania zadań
add_button = tk.Button(root, text="+", width=10)
add_button.pack(pady=5)

# Uruchamianie aplikacji
root.mainloop()
