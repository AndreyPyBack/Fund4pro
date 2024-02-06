from django.db import models
from django.contrib.auth.hashers import check_password as django_check_password


class InterestSector(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Investor(models.Model):
    username = models.CharField(max_length=30, unique=True)
    interest_sectors = models.ManyToManyField(InterestSector, blank=True)

    INVESTMENT_CHOICES = [
        ('100000-500000', 'От 100.000 до 500.000'),
        ('500000-1000000', 'От 500.000 до 1.000.000'),
        ('1000000-1500000', 'От 1.000.000 до 1.500.000'),
    ]

    investment_range = models.CharField(max_length=20, choices=INVESTMENT_CHOICES)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    password_confirmation = models.CharField(max_length=100)
    receive_interesting_offers = models.BooleanField(default=False, help_text="Получать интересные предложения на почту?")


    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)


class Businessman(models.Model):
    username = models.CharField(max_length=30, unique=True)
    interest_sectors = models.ManyToManyField(InterestSector, blank=True)


    BUSINESSMAN_CHOICES = [
        ('no', 'Еще нет, собираюсь на вашей платформе'),
        ('yes', 'Да, уже привлекал инвестиции'),
    ]

    business_range = models.CharField(max_length=20, choices=BUSINESSMAN_CHOICES)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    password_confirmation = models.CharField(max_length=100)
    receive_interesting_offers = models.BooleanField(default=False, help_text="Получать полезные материалы по привлечению инвестицый")


    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)