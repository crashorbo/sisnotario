# Generated by Django 2.1.4 on 2019-02-05 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tramite', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tramite',
            old_name='fecha_Actualizacion',
            new_name='fecha_actualizacion',
        ),
        migrations.AlterField(
            model_name='tramite',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tramite',
            name='tipo_tramite',
            field=models.IntegerField(choices=[(1, 'CERTIFICACION RUBRICAS')]),
        ),
        migrations.AlterField(
            model_name='tramite',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
