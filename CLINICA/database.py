import sqlite3

# Conexión global
conn = sqlite3.connect("clinica.db", check_same_thread=False)
cursor = conn.cursor()

def crear_tablas():
    """
    Crea las tablas necesarias. Si las tablas ya existen, añade columnas nuevas
    'especie', 'raza', 'estado' y 'resultado' si no estaban presentes.
    """
    # Tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    """)

    # Tabla mascotas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mascotas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        usuario_id INTEGER NOT NULL,
        especie TEXT,
        raza TEXT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    # Tabla citas: añade estado y resultado para soportar historial y estados
    cursor.execute("""
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
    )
    """)

    conn.commit()

    # Asegurar columnas adicionales si DB antigua
    cursor.execute("PRAGMA table_info(mascotas)")
    cols_m = [row[1] for row in cursor.fetchall()]
    if "especie" not in cols_m:
        cursor.execute("ALTER TABLE mascotas ADD COLUMN especie TEXT")
    if "raza" not in cols_m:
        cursor.execute("ALTER TABLE mascotas ADD COLUMN raza TEXT")

    cursor.execute("PRAGMA table_info(citas)")
    cols_c = [row[1] for row in cursor.fetchall()]
    if "estado" not in cols_c:
        cursor.execute("ALTER TABLE citas ADD COLUMN estado TEXT DEFAULT 'Reservada'")
    if "resultado" not in cols_c:
        cursor.execute("ALTER TABLE citas ADD COLUMN resultado TEXT")

    conn.commit()
