from django.db import migrations, models


def normalizar_nivel_y_puntuacion(apps, schema_editor):
    Usuario = apps.get_model('usuario', 'Usuario')
    Usuario.objects.filter(nivel__isnull=True).update(nivel=1)
    Usuario.objects.filter(puntuacion__isnull=True).update(puntuacion=0)


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_usuario_ciudad_usuario_created_at_usuario_nivel_and_more'),
    ]

    operations = [
        migrations.RunPython(normalizar_nivel_y_puntuacion, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='usuario',
            name='nivel',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='puntuacion',
            field=models.IntegerField(default=0),
        ),
    ]
