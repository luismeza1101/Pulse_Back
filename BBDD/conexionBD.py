import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

# Conexion a la base de datos
def get_db_connection():
    database_path = os.getenv('DATABASE_URL', 'database.db')
    conn = sqlite3.connect(database_path, timeout=10)
    conn.execute("PRAGMA busy_timeout = 5000")
    return conn