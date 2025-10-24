"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),

    # URLs de tu app principal
    path("", include(("core.urls", "core"), namespace="core")),

    # Auth de Django (login/logout/reset...)
    path("accounts/", include("django.contrib.auth.urls")),

    # Página de "sesión cerrada" (si la usas)
    path(
        "accounts/logged-out/",
        TemplateView.as_view(template_name="registration/logged_out.html"),
        name="logged_out",
    ),

    # Evitar /accounts/profile/ 404
    path(
        "accounts/profile/",
        RedirectView.as_view(pattern_name="core:home", permanent=False),
    ),
]
