# Generated by Django 3.0.7 on 2020-07-02 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_name', models.CharField(max_length=255)),
                ('institute_location', models.CharField(max_length=255)),
                ('institute_code', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female'), ('3', 'Both')], default='3', max_length=10)),
                ('institute_pic', models.ImageField(upload_to='institution')),
                ('active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_institute', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'InstitutionProfile',
                'verbose_name_plural': '1. InstitutionProfile',
            },
        ),
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
            name='AdmissionSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_name', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('status', models.BooleanField()),
                ('institute', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='institute_session', to='institution.InstitutionProfile')),
            ],
            options={
                'verbose_name': 'AdmissionSession',
                'verbose_name_plural': '2. AdmissionSession',
            },
        ),
    ]