"""DatabaseStorage keeps upload bytes in PostgreSQL and serves them at MEDIA_URL."""

import pytest
from django.core.files.base import ContentFile
from django.test import Client

from apps.files.models import StoredFile
from apps.files.storage import DatabaseStorage

pytestmark = pytest.mark.django_db


def test_save_open_size_exists_delete_round_trip():
    storage = DatabaseStorage()

    name = storage.save("attachments/2026/11/note.txt", ContentFile(b"hello", name="note.txt"))

    assert storage.exists(name)
    assert storage.size(name) == 5
    assert storage.open(name).read() == b"hello"
    assert storage.url(name) == f"/media/{name}"

    storage.delete(name)
    assert not storage.exists(name)


def test_duplicate_names_get_a_unique_suffix():
    storage = DatabaseStorage()

    first = storage.save("attachments/x.png", ContentFile(b"1"))
    second = storage.save("attachments/x.png", ContentFile(b"2"))

    assert first != second
    assert StoredFile.objects.count() == 2


@pytest.mark.urls("apps.files.tests.urls")
def test_serves_images_inline_with_a_sandbox_csp():
    StoredFile.objects.create(name="attachments/a.png", content=b"\x89PNG", content_type="image/png", size=4)

    response = Client().get("/media/attachments/a.png")

    assert response.status_code == 200
    assert response.content == b"\x89PNG"
    assert response["Content-Type"] == "image/png"
    assert response["Content-Disposition"].startswith("inline")
    assert "sandbox" in response["Content-Security-Policy"]
    assert response["X-Content-Type-Options"] == "nosniff"


@pytest.mark.urls("apps.files.tests.urls")
def test_other_types_are_forced_to_download():
    StoredFile.objects.create(
        name="attachments/page.html", content=b"<script>", content_type="text/html", size=8
    )

    response = Client().get("/media/attachments/page.html")

    assert response["Content-Disposition"].startswith("attachment")


@pytest.mark.urls("apps.files.tests.urls")
def test_missing_file_is_404():
    assert Client().get("/media/attachments/nope.png").status_code == 404
