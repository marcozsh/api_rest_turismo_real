# Generated by Django 4.1.1 on 2022-11-09 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0014_servicesinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesinformation',
            name='reservation',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api_rest.reservation'),
        ),
    ]