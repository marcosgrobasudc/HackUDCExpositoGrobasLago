from relational_db import insert_daily_record, read_daily_record
from datetime import date, timedelta
# Función para generar una lista de fechas válidas
def generar_fechas_validas():
    today = date.today()
    return [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

# Función para guardar o actualizar el registro diario
def guardar_registro(selected_date, entry, username):
    print('Guardando registro para el usuario:', username)
    # Llamar a la función insert_daily_record para guardar el registro en la base de datos
    insert_daily_record(selected_date, entry, username)
    return f"Registro para el día {selected_date} del usuario '{username}': {entry}"

# Función para cargar el registro si existe
def cargar_registro(selected_date, username):
    # Llamar a la función read_daily_record para obtener el registro de la base de datos
    record = read_daily_record(selected_date, username)
    return record
