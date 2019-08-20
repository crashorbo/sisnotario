# Generated by Django 2.2.4 on 2019-08-19 21:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20190703_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personaback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellido_pat', models.CharField(blank=True, max_length=100)),
                ('apellido_mat', models.CharField(blank=True, max_length=100)),
                ('expedido', models.IntegerField(choices=[(1, 'ORURO'), (2, 'LA PAZ'), (3, 'COCHABAMBA'), (4, 'SANTA CRUZ'), (5, 'CHUQUISACA'), (6, 'POTOSI'), (7, 'TARIJA'), (8, 'BENI'), (9, 'PANDO')], default=1)),
                ('nro_documento', models.CharField(max_length=50, unique=True)),
                ('estado_civil', models.IntegerField(choices=[(1, 'SOLTERO(A)'), (2, 'CASADO(A)'), (3, 'VIUDO(A)'), (4, 'DIVORCIADO(A)')], default=1)),
                ('genero', models.IntegerField(choices=[(1, 'MASCULINO'), (2, 'FEMENINO')], default=1)),
                ('nacionalidad', models.CharField(default='BOLIVIANA', max_length=100)),
                ('telefono', models.CharField(blank=True, default='', max_length=50)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('fecha_nacimiento', models.DateField(default=django.utils.timezone.now)),
                ('direccion', models.CharField(blank=True, max_length=200)),
                ('tipo_persona', models.IntegerField(choices=[(0, 'NATURAL'), (1, 'JURIDICO(A)')], default=0)),
                ('natural', models.CharField(blank=True, default='', max_length=200)),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_actualizacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('razon_social', models.CharField(blank=True, default='', max_length=200)),
                ('poder', models.CharField(blank=True, default='', max_length=200)),
                ('nit', models.CharField(blank=True, default='', max_length=20)),
                ('fundempresa', models.CharField(blank=True, default='', max_length=20)),
            ],
        ),
    ]
