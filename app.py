import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import pathlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Ensure data directory exists
DATA_DIR = pathlib.Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "records.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


class NotesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Notes App")
        self.geometry("400x300")
        self.resizable(False, False)

        self.listbox = tk.Listbox(self, height=12, width=50)
        self.listbox.pack(padx=10, pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=(0,10))

        add_btn = tk.Button(frame, text="Add Note", command=self.add_note)
        add_btn.pack(side=tk.LEFT, padx=5)

        del_btn = tk.Button(frame, text="Delete Selected", command=self.delete_note)
        del_btn.pack(side=tk.LEFT, padx=5)

        self.load_notes()

    def db_connection(self):
        return sqlite3.connect(DB_PATH)

    def load_notes(self):
        self.listbox.delete(0, tk.END)
        conn = self.db_connection()
        for row in conn.execute("SELECT id, text FROM notes"):
            self.listbox.insert(tk.END, f"{row[0]}: {row[1]}")
        conn.close()

    def add_note(self):
        note = simpledialog.askstring("New Note", "Enter your note:")
        if note:
            conn = self.db_connection()
            conn.execute("INSERT INTO notes (text) VALUES (?)", (note,))
            conn.commit()
            conn.close()
            self.load_notes()
        else:
            messagebox.showinfo("Cancelled", "No note added.")

    def delete_note(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Select a note", "Please select a note to delete.")
            return
        idx_text = self.listbox.get(sel[0]).split(":", 1)[0]
        conn = self.db_connection()
        conn.execute("DELETE FROM notes WHERE id=?", (idx_text,))
        conn.commit()
        conn.close()
        self.load_notes()


if __name__ == "__main__":
    init_db()
    app = NotesApp()
    app.mainloop()
