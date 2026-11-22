from models.task import Task


class Project:
    def __init__(self, title, description="", due_date=None):
        self.title = title            # goes through the setter
        self.description = description
        self.due_date = due_date
        self.tasks = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
       if not value or not value.strip():
           raise ValueError("Title cannot be blank")
       self._title = value.strip()
       return self._title
    
    def add_task(self, title, assigned_to=None):
        task = Task(title, assigned_to)
        self.tasks.append(task)
        return task

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def __str__(self):
        description = f" {self.description}." if self.description else ""
        due = f" Due: {self.due_date}." if self.due_date else ""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)

        return f"{self.title} -{description}{due}\n[{completed}/{total}] Tasks completed"

    def to_dict(self):
        return {
        "title": self.title,
        "description": self.description,
        "due_date": self.due_date,
        "tasks": [task.to_dict() for task in self.tasks]
        }   

    @classmethod
    def from_dict(cls, data):
        project = cls(data["title"], data.get("description", ""), data.get("due_date"))
        project.tasks = [Task.from_dict(t) for t in data["tasks"]]
        return project