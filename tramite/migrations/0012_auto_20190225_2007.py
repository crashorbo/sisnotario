# Generated by Django 2.1.4 on 2019-02-26 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramite', '0011_auto_20190222_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tramite',
            name='pagina_fin',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='tramite',
            name='pagina_inicio',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
