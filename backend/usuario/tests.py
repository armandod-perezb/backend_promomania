from django.test import TestCase

from .models import Usuario


class UsuarioPuntuacionTests(TestCase):
    def test_calcula_nivel_con_costos_incrementales(self):
        self.assertEqual(Usuario.calcular_nivel(0), 1)
        self.assertEqual(Usuario.calcular_nivel(199), 1)
        self.assertEqual(Usuario.calcular_nivel(200), 2)
        self.assertEqual(Usuario.calcular_nivel(599), 2)
        self.assertEqual(Usuario.calcular_nivel(600), 3)

    def test_agregar_puntuacion_actualiza_nivel(self):
        usuario = Usuario(nombre='Ana', correo='ana@test.com', password='secret')

        usuario.agregar_puntuacion(200)

        self.assertEqual(usuario.puntuacion, 200)
        self.assertEqual(usuario.nivel, 2)
