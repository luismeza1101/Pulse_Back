from BBDD.conexionBD import get_db_connection
import sqlite3

# Funcion para agregar una publicacion
def create_new_post(data: dict):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        new_data = data.copy()
        query = 'INSERT INTO posts (id, user_id, content) VALUES (?, ?, ?)'
        cursor.execute(query, (new_data['id'], new_data['user_id'], new_data['content']))
        conn.commit()
    return {'message': 'Post created'}
    
# Funcion para obtener todas las publicaciones 
def get_posts():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT 
                posts.id AS post_id,
                posts.user_id,
                posts.content,
                posts.publication_date,
                users.name AS user_name,
                users.email AS user_email,
                COUNT(comments.id) AS comment_count
            FROM 
                posts
            JOIN 
                users ON posts.user_id = users.id
            LEFT JOIN 
                comments ON posts.id = comments.post_id
            GROUP BY 
                posts.id, users.name, users.email
            ORDER BY 
                posts.publication_date DESC
            '''
        cursor.execute(query)
        result = cursor.fetchall()
        posts = []
        for row in result:
            post = {
                'post_id': row[0],
                'user_id': row[1],
                'content': row[2],
                'publication_date': row[3],
                'user_name': row[4],
                'user_email': row[5],
                'cant_comments': row[6], 
            }
            posts.append(post)
    return posts

# Funcion para obtener todas las publicaciones de un usuario
def posts_by_user(user_id: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT id, content, publication_date FROM posts WHERE user_id = ?
            '''
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        posts_user = []
        for row in result:
            post ={
                'post_id': row[0],
                'content': row[1],
                'publication_date': row[2],
            }
            posts_user.append(post)
    return posts_user

# Funcion para elimininar un post y sus comentarios de la base de datos 
def delete_post(post_id: str):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            queryComments = 'DELETE FROM comments WHERE post_id = ?'
            cursor.execute(queryComments, (post_id,))
            query = 'DELETE FROM posts WHERE id = ?'
            cursor.execute(query, (post_id,))
            conn.commit()

        return {'message': 'Delete successfully'}

    except sqlite3.Error as e:
        return {'error': f'An error occurred: {str(e)}'}, 500