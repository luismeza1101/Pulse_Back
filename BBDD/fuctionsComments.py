from BBDD.conexionBD import get_db_connection

# Funcion para agregar comentatios
def add_comment(data: dict):
    with get_db_connection() as conn:
        new_data = data.copy()
        cursor = conn.cursor()
        query = 'INSERT INTO comments (id, post_id, user_id, content) VALUES (?, ?, ?, ?)'
        cursor.execute(query, (new_data['id'], new_data['post_id'], new_data['user_id'], new_data['content']))
        conn.commit()
    return {'message': 'Comment add successfully'}
    
# Funcion para obtnener todos los comentarios de una publicacion
def get_comments(post_id: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT comments.content, users.name  
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE post_id = ?'''
        cursor.execute(query, (post_id,))
        results = cursor.fetchall()
        comments = []
        for row in results:
            comment = {
                'content': row[0],
                'name': row[1],
            }
            comments.append(comment)
    return comments
    

    
