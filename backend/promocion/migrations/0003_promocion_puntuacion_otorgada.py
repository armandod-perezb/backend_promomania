from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promocion', '0002_promocion_created_at_promocion_foto_es_local_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocion',
            name='puntuacion_otorgada',
            field=models.BooleanField(default=False),
        ),
    ]
