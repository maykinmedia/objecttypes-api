from django.db import migrations


def switch_to_new_token_model(apps, _):
    OldTokenAuth = apps.get_model("token", "OldTokenAuth")
    TokenAuth = apps.get_model("token", "TokenAuth")

    for old_token in OldTokenAuth.objects.all():
        TokenAuth.objects.get_or_create(
            token=old_token.token,
            defaults={
                "contact_person": old_token.contact_person,
                "email": old_token.email,
                "organization": old_token.organization,
                "last_modified": old_token.last_modified,
                "created": old_token.created,
                "application": old_token.application,
                "administration": old_token.administration,
            },
        )


def switch_to_old_token_model(apps, _):
    OldTokenAuth = apps.get_model("token", "OldTokenAuth")
    TokenAuth = apps.get_model("token", "TokenAuth")

    for token in TokenAuth.objects.all():
        OldTokenAuth.objects.get_or_create(
            token=token.token,
            defaults={
                "contact_person": token.contact_person,
                "email": token.email,
                "organization": token.organization,
                "last_modified": token.last_modified,
                "created": token.created,
                "application": token.application,
                "administration": token.administration,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("token", "0005_tokenauth"),
    ]

    operations = [
        migrations.RunPython(switch_to_new_token_model, switch_to_old_token_model),
    ]
