import mimetypes

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class DatabaseStorage(Storage):
    """Django storage backend that keeps file bytes in the `StoredFile` table."""

    def _model(self):
        # Imported lazily: storages are instantiated before the app registry is ready.
        from apps.files.models import StoredFile

        return StoredFile

    def _open(self, name, mode="rb"):
        row = self._model().objects.get(name=name)
        return ContentFile(bytes(row.content), name=name)

    def _save(self, name, content):
        content.seek(0)
        data = content.read()
        content_type = (
            getattr(content, "content_type", None)
            or mimetypes.guess_type(name)[0]
            or "application/octet-stream"
        )
        self._model().objects.create(
            name=name, content=data, content_type=content_type, size=len(data)
        )
        return name

    def exists(self, name):
        return self._model().objects.filter(name=name).exists()

    def delete(self, name):
        self._model().objects.filter(name=name).delete()

    def size(self, name):
        return self._model().objects.values_list("size", flat=True).get(name=name)

    def url(self, name):
        return f"{settings.MEDIA_URL}{name}"
