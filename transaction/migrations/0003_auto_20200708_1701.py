# Generated by Django 3.0.8 on 2020-07-08 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20200706_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutiontransactionmethod',
            name='counter_no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='institutiontransactionmethod',
            name='instruction',
            field=models.TextField(default='Instruction'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='institutiontransactionmethod',
            name='reference_id',
            field=models.CharField(default='12345', max_length=50),
            preserve_default=False,
        ),
    ]