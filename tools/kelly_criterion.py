from decimal import Decimal


def kelly_criterion(c, p, b):
    """
    Función que calcula la apuesta óptima según el Kelly Criterion
    :param c: Cuota que ofrece la casa de apuestas
    :param p: Probabilidad de acierto
    :param b: Cantidad total de dinero a apostar
    :return: Porcentaje de la banca a apostar, cantidad a apostar y ganancia esperada
    """

    porcentaje = ((c * p) - 1) / (c - 1)
    apuesta = b * porcentaje
    ganancia_esperada = apuesta * (c - 1)

    return porcentaje, apuesta, ganancia_esperada



# Ejecución principal
if __name__ == "__main__":

    """
Ejemplo de ejecución:
Cuota: 2.5
Probabilidad: 0.6
Bank: 10000
Porcentaje de la banca a apostar: 0.2
Apuesta: 2000.0
    """

    print("Kelly Criterion")
    print("---------------")

    # Guardamos los datos de entrada en formato decimal
    cuota = Decimal(input("Cuota: "))
    probabilidad = Decimal(input("Probabilidad: "))
    bank = Decimal(input("Bank: "))

    porcentaje_kelly, apuesta_kelly, ganancia = kelly_criterion(cuota, probabilidad, bank)

    print(f"Porcentaje de la banca a apostar: {round(porcentaje_kelly*100, 2)}%")
    print(f"Apuesta: {round(apuesta_kelly, 2)}")
    print(f"Ganancia esperada: {round(ganancia, 2)}")
