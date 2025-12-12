import streamlit as st
from database import crear_tablas
from auth import login, registro_cliente, crear_admin
from views.cliente import vista_cliente
from views.admin import vista_admin

st.set_page_config(page_title="Clínica Veterinaria", page_icon="🐾")

crear_tablas()
crear_admin()

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "modo_registro" not in st.session_state:
    st.session_state.modo_registro = False

# ----------- APP ------------
if st.session_state.usuario is None:
    if st.session_state.modo_registro:
        registro_cliente()
    else:
        login()
        if st.button("Registrarse como cliente"):
            st.session_state.modo_registro = True
            st.rerun()
else:
    if st.session_state.usuario["rol"] == "cliente":
        vista_cliente()
    else:
        vista_admin()
