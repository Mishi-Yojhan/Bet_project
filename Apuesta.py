# Import a base de datos
import sqlite3


class Apuesta:
    def __init__(self, fecha, deporte, evento, tipo_apuesta, casa, codigo, cuota, importe, resultado, beneficio):
        self.fecha = fecha
        self.deporte = deporte
        self.evento = evento
        self.tipo_apuesta = tipo_apuesta
        self.casa = casa
        self.codigo = codigo
        self.cuota = cuota
        self.importe = importe
        self.resultado = resultado
        self.beneficio = beneficio
        self.id = None

    def conectar(self):

        # Si la base de datos no existe, se crea y adentro de ella se crea la tabla apuestas

        try:
            self.conexion = sqlite3.connect("apuestas.db")
            self.cursor = self.conexion.cursor()
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS apuestas (fecha TEXT, deporte TEXT, evento TEXT, tipo_apuesta TEXT, casa TEXT, codigo TEXT, cuota REAL, importe REAL, resultado TEXT, beneficio REAL)")
            self.conexion.commit()
        except sqlite3.OperationalError as e:
            print(f"Error al conectar con la base de datos: {e}")

    def cerrar_conexion(self):
        self.conexion.close()

    def agregar_apuesta(self):
        self.conectar()

        if self.cursor:
            try:
                # Verificar si la apuesta ya existe
                self.cursor.execute(
                    "SELECT * FROM apuestas WHERE fecha = ? AND deporte = ? AND evento = ? AND tipo_apuesta = ? AND casa = ? AND codigo = ? AND cuota = ? AND importe = ? AND resultado = ? AND beneficio = ?",
                    (self.fecha, self.deporte, self.evento, self.tipo_apuesta, self.casa, self.codigo, self.cuota,
                     self.importe, self.resultado, self.beneficio))
                apuesta = self.cursor.fetchone()
                if apuesta:
                    print("La apuesta ya existe")
                else:
                    self.cursor.execute("INSERT INTO apuestas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        self.fecha, self.deporte, self.evento, self.tipo_apuesta, self.casa, self.codigo, self.cuota,
                        self.importe, self.resultado, self.beneficio))
                    self.conexion.commit()
                    print("Apuesta registrada con éxito")
            except sqlite3.OperationalError as e:
                print("Error al registrar la apuesta", e)
            finally:
                self.cerrar_conexion()

    def __str__(self):
        return f"Fecha: {self.fecha} - Deporte: {self.deporte} - Evento: {self.evento} - Tipo de apuesta: {self.tipo_apuesta} - Casa: {self.casa} - Código: {self.codigo} - Cuota: {self.cuota} - Importe: {self.importe} - Resultado: {self.resultado} - Beneficio: {self.beneficio}"

    def __repr__(self):
        return f"Fecha: {self.fecha} - Deporte: {self.deporte} - Evento: {self.evento} - Tipo de apuesta: {self.tipo_apuesta} - Casa: {self.casa} - Código: {self.codigo} - Cuota: {self.cuota} - Importe: {self.importe} - Resultado: {self.resultado} - Beneficio: {self.beneficio}"

    def __eq__(self, other):
        return self.fecha == other.fecha and self.deporte == other.deporte and self.evento == other.evento and self.tipo_apuesta == other.tipo_apuesta and self.casa == other.casa and self.codigo == other.codigo and self.cuota == other.cuota and self.importe == other.importe and self.resultado == other.resultado and self.beneficio == other.beneficio

    def __ne__(self, other):
        return self.fecha != other.fecha or self.deporte != other.deporte or self.evento != other.evento or self.tipo_apuesta != other.tipo_apuesta or self.casa != other.casa or self.codigo != other.codigo or self.cuota != other.cuota or self.importe != other.importe or self.resultado != other.resultado or self.beneficio != other.beneficio


if __name__ == "__main__":
    apuesta = Apuesta('2021-02-18', 'Fútbol', 'Real Madrid - Barcelona', 'Ganador', 'Bet365', '1', 1.5, 100, 'Ganado',
                      50)
    apuesta.agregar_apuesta()
