from abc import ABC, abstractmethod

# Interfaz común
class Operacion(ABC):
    @abstractmethod
    def ejecutar(self, a, b):
        pass

# Operaciones básicas
class Suma(Operacion):
    def ejecutar(self, a, b):
        return a + b

class Resta(Operacion):
    def ejecutar(self, a, b):
        return a - b

class Multiplicacion(Operacion):
    def ejecutar(self, a, b):
        return a * b

class Division(Operacion):
    def ejecutar(self, a, b):
        if b == 0:
            return "Error: no se puede dividir entre cero"
        return a / b

# Nueva operación (para probar el OCP)
class Potencia(Operacion):
    def ejecutar(self, a, b):
        return a ** b

# Calculadora
class Calculadora:
    def operar(self, operacion, a, b):
        return operacion.ejecutar(a, b)

# Menú interactivo
def mostrar_menu():
    print("\n=== CALCULADORA OCP ===")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    print("5. Potencia")
    print("0. Salir")

if __name__ == "__main__":
    calc = Calculadora()
    operaciones = {
        "1": Suma(),
        "2": Resta(),
        "3": Multiplicacion(),
        "4": Division(),
        "5": Potencia()
    }

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "0":
            print("Saliendo de la calculadora...")
            break

        if opcion not in operaciones:
            print("Opción no válida. Inténtalo de nuevo.")
            continue

        try:
            a = float(input("Introduce el primer número: "))
            b = float(input("Introduce el segundo número: "))
            resultado = calc.operar(operaciones[opcion], a, b)
            print("Resultado:", resultado)
        except ValueError:
            print("Error: introduce números válidos.")
