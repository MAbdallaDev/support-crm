from django.db import models


class StoredFile(models.Model):
    """File bytes kept in PostgreSQL.

    Serverless hosting (Vercel) has no persistent disk, so uploaded media lives
    in the database instead. `name` is the storage path Django generates
    (e.g. `attachments/2026/11/report.pdf`) and is what MEDIA_URL links to.
    """

    name = models.CharField(max_length=255, unique=True)
    content = models.BinaryField()
    content_type = models.CharField(max_length=127, blank=True)
    size = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name
