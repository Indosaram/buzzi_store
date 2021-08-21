"""Exceptions"""


class NotAnUrlError(Exception):
    """Raised when result is not an url"""

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)


class NoUrlExistError(Exception):
    """Raised when there is no url"""

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidMetadataError(Exception):
    """Raised when metadata is invalid"""

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)
