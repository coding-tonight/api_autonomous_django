import logging
from datetime import datetime
from smtplib import SMTP

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.authtoken.models import Token

from app.models import ForgetPasswordOtp
from . import globalMessage
from . validation import forget_password_validation, login_validation, register_validation, verify_otp_validation

# Create your views here.

logger = logging.getLogger('django')


class AuthView(APIView):
    authentication_classes  = []
    permission_classes = []
    
    def post(self, request, format=None):
        try:
            username, password = login_validation(
                request)  # decoded username and  password
            # nullable check
            if username is None and password is None:
                return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_403_FORBIDDEN)

            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                detail = User.objects.get(pk=user.pk)

                return Response({
                    'msg': globalMessage.LOGIN_MEG,
                    'data': {
                        'token': token.key,
                        'user_id':  user.pk,
                        'username': detail.username,
                        'email': detail.email,
                        'is_admin': detail.is_superuser,
                        'created': detail.date_joined,
                    },
                    'login_date': datetime.now(),
                    'status_code': globalMessage.SUCCESS_RESPONSE
                }, status=status.HTTP_200_OK)

            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as exe:
            logger.error(exe)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_400_BAD_REQUEST)


# for register user only admin can create user , group and access permission

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        try:
            if not request.data:   # check if request.data is empty or not
                return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_406_NOT_ACCEPTABLE)

            error_list, username, password, email, is_staff, is_active, is_admin = register_validation(
                request)

            if error_list:
                return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG,
                                'errors': error_list}, status=status.HTTP_403_FORBIDDEN)

            # hash password
            # user = User.set_password(password)
            user = User.objects.create_user(
                username=username, email=email, is_active=is_active, is_superuser=is_admin, is_staff=is_staff)
            user.set_password(password)
            user.save()

            return Response({globalMessage.MESSAGE: globalMessage.REGISTER_MSG}, status=status.HTTP_200_OK)

        except User.DoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgetPasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            error_list, otp, email = forget_password_validation(request)
            # check if email exists or not
            if error_list:
                return Response({globalMessage.MESSAGE: "Your Email does not exits.",
                                 'status': globalMessage.ERROR_MSG
                                 }, status=status.HTTP_401_UNAUTHORIZED)

            with transaction.atomic():
                # start smtp server
                server = SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('spicyh166@gmail.com', 'application password')
                msg = f'Hi {email}  your otp code is {otp}'
                server.sendmail('spicyh166@gmail.com', email, msg)
                server.quit()

                # store otp in the database
                ForgetPasswordOtp.objects.create(
                    email=email, otp=otp, created_at=datetime.now())

                return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG,
                                'status': globalMessage.SUCCESS_MSG,
                                 'opt_msg': 'otp is send'
                                 }, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG,
                             'status': globalMessage.ERROR_RESPONSE
                             }, status=status.HTTP_401_UNAUTHORIZED)


class VerifyForgetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            error_list, otp = verify_otp_validation(request)

            #  if otp is not verify then send error response to the client
            if error_list:
                return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_401_UNAUTHORIZED)

            # delete otp in the database
            ForgetPasswordOtp.objects.filter(otp=otp).delete()
            return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG}, status=status.HTTP_200_OK)

        except ForgetPasswordOtp.DoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
