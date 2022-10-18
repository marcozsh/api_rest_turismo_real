# Generated by Django 4.1.1 on 2022-10-10 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0004_rename_description_product_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=2)),
                ('transaction_date', models.DateField()),
                ('reservation_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reservation_id_fk', to='api_rest.reservation')),
            ],
            options={
                'db_table': 'transaction',
                'ordering': ['id'],
            },
        ),
    ]