# Generated by Django 5.0 on 2024-01-03 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apogee_', '0006_remove_resultat_classement_remove_resultat_moyennes'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultat',
            name='classement',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resultat',
            name='moyennes',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
