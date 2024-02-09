from django.db import models
from django.contrib.auth.models import User


class InterestSector(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor_profile')
    interest_sectors = models.JSONField()

    INVESTMENT_CHOICES = [
        ('100000-500000', 'От 100.000 до 500.000'),
        ('500000-1000000', 'От 500.000 до 1.000.000'),
        ('1000000-1500000', 'От 1.000.000 до 1.500.000'),
    ]

    investment_range = models.CharField(max_length=20, choices=INVESTMENT_CHOICES)
    receive_interesting_offers = models.BooleanField(default=False,
                                                     help_text="Получать интересные предложения на почту?")
    verification = models.BooleanField(default=False)


class Businessman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='businessman_profile')
    interest_sectors = models.JSONField()

    BUSINESSMAN_CHOICES = [
        ('no', 'Еще нет, собираюсь на вашей платформе'),
        ('yes', 'Да, уже привлекал инвестиции'),
    ]

    business_range = models.CharField(max_length=20, choices=BUSINESSMAN_CHOICES)
    email = models.EmailField(unique=True)
    receive_interesting_offers = models.BooleanField(default=False,
                                                     help_text="Получать полезные материалы по привлечению инвестиций")