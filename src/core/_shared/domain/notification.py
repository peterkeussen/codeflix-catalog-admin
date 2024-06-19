from dataclasses import dataclass


@dataclass
class Notification:
    def __init__(self):
        self._errors = []

    def add_error(self, field, message):
        self._errors.append({"field": field, "message": message})

    @property
    def has_errors(self):
        return len(self._errors) > 0

    @property
    def errors(self):
        return ",".join(
            [f"{error['field']} {error['message']}" for error in self._errors]
        )
