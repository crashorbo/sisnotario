# Generated by Django 2.1.4 on 2019-06-20 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramite', '0002_auto_20190620_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tramite',
            name='formularios',
            field=models.TextField(blank=True, default=0),
        ),
    ]
