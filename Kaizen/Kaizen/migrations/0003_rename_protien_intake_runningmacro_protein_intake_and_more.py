# Generated by Django 4.2.15 on 2024-09-16 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kaizen', '0002_runningmacro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='runningmacro',
            old_name='protien_intake',
            new_name='protein_intake',
        ),
        migrations.AlterField(
            model_name='runningmacro',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
