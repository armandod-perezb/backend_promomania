from django.test import TestCase
from rest_framework.test import APIClient

from categoria.models import Categoria
from supermercado.models import Supermercado
from usuario.models import Usuario

from .models import Promocion, TipoPromocion


class PromocionAprobacionPuntuacionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Usuario.objects.create(
            nombre='Admin',
            correo='admin@test.com',
            password='secret',
            rol='admin',
        )
        self.usuario = Usuario.objects.create(
            nombre='Usuario',
            correo='usuario@test.com',
            password='secret',
            rol='usuario',
        )
        self.categoria = Categoria.objects.create(nombre='Mercado')
        self.supermercado = Supermercado.objects.create(nombre='Tienda')
        self.tipo = TipoPromocion.objects.create(nombre='Descuento')
        self.promocion = Promocion.objects.create(
            codigo='PROMO_TEST',
            titulo='Promo test',
            precio=1000,
            tipo_vigencia='permanente',
            estado='pendiente',
            id_usuario=self.usuario,
            id_supermercado=self.supermercado,
            id_categoria=self.categoria,
            id_tipo_promocion=self.tipo,
        )
        self.client.force_authenticate(user=self.admin)

    def test_aprobar_promocion_otorga_puntos_al_usuario_creador(self):
        response = self.client.patch(
            f'/api/promociones/{self.promocion.codigo}/',
            {'estado': 'aprobada'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.usuario.refresh_from_db()
        self.promocion.refresh_from_db()
        self.assertEqual(self.usuario.puntuacion, 100)
        self.assertEqual(self.usuario.nivel, 1)
        self.assertTrue(self.promocion.puntuacion_otorgada)

    def test_reaprobar_promocion_no_duplica_puntos(self):
        self.client.patch(
            f'/api/promociones/{self.promocion.codigo}/',
            {'estado': 'aprobada'},
            format='json',
        )
        self.client.patch(
            f'/api/promociones/{self.promocion.codigo}/',
            {'estado': 'rechazada'},
            format='json',
        )
        self.client.patch(
            f'/api/promociones/{self.promocion.codigo}/',
            {'estado': 'aprobada'},
            format='json',
        )

        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.puntuacion, 100)
