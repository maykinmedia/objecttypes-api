# Generated by Django 2.2.24 on 2021-11-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_auto_20201126_2007"),
    ]

    operations = [
        migrations.AddField(
            model_name="objecttype",
            name="has_geometry",
            field=models.BooleanField(
                default=True,
                help_text="Shows whether the related objects have geographic coordinates",
                verbose_name="has geometry",
            ),
        ),
    ]