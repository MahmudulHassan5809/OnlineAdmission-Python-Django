# Generated by Django 3.0.8 on 2020-07-05 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionprofile',
            name='institute_city',
            field=models.CharField(default='Dhaka', max_length=150),
            preserve_default=False,
        ),
    ]