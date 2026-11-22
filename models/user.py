from models.project import Project


class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email            # goes through the setter

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or "@" not in value:
            raise ValueError("Email must be a valid email (must include an '@' symbol)")
        self._email = value
        return self._email

    def __str__(self):
        return f"{self.name} - {self.email}"


class User(Person):
    def __init__(self, name, email):
        super().__init__(name, email)
        self.projects = []

    def add_project(self, title, description="", due_date=None):
        project = Project(title, description, due_date)
        self.projects.append(project)
        return project

    def get_project(self, title):
        for project in self.projects:
            if project.title == title:
                return project
        return None

    def __str__(self):
        count = len(self.projects)
        return f"{super().__str__()}\nTotal projects: {count}"