# Generated by Django 2.1.4 on 2019-07-03 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramite', '0013_tramiteviaje_firma'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramiteviaje',
            name='lugar_trabajo',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
