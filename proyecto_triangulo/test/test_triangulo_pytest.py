"""
Pruebas con pytest.
Usa las funciones: area_por_base_altura() y area_por_lado()
"""

import pytest
from src.triangulo import area_por_base_altura, area_por_lado


def test_area_por_base_altura_basico():
    assert area_por_base_altura(10, 5) == 25.0


def test_area_por_base_altura_invalido():
    # Base cero -> error
    with pytest.raises(ValueError):
        area_por_base_altura(0, 5)
    # Altura negativa -> error
    with pytest.raises(ValueError):
        area_por_base_altura(5, -2)


def test_area_por_lado_3_4_5():
    assert pytest.approx(area_por_lado(3, 4, 5)) == 6.0


@pytest.mark.parametrize("a,b,c", [
    (1, 2, 3),    # 1+2 = 3 → no es triángulo
    (5, 1, 1),    # 1+1 < 5 → no es triángulo
    (0.1, 0.1, 0.5)  # 0.1+0.1 < 0.5 → no es triángulo
])
def test_area_por_lado_invalido(a, b, c):
    with pytest.raises(ValueError):
        area_por_lado(a, b, c)


def test_area_por_lado_negativo():
    with pytest.raises(ValueError):
        area_por_lado(-1, 2, 2)
