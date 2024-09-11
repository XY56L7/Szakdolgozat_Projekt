# from rest_framework import serializers
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

from rest_framework import serializers
from .models import User, EnergyAnalysis

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EnergyAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyAnalysis
        fields = '__all__'
