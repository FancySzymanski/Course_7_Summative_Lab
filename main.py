import argparse

from models.user import User
from services.ai_client import OllamaChatClient
from services.project_summary import summarize_project
from services.storage_service import load_users, save_users


def find_user(users, name):
    return next((u for u in users if u.name == name), None)


def add_user(args, users):
    if find_user(users, args.name):
        raise ValueError("A user with that name already exists")
    user = User(args.name, args.email)
    users.append(user)
    return f"User '{user.name}' added."


def list_users(args, users):
    if not users:
        return "No users yet."
    return "\n".join(str(u) for u in users)

def find_project(users, title):
    for user in users:
        project = user.get_project(title)
        if project:
            return project
    return None

def add_project(args, users):
    user = find_user(users, args.user)
    if not user:
        raise ValueError(f"User '{args.user}' not found")
    if find_project(users, args.title):
        raise ValueError("A project with that name already exists")
    user.add_project(args.title, args.description, args.due_date)
    return f"Project '{args.title}' added to {user.name}."

def list_projects(args, users):
    user = find_user(users, args.user)
    if not user:
        raise ValueError(f"User '{args.user}' not found")
    if not user.projects:
        return f"{user.name} has no projects yet."
    return "\n".join(str(p) for p in user.projects)

def add_task(args, users):
    project = find_project(users, args.project)
    if not project:
        raise ValueError(f"Project '{args.project}' not found")
    task = project.add_task(args.title, args.assigned_to)
    return f"Task '{task.title}' added to '{project.title}'."

def complete_task(args, users):
    project = find_project(users, args.project)
    if not project:
        raise ValueError(f"Project '{args.project}' not found")
    task = project.get_task(args.task)
    if not task:
        raise ValueError(f"Task '{args.task}' not found in '{project.title}'")
    task.complete()
    return f"Task '{task.title}' marked complete."

def summarize(args, users):
    project = find_project(users, args.project)
    if not project:
        raise ValueError(f"Project '{args.project}' not found")
    return summarize_project(OllamaChatClient(), project)

def build_parser():
    parser = argparse.ArgumentParser(description="Project Management CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-user", help="Create a user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=True)
    p.set_defaults(func=add_user)

    p = sub.add_parser("list-users", help="List all users")
    p.set_defaults(func=list_users)

    p = sub.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--due-date", default=None)
    p.set_defaults(func=add_project)

    p = sub.add_parser("list-projects", help="List a user's projects")
    p.add_argument("--user", required=True)
    p.set_defaults(func=list_projects)

    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assigned-to", default=None)
    p.set_defaults(func=add_task)

    p = sub.add_parser("complete-task", help="Mark a task complete")
    p.add_argument("--project", required=True)
    p.add_argument("--task", required=True)
    p.set_defaults(func=complete_task)

    p = sub.add_parser("summarize-project", help="AI summary of a project")
    p.add_argument("--project", required=True)
    p.set_defaults(func=summarize)

    return parser


def main():
    args = build_parser().parse_args()
    try:
        users = load_users()
        print(args.func(args, users))
        save_users(users)
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()