<<<<<<< HEAD
import streamlit as st
from database import conn, cursor

ESPECIES_COMUNES = [
    "Perro",
    "Gato",
    "Pájaro",
    "Conejo",
    "Hámster",
    "Pez",
    "Otro"
]

def vista_cliente():
    st.title("🐶 Panel del Cliente")

    menu = st.sidebar.selectbox(
        "Menú",
        ["Mis mascotas", "Mis citas", "Cerrar sesión"]
    )

    # ---------------- MASCOTAS ----------------
    if menu == "Mis mascotas":
        st.subheader("Mis mascotas")

        # Formulario para registrar mascota
        nombre = st.text_input("Nombre de la mascota")

        especie_sel = st.selectbox("Especie", ESPECIES_COMUNES)
        especie = None
        if especie_sel == "Otro":
            especie = st.text_input("Especifica la especie")
        else:
            especie = especie_sel

        raza = st.text_input("Raza (opcional)")

        if st.button("Registrar mascota"):
            if not nombre.strip():
                st.error("El nombre de la mascota es obligatorio.")
            else:
                cursor.execute("""
                INSERT INTO mascotas (nombre, usuario_id, especie, raza)
                VALUES (?, ?, ?, ?)
                """, (nombre.strip(), st.session_state.usuario["id"],
                      especie.strip() if especie else None,
                      raza.strip() if raza else None))
                conn.commit()
                st.success("Mascota registrada")
                st.rerun()

        # Listado de mascotas con botón para ver ficha (historial)
        cursor.execute("""
        SELECT id, nombre, especie, raza FROM mascotas WHERE usuario_id=?
        """, (st.session_state.usuario["id"],))
        mascotas = cursor.fetchall()

        if mascotas:
            st.markdown("**Tus mascotas registradas:**")
            for m in mascotas:
                id_m, nombre_m, especie_m, raza_m = m
                linea = f"🐾 ID {id_m} - {nombre_m} - {especie_m if especie_m else 'Especie no indicada'}"
                if raza_m:
                    linea += f" - {raza_m}"
                st.write(linea)

                # Mostrar botón para ver historial/ficha de la mascota
                if st.button(f"Ver ficha / historial - {nombre_m}", key=f"hist_{id_m}"):
                    mostrar_ficha_mascota(id_m)

        else:
            st.info("No tienes mascotas registradas.")

    # ---------------- CITAS ----------------
    elif menu == "Mis citas":
        st.subheader("Mis citas")

        # Obtener mascotas
        cursor.execute("""
        SELECT * FROM mascotas WHERE usuario_id=?
        """, (st.session_state.usuario["id"],))
        mascotas = cursor.fetchall()

        if not mascotas:
            st.info("Primero registra una mascota")
            return

        opciones = {f"{m[1]} (ID {m[0]})": m[0] for m in mascotas}

        mascota_sel = st.selectbox("Mascota", opciones.keys())
        fecha = st.date_input("Fecha")
        hora = st.selectbox("Hora", [f"{h:02d}:00" for h in range(9, 18)])
        motivo = st.selectbox("Motivo", ["Revisión", "Vacunación", "Desparasitación", "Urgencia", "Otros"])
        if motivo == "Otros":
            motivo = st.text_input("Especifica motivo")

        if st.button("Reservar cita"):
            try:
                cursor.execute("""
                INSERT INTO citas (mascota_id, fecha, hora, motivo)
                VALUES (?, ?, ?, ?)
                """, (opciones[mascota_sel], str(fecha), hora, motivo))
                conn.commit()
                st.success("✅ Cita reservada")
            except Exception:
                st.error("⛔ Esa hora ya está ocupada para esa mascota/fecha/hora")

        st.divider()

        # Mostrar citas del cliente (todas) con estado y opción de cancelar si está 'Reservada'
        cursor.execute("""
        SELECT c.id, c.fecha, c.hora, c.motivo, c.estado, c.resultado, m.nombre
        FROM citas c
        JOIN mascotas m ON c.mascota_id = m.id
        WHERE m.usuario_id=?
        ORDER BY c.fecha, c.hora
        """, (st.session_state.usuario["id"],))
        citas = cursor.fetchall()

        if citas:
            for c in citas:
                cid, fecha_c, hora_c, motivo_c, estado_c, resultado_c, nombre_m = c
                st.write(f"📅 {fecha_c} {hora_c} | 🐶 {nombre_m} | Estado: **{estado_c}**")
                st.write(f"Motivo: {motivo_c if motivo_c else '-'}")
                if resultado_c:
                    st.write(f"Resultado / notas: {resultado_c}")
                # Acción del cliente: permite cancelar si todavía está Reservada
                if estado_c == "Reservada":
                    cols = st.columns([1, 3])
                    if cols[0].button("Cancelar cita", key=f"cancel_{cid}"):
                        cursor.execute("UPDATE citas SET estado=? WHERE id=?", ("Cancelada", cid))
                        conn.commit()
                        st.success("Cita cancelada.")
                        st.rerun()
                st.divider()
        else:
            st.info("No tienes citas registradas.")

    elif menu == "Cerrar sesión":
        st.session_state.usuario = None
        st.rerun()


