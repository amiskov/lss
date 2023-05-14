from django.db import models

from djmoney.models.fields import MoneyField


class IncomeSource(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=512)

    def __str__(self):
        return self.name


class Income(models.Model):
    amount = MoneyField(max_digits=14, decimal_places=2,
                        default_currency='RUB')
    source = models.ForeignKey(IncomeSource, on_delete=models.CASCADE)
    datetime = models.DateTimeField('Income received')
    description = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = ['-datetime', 'source']

    def __str__(self):
        return self.source.name + ', ' + str(self.amount)
