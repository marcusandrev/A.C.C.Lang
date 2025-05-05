class UnexpectedError(Exception):
    def __init__(self, message, position=None):
        self.message = message
        self.position = position
        super().__init__(self.message)

    def __str__(self):
        return self.message