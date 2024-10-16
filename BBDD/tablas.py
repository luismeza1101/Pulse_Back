import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Crea la base de datos en la misma carpeta que este archivo
database_path = os.path.join(current_dir, 'database.db')
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Tabla de usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id TEXT UNIQUE PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    is_delete INTEGER NOT NULL DEFAULT 0
)
''')


# Tabla de publicaciones
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts(
    id TEXT PRIMARY KEY UNIQUE,
    user_id TEXT,
    content TEXT NOT NULL,
    publication_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)            
''')


# Tabla de comentarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments(
    id TEXT PRIMARY KEY,
    post_id TEXT,
    user_id TEXT,
    content TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)            
''')

conn.commit()
conn.close()
