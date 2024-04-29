from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.exceptions import (
    GenreDoesNotExistsException,
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.list_genre import (
    ListGenre,
    ListGenreInput,
    ListGenreOutput,
)
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import (
    CreateGenreInputSerializer,
    CreateGenreOutputSerializer,
    DeleteGenreInputSerializer,
    ListGenreResponseSerializer,
    UpdateGenreInputSerializer,
)


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        ordering = request.query_params.get("ordering", "asc")
        current_page = request.query_params.get("current_page", 1)
        page_size = request.query_params.get("page_size", 10)
        input = ListGenreInput(
            order_by=order_by,
            ordering=ordering,
            current_page=int(current_page),
            page_size=int(page_size),
        )
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenreOutput = use_case.execute(input)
        response_serializer = ListGenreResponseSerializer(instance=output)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateGenre.Input(**serializer.validated_data)
        use_case = CreateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )
        try:
            output = use_case.execute(input)
        except (InvalidGenreData, RelatedCategoriesNotFound) as error:
            return Response(data={"Error"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            status=status.HTTP_201_CREATED,
            data=CreateGenreOutputSerializer(instance=output).data,
        )

    def retrieve(self):
        pass

    def update(self, request: Request, pk: UUID = None) -> Response:
        serializer = UpdateGenreInputSerializer(data={**request.data, "id": pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateGenre.Input(**serializer.validated_data)
        use_case = UpdateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )
        try:
            use_case.execute(input)
        except GenreDoesNotExistsException:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (InvalidGenreData, RelatedCategoriesNotFound) as error:
            return Response(
                data={"error": str(error)}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self):
        pass

    def destroy(self, request: Request, pk: UUID = None) -> Response:
        request_data = DeleteGenreInputSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)

        input = DeleteGenre.Input(**request_data.validated_data)
        use_case = DeleteGenre(repository=DjangoORMGenreRepository())

        try:
            use_case.execute(input)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
