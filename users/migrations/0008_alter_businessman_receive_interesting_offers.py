# Generated by Django 5.0.1 on 2024-02-09 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_businessman_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessman',
            name='receive_interesting_offers',
            field=models.BooleanField(default=False, help_text='Получать полезные материалы по привлечению инвестиций'),
        ),
    ]
