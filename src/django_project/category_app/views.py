from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.use_cases.exceptions import (
    CategoryDoesNotExistsException,
)
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.django_project.category_app.repository import DjangoCategoryRepository
from src.django_project.category_app.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    ListCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
)


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()
        use_case = ListCategory(repository=DjangoCategoryRepository())
        output = use_case.execute(input)

        serializer = ListCategoryResponseSerializer(instance=output)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request: Request, pk: str) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        category_pk = serializer.validated_data["id"]

        use_case = GetCategory(repository=DjangoCategoryRepository())

        input = GetCategoryRequest(id=category_pk)

        try:
            output = use_case.execute(input)
        except CategoryDoesNotExistsException:
            return Response(status=status.HTTP_404_NOT_FOUND)

        category_output = RetrieveCategoryResponseSerializer(instance=output)

        return Response(
            status=status.HTTP_200_OK,
            data=category_output.data,
        )

    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoCategoryRepository())
        output = use_case.execute(input)

        return Response(
            status=status.HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(instance=output).data,
        )

    def update(self, request: Request, pk: str) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={**request.data, "id": pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoCategoryRepository())
        try:
            output = use_case.execute(input)
        except CategoryDoesNotExistsException:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request: Request, pk: str) -> Response:
        serializer = UpdateCategoryRequestSerializer(
            data={**request.data, "id": pk}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoCategoryRepository())
        try:
            output = use_case.execute(input)
        except CategoryDoesNotExistsException:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk: str) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCategory(repository=DjangoCategoryRepository())

        try:
            use_case.execute(DeleteCategoryRequest(**serializer.validated_data))
            # use_case.execute(DeleteCategoryRequest(id=serializer.validated_data["id"]))
        except CategoryDoesNotExistsException:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)