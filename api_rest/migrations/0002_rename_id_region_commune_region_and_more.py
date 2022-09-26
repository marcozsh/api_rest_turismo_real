# Generated by Django 4.1.1 on 2022-09-26 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commune',
            old_name='id_region',
            new_name='region',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='commune_id',
            new_name='commune',
        ),
        migrations.RenameField(
            model_name='customeraccount',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='commune_id',
            new_name='commune',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='department_type_id',
            new_name='department_type',
        ),
        migrations.RenameField(
            model_name='departmentinventory',
            old_name='department_id',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='departmentinventory',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='departmentmaintenance',
            old_name='department_id',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='employee_type_id',
            new_name='employee_type',
        ),
        migrations.RenameField(
            model_name='employeeaccount',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='employeesession',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='employeetype',
            old_name='work_area_id',
            new_name='work_area',
        ),
        migrations.RenameField(
            model_name='finance',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='rent',
            old_name='payment_id',
            new_name='payment',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='id_customer',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='id_department',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='id_employee',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='id_payment',
            new_name='payment',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='id_reservation_status',
            new_name='reservation_status',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='id_service',
            new_name='service',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='id_vehicle',
            new_name='vehicle',
        ),
    ]
