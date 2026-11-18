from django.http import Http404, HttpResponse
from django.utils.http import content_disposition_header

from apps.files.models import StoredFile

# Types a browser may render inline. Anything else (HTML, SVG, scripts...) is
# forced to download so an upload can never run as a page on the API origin.
INLINE_TYPES = {
    "image/png", "image/jpeg", "image/gif", "image/webp", "application/pdf", "text/plain",
}


def serve_file(request, name):
    """Serve a database-stored upload at MEDIA_URL/<name>.

    Public by path, exactly like the filesystem `static()` serving it replaces:
    paths include Django's upload_to date folders and a de-duplicated filename.
    """
    try:
        row = StoredFile.objects.only("content", "content_type", "name").get(name=name)
    except StoredFile.DoesNotExist as exc:
        raise Http404("File not found") from exc
    content_type = row.content_type or "application/octet-stream"
    response = HttpResponse(bytes(row.content), content_type=content_type)
    response["Content-Disposition"] = content_disposition_header(
        as_attachment=content_type not in INLINE_TYPES, filename=name.rsplit("/", 1)[-1]
    )
    response["Content-Security-Policy"] = "sandbox; default-src 'none'; img-src 'self'"
    response["Cache-Control"] = "public, max-age=86400"
    response["X-Content-Type-Options"] = "nosniff"
    return response
