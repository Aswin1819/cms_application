import re
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger(__name__)


class RegisterUserSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['username','email','password']
        extra_kwargs = {
            'password' : {'write_only':True,'min_length':6},
        }
        
    def validate_email(self, value):
        user_qs = CustomUser.objects.filter(email=value)
        if user_qs.exists():
            user = user_qs.first()
            if not user.is_active:
                raise serializers.ValidationError('This account exists but deactiated')
            raise serializers.ValidationError('A user with this email already exists')
        return value
    
    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError('Username cannot be empty')
        
        if not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$',value):
            raise serializers.ValidationError('username must contain only alphabets and spaces')
        return value
    
    def validate_password(self, value):
        if len(value)<6:
            raise serializers.ValidationError("Password must be atleast 6 characters")
        return value
        
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # username_field = CustomUser.USERNAME_FIELD
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'] = self.fields.pop('username')
    
    def validate(self, attrs):
        email_or_username = attrs.get('email') or attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=email_or_username,password=password)
        
        if user is None:
            raise AuthenticationFailed(_('Invalid Credentials'),code='invalid_credentials')
        
        if not user.is_active:
            raise AuthenticationFailed(_('This account has been deactivated by admin'),code='inactive')
        
        self.user = user
        
        data = super().validate(attrs)
        return data
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['id', 'email', 'username','bio','profile_image',
                  'is_verified', 'date_joined', 'updated_at', 'is_active', 'is_superuser']
        read_only_fields = ['id','email','is_verified', 'date_joined', 'updated_at']
        
    
    
