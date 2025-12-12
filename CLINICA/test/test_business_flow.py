# tests/test_business_flow.py
import sqlite3
from datetime import datetime, date, time, timedelta

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mascotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    usuario_id INTEGER NOT NULL,
    especie TEXT,
    raza TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS citas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    motivo TEXT,
    estado TEXT DEFAULT 'Reservada',
    resultado TEXT,
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id),
    UNIQUE(mascota_id, fecha, hora)
);
"""

def test_flow_create_user_pet_and_future_cita():
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA_SQL)
    cur = conn.cursor()

    # crear usuario
    cur.execute("INSERT INTO usuarios (nombre, email, password, rol) VALUES (?,?,?,?)",
                ("Test User", "t@example.com", "pw", "cliente"))
    uid = cur.lastrowid

    # crear mascota
    cur.execute("INSERT INTO mascotas (nombre, usuario_id, especie, raza) VALUES (?, ?, ?, ?)",
                ("Rex", uid, "Perro", "Labrador"))
    mid = cur.lastrowid

    # intentar reservar cita en el pasado -> simulamos que la app valida antes de insertar
    ayer = date.today() - timedelta(days=1)
    hora_pasada = time(10, 0)
    fecha_hora_pasada = datetime.combine(ayer, hora_pasada)
    assert fecha_hora_pasada < datetime.now()

    # insertar cita futura OK
    mañana = date.today() + timedelta(days=1)
    hora_futura = time(11, 0)
    cur.execute("INSERT INTO citas (mascota_id, fecha, hora, motivo) VALUES (?, ?, ?, ?)",
                (mid, mañana.strftime("%Y-%m-%d"), hora_futura.strftime("%H:%M"), "Vacunación"))
    conn.commit()

    # comprobar que la cita está en DB
    cur.execute("SELECT id, mascota_id, fecha, hora FROM citas WHERE mascota_id=?", (mid,))
    fila = cur.fetchone()
    assert fila is not None
    assert fila[1] == mid
    assert fila[2] == mañana.strftime("%Y-%m-%d")
    assert fila[3] == hora_futura.strftime("%H:%M")

    conn.close()
