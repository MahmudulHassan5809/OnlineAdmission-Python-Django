# Generated by Django 3.0.8 on 2020-07-06 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0005_auto_20200706_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='roll_number',
            field=models.CharField(default='5432106092', editable=False, max_length=10, unique=True),
        ),
    ]
