"""Custom validations file"""
import re

def verify_email(email):
    """Function to verify a valid email format"""
    return bool(re.match('[^@]+@[^@]+\.[^@]+', email))

def validate_empty_fields(**kwargs):
    """
    Function to validate empty fields.
    Raises an error if the fields are empty
    """
    for field in kwargs:
        value = kwargs.get(field)
        if isinstance(value, str):
            value = value.strip()
        if not type(value) is bool and not value:
            raise AttributeError(field + " is required field")
