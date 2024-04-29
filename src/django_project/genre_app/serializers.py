from rest_framework import serializers


class GenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    total = serializers.IntegerField()


class ListGenreResponseSerializer(serializers.Serializer):
    data = GenreOutputSerializer(many=True)  # type: ignore
    meta = ListOutputMetaSerializer()


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
