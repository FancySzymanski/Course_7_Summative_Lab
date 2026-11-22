import json

from models.user import User

DATA_FILE = "data/project_data.json"


def save_users(users, path=DATA_FILE):
    data = {"users": [user.to_dict() for user in users]}
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


def load_users(path=DATA_FILE):
    try:
        with open(path) as file:
            data = json.load(file)
        return [User.from_dict(u) for u in data["users"]]
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        raise RuntimeError(f"Could not read {path}: {error}") from error