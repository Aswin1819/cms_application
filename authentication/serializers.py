from rest_framework import serializers
from .models import CustomUser
import re

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
        