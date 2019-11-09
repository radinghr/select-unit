from django.contrib.auth import authenticate, login
from django.forms.models import model_to_dict
from rest_framework import generics
from rest_framework_jwt.settings import api_settings
from rest_framework.authentication import get_authorization_header
from . import utils
from .models import User, Major
from .serializer import ProfileSerializer, LoginSerializer, AddMajorSerializer
from .http_response import bad_request_response, success_response, not_found_response, not_acceptable_response, \
    error_response, un_auth_response
import jwt
import json


# Create your views here.

class RegisterUser(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    name = "User_Register"

    def post(self, request):
        post_params = json.loads(request.body.decode('utf-8'))
        username = post_params.get("username")
        password = post_params.get("password")
        semester = int(post_params.get("semester", 1))
        major_id = int(post_params.get("major", 0))
        full_name = post_params.get("full_name")

        for i in [username, password, semester, major_id, full_name]:
            if i is None or i is 0:
                return bad_request_response(message=str(i) + ' is Missing', code=400)

        if User.objects.filter(username=username).exists():
            content = "This username already exists."
            return bad_request_response(message=content, code=409)

        major_obj = Major.objects.filter(id=major_id)
        if bool(major_obj):
            try:
                user = User.objects.create(username=username, semester=semester, major=major_obj[0],
                                           full_name=full_name, is_normal_user=1, is_staff=0, is_superuser=0)
                user.set_password(password)
                user.save()
                content = {'messsage': 'User created successfully!'}
                return success_response(data=content)
            except Exception as e:
                return error_response(utils.DATABASE_ERROR)
        else:
            return error_response(utils.MAJOR_NOT_FOUND)


class LoginUser(generics.GenericAPIView):
    serializer_class = LoginSerializer
    name = 'User_Login'

    def post(self, request):
        post_params = json.loads(request.body.decode('utf-8'))
        username = post_params.get("username")
        password = post_params.get("password")
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        user = authenticate(username=username, password=password)
        if user:
            if user.is_normal_user and user.is_active:
                payload = jwt_payload_handler(user)
                login(request, user)
                user_token = jwt_encode_handler(payload)
                content = {'token': str(user_token)}
                return success_response(content)
        return un_auth_response(code=403)




class MajorList(generics.GenericAPIView):
    name = "Major_List"

    def get(self, request):
        major_all_obj = Major.objects.all()
        major_list = list()

        for obj in major_all_obj:
            major_list.append(model_to_dict(obj))
        return success_response(major_list)


class AddMajor(generics.GenericAPIView):
    name = "Major_Add"
    serializer_class = AddMajorSerializer

    def post(self, request):
        post_params = json.loads(request.body.decode('utf-8'))
        major_name = post_params.get('name')
        major_obj = Major.objects.create(name=major_name)
        data = model_to_dict(major_obj)
        return success_response({'object': data})


class TokenTest(generics.GenericAPIView):
    name = "test"

    def post(self, request):
        auth_keyword, token = get_authorization_header(request).split()
        user_id = get_user_id_from_token(token)
        return success_response("test")


def get_user_id_from_token(token):
    """

    auth_keyword, token = get_authorization_header(request).split()

    :param token:
    :return:
    """
    try:
        payload = api_settings.JWT_DECODE_HANDLER(token)
        user_id = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER(payload)
        return user_id
    except jwt.ExpiredSignature:
        msg = 'Signature has expired.'
    except jwt.DecodeError:
        msg = 'Error decoding signature.'
    return msg
