# Generated by Django 4.1.1 on 2022-10-02 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0003_remove_departmentdisponibility_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='brand',
        ),
    ]
