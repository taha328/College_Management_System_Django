# Generated by Django 5.0 on 2024-01-02 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apogee_', '0004_stage_adresse_d_entreprise_stage_entreprise_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossieretudiant',
            name='adresse',
            field=models.TextField(default='Votre adresse', max_length=255),
        ),
    ]