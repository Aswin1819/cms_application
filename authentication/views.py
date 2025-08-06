from rest_framework.generics import CreateAPIView
from . models import *
from . serializers import * 
from rest_framework.permissions import AllowAny


class RegisterUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerialzier
    queryset = CustomUser.objects.all()
    
    
    


# Create your views here.
