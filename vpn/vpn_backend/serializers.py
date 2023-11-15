from rest_framework import serializers
from .models import User, Website, Statistics

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(style={'input_type':'email'}, required=False)
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'

class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'
