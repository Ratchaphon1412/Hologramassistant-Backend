from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework import authentication, permissions

from .models import UserProfiles
from .serializers import UserProfilesSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.permissions import BasePermission






@method_decorator(csrf_protect, name='dispatch')
class UserProfilesAPI(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        serializer = UserProfilesSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    
    def post(self,request):
        # Your code here
        user_data = request.data
        serializer = UserProfilesSerializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Register User Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        return Response({"csrftoken": "success"})