from rest_framework.routers import DefaultRouter

from .views import UsuarioNotificacionViewSet, UsuarioViewSet

router = DefaultRouter()
router.register('', UsuarioViewSet, basename='usuario')
router.register('notificaciones', UsuarioNotificacionViewSet, basename='usuario-notificacion')

urlpatterns = router.urls
