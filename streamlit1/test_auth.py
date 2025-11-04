from auth import verify_user

def test_login_correcto():
    assert verify_user("Pedro", "1234")

def test_login_incorrecto():
    assert not verify_user("Pedro", "mal")

def test_usuario_inexistente():
    assert not verify_user("Pedro", "1234")
