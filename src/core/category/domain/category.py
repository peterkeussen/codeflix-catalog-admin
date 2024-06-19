from dataclasses import dataclass

from src.core._shared.domain.entity import Entity


@dataclass
class Category(Entity):
    name: str
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            self.notification.add_error("Name", "must be less than 255 characters")
            # raise ValueError("Name must be less than 255 characters")

        if not self.name:
            self.notification.add_error("Name", "cannot be empty")
            # raise ValueError("Name cannot be empty")

        if len(self.description) > 1024:
            self.notification.add_error(
                "Description", "must be less than 1024 characters"
            )
            # raise ValueError("Description must be less than 1024 characters")

        if self.notification.has_errors:
            raise ValueError(self.notification.errors)

    def __str__(self) -> str:
        return f"{self.name} - {self.description} ({self.is_active})"

    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.id})>"

    def update(self, name, description):
        self.name = name
        self.description = description

        self.validate()

    def activate(self):
        self.is_active = True

        self.validate()

    def deactivate(self):
        self.is_active = False

        self.validate()
