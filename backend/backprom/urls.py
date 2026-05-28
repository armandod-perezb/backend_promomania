"""
URL configuration for backprom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.api_views import HealthCheckView

from categoria.views import CategoriaViewSet
from comentario.views import ComentarioViewSet
from favorito.views import FavoritoViewSet
from notificacion.views import NotificacionViewSet
from promocion.views import (
    PromocionHorarioViewSet,
    PromocionViewSet,
    TipoPromocionViewSet,
)
from reporte.views import ReporteViewSet
from supermercado.views import SupermercadoViewSet
from usuario.views import AuthLoginView, AuthMeView, UsuarioNotificacionViewSet, UsuarioViewSet
from valoracion.views import ValoracionViewSet

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='usuarios')
router.register('usuarios-notificaciones', UsuarioNotificacionViewSet, basename='usuarios-notificaciones')
router.register('categorias', CategoriaViewSet, basename='categorias')
router.register('supermercados', SupermercadoViewSet, basename='supermercados')
router.register('promociones', PromocionViewSet, basename='promociones')
router.register('tipos-promocion', TipoPromocionViewSet, basename='tipos-promocion')
router.register('promociones-horarios', PromocionHorarioViewSet, basename='promociones-horarios')
router.register('comentarios', ComentarioViewSet, basename='comentarios')
router.register('favoritos', FavoritoViewSet, basename='favoritos')
router.register('reportes', ReporteViewSet, basename='reportes')
router.register('notificaciones', NotificacionViewSet, basename='notificaciones')
router.register('valoraciones', ValoracionViewSet, basename='valoraciones')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/auth/login/', AuthLoginView.as_view(), name='auth-login'),
    path('api/auth/me/', AuthMeView.as_view(), name='auth-me'),
    path('api/', include(router.urls)),
]
