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


class TeamAddAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        try:
            # user input and user instance
            data = request.data
            user = request.user

            if not data:
                return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_400_BAD_REQUEST)

            try:
                serializer = TeamSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(created_at=datetime.now(),
                                    created_by=user)

                    MSG = {
                        globalMessage.MESSAGE: globalMessage.SUCCESS_MSG,
                        'status': globalMessage.SUCCESS_RESPONSE,
                        'data': serializer.data
                    }
                    return Response(MSG, status=status.HTTP_200_OK)
                return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG, 'status': globalMessage.SUCCESS_RESPONSE},
                                status=status.HTTP_401_UNAUTHORIZED)

            except Exception as exe:
                raise Exception(exe)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG, 'status': globalMessage.SUCCESS_RESPONSE},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeamDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    """ retrive data with ref_id and update and delete
    """
    def get(self, request, ref_id, format=None):
        try:
            try:
                member = Team.objects.get(reference_id=ref_id)
            
            except Team.DoesNotExist as exe:
                raise Exception(exe)
            
            serializer = TeamSerializer(member)
            return Response({globalMessage.MESSAGE: globalMessage.SUCCESS_MSG, 'status': globalMessage.SUCCESS_RESPONSE, 
                            'data': serializer.data}, 
                            status=status.HTTP_200_OK)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, ref_id, format=None):
        try:
            data = request.data
            user = request.user

            try:
                member = Team.objects.get(reference_id=ref_id)
            
            except Team.DoesNotExist as exe:
                raise Exception(exe)
            
            serializer = TeamSerializer(member, data=data)
            if serializer.is_valid():
                serializer.save(created_at=datetime.now(), 
                                created_by=user)
                MSG = {
                    globalMessage.MESSAGE: globalMessage.SUCCESS_MSG,
                    'status': globalMessage.SUCCESS_RESPONSE,
                }

                return Response(MSG, status=status.HTTP_200_OK)
            
            return Response({ globalMessage.MESSAGE: globalMessage.ERROR_MSG}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGE: globalMessage.ERROR_MSG}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, ref_id, format=None):
        try:
            Team.objects.get(reference_id=ref_id).delete()
            MSG = {
                globalMessage.MESSAGE: globalMessage.SUCCESS_MSG,
                'status': globalMessage.SUCCESS_RESPONSE
            }

            return Response(MSG, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response({globalMessage.MESSAGEL: globalMessage.SUCCESS_MSG})
    