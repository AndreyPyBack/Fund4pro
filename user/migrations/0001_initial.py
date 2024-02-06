# Generated by Django 5.0.1 on 2024-02-06 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InterestSector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Businessman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('business_range', models.CharField(choices=[('no', 'Еще нет, собираюсь на вашей платформе'), ('yes', 'Да, уже привлекал инвестиции')], max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('password_confirmation', models.CharField(max_length=100)),
                ('receive_interesting_offers', models.BooleanField(default=False, help_text='Получать полезные материалы по привлечению инвестицый')),
                ('interest_sectors', models.ManyToManyField(blank=True, to='user.interestsector')),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('investment_range', models.CharField(choices=[('100000-500000', 'От 100.000 до 500.000'), ('500000-1000000', 'От 500.000 до 1.000.000'), ('1000000-1500000', 'От 1.000.000 до 1.500.000')], max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('password_confirmation', models.CharField(max_length=100)),
                ('receive_interesting_offers', models.BooleanField(default=False, help_text='Получать интересные предложения на почту?')),
                ('interest_sectors', models.ManyToManyField(blank=True, to='user.interestsector')),
            ],
        ),
    ]