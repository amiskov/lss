from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.formats import localize

from djmoney.models.fields import MoneyField


class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)

    def __str__(self):
        return self.name + ', ' + self.address


class Purchase(models.Model):
    datetime = models.DateTimeField('purchase date')
    place = models.ForeignKey(Place, on_delete=models.DO_NOTHING)
    note = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = ['-datetime', 'place']

    @property
    def totals(self):
        totals = 0
        for e in self.expenses.all():
            totals += e.price
        return totals

    def __str__(self):
        return self.place.name + '(' + str(self.datetime) + ')'


class Expense(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    price = MoneyField(max_digits=14, decimal_places=2,
                       default_currency='RUB')
    purchase = models.ForeignKey(to=Purchase, related_name="expenses", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-price']


    def __str__(self):
        return self.product.name + ', ' + str(self.price)
