# views/admin.py
import streamlit as st
from database import cursor, conn
from streamlit_calendar import calendar
from ui import render_hero

def calendario_visual(fecha):
    """
    Calendario horario simple (lista por horas) — se deja por compatibilidad.
    """
    st.subheader(f"📅 Calendario {fecha}")

    horas = [f"{h:02d}:00" for h in range(9, 18)]

    cursor.execute("""
    SELECT hora FROM citas WHERE fecha=?
    """, (str(fecha),))
    horas_ocupadas = [h[0] for h in cursor.fetchall()]

    st.markdown("""
    <style>
    .slot { padding: 10px; margin: 4px 0; border-radius: 6px; text-align: center; font-weight: bold; color: white; }
    .libre {background-color: #2ecc71;}
    .ocupado {background-color: #e74c3c;}
    </style>
    """, unsafe_allow_html=True)

    for h in horas:
        if h in horas_ocupadas:
            st.markdown(f"<div class='slot ocupado'>🟥 {h} - OCUPADO</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='slot libre'>🟩 {h} - DISPONIBLE</div>", unsafe_allow_html=True)


def abrir_gestion_cita_en_modal(cita_id):
    """
    Abre un modal con la gestión de la cita:
    - Ver datos (cliente, mascota, fecha, hora, motivo, estado, resultado)
    - Cambiar estado
    - Guardar resultado / notas
    """
    cursor.execute("""
    SELECT c.id, c.mascota_id, c.fecha, c.hora, c.motivo, c.estado, c.resultado,
           m.nombre as mascota, u.nombre as cliente, u.email
    FROM citas c
    JOIN mascotas m ON c.mascota_id = m.id
    JOIN usuarios u ON m.usuario_id = u.id
    WHERE c.id = ?
    """, (cita_id,))
    fila = cursor.fetchone()
    if not fila:
        st.error("Cita no encontrada.")
        return

    cid, mascota_id, fecha, hora, motivo, estado, resultado, nombre_mascota, nombre_cliente, cliente_email = fila

    # Abrir modal (dialog)
    with st.dialog(f"Gestión cita {cid}", key=f"dialog_{cid}"):
        st.markdown(f"**Cita #{cid}** — {fecha} {hora}")
        st.write(f"**Cliente:** {nombre_cliente} ({cliente_email})")
        st.write(f"**Mascota:** {nombre_mascota} (ID {mascota_id})")
        st.write(f"**Motivo:** {motivo if motivo else '-'}")
        st.write(f"**Estado actual:** **{estado}**")
        st.divider()

        # Campo para cambiar estado
        estados = ["Reservada", "En curso", "Finalizada", "Cancelada"]
        index = estados.index(estado) if estado in estados else 0
        nuevo_estado = st.selectbox("Cambiar estado", estados, index=index, key=f"modal_estado_{cid}")

        # Campo para resultado / notas
        resultado_input = st.text_area("Resultado / notas", value=(resultado if resultado else ""), key=f"modal_res_{cid}", height=120)

        cols = st.columns([1,1,1])
        if cols[0].button("Guardar cambios", key=f"modal_guardar_{cid}"):
            cursor.execute("UPDATE citas SET estado=?, resultado=? WHERE id=?", (nuevo_estado, resultado_input.strip() if resultado_input else None, cid))
            conn.commit()
            st.success("Cambios guardados.")
            st.experimental_rerun()

        if cols[1].button("Marcar como Finalizada", key=f"modal_final_{cid}"):
            cursor.execute("UPDATE citas SET estado=?, resultado=? WHERE id=?", ("Finalizada", resultado_input.strip() if resultado_input else None, cid))
            conn.commit()
            st.success("Cita marcada como Finalizada.")
            st.experimental_rerun()

        if cols[2].button("Cerrar", key=f"modal_close_{cid}"):
            st.info("Cerrando gestión.")
            # cerrar modal simplemente termina el contexto; la UI volverá al calendario


