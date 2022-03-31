import re

from django.forms import ValidationError

REGEX_USERNAME = '^[a-z0-9+]{3,15}$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$'
REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def username_validate(username):
    if not re.match(REGEX_USERNAME, username):
        raise ValidationError("Invalid username")

def password_validate(password):
    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError("Invalid password")
    
def email_validate(email):
    if email == "":
        pass
    else:
        if not re.match(REGEX_EMAIL, email):
            raise ValidationError("Invalid email")