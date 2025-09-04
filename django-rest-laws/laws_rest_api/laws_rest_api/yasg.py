from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Закомментированные строки - параметры с защитой
schema_view = get_schema_view(
    openapi.Info(
        title           = 'Django-react-web-game',
        default_version = 'v1',
        description     = 'Test description',
        license         = openapi.License(name='BSD Lisense'),
    ),
    public = True,
    # Кто может просматривать документацию
    permission_classes = (
        permissions.AllowAny,
        #permissions.IsAdminUser,  # Доступ к документации только для пользователей с is_staff
    ),
)

urlpatterns = [
    # staff_member_required - Проверяет, авторизирован ли пользователь и есть ли у него привилегия is_staff
    #path('swagger(?P<format>\.json|\.yaml)', staff_member_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    path('swagger<format:json|yaml>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/',                         schema_view.with_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/',                           schema_view.with_ui(cache_timeout=0), name='schema-redoc'),
]