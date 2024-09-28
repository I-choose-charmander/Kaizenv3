# Generated by Django 4.2.15 on 2024-09-10 04:34

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
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(null=True)),
                ('ticker', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BMR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('feet', models.IntegerField()),
                ('inches', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('activity_level', models.FloatField(choices=[(1.2, 'Sedentary'), (1.375, 'Light Activity'), (1.55, 'Moderate Activity'), (1.725, 'Very Active'), (1.9, 'Super Activity')])),
                ('goal', models.CharField(choices=[('Muscle Gain', 'Muscle Gain'), ('Maintenace', 'Maintenance'), ('Fat Loss', 'Fat Loss')], max_length=11)),
                ('tdee', models.FloatField(blank=True, null=True)),
                ('protein', models.FloatField(blank=True, null=True)),
                ('fat', models.FloatField(blank=True, null=True)),
                ('carb', models.FloatField(blank=True, null=True)),
                ('save_to_profile', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
