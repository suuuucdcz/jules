#!/usr/bin/env python3
import sqlite3
import argparse
import sys
import os
from datetime import datetime

# ANSI escape codes for styling
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

DB_FILE = os.path.expanduser('~/.todo_list.db')

def init_db():
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

def add_task(conn, description, priority):
    c = conn.cursor()
    c.execute('INSERT INTO tasks (description, priority) VALUES (?, ?)', (description, priority))
    conn.commit()
    print(f"{GREEN}✓ Tâche ajoutée avec succès !{RESET} (ID: {c.lastrowid})")

def list_tasks(conn, show_completed=False):
    c = conn.cursor()
    query = 'SELECT id, description, priority, completed, created_at, completed_at FROM tasks'
    if not show_completed:
        query += ' WHERE completed = 0'
    query += ' ORDER BY completed ASC, priority ASC, created_at DESC'

    c.execute(query)
    tasks = c.fetchall()

    if not tasks:
        print(f"{YELLOW}Aucune tâche trouvée ! Vous êtes à jour.{RESET}")
        return

    print(f"\n{BOLD}{CYAN}Vos tâches :{RESET}\n")
    print(f"{BOLD}{'ID':<4} | {'Priorité':<10} | {'Statut':<8} | {'Description'}{RESET}")
    print("-" * 50)

    priority_map = {1: f"{RED}Haute{RESET}  ", 2: f"{YELLOW}Moyenne{RESET}", 3: f"{GREEN}Basse{RESET}  "}

    for task in tasks:
        task_id, desc, priority, completed, created, completed_at = task
        status = f"{GREEN}[x]{RESET}" if completed else f"{RED}[ ]{RESET}"
        pri_str = priority_map.get(priority, "Inconnu")

        # Strikethrough if completed
        desc_str = f"\033[9m{desc}\033[29m" if completed else desc

        print(f"{task_id:<4} | {pri_str:<19} | {status:<17} | {desc_str}")
    print("\n")

def complete_task(conn, task_id):
    c = conn.cursor()
    c.execute('SELECT completed FROM tasks WHERE id = ?', (task_id,))
    result = c.fetchone()

    if not result:
        print(f"{RED}Erreur: Tâche avec l'ID {task_id} introuvable.{RESET}")
        return

    if result[0]:
        print(f"{YELLOW}La tâche {task_id} est déjà terminée.{RESET}")
        return

    c.execute('UPDATE tasks SET completed = 1, completed_at = CURRENT_TIMESTAMP WHERE id = ?', (task_id,))
    conn.commit()
    print(f"{GREEN}✓ Tâche {task_id} marquée comme terminée ! Bien joué !{RESET}")

def delete_task(conn, task_id):
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    if c.rowcount > 0:
        conn.commit()
        print(f"{GREEN}✓ Tâche {task_id} supprimée.{RESET}")
    else:
        print(f"{RED}Erreur: Tâche avec l'ID {task_id} introuvable.{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de tâches en ligne de commande avancé")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Command: add
    parser_add = subparsers.add_parser("add", help="Ajouter une nouvelle tâche")
    parser_add.add_argument("description", type=str, help="Description de la tâche")
    parser_add.add_argument("-p", "--priority", type=int, choices=[1, 2, 3], default=2,
                           help="Priorité de la tâche (1: Haute, 2: Moyenne, 3: Basse). Défaut: 2")

    # Command: ls
    parser_ls = subparsers.add_parser("ls", help="Lister les tâches")
    parser_ls.add_argument("-a", "--all", action="store_true", help="Afficher également les tâches terminées")

    # Command: done
    parser_done = subparsers.add_parser("done", help="Marquer une tâche comme terminée")
    parser_done.add_argument("id", type=int, help="ID de la tâche à terminer")

    # Command: rm
    parser_rm = subparsers.add_parser("rm", help="Supprimer une tâche")
    parser_rm.add_argument("id", type=int, help="ID de la tâche à supprimer")

    args = parser.parse_args()

    conn = init_db()

    if args.command == "add":
        add_task(conn, args.description, args.priority)
    elif args.command == "ls" or args.command is None:
        if args.command is None:
            # Default behavior when no arguments are provided
            list_tasks(conn, show_completed=False)
        else:
            list_tasks(conn, show_completed=args.all)
    elif args.command == "done":
        complete_task(conn, args.id)
    elif args.command == "rm":
        delete_task(conn, args.id)
    else:
        parser.print_help()

    conn.close()

if __name__ == "__main__":
    main()
