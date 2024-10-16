from BBDD.conexionBD import get_db_connection
import bcrypt

# Funcion para ver si ya se esta usando el email
def user_exists(email: str) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = 'SELECT 1 FROM users WHERE email = ? AND is_delete = 0 LIMIT 1'
        cursor.execute(query, (email,))
        exists = cursor.fetchone() is not None
    return exists


# Crear la imagen de usuario
def create_img_user(full_name: str):
    arr_name = full_name.split(' ')
    return f'{arr_name[0][0].upper()}{arr_name[1][0].upper()}'

# Función para agregar un usuario
def add_user(user_id: str, name: str, email: str, password: str):
    with get_db_connection() as conn:        
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (id, name, email, password) VALUES (?, ?, ?, ?)', (user_id, name, email, password))
        conn.commit()

# Función para que el usuario inicie sesion
def login_user(email: str, password: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = 'SELECT id, password FROM users WHERE email = ? AND is_delete = 0'
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        if user:
            hashed_password = user[1]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return {'message': 'Login successful', 'success': True, 'user_id': user[0]}
    return {'message': 'Invalid Credentials', 'success': False}

# Obtener la informacion del usuario
def get_info_user(user_id: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = 'SELECT name, email FROM users WHERE id = ? AND is_delete = 0'
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
    return {'name': user[0], 'email': user[1]}
    
# Funcion para actualizar informacion del usuario
def update_data_user(data: dict):
    with get_db_connection() as conn:
        new_data = data.copy()
        cursor = conn.cursor()
        query = 'UPDATE users SET name = ? WHERE id = ?'
        cursor.execute(query, ( new_data['name'], new_data['user_id']))
        conn.commit()
    return {'message': 'User information updated successfully'}
    
# Funcion para eliminar un usuario
def delete_user(user_id: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = 'UPDATE users SET is_delete = 1 WHERE id = ?'
        cursor.execute(query, (user_id,))
        conn.commit()
    return {'message': 'User delete succesfully'}