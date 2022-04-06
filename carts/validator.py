from django.forms import ValidationError
    
def validate_quantity(quantity):
    if quantity <= 0:
        raise ValidationError('Quantity must be positive number')