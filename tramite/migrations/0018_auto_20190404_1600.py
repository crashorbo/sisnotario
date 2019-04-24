# Generated by Django 2.1.4 on 2019-04-04 20:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0010_remove_persona_fecha_documento'),
        ('tramite', '0017_auto_20190227_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='TramiteViaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cn', models.CharField(blank=True, max_length=50)),
                ('residencia', models.CharField(blank=True, max_length=250)),
                ('persona', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='persona.Persona')),
            ],
        ),
        migrations.AlterField(
            model_name='tramite',
            name='fecha_documento',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='tramite',
            name='fecha_registro',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='tramite',
            name='hora_registro',
            field=models.TimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='tramite',
            name='tipo_tramite',
            field=models.IntegerField(choices=[(1, 'CERTIFICACION FIRMAS Y RUBRICAS'), (2, 'AUTORIZACION DE VIAJE DE MENOR')], default=1),
        ),
        migrations.AlterField(
            model_name='tramitepersona',
            name='fecha_registro',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='tramiteviaje',
            name='tramite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tramite.Tramite'),
        ),
    ]
