from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('teryt', '0006_add_JednostkaAdministracyjna_typ'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='jednostkaadministracyjna',
            managers=[
                ('wojewodztwa', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='miejscowosc',
            managers=[
                ('miasta', django.db.models.manager.Manager()),
            ],
        ),
    ]
