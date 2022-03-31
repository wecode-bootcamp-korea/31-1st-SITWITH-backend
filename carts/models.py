from django.db    import models

from cores.models import TimestampZone

class Cart(TimestampZone): 
<<<<<<< HEAD
    user     = models.ForeignKey('users.user', on_delete=models.CASCADE)
    product  = models.ForeignKey('products.product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
=======
    user          = models.ForeignKey('users.user', on_delete=models.CASCADE)
    product_color = models.ForeignKey('products.productcolor', on_delete=models.CASCADE)
    quantity      = models.IntegerField()
>>>>>>> e9b79c0306fc3d484eb26c877a860da22cbc501d

    def total_price(self): 
        return self.quantity * self.product.price

    class Meta: 
        db_table = 'carts'