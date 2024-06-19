from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response


class VideoViewSet(viewsets.ModelViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "title")
        ordering = request.query_params.get("ordering", "asc")
        current_page = request.query_params.get("current_page", 1)
        page_size = request.query_params.get("page_size", 10)
        input = ListVideoRequest(
            order_by=order_by,
            ordering=ordering,
            current_page=int(current_page),
            page_size=int(page_size),
        )
        use_case = ListVideo(repository=DjangoORMVideoRepository())
        output = use_case.execute(input)

        serializer = ListVideoResponseSerializer(instance=output)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request: Request) -> Response:
        raise NotImplementedError

    def update(self, request: Request, pk: UUID) -> Response:
        raise NotImplementedError

    def partial_update(self, request: Request, pk: UUID) -> Response:
        raise NotImplementedError

    def destroy(self, request: Request, pk: UUID) -> Response:
        raise NotImplementedError
