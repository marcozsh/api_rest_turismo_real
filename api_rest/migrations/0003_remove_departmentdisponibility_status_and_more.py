# Generated by Django 4.1.1 on 2022-10-01 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0002_remove_reservation_department_disponibility_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departmentdisponibility',
            name='status',
        ),
        migrations.AddField(
            model_name='department',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]
