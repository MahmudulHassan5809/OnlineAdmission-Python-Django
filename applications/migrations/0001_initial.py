# Generated by Django 3.0.7 on 2020-07-02 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applicant', '0001_initial'),
        ('institution', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_applications', to='applicant.ApplicantProfile')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_applications', to='institution.InstitutionProfile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]