def mostrar_ficha_mascota(id_mascota):
    """
    Muestra la ficha básica y el historial de citas de la mascota.
    """
    cursor.execute("SELECT id, nombre, especie, raza FROM mascotas WHERE id=?", (id_mascota,))
    m = cursor.fetchone()
    if not m:
        st.error("Mascota no encontrada.")
        return

    id_m, nombre_m, especie_m, raza_m = m
    st.header(f"Ficha: {nombre_m} (ID {id_m})")
    st.write(f"Especie: {especie_m if especie_m else 'No indicada'}")
    if raza_m:
        st.write(f"Raza: {raza_m}")

    st.subheader("Historial de visitas / citas")
    cursor.execute("""
    SELECT fecha, hora, motivo, estado, resultado
    FROM citas
    WHERE mascota_id=?
    ORDER BY fecha DESC, hora DESC
    """, (id_mascota,))
    citas = cursor.fetchall()

    if not citas:
        st.info("No hay historial de visitas para esta mascota.")
        return

    for c in citas:
        fecha_c, hora_c, motivo_c, estado_c, resultado_c = c
        st.write(f"📅 {fecha_c} {hora_c} | Estado: **{estado_c}**")
        st.write(f"Motivo: {motivo_c if motivo_c else '-'}")
        if resultado_c:
            st.write(f"Resultado / notas: {resultado_c}")
        st.divider()
=======
import streamlit as st
from database import conn, cursor

ESPECIES_COMUNES = [
    "Perro",
    "Gato",
    "Pájaro",
    "Conejo",
    "Hámster",
    "Pez",
    "Otro"
]

