from django.db import models
from cores.models import TimestampZone

class Category(TimestampZone): 
    name = models.CharField(max_length=45)

    class Meta: 
        db_table = 'categories'

class Product(TimestampZone): 
    name     = models.CharField(max_length=45)
    price    = models.DecimalField(max_digits=None)
    color    = models.ManyToManyField('Color', 'self',on_delete=models.CASCADE, through='productcolor', related_name='productcolor')
    category = models.ForeignKey('Category', on_delete = models.CASCADE)

    class Meta: 
        db_table = 'products'

class Color(TimestampZone): 
    name = models.CharField(max_length=45)

    class Meta: 
        db_table = 'colors'

class Image(TimestampZone): 
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=45)
    sequence  = models.IntegerField()

    class Meta: 
        db_table = 'images'

class ProductColor(TimestampZone): 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color   = models.ForeignKey('Color', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'productcolor'