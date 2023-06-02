from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.formats import localize
from django.db.models import Sum

from djmoney.models.fields import MoneyField, Money


class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING)

    class Type(models.TextChoices):
        GOOD = 'good', _('Good')
        BAD = 'bad', _('Bad')
        NECESSARY = 'necessary', _('Necessary')

    product_type = models.CharField(
        max_length=56,
        choices=Type.choices,
        default=Type.NECESSARY,
    )
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)

    def __str__(self):
        return self.name + ', ' + self.address


class Purchase(models.Model):
    datetime = models.DateTimeField('purchase date')
    place = models.ForeignKey(to=Place, related_name='place', on_delete=models.DO_NOTHING)
    note = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = ['-datetime', 'place']

    def __str__(self):
        return self.place.name + '(' + str(self.datetime) + ')'


class Expense(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    price = MoneyField(max_digits=14, decimal_places=2,
                       default_currency='RUB')
    purchase = models.ForeignKey(to=Purchase, related_name="expenses", on_delete=models.CASCADE)

    # class Meta:
        # ordering = ['-price']


    def __str__(self):
        return self.product.name + ', ' + str(self.price)