def vista_cliente():
    st.title("🐶 Panel del Cliente")

    menu = st.sidebar.selectbox(
        "Menú",
        ["Mis mascotas", "Mis citas", "Cerrar sesión"]
    )

    # ---------------- MASCOTAS ----------------
    if menu == "Mis mascotas":
        st.subheader("Mis mascotas")

        # Formulario para registrar mascota
        nombre = st.text_input("Nombre de la mascota")

        especie_sel = st.selectbox("Especie", ESPECIES_COMUNES)
        especie = None
        if especie_sel == "Otro":
            especie = st.text_input("Especifica la especie")
        else:
            especie = especie_sel

        raza = st.text_input("Raza (opcional)")

        if st.button("Registrar mascota"):
            if not nombre.strip():
                st.error("El nombre de la mascota es obligatorio.")
            else:
                cursor.execute("""
                INSERT INTO mascotas (nombre, usuario_id, especie, raza)
                VALUES (?, ?, ?, ?)
                """, (nombre.strip(), st.session_state.usuario["id"],
                      especie.strip() if especie else None,
                      raza.strip() if raza else None))
                conn.commit()
                st.success("Mascota registrada")
                st.rerun()

        # Listado de mascotas con botón para ver ficha (historial)
        cursor.execute("""
        SELECT id, nombre, especie, raza FROM mascotas WHERE usuario_id=?
        """, (st.session_state.usuario["id"],))
        mascotas = cursor.fetchall()

        if mascotas:
            st.markdown("**Tus mascotas registradas:**")
            for m in mascotas:
                id_m, nombre_m, especie_m, raza_m = m
                linea = f"🐾 ID {id_m} - {nombre_m} - {especie_m if especie_m else 'Especie no indicada'}"
                if raza_m:
                    linea += f" - {raza_m}"
                st.write(linea)

                # Mostrar botón para ver historial/ficha de la mascota
                if st.button(f"Ver ficha / historial - {nombre_m}", key=f"hist_{id_m}"):
                    mostrar_ficha_mascota(id_m)

        else:
            st.info("No tienes mascotas registradas.")

    # ---------------- CITAS ----------------
    elif menu == "Mis citas":
        st.subheader("Mis citas")

        # Obtener mascotas
        cursor.execute("""
        SELECT * FROM mascotas WHERE usuario_id=?
        """, (st.session_state.usuario["id"],))
        mascotas = cursor.fetchall()

        if not mascotas:
            st.info("Primero registra una mascota")
            return

        opciones = {f"{m[1]} (ID {m[0]})": m[0] for m in mascotas}

        mascota_sel = st.selectbox("Mascota", opciones.keys())
        fecha = st.date_input("Fecha")
        hora = st.selectbox("Hora", [f"{h:02d}:00" for h in range(9, 18)])
        motivo = st.selectbox("Motivo", ["Revisión", "Vacunación", "Desparasitación", "Urgencia", "Otros"])
        if motivo == "Otros":
            motivo = st.text_input("Especifica motivo")

        if st.button("Reservar cita"):
            try:
                cursor.execute("""
                INSERT INTO citas (mascota_id, fecha, hora, motivo)
                VALUES (?, ?, ?, ?)
                """, (opciones[mascota_sel], str(fecha), hora, motivo))
                conn.commit()
                st.success("✅ Cita reservada")
            except Exception:
                st.error("⛔ Esa hora ya está ocupada para esa mascota/fecha/hora")

        st.divider()

        # Mostrar citas del cliente (todas) con estado y opción de cancelar si está 'Reservada'
        cursor.execute("""
        SELECT c.id, c.fecha, c.hora, c.motivo, c.estado, c.resultado, m.nombre
        FROM citas c
        JOIN mascotas m ON c.mascota_id = m.id
        WHERE m.usuario_id=?
        ORDER BY c.fecha, c.hora
        """, (st.session_state.usuario["id"],))
        citas = cursor.fetchall()

        if citas:
            for c in citas:
                cid, fecha_c, hora_c, motivo_c, estado_c, resultado_c, nombre_m = c
                st.write(f"📅 {fecha_c} {hora_c} | 🐶 {nombre_m} | Estado: **{estado_c}**")
                st.write(f"Motivo: {motivo_c if motivo_c else '-'}")
                if resultado_c:
                    st.write(f"Resultado / notas: {resultado_c}")
                # Acción del cliente: permite cancelar si todavía está Reservada
                if estado_c == "Reservada":
                    cols = st.columns([1, 3])
                    if cols[0].button("Cancelar cita", key=f"cancel_{cid}"):
                        cursor.execute("UPDATE citas SET estado=? WHERE id=?", ("Cancelada", cid))
                        conn.commit()
                        st.success("Cita cancelada.")
                        st.rerun()
                st.divider()
        else:
            st.info("No tienes citas registradas.")

    elif menu == "Cerrar sesión":
        st.session_state.usuario = None
        st.rerun()


def mostrar_ficha_mascota(id_mascota):
    """
    Muestra la ficha básica y el historial de citas de la mascota.
    """
    cursor.execute("SELECT id, nombre, especie, raza FROM mascotas WHERE id=?", (id_mascota,))
    m = cursor.fetchone()
    if not m:
        st.error("Mascota no encontrada.")
        return

    id_m, nombre_m, especie_m, raza_m = m
    st.header(f"Ficha: {nombre_m} (ID {id_m})")
    st.write(f"Especie: {especie_m if especie_m else 'No indicada'}")
    if raza_m:
        st.write(f"Raza: {raza_m}")

    st.subheader("Historial de visitas / citas")
    cursor.execute("""
    SELECT fecha, hora, motivo, estado, resultado
    FROM citas
    WHERE mascota_id=?
    ORDER BY fecha DESC, hora DESC
    """, (id_mascota,))
    citas = cursor.fetchall()

    if not citas:
        st.info("No hay historial de visitas para esta mascota.")
        return

    for c in citas:
        fecha_c, hora_c, motivo_c, estado_c, resultado_c = c
        st.write(f"📅 {fecha_c} {hora_c} | Estado: **{estado_c}**")
        st.write(f"Motivo: {motivo_c if motivo_c else '-'}")
        if resultado_c:
            st.write(f"Resultado / notas: {resultado_c}")
        st.divider()
>>>>>>> 026f3e994c2b75a2bb49e6d1f41a472a50ddd70b
