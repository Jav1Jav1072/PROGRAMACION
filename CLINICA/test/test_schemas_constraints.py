# tests/test_schema_constraints.py
import sqlite3
import pytest

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

@pytest.fixture
def conn():
    # DB en memoria para tests aislados
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA_SQL)
    c.row_factory = sqlite3.Row
    yield c
    c.close()

def test_foreign_key_constraint(conn):
    cur = conn.cursor()
    # Insertar usuario y mascota correctamente
    cur.execute("INSERT INTO usuarios (nombre, email, password, rol) VALUES (?,?,?,?)",
                ("User A", "a@example.com", "pass", "cliente"))
    uid = cur.lastrowid

    cur.execute("INSERT INTO mascotas (nombre, usuario_id) VALUES (?,?)",
                ("Fido", uid))
    mid = cur.lastrowid

    # Intentar insertar mascota con usuario inexistente debe fallar por FK
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("PRAGMA foreign_keys = ON")  # activar comprobación de FK
        cur.execute("INSERT INTO mascotas (nombre, usuario_id) VALUES (?, ?)",
                    ("Ghost", 9999))
        conn.commit()

def test_unique_cita_constraint(conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (nombre, email, password, rol) VALUES (?,?,?,?)",
                ("User B", "b@example.com", "pass", "cliente"))
    uid = cur.lastrowid
    cur.execute("INSERT INTO mascotas (nombre, usuario_id) VALUES (?,?)", ("Whiskers", uid))
    mid = cur.lastrowid

    # Insertar cita primera vez
    cur.execute("INSERT INTO citas (mascota_id, fecha, hora, motivo) VALUES (?, ?, ?, ?)",
                (mid, "2099-01-01", "10:00", "Revisión"))
    conn.commit()

    # Intentar insertar la misma mascota/fecha/hora => UNIQUE debe impedirlo
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO citas (mascota_id, fecha, hora, motivo) VALUES (?, ?, ?, ?)",
                    (mid, "2099-01-01", "10:00", "Otra"))
        conn.commit()
