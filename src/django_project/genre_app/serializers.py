from rest_framework import serializers

from src.django_project._shared.serializers.serializers import (
    ListPaginatorResponseSerializer,
)


class GenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListGenreResponseSerializer(ListPaginatorResponseSerializer):
    data = GenreOutputSerializer(many=True)  # type: ignore


class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_internal_value(value))


class CreateGenreInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField())


class CreateGenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class DeleteGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()
    categories = SetField(child=serializers.UUIDField())
