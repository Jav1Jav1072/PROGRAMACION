class Utilidades:
    @staticmethod
    def es_primo(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def factorial(n):
        resultado = 1
        for i in range(1, n + 1):
            resultado *= i
        return resultado

    @staticmethod
    def es_palindromo(cadena):
        cadena = cadena.lower().replace(" ", "")
        return cadena == cadena[::-1]

    @staticmethod
    def suma_digitos(n):
        return sum(int(d) for d in str(abs(n)))


# Pruebas
if __name__ == "__main__":
    print(Utilidades.es_primo(7))              # True
    print(Utilidades.factorial(5))             # 120
    print(Utilidades.es_palindromo("oso"))     # True
    print(Utilidades.suma_digitos(1234))       # 10
