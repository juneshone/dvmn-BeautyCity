from django.db import models

# Create your models here.


class Pay(models.Model):
    appointment = models.BigIntegerField(verbose_name="Номер записи", blank=True, null=True)
    operation_id = models.CharField(verbose_name="ID операции", max_length=255, unique=True)
    amount = models.DecimalField(verbose_name="Сумма", max_digits=10, decimal_places=2, blank=True, null=True)
    is_success = models.BooleanField(verbose_name="Успешно", blank=True, null=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.operation_id}"
