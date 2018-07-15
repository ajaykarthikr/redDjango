from django.core.exceptions import ValidationError


def minPhoneLength(val):
    if len(val) < 10:
        raise ValidationError("Phone number has to be at least 10 digits long")


def minPasswordLength(val):
    if len(val) < 8:
        raise ValidationError("Password must be 8 characters long")


def genderValidator(val):
    if val not in ['M', 'F', 'O', '']:
        raise ValidationError("Invalid gender")
