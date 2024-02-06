from rest_framework import serializers
from .models import InterestSector, Investor, Businessman

class InterestSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestSector
        fields = '__all__'

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['id', 'username', 'interest_sectors', 'investment_range', 'email', 'password', 'password_confirmation', 'receive_interesting_offers']

class BusinessmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Businessman
        fields = ['id', 'username', 'interest_sectors', 'business_range', 'email', 'password', 'password_confirmation', 'receive_interesting_offers']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
