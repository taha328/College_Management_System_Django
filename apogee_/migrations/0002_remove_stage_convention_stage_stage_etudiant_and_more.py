# Generated by Django 5.0 on 2023-12-31 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apogee_', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stage',
            name='convention_stage',
        ),
        migrations.AddField(
            model_name='stage',
            name='etudiant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apogee_.dossieretudiant'),
        ),
        migrations.DeleteModel(
            name='Etudiant',
        ),
    ]
