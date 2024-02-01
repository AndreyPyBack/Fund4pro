# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvestorViewSet, BusinessmanViewSet

router = DefaultRouter()
router.register(r'investors', InvestorViewSet)
router.register(r'businessmen', BusinessmanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
