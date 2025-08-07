from rest_framework.generics import CreateAPIView
from . models import *
from . serializers import * 
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from . utils import *
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)



class RegisterUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerialzier
    queryset = CustomUser.objects.all()
    
    

class LoginUserView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            data = response.data
            access_token = data.get('access')
            refresh_token = data.get('refresh')
            response = set_jwt_cookies(response, access_token, refresh_token)
            
            response.data.pop('access',None)
            response.data.pop('refresh',None)
            logger.info("user logedin successfully")
        
        return response
    
    
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES.get('refresh')
        logger.info("refresh token initialized")
        return super().post(request, *args, **kwargs)    

            
    

class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        response = Response({
            'message': 'Logout Successfully'
        },status=status.HTTP_200_OK)
        
        response.delet_cookie('access')
        response.delete_cookie('refresh')
        logger.info(f'User logout successfully: {request.user.email}')
        return response

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        logger.info('User profile fetched')
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("user profile fully updated")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error('error on updating user profile')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("User profile partially updated")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error('error on user profile patch')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
