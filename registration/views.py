# views.py
from rest_framework import viewsets
from .models import Investor, Businessman
from .serializers import InvestorSerializer, BusinessmanSerializer

class InvestorViewSet(viewsets.ModelViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer

class BusinessmanViewSet(viewsets.ModelViewSet):
    queryset = Businessman.objects.all()
    serializer_class = BusinessmanSerializer