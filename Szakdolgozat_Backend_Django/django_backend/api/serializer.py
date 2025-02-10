from .models import EnergyAnalysis

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password']

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Ez a felhasználónév már foglalt."
            )
        ]
    )

    print("Serialize hiba")
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class EnergyAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyAnalysis
        fields = '__all__'
