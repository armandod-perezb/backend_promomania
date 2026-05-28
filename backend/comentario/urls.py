from rest_framework.routers import DefaultRouter

from .views import ComentarioViewSet

router = DefaultRouter()
router.register('', ComentarioViewSet, basename='comentario')

urlpatterns = router.urls
