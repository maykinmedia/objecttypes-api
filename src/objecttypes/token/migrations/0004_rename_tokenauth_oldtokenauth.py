# Generated by Django 4.2.11 on 2024-05-02 12:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("token", "0003_auto_20210315_1547"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="TokenAuth",
            new_name="OldTokenAuth",
        ),
    ]