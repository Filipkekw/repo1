import tkinter as tk
from tkinter import messagebox

# Funkcja dodająca zadanie do listy
def add_to_list():
    text = task_entry.get()  # Pobiera tekst z pola tekstowego
    if text != "":  # Jeżeli tekst nie jest pusty
        task_listbox.insert(tk.END, text)  # Dodaje tekst do listy
        task_entry.delete(0, tk.END)  # Czyści pole tekstowe
    else:
        messagebox.showwarning("Uwaga!", "Nie można dodać pustego zadania!")

# Tworzenie głównego okna
root = tk.Tk()
root.title("To-Do List")
root.geometry("600x400")

# Pole do wpisywania zadań
task_entry = tk.Entry(root, width=50)
task_entry.pack(pady=10)

# Przycisk do dodawania i usuwania zadań (tylko grafika)
add_button = tk.Button(root, text="Dodaj zadanie", width=12, command=add_to_list)
add_button.pack(pady=5)

# Lista zadań
task_listbox = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE, selectbackground="#a6a6a6")
task_listbox.pack(pady=10)

# Uruchamianie aplikacji
root.mainloop()
