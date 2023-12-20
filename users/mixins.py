# mixins.py in your Django app directory
from django.core.exceptions import ValidationError

class AgeValidationMixin:
    def clean_age(self):
        age = self.cleaned_data.get('age') # type: ignore
        if age is not None and age <= 0:
            raise ValidationError("Age must be greater than zero.")
        return age
