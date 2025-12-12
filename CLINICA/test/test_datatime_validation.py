# tests/test_datetime_validation.py
from datetime import datetime, timedelta, date, time

def is_future_datetime(fecha: date, hora: time) -> bool:
    """
    Misma lógica que debemos aplicar en la app: combinar y comparar con 'now'.
    """
    dt = datetime.combine(fecha, hora)
    return dt > datetime.now()

def test_is_future_with_future_datetime():
    mañana = date.today() + timedelta(days=1)
    hora = time(9, 0)
    assert is_future_datetime(mañana, hora) is True

def test_is_future_with_past_datetime():
    ayer = date.today() - timedelta(days=1)
    hora = time(12, 0)
    assert is_future_datetime(ayer, hora) is False

def test_is_future_with_same_day_past_hour():
    hoy = date.today()
    # hora pasada: tomar ahora -1 hora
    ahora = datetime.now()
    pasada = (ahora - timedelta(hours=1)).time()
    assert is_future_datetime(hoy, pasada) is False

def test_is_future_with_same_day_future_hour():
    hoy = date.today()
    ahora = datetime.now()
    futura = (ahora + timedelta(hours=1)).time()
    assert is_future_datetime(hoy, futura) is True
