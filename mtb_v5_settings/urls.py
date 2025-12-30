from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("django_ckeditor_5/", include("django_ckeditor_5.urls")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=settings.STATIC_URL + "imgs/icons/favicon.ico"),
    ),
    path("", include("mtb_v5_app.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
