# Generated by Django 4.1.1 on 2022-09-27 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0003_departmentdisponibility_alter_reservation_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departmentdisponibility',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelTable(
            name='departmentdisponibility',
            table='department_disponibility',
        ),
    ]