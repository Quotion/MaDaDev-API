from main.views import *
from activation.views import *
from MaDaDevAPI import settings

from rest_framework import routers, permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework_simplejwt.views import TokenRefreshView

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename="User Models")
router.register('auth', AuthAPIView, basename="User Auth")
router.register('products', ProductAPIView, basename="Project's Product")
router.register('product_types', ProductTypeAPIView, basename="Project's type")
router.register('mini_news', MiniNewsAPIView, basename="Mini news")


activation_router = routers.DefaultRouter()
activation_router.register('token', TokenConfirmView, basename="TokenConfirm")


schema_view = get_schema_view(
    openapi.Info(
        title="MaDaDev API",
        default_version='v0.3.1',
        description="MaDaDev API предоставляет доступ к всем необходимым ресурсам сервисов MaDaDev",
        terms_of_service="https://madadev.ru",
        contact=openapi.Contact(url="https://madadev.ru", email="testsystemmadadev@mail.ru"),
        license=openapi.License(name="MaDaDev License")
    ),
    patterns=[path('api/v1/', include(router.urls)),
              path('user/', include(activation_router.urls)), ],
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('api/v1/', include(router.urls)),
    path('user/', include(activation_router.urls)),

    path('api/v1/user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
