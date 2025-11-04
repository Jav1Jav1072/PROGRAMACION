"""
Pruebas con unittest.
Usa las funciones: area_por_base_altura() y area_por_lado()
"""

import unittest
import math
from src.triangulo import area_por_base_altura, area_por_lado



class TestTriangleUnittest(unittest.TestCase):

    # Tests para base/altura

    def test_area_por_base_altura_basico(self):
        # 10 * 5 / 2 = 25
        self.assertEqual(area_por_base_altura(10, 5), 25.0)

    def test_area_por_base_altura_decimal(self):
        # Comprobamos que funciona con números decimales
        self.assertAlmostEqual(area_por_base_altura(3.3, 2.0), (3.3 * 2.0) / 2)

    def test_area_por_base_altura_cero_o_negativo(self):
        # Base cero -> error
        with self.assertRaises(ValueError):
            area_por_base_altura(0, 5)
        # Altura negativa -> error
        with self.assertRaises(ValueError):
            area_por_base_altura(5, -1)

    # Tests para los lados

    def test_area_por_lado_3_4_5(self):
        # Triángulo 3-4-5 tiene área 6
        self.assertAlmostEqual(area_por_lado(3, 4, 5), 6.0)

    def test_area_por_lado_equilatero(self):
        # Equilátero de lado 2: área = sqrt(3)/4 * lado^2
        esperado = (math.sqrt(3) / 4) * (2 ** 2)
        self.assertAlmostEqual(area_por_lado(2, 2, 2), esperado)

    def test_area_por_lado_triangulo_invalido(self):
        # 1,2,3 no forman triángulo válido
        with self.assertRaises(ValueError):
            area_por_lado(1, 2, 3)

    def test_area_por_lado_negativo(self):
        # Lado negativo -> error
        with self.assertRaises(ValueError):
            area_por_lado(-3, 4, 5)


if __name__ == "__main__":
    unittest.main()
