from django.contrib import admin

from src.django_project.genre_app.models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
