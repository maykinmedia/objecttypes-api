# Generated by Django 4.2.11 on 2024-05-02 13:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("token", "0006_copy_token_auth"),
    ]

    operations = [
        migrations.DeleteModel(
            name="OldTokenAuth",
        ),
    ]
