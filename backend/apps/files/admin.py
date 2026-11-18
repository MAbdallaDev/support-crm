from django.contrib import admin

from apps.files.models import StoredFile


@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    list_display = ("name", "content_type", "size", "created_at")
    search_fields = ("name",)
    exclude = ("content",)
