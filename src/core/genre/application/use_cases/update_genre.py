from dataclasses import dataclass, field
from uuid import UUID

from core.genre.application.exceptions import GenreDoesNotExistsException, InvalidGenreData, RelatedCategoriesNotFound


class UpdateGenre:
    def __init__(self, repository, category_repository) -> None:
        self.repository = repository
        self.category_repository = category_repository
    
    @dataclass
    class Input:
        id: UUID
        name: str
        category_ids: set[UUID] = field(default_factory=set)
    
    @dataclass
    class Output:
        id: UUID
        
    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(input.id)
        
        if not genre:
            raise GenreDoesNotExistsException(f"Genre id {input.id} does not exists")
        try:
            if input.name is not None:
                genre.name = input.name
            if input.category_ids is not None:
                for category_id in input.category_ids:
                    if not self.category_repository.get_by_id(category_id):
                        raise RelatedCategoriesNotFound(f"Related category not found: {category_id}")
                genre.categories = input.category_ids
            if genre.is_active is True:
                genre.activate()
            else:
                genre.deactivate()
            
            genre.validate()
        except ValueError as error:
            raise InvalidGenreData(error) from error
        self.repository.update(genre)
        
        