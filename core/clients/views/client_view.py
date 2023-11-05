import glob
import logging
from datetime import datetime
from sys import exc_info
from tokenize import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from clients.models import Clients
from clients.serializer import ClientSerializer
from app import globalMessage


logger = logging.getLogger('django')


class ClientAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            try:
                list_client = Clients.objects.filter(is_delete=False)

            except Clients.DoesNotExist as exe:
                Exception(exe)

            serializer = ClientSerializer(list_client, many=True)
            return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG, 'data': serializer.data}, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientAddAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        try:
            if not request.data:
                return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_400_BAD_REQUEST)

            data = request.data
            serializer = ClientSerializer(data=data)
            if serializer.is_valid():
                serializer.save(created_at=datetime.now(),
                                created_by=request.user)
                MSG = {
                    globalMessage.MESSAGE: globalMessage.SUCCESS_MSG,
                    'status': globalMessage.SUCCESS_RESPONSE
                }
                return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientDetailAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]
    """ client api reterive data with reference id 
    """

    def get(self, request, ref_id):
        try:
            try:
                client = Clients.objects.get(reference_id=ref_id)

            except Clients.DoesNotExist as exe:
                raise Exception(exe)

            serializer = ClientSerializer(client)
            MSG = {
                globalMessage.MESSAGE: globalMessage.ERROR_MSG,
                'data': serializer.data
            }

            return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, ref_id):
        try:
            #  if request.data does not contain any data
            if not request.data:
                return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_400_BAD_REQUEST)

            try:
                client = Clients.objects.get(reference_id=ref_id)

            except Clients.DoesNotExist as exe:
                raise Exception(exe)

            data = request.data
            serializer = ClientSerializer(client, data=data)
            if serializer.is_valid():
                serializer.save()
                MSG = {
                    globalMessage.MESSAGE: globalMessage.SUCCESS_MSG,
                    'status': globalMessage.SUCCESS_RESPONSE
                }
                return Response(MSG, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, ref_id):
        try:
            Clients.objects.get(reference_id=ref_id).delete()
            return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG}, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG})
