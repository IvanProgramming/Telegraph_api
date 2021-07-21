class MethodIsNotAllowed(Exception):
    def __str__(self):
        return "Method is not allowed"


class TelegraphError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return f"Telegraph Error: {self.description}"


class FileIsNotPresented(Exception):
    def __str__(self):
        return "File is not presented, so it can't be uploaded!"


class InvalidFileExtension(Exception):
    def __str__(self):
        return "File extension is not supported by telegraph!"
