# serializers.py
from rest_framework import serializers
from .models import Investor, Businessman

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = '__all__'

class BusinessmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Businessman
        fields = '__all__'
