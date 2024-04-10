from django.contrib import admin

from src.django_project.category_app.models import Category


@admin.register(Category)
class CategiryAdmin(admin.ModelAdmin):
    pass
