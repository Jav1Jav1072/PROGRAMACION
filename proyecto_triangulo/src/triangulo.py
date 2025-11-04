"""
triangle.py
Código para calcular el área de un triángulo.
Incluye:
 - area_por_base_altura(base, altura): área usando base y altura.
 - area_por_lados(a, b, c): área usando los tres lados (fórmula de Herón).
Comentarios paso a paso dentro de cada función para que se entienda bien.
"""

import math  # Necesario para la función sqrt (raíz cuadrada)


def area_por_base_altura(base: float, altura: float) -> float:
    """
    Calcula el área a partir de base y altura.
    Fórmula: (base * altura) / 2

    Pasos:
    1. Comprobamos que base y altura sean números mayores que cero.
       - Si no lo son, lanzamos ValueError para avisar al llamante.
    2. Aplicamos la fórmula y devolvemos el resultado como float.
    """
    # 1) Validación sencilla: deben ser mayores que cero
    if base <= 0:
        raise ValueError("La base debe ser mayor que cero.")
    if altura <= 0:
        raise ValueError("La altura debe ser mayor que cero.")

    # 2) Cálculo del área con la fórmula clásica
    area = (base * altura) / 2

    # 3) Devolvemos el resultado
    return area


def area_por_lado(a: float, b: float, c: float) -> float:
    """
    Calcula el área a partir de los tres lados usando la fórmula de Herón.

    Fórmula:
      s = (a + b + c) / 2
      area = sqrt( s * (s - a) * (s - b) * (s - c) )

    Pasos (comentados):
    1. Validamos que los tres lados sean mayores que cero.
    2. Comprobamos que los lados formen un triángulo válido:
       - La suma de dos lados debe ser estrictamente mayor que el tercero.
       - Si no cumplen, lanzamos ValueError.
    3. Calculamos semiperímetro s.
    4. Aplicamos la fórmula de Herón y devolvemos la raíz cuadrada.
    """
    #Validación de positivos
    if a <= 0 or b <= 0 or c <= 0:
        raise ValueError("Todos los lados deben ser mayores que cero.")

    #Validación: desigualdad triangular
    #Si alguna suma de dos lados es <= tercer lado, no existe triángulo.
    if (a + b) <= c or (a + c) <= b or (b + c) <= a:
        raise ValueError("Los lados no forman un triángulo válido.")

    #Semiperímetro
    s = (a + b + c) / 2

    #Producto dentro de la raíz (puede ser pequeño por flotantes, pero aquí es directo)
    inner = s * (s - a) * (s - b) * (s - c)

    #Como protección extra (por errores numéricos mínimos) nos aseguramos de no pasar un negativo pequeño a sqrt
    if inner < 0 and abs(inner) < 1e-12:
        #Si es un negativo por error numérico minúsculo, lo ajustamos a 0
        inner = 0.0
    elif inner < 0:
        #Si es significativamente negativo, hay un problema; lanzamos excepción
        raise ValueError("Error numérico: expresión dentro de la raíz negativa.")

    #Calculamos la raíz cuadrada y devolvemos el área
    area = math.sqrt(inner)
    return area