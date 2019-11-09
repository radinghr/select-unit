from rest_framework import serializers
from .models import User, Major

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'semester', 'major']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']


class AddMajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'