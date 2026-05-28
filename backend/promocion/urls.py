from rest_framework.routers import DefaultRouter

from .views import PromocionHorarioViewSet, PromocionViewSet, TipoPromocionViewSet

router = DefaultRouter()
router.register('', PromocionViewSet, basename='promocion')
router.register('tipos', TipoPromocionViewSet, basename='tipo-promocion')
router.register('horarios', PromocionHorarioViewSet, basename='promocion-horario')

urlpatterns = router.urls
