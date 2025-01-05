from flask_login import UserMixin
import mysql.connector
from app.config import Config
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, email, role FROM users WHERE id = %s', (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user_data:
        return User(
            id=user_data['id'],
            name=user_data['name'],
            email=user_data['email'],
            role=user_data['role']
        )
    return None

def authenticate_user(email_or_username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        'SELECT * FROM users WHERE email = %s OR name = %s',
        (email_or_username, email_or_username)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and verify_password(password, user['password']):
        return type('User', (), {
            'id': user['id'],
            'username': user['name'],
            'role': user['role'],
            'is_authenticated': True,
            'is_active': True,
            'is_anonymous': False,
            'get_id': lambda self: str(self.id)
        })()
    return None

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE name = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password) 