def vista_admin():
    # Mostrar hero (opcional). El header ya está renderizado por app.py
    render_hero()

    st.title("🩺 Panel de la Clínica")

    menu = st.sidebar.selectbox(
        "Menú",
        ["Calendario", "Ver todas las citas", "Ver clientes", "Calendario horario", "Cerrar sesión"]
    )

    # ---------------- CALENDARIO GOOGLE STYLE ----------------
    if menu == "Calendario":
        st.subheader("📅 Calendario de citas (clic en una cita para gestionarla)")

        # Obtener citas desde BD
        cursor.execute("""
        SELECT 
            c.id,
            u.nombre AS cliente,
            m.nombre AS mascota,
            c.fecha,
            c.hora,
            c.motivo,
            c.estado,
            c.resultado
        FROM citas c
        JOIN mascotas m ON c.mascota_id = m.id
        JOIN usuarios u ON m.usuario_id = u.id
        """)
        citas = cursor.fetchall()

        # Convertir a formato de eventos (incluimos 'id' como entero/str para identificar)
        eventos = []
        for c in citas:
            cid, cliente, mascota, fecha, hora, motivo, estado, resultado = c
            # Elegir color por estado
            color = "#FF4B4B" if estado in ("Reservada", "En curso") else "#6c757d" if estado == "Cancelada" else "#4CAF50"
            eventos.append({
                "id": str(cid),  # streamlit-calendar devuelve el evento con el id que pongamos; lo convertimos a str por seguridad
                "title": f"{mascota} ({cliente}) - {estado}",
                "start": f"{fecha}T{hora}:00",
                "end": f"{fecha}T{int(hora[:2]) + 1:02d}:00",
                "backgroundColor": color,
                "borderColor": color
            })

        opciones = {
            "initialView": "timeGridWeek",
            "slotMinTime": "09:00:00",
            "slotMaxTime": "18:00:00",
            "locale": "es",
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,timeGridWeek,timeGridDay"
            }
        }

        # LLamada al componente calendar. El valor devuelto indica interacciones (p.ej. eventClick).
        comp_value = calendar(events=eventos, options=opciones)

        # Manejo de callbacks del componente: cuando el usuario clica un evento,
        # comp_value tendrá: {"callback":"eventClick", "eventClick": {"event": {...}}, ...}
        if isinstance(comp_value, dict) and comp_value.get("callback") == "eventClick":
            # Extraer id del evento clicado
            event_payload = comp_value.get("eventClick", {}).get("event", {})
            event_id = event_payload.get("id") or event_payload.get("extendedProps", {}).get("id")
            if event_id:
                # convertir a int por si viene como string
                try:
                    cid = int(event_id)
                except Exception:
                    cid = int(str(event_id))
                # Abrir modal de gestión de la cita
                abrir_gestion_cita_en_modal(cid)

        st.markdown("---")
        st.info("Haz clic en un bloque (cita) para abrir su gestión.")

    # ---------------- VER TODAS LAS CITAS ----------------
    elif menu == "Ver todas las citas":
        st.subheader("Todas las citas")

        cursor.execute("""
        SELECT c.id, u.nombre, m.nombre, c.fecha, c.hora, c.motivo, c.estado, c.resultado
        FROM citas c
        JOIN mascotas m ON c.mascota_id = m.id
        JOIN usuarios u ON m.usuario_id = u.id
        ORDER BY c.fecha, c.hora
        """)
        citas = cursor.fetchall()

        if not citas:
            st.info("No hay citas registradas.")
            return

        for c in citas:
            cid, cliente, mascota, fecha, hora, motivo, estado, resultado = c
            st.write(f"📅 {fecha} {hora} | 👤 {cliente} | 🐶 {mascota} | Estado: **{estado}**")
            st.write(f"Motivo: {motivo if motivo else '-'}")
            if resultado:
                st.write(f"Resultado / notas: {resultado}")

            # Controles admin: cambiar estado y añadir resultado si procede
            cols = st.columns([1, 1, 3])
            with cols[0]:
                estados = ["Reservada", "En curso", "Finalizada", "Cancelada"]
                index = estados.index(estado) if estado in estados else 0
                nuevo_estado = st.selectbox("Cambiar estado", estados, index=index, key=f"estado_{cid}")
                if st.button("Actualizar estado", key=f"act_{cid}"):
                    cursor.execute("UPDATE citas SET estado=? WHERE id=?", (nuevo_estado, cid))
                    conn.commit()
                    st.success("Estado actualizado.")
                    st.experimental_rerun()
            with cols[1]:
                resultado_input = st.text_input("Resultado (si Finalizada)", value=(resultado if resultado else ""), key=f"res_{cid}")
                if st.button("Guardar resultado", key=f"resbtn_{cid}"):
                    cursor.execute("UPDATE citas SET resultado=? WHERE id=?", (resultado_input.strip() if resultado_input else None, cid))
                    conn.commit()
                    st.success("Resultado guardado.")
                    st.experimental_rerun()
            st.divider()

    # ---------------- VER CLIENTES ----------------
    elif menu == "Ver clientes":
        st.subheader("Clientes y mascotas")

        cursor.execute("""
        SELECT u.id, u.nombre, u.email, COUNT(m.id) as n_mascotas
        FROM usuarios u
        LEFT JOIN mascotas m ON u.id = m.usuario_id
        WHERE u.rol='cliente'
        GROUP BY u.id
        """)
        datos = cursor.fetchall()

        for d in datos:
            uid, nombre, email, n_masc = d
            st.write(f"👤 {nombre} ({email}) - {n_masc} mascota(s)")
            cursor.execute("SELECT id, nombre, especie FROM mascotas WHERE usuario_id=?", (uid,))
            mascotas = cursor.fetchall()
            if mascotas:
                for m in mascotas:
                    mid, mname, especie = m
                    st.write(f"   🐶 ID {mid} - {mname} - {especie if especie else 'Especie no indicada'}")
            st.divider()

    # ---------------- CALENDARIO HORARIO SIMPLE ----------------
    elif menu == "Calendario horario":
        fecha = st.date_input("Selecciona fecha")
        calendario_visual(fecha)

    # ---------------- CERRAR SESIÓN ----------------
    elif menu == "Cerrar sesión":
        st.session_state.usuario = None
        st.rerun()
