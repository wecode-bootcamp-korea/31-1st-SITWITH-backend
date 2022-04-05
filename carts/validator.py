from django.forms import ValidationError

def validate_quantity(quantity, inventory):
    if quantity <= 0:
        raise ValidationError('Quantity must be positive number')
    
    if quantity > inventory:
        raise ValidationError('Quantity cannot be more than inventory')