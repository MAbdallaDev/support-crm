from django.urls import path

from apps.files.views import serve_file

# The media route is only mounted in config.urls when MEDIA_STORAGE == "db";
# these tests exercise the view regardless of the environment's storage mode.
urlpatterns = [path("media/<path:name>", serve_file)]
