# Generated by Django 4.1.1 on 2022-11-08 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0013_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicesInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(default=None, max_length=250, null=True)),
                ('service', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='service_information_fk', to='api_rest.services')),
            ],
            options={
                'db_table': 'service_information',
                'ordering': ['id'],
            },
        ),
    ]
