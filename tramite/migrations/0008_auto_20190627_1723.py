# Generated by Django 2.1.4 on 2019-06-27 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramite', '0007_tramite_parte_aux'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramite',
            name='contra_parte_imp',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='tramite',
            name='parte_imp',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]