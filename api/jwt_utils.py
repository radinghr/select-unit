import jwt
from django.conf import settings
from datetime import datetime, timedelta, date
from api.models import User
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder


def create_jwt_token(user_object: User):
    key = settings.SECRET_KEY
    adata = datetime.now().strftime("%m/%d/%Y")
    payload = {
        "adata": adata,
        "username": user_object.username,
    }
    token = jwt.encode(payload, key, algorithm='HS256')
    token = token.decode('utf-8')
    return token


def extract_jwt_payload(token):
    key = settings.SECRET_KEY
    jwt_err = None
    payload = {}
    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
    except Exception as e:
        jwt_err = str(e)
    payload['err'] = jwt_err
    return payload, jwt_err
