import streamlit as st
from database import conn, cursor

# Lista de especies (6 más comunes) + 'Otro'
ESPECIES_COMUNES = [
    "Perro",
    "Gato",
    "Pájaro",
    "Conejo",
    "Hámster",
    "Pez",
    "Otro"
]

def crear_admin():
    """
    Crea un admin por defecto si no existe ninguno.
    """
    cursor.execute("SELECT * FROM usuarios WHERE rol='admin'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO usuarios (nombre, email, password, rol)
        VALUES ('Clínica', 'admin@clinica.com', 'admin123', 'admin')
        """)
        conn.commit()

def login():
    """
    Formulario de inicio de sesión.
    """
    st.title("🐾 Login")

    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        cursor.execute("""
        SELECT * FROM usuarios WHERE email=? AND password=?
        """, (email, password))
        user = cursor.fetchone()

        if user:
            st.session_state.usuario = {
                "id": user[0],
                "nombre": user[1],
                "rol": user[4]
            }
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

def registro_cliente():
    """
    Registro de cliente con opción de registrar una mascota al mismo tiempo.
    La especie se selecciona mediante un selectbox con 6 opciones + "Otro".
    """
    st.title("Registro de cliente")

    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Email")
    with col2:
        password = st.text_input("Contraseña", type="password")
        tiene_mascota = st.checkbox("¿Tienes mascota?")

    # Campos de mascota que sólo se muestran si marca 'tiene_mascota'
    nombre_mascota = ""
    especie = ""
    raza = ""
    if tiene_mascota:
        st.markdown("**Datos de la mascota**")
        nombre_mascota = st.text_input("Nombre de la mascota")
        # Desplegable con especies comunes
        especie_sel = st.selectbox("Especie", ESPECIES_COMUNES)
        if especie_sel == "Otro":
            especie = st.text_input("Especifica la especie")
        else:
            especie = especie_sel
        raza = st.text_input("Raza (opcional)")

    if st.button("Crear cuenta"):
        # Validaciones básicas
        if not nombre.strip():
            st.error("El nombre es obligatorio.")
            return
        if not email.strip():
            st.error("El email es obligatorio.")
            return
        if not password:
            st.error("La contraseña es obligatoria.")
            return

        try:
            # Insertar usuario y obtener id
            cursor.execute("""
            INSERT INTO usuarios (nombre, email, password, rol)
            VALUES (?, ?, ?, 'cliente')
            """, (nombre.strip(), email.strip(), password))
            conn.commit()
            usuario_id = cursor.lastrowid

            # Si el cliente indicó que tiene mascota, la registramos inmediatamente
            if tiene_mascota:
                if not nombre_mascota.strip():
                    # Revertir usuario creado para mantener consistencia
                    cursor.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
                    conn.commit()
                    st.error("Si indicas que tienes mascota, el nombre de la mascota es obligatorio. Registro cancelado.")
                    return

                cursor.execute("""
                INSERT INTO mascotas (nombre, usuario_id, especie, raza)
                VALUES (?, ?, ?, ?)
                """, (nombre_mascota.strip(), usuario_id, especie.strip() if especie else None, raza.strip() if raza else None))
                conn.commit()

            st.success("Cuenta creada correctamente.")
            st.info("Ahora puedes iniciar sesión con tus credenciales.")
            # Restablecer el modo_registro si lo utilizas en app.py
            if "modo_registro" in st.session_state:
                st.session_state.modo_registro = False
            st.rerun()

        except Exception as e:
            conn.rollback()
            # Mensaje genérico para el usuario; puedes activar st.error(str(e)) para debug
            st.error("Error al crear la cuenta. Es posible que el email ya exista.")
