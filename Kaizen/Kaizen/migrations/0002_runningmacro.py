# Generated by Django 4.2.15 on 2024-09-16 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Kaizen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunningMacro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True)),
                ('protien_intake', models.FloatField(blank=True, null=True)),
                ('carb_intake', models.FloatField(blank=True, null=True)),
                ('fat_intake', models.FloatField(blank=True, null=True)),
                ('tdee_intake', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
