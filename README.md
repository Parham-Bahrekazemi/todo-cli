# Todo CLI

A lightweight command-line To-Do application built with **Python** and **Typer**.

This project provides a simple way to manage tasks directly from the terminal while demonstrating clean project organization, JSON file storage, and unit testing with **pytest**.

---

## Features

- Initialize a new todo database
- Add new tasks
- List all tasks
- Mark tasks as completed
- Remove individual tasks
- Remove all tasks
- JSON-based storage
- Command-line interface powered by Typer
- Unit tests with pytest

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/todo-cli.git

cd todo-cli
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Requirements

- Python 3.10+
- Typer
- Colorama
- Shellingham
- Pytest

---

## Usage

### Initialize the application

```bash
python -m todo init
```

---

### Add a task

```bash
python -m todo add Buy milk
```

or

```bash
python -m todo add Clean the house --priority 1
```

---

### List tasks

```bash
python -m todo list
```

Example:

```
to-do list:

ID | priority | done | description
----------------------------------
1  | (1)      | False | Buy milk.
2  | (2)      | False | Clean the house.
```

---

### Complete a task

```bash
python -m todo complete 1
```

---

### Remove a task

```bash
python -m todo remove 2
```

Force removal without confirmation:

```bash
python -m todo remove 2 --force
```

---

### Remove all tasks

```bash
python -m todo clear
```

---

### Show version

```bash
python -m todo --version
```

---

## Project Structure

```
todo-cli/
│
├── todo/
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   └── todo.py
│
├── test/
│   └── test_todo.py
│
├── requirements.txt
└── README.md
```

---

## Running Tests

```bash
pytest
```

---

## Technologies

- Python
- Typer
- Pytest
- JSON
- pathlib
- configparser

---

## Future Improvements

- Edit existing tasks
- Search tasks
- Due dates
- Colored terminal output
- Task categories
- Export/Import tasks
- Sorting and filtering
- Rich terminal UI
