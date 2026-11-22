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