from rest_framework.routers import DefaultRouter

from .views import SupermercadoViewSet

router = DefaultRouter()
router.register('', SupermercadoViewSet, basename='supermercado')

urlpatterns = router.urls
