from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import include

# Swagger/OpenAPI schema view
schema_view = get_schema_view(
   openapi.Info(
      title="My Project API",
      default_version='v1',
      description="API documentation for my project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Root view
def home(request):
    return HttpResponse("Welcome to My API! Go to /api/doc/ to see docs.")

urlpatterns = [
    # Root URL
    path('', home, name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # API Docs (Swagger UI)
    path('api/doc/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),

    # Redoc UI (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API Schema (OpenAPI JSON)
    path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Optional: YAML schema
    path('api/schema.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),

    path('api/', include('user.urls')),
]
