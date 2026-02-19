from django.http import HttpResponse, FileResponse
from django.conf import settings
import os

def animated_favicon(request):
    file_path = os.path.join(settings.BASE_DIR, "Pyshop", "animated_favicon.gif")
    return FileResponse(open(file_path, "rb"), content_type="image/x-icon")

def favicon(request):
    file_path = os.path.join(settings.BASE_DIR, "Pyshop", "favicon.ico")
    return FileResponse(open(file_path, "rb"), content_type="image/x-icon")


def robots_txt(request):
    file_path = os.path.join(settings.BASE_DIR, "Pyshop", "robots.txt")
    with open(file_path, "r") as f:
        content = f.read()
    return HttpResponse(content, content_type="text/plain")
