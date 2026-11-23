#!/usr/bin/env python3
"""todo-cli: manage daily tasks from the terminal.

Zero-dependency Python CLI. Tasks are stored as JSON in ~/.todo.json.

Usage:
    python3 todo.py add "Buy milk" -p high --due 2026-11-25
    python3 todo.py list
    python3 todo.py list --all
    python3 todo.py done 2
    python3 todo.py remove 3
    python3 todo.py clear
"""

import argparse
import json
import os
import sys
from datetime import date

STORE = os.path.expanduser("~/.todo.json")
PRIORITIES = ("low", "medium", "high")


def load_tasks():
    if not os.path.exists(STORE):
        return []
    with open(STORE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{STORE} is not a task list")
    return data


def save_tasks(tasks):
    tmp = STORE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STORE)


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


def valid_due(value):
    try:
        date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError("due date must be YYYY-MM-DD")
    return value


def cmd_add(args):
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": args.title,
        "priority": args.priority,
        "due": args.due,
        "done": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added #{task['id']}: {task['title']}")
    return 0


def cmd_list(args):
    tasks = load_tasks()
    shown = tasks if args.all else [t for t in tasks if not t["done"]]
    if not shown:
        print("No tasks." if args.all else "No open tasks. Nice work.")
        return 0
    rank = {"high": 0, "medium": 1, "low": 2}
    shown.sort(key=lambda t: (t["done"], rank[t["priority"]], t["due"] or "9999"))
    print(f"{'ID':>3}  {'!':1}  {'Due':10}  Title")
    for t in shown:
        mark = "x" if t["done"] else " "
        due = t["due"] or "-"
        print(f"{t['id']:>3} [{mark}] {t['priority'][0].upper()}  {due:10}  {t['title']}")
    open_count = sum(1 for t in tasks if not t["done"])
    print(f"\n{open_count} open, {len(tasks) - open_count} done.")
    return 0


def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def cmd_done(args):
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if task is None:
        print(f"No task #{args.id}.", file=sys.stderr)
        return 1
    if task["done"]:
        print(f"Task #{args.id} is already done.")
        return 0
    task["done"] = True
    save_tasks(tasks)
    print(f"Done #{task['id']}: {task['title']}")
    return 0


def cmd_remove(args):
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if task is None:
        print(f"No task #{args.id}.", file=sys.stderr)
        return 1
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Removed #{task['id']}: {task['title']}")
    return 0


def cmd_clear(args):
    tasks = load_tasks()
    done = [t for t in tasks if t["done"]]
    if not done:
        print("No completed tasks to clear.")
        return 0
    if not args.yes:
        answer = input(f"Clear {len(done)} completed task(s)? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return 0
    save_tasks([t for t in tasks if not t["done"]])
    print(f"Cleared {len(done)} completed task(s).")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Manage daily tasks from the terminal.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument("-p", "--priority", choices=PRIORITIES, default="medium")
    p_add.add_argument("--due", type=valid_due, default=None, help="Due date YYYY-MM-DD")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--all", action="store_true", help="Include completed tasks")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Mark a task done")
    p_done.add_argument("id", type=int, help="Task id")
    p_done.set_defaults(func=cmd_done)

    p_rm = sub.add_parser("remove", help="Delete a task")
    p_rm.add_argument("id", type=int, help="Task id")
    p_rm.set_defaults(func=cmd_remove)

    p_clear = sub.add_parser("clear", help="Delete all completed tasks")
    p_clear.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    p_clear.set_defaults(func=cmd_clear)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
