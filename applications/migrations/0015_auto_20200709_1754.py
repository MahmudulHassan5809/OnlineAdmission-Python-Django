# Generated by Django 3.0.8 on 2020-07-09 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0014_auto_20200709_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='roll_number',
            field=models.CharField(default='9401514050', editable=False, max_length=10, unique=True),
        ),
    ]
