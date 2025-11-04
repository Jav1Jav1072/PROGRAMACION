USERS = {
    "Pedro": "1234",
    "Pepe": "abcd"
}

def verify_user(username, password):
    """Verifica si el usuario y contraseña son válidos."""
    return USERS.get(username) == password
