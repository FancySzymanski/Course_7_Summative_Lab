class Task:
    _next_id = 1

    def __init__(self, title, assigned_to=None):
        self.id = Task._next_id
        Task._next_id += 1
        self.title = title
        self.assigned_to = assigned_to
        self.completed = False 

    @property
    def status(self):
        return "complete" if self.completed else "pending"

    def complete(self):
        self.completed = True

    def __str__(self):
        box = "x" if self.completed else " "
        who = f" ({self.assigned_to})" if self.assigned_to else ""
        return f"[{box}] {self.id}: {self.title}{who}"

    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "assigned_to": self.assigned_to,
        "completed": self.completed,
        }   

    @classmethod
    def from_dict(cls, data):
        task = cls(data["title"], data.get("assigned_to"))
        task.id = data["id"]                    # replace the fresh ID with the saved one
        task.completed = data["completed"]      # replace the default False with the saved value
        Task._next_id = max(Task._next_id, task.id + 1)
        return task