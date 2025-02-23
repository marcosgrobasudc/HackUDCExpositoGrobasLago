from relational_db import insert_daily_record, read_daily_record
from datetime import date, timedelta

def generar_fechas_validas():
    """
    Genera una lista con las fechas de los últimos 30 días

    Returns:
    fechas: lista de fechas en formato
    """
    today = date.today()
    return [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

def guardar_registro(selected_date, entry, username):
    """
    Guarda un registro en la base de datos
    
    Args:
    selected_date: fecha seleccionada
    entry: registro a guardar
    username: nombre de usuario

    Returns:
    mensaje: mensaje de confirmación
    """
    print('Guardando registro para el usuario:', username)
    insert_daily_record(selected_date, entry, username)
    return f"Registro para el día {selected_date} del usuario '{username}': {entry}"

def cargar_registro(selected_date, username):
    """
    Carga un registro de la base de datos

    Args:
    selected_date: fecha seleccionada
    username: nombre de usuario

    Returns:
    record: registro del usuario
    """
    record = read_daily_record(selected_date, username)
    return record
