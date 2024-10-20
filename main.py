from fastapi import FastAPI, HTTPException
from BBDD.fuctionsComments import  add_comment, get_comments
from BBDD.functionUser import user_exists, add_user, create_img_user, delete_user, get_info_user, login_user, update_data_user
from BBDD.functionsPosts import create_new_post, get_posts, delete_post, posts_by_user
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
import bcrypt
import shortuuid
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

allow_origins = os.getenv("ALLOW_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],  
    allow_headers=["Content-Type"],  
)

class User(BaseModel):
    name: str 
    email: EmailStr
    password: str = Field(..., min_length=6) 
    
class Credentials(BaseModel):
    email: EmailStr
    password: str =  Field(..., min_length=6) 

class NewDataUser(BaseModel):
    user_id: str
    new_name: str = Field(..., min_length=1)
    
class Post(BaseModel):
    user_id: str
    content: str = Field(..., min_length=1, max_length=200)
    
class Comment(BaseModel):
    post_id: str
    user_id: str
    content: str

# Añadir usuarios
@app.post("/register/")
async def create_user(user: User):
    try:
        if(user_exists(user.email)):
            return {'message': 'Email already registered', 'success': False}
        
        create_id = shortuuid.uuid()
        
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        add_user(user_id = create_id, name = user.name, email = user.email, password = hashed_password.decode('utf-8'))
        return {'message': 'User created successfully', 'success': True}
    except Exception as e:
        return {'message': f'Error creating user: {str(e)}', 'success': False}

# Iniciar sesion
@app.post('/login/')
async def login(credentials: Credentials):  
    if not user_exists(credentials.email):
        raise HTTPException(status_code=404, detail='User not found')

    login_message = login_user(credentials.email, credentials.password)

    return login_message
    
# Obtener datos del usuario 
@app.get('/info_user/{user_id}')
async def get_user_data(user_id: str):
    user_data = get_info_user(user_id)
    return {'name': user_data['name'], 'email': user_data['email'], 'img_user': create_img_user(user_data['name'])}
       

# Editar datos de usuario
@app.patch('/edit_user/')
async def edit_info_user(new_data: NewDataUser):
    message = update_data_user(data={
        'user_id': new_data.user_id,
        'name': new_data.new_name
    })
    return message

# Eliminar un usuario
@app.patch('/delete-user/{user_id}')
async def delete_user_from_db(user_id: str):
    message = delete_user(user_id)
    return message

# Crear una publicacion
@app.post('/post/')
async def add_pos(post: Post):
    try:
        message = create_new_post(data={
            'id': shortuuid.uuid(),
            'user_id': post.user_id,
            'content': post.content
        })
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Obtener todas las publicaciones
@app.get('/posts')
async def get_posts_from_bd():
    posts = get_posts()
    return posts

# Agregar comentarios 
@app.post('/add_comment/')
async def add_comment_bd(comment: Comment):
    comment_id = shortuuid.uuid()
    message = add_comment(data={
        'id': comment_id,
        'post_id': comment.post_id,
        'user_id': comment.user_id,
        'content': comment.content
    })
    return message

# Obtener los comentarios de una publicacion
@app.get('/comments/{post_id}')
async def get_comments_from_bd(post_id: str):
    comments = get_comments(post_id)
    return comments

# Obtener publicaciones por usuario
@app.get('/post-by-id/{user_id}')
async def get_posts_by_id(user_id: str):
    message = posts_by_user(user_id)
    return message
    
# Eliminar un post
@app.delete('/delete_post/{post_id}')
async def delete_post_by_id(post_id: str):
    message = delete_post(post_id)
    return message

