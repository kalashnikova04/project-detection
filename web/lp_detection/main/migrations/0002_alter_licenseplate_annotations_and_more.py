# Generated by Django 5.0.6 on 2024-05-08 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="licenseplate",
            name="annotations",
            field=models.FileField(blank=True, upload_to="uploads/"),
        ),
        migrations.AlterField(
            model_name="licenseplate",
            name="number",
            field=models.IntegerField(blank=True),
        ),
    ]
