import tkinter as tk
from tkinter import messagebox
from datetime import datetime


window = tk.Tk()
window.title("Advanced To-Do List")
window.geometry("550x650")
window.configure(bg="#1e1e1e")

tasks = []

def add_task():
    task = task_entry.get().strip()
    priority = priority_var.get()
    due_date = date_entry.get().strip()

    if task == "":
        messagebox.showwarning("Warning", "Task cannot be empty")
        return

    if due_date:
        try:
            datetime.strptime(due_date, "%d-%m-%Y")
        except ValueError:
            messagebox.showwarning("Warning", "Date format: DD-MM-YYYY")
            return

    tasks.append({
        "task": task,
        "priority": priority,
        "due": due_date,
        "done": False
    })

    task_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    refresh_list()
    save_tasks()

def delete_task():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)
        refresh_list()
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task")

def toggle_done(event):
    try:
        index = listbox.curselection()[0]
        tasks[index]["done"] = not tasks[index]["done"]
        refresh_list()
        save_tasks()
    except:
        pass

def refresh_list(filtered=None):
    listbox.delete(0, tk.END)
    show_tasks = filtered if filtered is not None else tasks

    for t in show_tasks:
        status = "✔" if t["done"] else "○"
        text = f"{status} [{t['priority']}] {t['task']} (Due: {t['due'] or 'N/A'})"
        listbox.insert(tk.END, text)

def search_task():
    keyword = search_entry.get().lower()
    filtered = [t for t in tasks if keyword in t["task"].lower()]
    refresh_list(filtered)

def clear_search():
    search_entry.delete(0, tk.END)
    refresh_list()

def save_tasks():
    with open("tasks.txt", "w") as f:
        for t in tasks:
            f.write(f"{t['task']}|{t['priority']}|{t['due']}|{t['done']}\n")

def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            for line in f:
                task, priority, due, done = line.strip().split("|")
                tasks.append({
                    "task": task,
                    "priority": priority,
                    "due": due,
                    "done": done == "True"
                })
    except:
        pass

tk.Label(
    window,
    text="📝 Smart To-Do List",
    font=("Segoe UI Semibold", 20),
    bg="#1e1e1e",
    fg="#f2c94c"
).pack(pady=10)

search_frame = tk.Frame(window, bg="#1e1e1e")
search_frame.pack(fill="x", padx=15)

search_entry = tk.Entry(
    search_frame,
    font=("Segoe UI", 11),
    bg="#3a3a3a",
    fg="white",
    insertbackground="white",
    borderwidth=0
)
search_entry.pack(side="left", fill="x", expand=True, padx=5)

tk.Button(
    search_frame, text="Search",
    bg="#3498db", fg="white",
    borderwidth=0, command=search_task
).pack(side="left", padx=5)

tk.Button(
    search_frame, text="Clear",
    bg="#6c757d", fg="white",
    borderwidth=0, command=clear_search
).pack(side="left", padx=5)


listbox = tk.Listbox(
    window,
    font=("Segoe UI", 11),
    bg="#2b2b2b",
    fg="white",
    selectbackground="#f2c94c",
    selectforeground="black",
    borderwidth=0,
    height=14
)
listbox.pack(fill="both", expand=True, padx=15, pady=10)
listbox.bind("<Double-Button-1>", toggle_done)

task_entry = tk.Entry(
    window,
    font=("Segoe UI", 11),
    bg="#3a3a3a",
    fg="white",
    insertbackground="white",
    borderwidth=0
)
task_entry.pack(fill="x", padx=15, pady=5)
task_entry.insert(0, "Enter task...")

option_frame = tk.Frame(window, bg="#1e1e1e")
option_frame.pack(fill="x", padx=15, pady=5)

priority_var = tk.StringVar(value="Medium")
priority_menu = tk.OptionMenu(option_frame, priority_var, "High", "Medium", "Low")
priority_menu.config(bg="#f2c94c", fg="black", borderwidth=0)
priority_menu.pack(side="left", padx=5)

date_entry = tk.Entry(
    option_frame,
    font=("Segoe UI", 10),
    bg="#3a3a3a",
    fg="white",
    insertbackground="white",
    borderwidth=0
)
date_entry.pack(side="left", fill="x", expand=True, padx=5)
date_entry.insert(0, "DD-MM-YYYY")

btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(
    btn_frame, text="Add Task",
    bg="#27ae60", fg="white",
    width=14, borderwidth=0,
    command=add_task
).grid(row=0, column=0, padx=10)

tk.Button(
    btn_frame, text="Delete Task",
    bg="#e74c3c", fg="white",
    width=14, borderwidth=0,
    command=delete_task
).grid(row=0, column=1, padx=10)

load_tasks()
refresh_list()

window.mainloop()

