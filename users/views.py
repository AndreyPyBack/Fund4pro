from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Investor, Businessman
from .serializers import UserLoginSerializer, BusinessmanRegistrationSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import InterestSector, Investor
from .serializers import InterestSectorSerializer, InvestorRegistrationSerializer



import jwt
from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail

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


class BusinessmanCreateAPIView(APIView):
    def post(self, request):
        serializer = BusinessmanRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Попытка найти пользователя по email
            user, created = User.objects.get_or_create(
                email=serializer.validated_data['email'],
                defaults={
                    'username': serializer.validated_data['email'],
                    'password': serializer.validated_data['password'],
                }
            )
            # Если пользователь уже существует, возвращаем ошибку
            if not created:
                return Response({'error': 'Пользователь с таким email уже существует'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Создаем бизнесмена, связанного с пользователем
            businessman = Businessman.objects.create(
                user=user,
                interest_sectors=serializer.validated_data['interest_sectors'],
                business_range=serializer.validated_data['business_range'],
                receive_interesting_offers=serializer.validated_data['receive_interesting_offers']
            )
            # Возвращаем успешный ответ
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Возвращаем ошибку, если данные невалидны
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Неправильные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    def post(self, request):
        token = request.data.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'], is_email_verified=False)
            user.is_email_verified = True
            user.save()
            return Response({'message': 'Email successfully verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Verification link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except (jwt.DecodeError, User.DoesNotExist):
            return Response({'error': 'Invalid token or user not found'}, status=status.HTTP_400_BAD_REQUEST)
def generate_verification_token(user_id):
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Токен действителен 24 часа
    }, settings.SECRET_KEY, algorithm='HS256')
    return token
def send_verification_email(user):
    token = generate_verification_token(user.id)
    subject = 'Подтверждение адреса электронной почты'
    message = f'Привет {user.username},\n\n' \
              f'Пожалуйста, подтвердите ваш адрес электронной почты, перейдя по следующей ссылке:\n' \
              f'http://fund4pro@schoolprojecttesting.ru/verify-email/?token={token}\n\n' \
              'С уважением,\nКоманда сайта'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)