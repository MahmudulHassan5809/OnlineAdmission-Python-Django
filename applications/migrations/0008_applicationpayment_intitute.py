# Generated by Django 3.0.7 on 2020-07-03 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0006_admissionsession_level'),
        ('applications', '0007_auto_20200703_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationpayment',
            name='intitute',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='institution.InstitutionProfile'),
            preserve_default=False,
        ),
    ]
