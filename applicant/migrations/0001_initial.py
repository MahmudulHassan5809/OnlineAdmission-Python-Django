# Generated by Django 3.0.7 on 2020-07-03 18:18

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
            name='ApplicantProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=250)),
                ('father_name', models.CharField(max_length=250)),
                ('father_occupation', models.CharField(max_length=250)),
                ('mother_name', models.CharField(max_length=250)),
                ('mother_occupation', models.CharField(max_length=250)),
                ('present_address', models.TextField()),
                ('permanent_address', models.TextField()),
                ('contact_number', models.CharField(max_length=20)),
                ('email_address', models.EmailField(blank=True, max_length=254, null=True)),
                ('birth_date', models.CharField(max_length=230)),
                ('birth_id', models.CharField(blank=True, max_length=250, null=True)),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], max_length=10)),
                ('religion', models.CharField(choices=[('1', 'Islam'), ('2', 'Hinduism'), ('3', 'Cristian'), ('4', 'Buddhist')], max_length=10)),
                ('blood_group', models.CharField(max_length=20)),
                ('freedom_fighter_quota', models.CharField(choices=[('0', 'No'), ('1', 'Yes')], default='0', max_length=150)),
                ('is_autism', models.CharField(choices=[('0', 'No'), ('1', 'Yes')], default='0', max_length=150)),
                ('height', models.FloatField(blank=True, null=True)),
                ('local_guardian_name', models.CharField(blank=True, max_length=250, null=True)),
                ('relation_with_applicant', models.CharField(blank=True, max_length=255, null=True)),
                ('guardian_income', models.FloatField()),
                ('student_pic', models.ImageField(upload_to='student')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Applicant Form',
                'verbose_name_plural': '1. Applicant Form',
            },
        ),
        migrations.CreateModel(
            name='ApplicantPrevEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(choices=[('1', 'SSC'), ('2', 'HSC')], max_length=10)),
                ('board_name', models.CharField(choices=[('1', 'Dhaka'), ('2', 'Khulna'), ('3', 'Rajshahi'), ('4', 'Barishal'), ('5', 'Jessore'), ('6', 'Comilla')], max_length=10)),
                ('institute_name', models.CharField(max_length=255)),
                ('passing_year', models.IntegerField()),
                ('result', models.FloatField()),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_pre_edu', to='applicant.ApplicantProfile')),
            ],
        ),
    ]
