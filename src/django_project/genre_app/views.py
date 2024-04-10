from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from core.genre.application.exceptions import InvalidGenreData, RelatedCategoriesNotFound
from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.tests.application import use_cases
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.serializers import CreateGenreInputSerializer, CreateGenreOutputSerializer, ListGenreResponseSerializer
from src.core.genre.application.use_cases.list_genre import (
    ListGenre,
)

class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(ListGenre.Imput())
        response_serializer = ListGenreResponseSerializer(instance=output)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateGenre.Input(**serializer.validated_data)
        use_case = CreateGenre(
            repository=DjangoORMGenreRepository(), 
            category_repository=DjangoORMCategoryRepository()
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

    def update(self):
        pass

    def partial_update(self):
        pass

    def destroy(self):
        pass