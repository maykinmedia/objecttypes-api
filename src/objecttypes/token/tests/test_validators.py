from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from objecttypes.token.validators import validate_no_whitespace


class WhiteSpaceValidatorTestCase(SimpleTestCase):
    def test_characters_only(self):
        self.assertIsNone(validate_no_whitespace("test123"))

    def test_trailing_whitespace(self):
        with self.assertRaises(ValidationError):
            validate_no_whitespace("test123  ")

    def test_leading_whitespace(self):
        with self.assertRaises(ValidationError):
            validate_no_whitespace("  test123")

    def test_whitespace_in_between(self):
        with self.assertRaises(ValidationError):
            validate_no_whitespace("test  123")

    def test_whitespace_only(self):
        with self.assertRaises(ValidationError):
            validate_no_whitespace("  ")

    def test_trailing_tab_character(self):
        with self.assertRaises(ValidationError):
            validate_no_whitespace("test123\t")

    def test_leading_tab_character(self):
        with self.assertRaises(ValidationError):
            validate_no_whitespace("\ttest123")

    def test_tab_character_in_between(self):
        with self.assertRaises(ValidationError):
            validate_no_whitespace("test\t123")

    def test_tab_characters_only(self):
        with self.assertRaises(ValidationError):
            validate_no_whitespace("\t\t")

    def test_blank_value(self):
        with self.assertRaises(ValidationError):
            validate_no_whitespace("")
