# todo-cli

Manage daily tasks from the terminal — zero-dependency Python CLI.

Tasks are stored as JSON in `~/.todo.json`, so the list survives restarts
and stays readable by any other tool.

## Install

Requires Python 3.8+. No third-party packages.

```sh
chmod +x todo.py
# optional: put it on your PATH
ln -s "$PWD/todo.py" /usr/local/bin/todo
```

## Usage

```sh
# add a task (priority: low / medium / high, default medium)
python3 todo.py add "Buy milk" -p high --due 2026-11-25
python3 todo.py add "Read the weekly report"

# list open tasks, highest priority first
python3 todo.py list

# list everything, including completed tasks
python3 todo.py list --all

# mark a task done / delete a task
python3 todo.py done 2
python3 todo.py remove 3

# delete all completed tasks (asks first; -y skips the prompt)
python3 todo.py clear
```

## Example

```sh
$ python3 todo.py add "Ship the release notes" -p high --due 2026-11-24
Added #1: Ship the release notes

$ python3 todo.py add "Water the plants"
Added #2: Water the plants

$ python3 todo.py list
 ID  !  Due         Title
  1 [ ] H  2026-11-24  Ship the release notes
  2 [ ] M  -         Water the plants

2 open, 0 done.

$ python3 todo.py done 1
Done #1: Ship the release notes
```

## Data format

`~/.todo.json` is a JSON list of objects:

```json
[
  {"id": 1, "title": "Ship the release notes", "priority": "high",
   "due": "2026-11-24", "done": true}
]
```

## License

MIT
