#!/usr/bin/env python3
"""
CLI Todo App - A minimalist task manager
Project 1: Command-line todo application with persistence
"""

import json
from datetime import datetime
from argparse import ArgumentParser

class TodoApp:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = self.load()
    
    def load(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def add(self, description):
        todo = {
            "id": len(self.todos) + 1,
            "description": description,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.todos.append(todo)
        self.save()
        print(f"✓ Added: {description}")
    
    def complete(self, todo_id):
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                self.save()
                print(f"✓ Completed task #{todo_id}")
                return
        print(f"✗ Task #{todo_id} not found")
    
    def list(self):
        if not self.todos:
            print("No tasks yet. Add one with 'add <task>'")
            return
        
        print("\n=== Your Tasks ===\n")
        for todo in self.todos:
            status = "✓" if todo["completed"] else "○"
            date = datetime.fromisoformat(todo["created_at"]).strftime("%b %d, %Y")
            print(f"{status} #{todo['id']}: {todo['description']} [{date}]")

def main():
    parser = ArgumentParser(description="Minimalist CLI Todo App")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", help="Task description")
    
    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as done")
    complete_parser.add_argument("id", type=int, help="Task ID to complete")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    
    args = parser.parse_args()
    
    app = TodoApp()
    
    if args.command == "add":
        app.add(args.task)
    elif args.command == "complete":
        app.complete(args.id)
    elif args.command == "list":
        app.list()
    else:
        print("\n=== CLI Todo App ===\n")
        print("Commands:")
        print("  add <task>   - Add a new task")
        print("  complete <id>- Mark task as done")
        print("  list         - List all tasks")
        app.list()

if __name__ == "__main__":
    main()
