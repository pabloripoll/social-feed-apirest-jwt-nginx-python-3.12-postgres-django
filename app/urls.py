from django.urls import path, include
from django.http import JsonResponse

def root(request):
    return JsonResponse({"message": "Welcome. API available at /api/<version>/"})

def apiroot(request):
    return JsonResponse({"message": "Welcome. API V1 available at /api/v1/"})

urlpatterns = [
    path("", root, name="root"),

    path("api/", apiroot, name="api-root"),

    # capture version in the URL and pass it into the included urls (request.version will be set <str:version>)
    path("api/v1/", include("api.urls_v1"), name="api-v1"),
]
