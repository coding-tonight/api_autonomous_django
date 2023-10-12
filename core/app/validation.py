import base64
import secrets

from django.contrib.auth.models import User


def login_validation(request):
    # getting username and password from the  header
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    # split credential form the header
    encode_data = auth_header.split(' ')[1]
    decode_data = base64.b64decode(encode_data).decode('utf-8').split(':')
    username = decode_data[0]
    password = decode_data[1]
    return username, password


def register_validation(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    email = data.get('email')
    is_staff = True
    is_admin = False
    is_active = True
    error_list = []

    if User.objects.filter(username=data.get('username')).exists():
        error_list.append('Username already exists')

    if password != confirm_password:
        error_list.append('Password does not match.')

    return error_list, username, password, email, is_staff, is_active, is_admin


def forget_password_validation(request):
    data = request.data
    email = data.get('email')
    error_list = []

    if not User.objects.filter(email=email).exists():
        error_list.append('email is not valid')

    token = secrets.token_hex(16)

    return error_list, token, email
