# Generated by Django 5.0.7 on 2024-07-25 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_salons', '0004_alter_master_image_alter_service_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
