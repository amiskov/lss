# Generated by Django 4.2 on 2023-05-14 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]