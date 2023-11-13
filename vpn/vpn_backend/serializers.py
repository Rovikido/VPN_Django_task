from rest_framework import serializers
from .models import User, Website, Statistics

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'

class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'
