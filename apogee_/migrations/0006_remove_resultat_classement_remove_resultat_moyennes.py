# Generated by Django 5.0 on 2024-01-03 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apogee_', '0005_alter_dossieretudiant_adresse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultat',
            name='classement',
        ),
        migrations.RemoveField(
            model_name='resultat',
            name='moyennes',
        ),
    ]
