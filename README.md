# Course_7_Summative_Lab
# Project Tracker CLI

## Problem
A command-line tool for a development team. Admins manage users, projects,
and tasks through CLI commands, data is saved to a local file, and an AI
client can generate a summary of a project.

## Entities and relationships
- **User**: `name`, `email`. A user has many projects (one-to-many).
- **Project**: `title`, `description`, `due_date`. A project has many tasks (one-to-many).
- **Task**: `title`, `status`, `assigned_to`.

## Commands
| Command | Purpose |
|---|---|
| `add-user --name --email` | Create a user |
| `list-users` | Show all users |
| `add-project --user --title --description` | Add a project to a user |
| `list-projects --user` | Show a user's projects |
| `add-task --project --title` | Add a task to a project |
| `assign-task --project --task --user` | Add a contributor to a task |
| `complete-task --project --task` | Mark a task complete |
| `summarize-project --project` | AI-generated project summary |

## File structure
- `main.py`: entry point, argparse commands
- `models/`: `user.py`, `project.py`, `task.py`
- `services/storage_service.py`: JSON save/load
- `services/ai_client.py`: reusable AI client
- `utils/formatters.py`: output formatting
- `data/project_data.json`: persisted data
- `requirements.txt` and `Pipfile`: dependencies (ollama)

## External package
`ollama`, used by the AI client for `summarize-project`. Listed in the Pipfile.

## Error handling
Missing users or projects, duplicate names, and an unavailable AI service
all produce a readable error message instead of a crash.