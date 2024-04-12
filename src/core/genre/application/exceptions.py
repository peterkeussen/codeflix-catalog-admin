class RelatedCategoriesNotFound(Exception):
    pass


class InvalidGenreData(Exception):
    pass


class GenreDoesNotExistsException(Exception):
    def __init__(self, message="Genre does not exists"):
        super().__init__(message)

    # def __init__(self, message, error_code):
    #     super().__init__(message)
    #     self.error_code = error_code


class GenreNotFoundException(Exception):
    pass
