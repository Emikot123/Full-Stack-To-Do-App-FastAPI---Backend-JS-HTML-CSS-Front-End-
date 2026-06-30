from jose import jwt 
from datetime import timedelta, datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv()
KEY = getenv('SECRET_KEY')

def create_token(user_id: int):
    expire = datetime.utcnow() + timedelta(days= 31)
    data = {'user_id': user_id, 'exp': expire}
    token = jwt.encode(data, KEY, algorithm='HS256')
    return token

def verify_token(token: str):
    data = jwt.decode(token, KEY, algorithms= ['HS256'])
    return data['user_id']