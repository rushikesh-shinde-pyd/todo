# django imports
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# third-party imports
import re

User = get_user_model()


# def validate_email(value):
#     if value:
#         print(Profile.objects.filter(user__email=value).exists())
#         print(User.objects.filter(email=value).exists())
#         if Profile.objects.filter(user__email=value).exists():
#             raise ValidationError('Email already exists')

def validate_mobile(value):
    from .models import Profile
    if value:
        pattern = '[6-9][0-9]{9}'
        if not re.fullmatch(pattern, value):
            raise ValidationError('Invalid mobile number')
            # errors.append('Invalid mobile number')
        if Profile.objects.filter(mobile=value).exists():
            raise ValidationError('Mobile number already exists')
            # errors.append('Mobile number already exists')