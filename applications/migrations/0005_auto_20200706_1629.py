# Generated by Django 3.0.8 on 2020-07-06 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_application_roll_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='roll_number',
            field=models.CharField(default='9897891297', editable=False, max_length=10, unique=True),
        ),
    ]