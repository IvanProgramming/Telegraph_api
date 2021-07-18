class MethodIsNotAllowed(Exception):
    def __str__(self):
        return "Method is not allowed"


class TelegraphError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return f"Telegraph Error: {self.description}"
