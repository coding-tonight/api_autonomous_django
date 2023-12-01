import logging

from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from app import globalMessage


logger = logging.getLogger('django')


class DocListApi(APIView):
    permission_classes = []
    authentication_classes = []
    base_url = settings.BASE_URL

    def get(self, request, format=None):
        try:
            urls = {
                'message': 'Choice one of these.',
                'swagger': f"{self.base_url}/swagger/",
                'redoc': f"{self.base_url}/redoc/"
            }

            return Response(urls, status=status.HTTP_200_OK)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
