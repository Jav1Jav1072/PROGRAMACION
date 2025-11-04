import streamlit as st
from auth import verify_user

st.set_page_config(page_title="Login simple")

if "user" not in st.session_state:
    st.session_state["user"] = None

def login_page():
    st.title("Inicio de sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if verify_user(username, password):
            st.session_state["user"] = username
            st.success(f"Bienvenido, {username}")
        else:
            st.error("Usuario o contraseña incorrectos")

def home_page():
    st.title("Página principal")
    st.write(f"Has iniciado sesión como **{st.session_state['user']}**")
    if st.button("Cerrar sesión"):
        st.session_state["user"] = None
        st.experimental_rerun()

if st.session_state["user"]:
    home_page()
else:
    login_page()
