from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import RedirectView

def root(request):
    return JsonResponse({"message": "Welcome. API available at /api/<version>/"})

urlpatterns = [
    path("", root, name="root"),
    path("admin/", admin.site.urls),
    # capture version in the URL and pass it into the included urls (request.version will be set)
    path("api/<str:version>/", include("api.urls")),
    # Optional convenience: redirect /api to default version path
    #path("api/", RedirectView.as_view(pattern_name='api-root', permanent=False)),
]
