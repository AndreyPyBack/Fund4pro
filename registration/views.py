from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import InterestSector, Investor
from .serializers import InterestSectorSerializer, InvestorRegistrationSerializer


class InterestSectorListCreateAPIView(APIView):
    def get(self, request):
        sectors = InterestSector.objects.all()
        serializer = InterestSectorSerializer(sectors, many=True)
        return Response(serializer.data)


class InvestorCreateAPIView(APIView):
    def post(self, request):
        serializer = InvestorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Попытка найти пользователя по email
            user, created = User.objects.get_or_create(
                email=serializer.validated_data['email'],
                defaults={
                    'username': serializer.validated_data['email'],
                    'password': serializer.validated_data['password'],
                    'first_name': serializer.validated_data.get('first_name', ''),
                    # Получаем данные о имени, если они были переданы
                    'last_name': serializer.validated_data.get('last_name', ''),
                    # Получаем данные о фамилии, если они были переданы
                }
            )
            # Если пользователь уже существует, возвращаем ошибку
            if not created:
                return Response({'error': 'Пользователь с таким email уже существует'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Создаем инвестора, связанного с пользователем
            investor = Investor.objects.create(
                user=user,
                interest_sectors=serializer.validated_data['interest_sectors'],
                investment_range=serializer.validated_data['investment_range'],
                receive_interesting_offers=serializer.validated_data['receive_interesting_offers']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
