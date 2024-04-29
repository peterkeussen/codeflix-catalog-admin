from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.cast_member.application.use_case.create_cast_member import (
    CreateCastMember,
    CreateCastMemberRequest,
)
from src.core.cast_member.application.use_case.delete_cast_member import (
    DeleteCastMember,
    DeleteCastMemberRequest,
)
from src.core.cast_member.application.use_case.exceptions import CastmemberNotFound
from src.core.cast_member.application.use_case.list_cast_member import (
    ListCastMember,
    ListCastMemberRequest,
)
from src.core.cast_member.application.use_case.update_cast_member import (
    UpdateCastMember,
    UpdateCastMemberResquest,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer,
    CreateCastMemberResponseSerializer,
    DeleteCastMemberRequestSerializer,
    ListCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer,
)


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        ordering = request.query_params.get("ordering", "asc")
        current_page = request.query_params.get("current_page", 1)
        page_size = request.query_params.get("page_size", 10)
        input = ListCastMemberRequest(
            order_by=order_by,
            ordering=ordering,
            current_page=int(current_page),
            page_size=int(page_size),
        )
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())
        output = use_case.execute(input)
        serializer = ListCastMemberResponseSerializer(instance=output)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCastMemberRequest(**serializer.validated_data)
        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        output = use_case.execute(input)

        return Response(
            status=status.HTTP_201_CREATED,
            data=CreateCastMemberResponseSerializer(instance=output).data,
        )

    def update(self, request: Request, pk: UUID) -> Response:
        serializer = UpdateCastMemberRequestSerializer(data={**request.data, "id": pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateCastMemberResquest(**serializer.validated_data)
        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            output = use_case.execute(input)
        except CastmemberNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk: UUID) -> Response:
        serializer = DeleteCastMemberRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())

        try:
            use_case.execute(DeleteCastMemberRequest(**serializer.validated_data))
            # use_case.execute(DeleteCategoryRequest(id=serializer.validated_data["id"]))
        except CastmemberNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
