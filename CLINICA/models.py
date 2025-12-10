class Cliente:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class Mascota:
    def __init__(self, id, nombre, usuario_id):
        self.id = id
        self.nombre = nombre
        self.usuario_id = usuario_id

class Cita:
    def __init__(self, id, mascota_id, fecha, hora, motivo):
        self.id = id
        self.mascota_id = mascota_id
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
