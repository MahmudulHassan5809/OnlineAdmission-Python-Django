# Generated by Django 3.0.7 on 2020-07-03 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0001_initial'),
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionTransactionMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method_name', models.CharField(max_length=50)),
                ('account_number', models.CharField(max_length=50)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_transaction', to='institution.InstitutionProfile')),
            ],
            options={
                'verbose_name': 'Institution Transaction',
                'verbose_name_plural': '3. Institution Transaction',
            },
        ),
        migrations.CreateModel(
            name='ApplicationPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_from', models.CharField(max_length=20)),
                ('transaction_number', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'Completed'), ('2', 'Canceled')], default='0', max_length=10)),
                ('completed', models.BooleanField(default=False)),
                ('pending', models.BooleanField(default=False)),
                ('cancel', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applications.Application')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institution.InstitutionProfile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.InstitutionTransactionMethod')),
            ],
        ),
    ]
