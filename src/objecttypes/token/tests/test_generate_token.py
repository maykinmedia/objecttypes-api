from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from objecttypes.token.models import TokenAuth


class GenerateTokenCommandTests(TestCase):
    def test_generate_token(self):
        out = StringIO()

        call_command(
            "generate_token",
            "john doe",
            "john@example.com",
            organization="ACME",
            application="Foo",
            administration="Bar",
            stdout=out,
        )

        token = TokenAuth.objects.get()

        self.assertIsNotNone(token.token)
        self.assertEqual(token.contact_person, "john doe")
        self.assertEqual(token.email, "john@example.com")
        self.assertEqual(token.organization, "ACME")
        self.assertEqual(token.application, "Foo")
        self.assertEqual(token.administration, "Bar")
        self.assertEqual(out.getvalue(), f"Token {token.token} was generated\n")
