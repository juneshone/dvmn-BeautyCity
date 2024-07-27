# Generated by Django 5.0.7 on 2024-07-25 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_salons', '0006_customuser_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, verbose_name='номер телефона')),
                ('pin', models.CharField(max_length=4, verbose_name='код')),
            ],
        ),
    ]
