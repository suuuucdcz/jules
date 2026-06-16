#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os

DB_FILE = os.path.expanduser('~/.todo_list.db')

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Tâches")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f0f0")

        self.conn = self.init_db()

        self.create_widgets()
        self.refresh_list()

    def init_db(self):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                priority INTEGER DEFAULT 2,
                completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        conn.commit()
        return conn

    def create_widgets(self):
        # Top Frame for input
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(top_frame, text="Tâche:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)

        self.task_entry = tk.Entry(top_frame, width=30)
        self.task_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.task_entry.bind('<Return>', lambda event: self.add_task())

        tk.Label(top_frame, text="Priorité:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.priority_var = tk.StringVar(value="2")
        priority_combo = ttk.Combobox(top_frame, textvariable=self.priority_var, values=["1 (Haute)", "2 (Moyenne)", "3 (Basse)"], width=10, state="readonly")
        priority_combo.pack(side=tk.LEFT, padx=5)

        add_btn = tk.Button(top_frame, text="Ajouter", bg="#4CAF50", fg="white", command=self.add_task)
        add_btn.pack(side=tk.LEFT, padx=5)

        # Middle Frame for Treeview
        mid_frame = tk.Frame(self.root)
        mid_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        columns = ("id", "statut", "priorite", "description")
        self.tree = ttk.Treeview(mid_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("statut", text="Statut")
        self.tree.heading("priorite", text="Priorité")
        self.tree.heading("description", text="Description")

        self.tree.column("id", width=30, anchor=tk.CENTER)
        self.tree.column("statut", width=80, anchor=tk.CENTER)
        self.tree.column("priorite", width=80, anchor=tk.CENTER)
        self.tree.column("description", width=300, anchor=tk.W)

        # Tags for colors
        self.tree.tag_configure('high', foreground='red')
        self.tree.tag_configure('medium', foreground='orange')
        self.tree.tag_configure('low', foreground='green')
        self.tree.tag_configure('done', foreground='gray')

        scrollbar = ttk.Scrollbar(mid_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottom Frame for Actions
        bottom_frame = tk.Frame(self.root, bg="#f0f0f0")
        bottom_frame.pack(pady=10, padx=10, fill=tk.X)

        self.show_completed_var = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(bottom_frame, text="Afficher les terminées", variable=self.show_completed_var, command=self.refresh_list, bg="#f0f0f0")
        chk.pack(side=tk.LEFT, padx=5)

        del_btn = tk.Button(bottom_frame, text="Supprimer", bg="#f44336", fg="white", command=self.delete_task)
        del_btn.pack(side=tk.RIGHT, padx=5)

        done_btn = tk.Button(bottom_frame, text="Terminer", bg="#2196F3", fg="white", command=self.complete_task)
        done_btn.pack(side=tk.RIGHT, padx=5)

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        c = self.conn.cursor()
        query = 'SELECT id, description, priority, completed FROM tasks'
        if not self.show_completed_var.get():
            query += ' WHERE completed = 0'
        query += ' ORDER BY completed ASC, priority ASC, created_at DESC'

        c.execute(query)
        tasks = c.fetchall()

        priority_map = {1: "Haute", 2: "Moyenne", 3: "Basse"}

        for task in tasks:
            t_id, desc, prio, comp = task
            statut_str = "Terminé" if comp else "En cours"
            prio_str = priority_map.get(prio, str(prio))

            tag = 'done'
            if not comp:
                if prio == 1: tag = 'high'
                elif prio == 2: tag = 'medium'
                elif prio == 3: tag = 'low'

            self.tree.insert("", tk.END, values=(t_id, statut_str, prio_str, desc), tags=(tag,))

    def add_task(self):
        desc = self.task_entry.get().strip()
        if not desc:
            messagebox.showwarning("Attention", "La description ne peut pas être vide.")
            return

        prio_str = self.priority_var.get()
        prio = int(prio_str.split(' ')[0])

        c = self.conn.cursor()
        c.execute('INSERT INTO tasks (description, priority) VALUES (?, ?)', (desc, prio))
        self.conn.commit()

        self.task_entry.delete(0, tk.END)
        self.refresh_list()

    def complete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Veuillez sélectionner une tâche.")
            return

        for item in selected:
            values = self.tree.item(item, "values")
            t_id = values[0]

            c = self.conn.cursor()
            c.execute('UPDATE tasks SET completed = 1, completed_at = CURRENT_TIMESTAMP WHERE id = ?', (t_id,))

        self.conn.commit()
        self.refresh_list()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Veuillez sélectionner une tâche.")
            return

        if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer la/les tâche(s) sélectionnée(s) ?"):
            for item in selected:
                values = self.tree.item(item, "values")
                t_id = values[0]

                c = self.conn.cursor()
                c.execute('DELETE FROM tasks WHERE id = ?', (t_id,))

            self.conn.commit()
            self.refresh_list()

    def on_closing(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
