import logging
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from enquiry.serializer import EnquirySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from enquiry.models import Enquiry
from app import globalMessage
# Create your views here.


logger = logging.getLogger('django')


class EnquiryView(APIView):
    """API views  for enquires from the  website
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            enquires = Enquiry.objects.filter(is_delete=False)
            serializer = EnquirySerializer(enquires, many=True)
            data = {
                globalMessage.MESSAGE: globalMessage.SUCCESS_MSG,
                'status': globalMessage.SUCCESS_RESPONSE,
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)

        except Enquiry.DoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG, 'status': globalMessage.ERROR_RESPONSE},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            data = request.data
            serializer = EnquirySerializer(data=data)
            if serializer.is_valid():
                serializer.save(created_at=datetime.now(),
                                created_by=request.user)
                return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG}, status=status.HTTP_200_OK)

            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as exe:
            logger.error(exe)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
