"""URL configuration for config project."""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Support API",
        default_version="v1.0.1",
        description="Test API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("users/", include("users.urls")),
    path("tickets/", include("tickets.urls")),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),  # type: ignore
        name="schema-swagger-ui",
    ),
]
