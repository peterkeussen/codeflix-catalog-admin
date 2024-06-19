from rest_framework import serializers


class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    num_pages = serializers.IntegerField()
    total = serializers.IntegerField()


class ListPaginatorResponseSerializer(serializers.Serializer):
    meta = ListOutputMetaSerializer(read_only=True)
