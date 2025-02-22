import sqlite3

# Crear la base de datos y la tabla si no existen
def create_db():
    conn = sqlite3.connect('daily_records.db')
    cursor = conn.cursor()
    
    # Crear la tabla si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_records (
        user_name TEXT NOT NULL,
        date TEXT NOT NULL,
        record TEXT NOT NULL,
        PRIMARY KEY (user_name, date)
    )
    ''')
    
    conn.commit()
    conn.close()


def insert_daily_record(user_name, date, record):
    conn = sqlite3.connect('daily_records.db')
    cursor = conn.cursor()
    
    # Insertar un nuevo registro en la base de datos
    cursor.execute('''
    INSERT OR REPLACE INTO daily_records (user_name, date, record)
    VALUES (?, ?, ?)
    ''', (user_name, date, record))
    
    conn.commit()
    conn.close()

def read_daily_record(user_name, date):
    try:
        conn = sqlite3.connect('daily_records.db')
        cursor = conn.cursor()
        
        # Consultar el registro para el usuario y la fecha
        cursor.execute('''
        SELECT record FROM daily_records
        WHERE user_name = ? AND date = ?
        ''', (user_name, date))
        
        # Obtener el resultado
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]  # Retornar el registro
        else:
            return None
    except Exception as e:
        print(f"Error al leer el registro diario: {e}")
        return None




# Llamar a la función para crear la base de datos
create_db()
# Ejemplo de inserción
insert_daily_record("usuario_1", "2025-02-22", "Este es el registro para el 22 de febrero de 2025.")

# Ejemplo de uso
user_name = "usuario_1"
current_date = "2025-02-22"

record = read_daily_record(user_name, current_date)
if record:
    print("Registro encontrado:", record)
else:
    print("No se encontró registro para esta fecha.")