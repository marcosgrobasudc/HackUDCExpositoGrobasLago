import sqlite3
import os

def get_db_connection():
    """
    Obtiene una conexión a la base de datos

    Returns:
    sqlite3.Connection: conexión a la base de datos
    """
    return sqlite3.connect('daily_records.db')

def create_db():
    """
    Crea la base de datos si no existe
    
    Returns:
    None
    """
    if not os.path.exists('daily_records.db'):
        conn = get_db_connection()
        cursor = conn.cursor()
        
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

def insert_daily_record(date, record, user_name):
    """
    Inserta un registro diario en la base de datos

    Args:
    date (str): fecha del registro
    record (str): contenido del registro
    user_name (str): nombre del usuario

    Returns:
    None
    """
    create_db()  # Asegurar que la base de datos existe
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insertar un nuevo registro en la base de datos
    cursor.execute('''
    INSERT OR REPLACE INTO daily_records (user_name, date, record)
    VALUES (?, ?, ?)
    ''', (user_name, date, record))
    
    conn.commit()
    conn.close()

def read_daily_record(date, user_name):
    """
    Lee un registro diario de la base de datos

    Args:
    date (str): fecha del registro
    user_name (str): nombre del usuario

    Returns:
    str: contenido del registro
    """
    create_db()  # Asegurar que la base de datos existe
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consultar el registro para el usuario y la fecha
        cursor.execute('''
        SELECT record FROM daily_records
        WHERE user_name = ? AND date = ?
        ''', (user_name, date))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Error al leer el registro diario: {e}")
        return None

def read_all_records(user_name):
    """
    Lee todos los registros diarios de un usuario

    Args:
    user_name (str): nombre del usuario

    Returns:
    list: lista de tuplas con la fecha y el contenido del registro
    """
    create_db()  # Asegurar que la base de datos existe
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consultar todos los registros del usuario ordenados por fecha
        cursor.execute('''
        SELECT date, record FROM daily_records
        WHERE user_name = ?
        ORDER BY date ASC
        ''', (user_name,))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            return [(date, record) for date, record in results]
        else:
            return []
    except Exception as e:
        print(f"Error al leer los registros diarios: {e}")
        return []
