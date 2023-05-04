# Generated by Django 4.2 on 2023-04-18 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('activity_type', models.CharField(choices=[('good', 'Good'), ('bad', 'Bad'), ('necessary', 'Necessary')], default='necessary', max_length=56)),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='ActedActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(verbose_name='action started')),
                ('finished', models.DateTimeField(verbose_name='action finished')),
                ('note', models.CharField(max_length=1024)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='activities.activity')),
            ],
            options={
                'verbose_name_plural': 'Acted Activities',
            },
        ),
    ]