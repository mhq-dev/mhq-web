from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="MHQ",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/admin/', admin.site.urls),
    path('api/auth', include('authentication.urls')),
    path('api/', include('collection.urls')),
    path('api/', include('request.urls'))
]
