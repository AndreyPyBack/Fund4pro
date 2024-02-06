from .serializers import InvestorSerializer, BusinessmanSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Investor, Businessman
from .serializers import UserLoginSerializer
from django.contrib.auth import authenticate


class InvestorCreateView(generics.CreateAPIView):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer

class BusinessmanCreateView(generics.CreateAPIView):
    queryset = Businessman.objects.all()
    serializer_class = BusinessmanSerializer

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