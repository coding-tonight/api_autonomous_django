import logging
from datetime import datetime 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from team.models import Team
from team.serializer import TeamSerializer
from app import globalMessage


logger = logging.getLogger('django')


class TeamAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            try:
                teams = Team.objects.filter(is_delete=False)

            except Team.DoesNotExist as exe:
                raise Exception(exe)
            
            serializer = TeamSerializer(teams)
            MSG = {
                globalMessage.MESSAGE: globalMessage.SUCCESS_MSG,
                'status': globalMessage.SUCCESS_RESPONSE,
                'data': serializer.data
            }

            return Response(MSG, status=status.HTTP_200_OK)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)