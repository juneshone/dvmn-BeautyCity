from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phonenumber = models.CharField(
        'Телефон',
        max_length=100,
        unique=True
    )

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} {self.phonenumber}'


class ServiceCategory(models.Model):
    title = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField('Название', max_length=100)
    price = models.IntegerField('Цена')
    image = models.ImageField(
        'Изображение',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Address(models.Model):
    city = models.CharField('Город', max_length=100)
    street = models.CharField('Улица', max_length=100)
    house = models.CharField('Дом', max_length=100)
    lng = models.FloatField(
        'Координаты (долгота)'
    )
    lat = models.FloatField(
        'Координаты (широта)'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Адрес салона'
        verbose_name_plural = 'Адреса салонов'


class Master(models.Model):
    name = username = models.CharField(
        'ФИО',
        max_length=100,
        unique=True
    )
    profile = models.ManyToManyField(
        ServiceCategory,
        related_name='masters_profiles'
    )
    image = models.ImageField(
        'Изображение',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class Salon(models.Model):
    title = models.CharField(
        'Название',
        max_length=100,
        unique=True
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name = 'Адреса салонов'
    )
    image = models.ImageField(
        'Изображение',
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Салон красоты'
        verbose_name_plural = 'Салоны красоты'


class Appointment(models.Model):
    name = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Наименование услуги'
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        related_name='salons_appointments',
        verbose_name='Салон'
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name='masters_appointments',
        verbose_name = 'Мастер'
    )
    client = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='clients_appointments',
        verbose_name='Клиент'
    )
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    STATUS_CHOICES = [
        ('PAID', 'Оплаченный'),
        ('NOT_PAID', 'Не оплаченный'),
    ]
    status = models.CharField(
        'Статус',
        max_length=50,
        choices=STATUS_CHOICES,
        default='NOT_PAID'
    )


def __str__(self):
    return f'{self.name} {self.salon} {self.master}'


class Meta:
    verbose_name = 'Запись'
    verbose_name_plural = 'Записи'
