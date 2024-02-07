from .models import InterestSector, Investor
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Investor


class InterestSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestSector
        fields = '__all__'


class InvestorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = Investor
        fields = ['email', 'password', 'password_confirmation', 'first_name', 'last_name', 'interest_sectors',
                  'investment_range', 'receive_interesting_offers', 'verification']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        user_data = {
            'username': validated_data['email'],  # Можете использовать email в качестве имени пользователя
            'email': validated_data['email'],
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
        }
        user = User.objects.create_user(**user_data)
        investor = Investor.objects.create(user=user, **validated_data)
        return investor
