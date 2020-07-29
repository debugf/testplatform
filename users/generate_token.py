from datetime import datetime, timedelta
import jwt

from django.conf import settings

def generate_jwt_token(username):
    token = jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'data': {
            'username': username
        }
    }, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')


