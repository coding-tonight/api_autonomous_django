import logging
from datetime import datetime

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from metadata.serializer import MetaDataSerializer
from metadata.models import MetaData
from app import globalMessage


# Create your views here.

logger = logging.getLogger('django')


class MetaDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            meta_data = MetaData.objects.filter(is_delete=False)
            serializer = MetaDataSerializer(meta_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            data = request.data
            print(data)
            serializer = MetaDataSerializer(data=data)
            if serializer.is_valid():
                print('valid')
                serializer.save(created_at=datetime.now(),
                                created_by=request.user)

                return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG}, status=status.HTTP_200_OK)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MetaDataUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """ get data with id or reference id
    """

    def get(self, request, pk):
        try:
            meta_data = MetaData.objects.get(reference_id=pk)
            serializer = MetaDataSerializer(meta_data)
            return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG, 'data': serializer.data}, status=status.HTTP_200_OK)

        except MetaData.DoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE:  globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            data = request.data
            meta_data = MetaData.objects.get(reference_id=pk)
            # serializer data
            serializer = MetaDataSerializer(meta_data, data=data)
            if serializer.is_valid():
                serializer.save(updated_at=datetime.now,
                                updated_by=request.user)
                return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG}, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
