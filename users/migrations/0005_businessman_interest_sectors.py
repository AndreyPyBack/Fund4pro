# Generated by Django 5.0.1 on 2024-02-01 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_businessman_interest_sectors_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessman',
            name='interest_sectors',
            field=models.ManyToManyField(blank=True, to='users.interestsector'),
        ),
    ]
