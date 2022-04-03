from django.db.models       import Q
from django.http            import JsonResponse
from django.views           import View

from products.models import Image, ProductColor

class ProductListView(View): 
    def get(self, request): 
        category = request.GET.getlist('category', None)
        color= request.GET.getlist('color',None)
        product = request.GET.get('product',None)
        price_upper_range  = request.GET.get('priceupper',100000000)
        price_lower_range  = request.GET.get('pricelower',0)
        result=[]
        
        q = Q()

        if category:
            q &= Q(product__category_id__in = category)

        if product:
            q &= Q(product__name__istartswith = product)
                       
        if color :
            q &= Q(color__name__in = (color))

        q &= Q (product__price__range = (price_lower_range, price_upper_range))

        products = ProductColor.objects.filter(q) 

        result=[{
            "primary_key" : pc.id,
            "category" : pc.product.category.name,
            "name" :  pc.product.name,
            "color" : pc.color.name,
            "price" : pc.product.price,
            "image" : [image.image_url for image in Image.objects.filter(product_color_id = pc.id, sequence=1)]       
        }for pc in products]
            

        return JsonResponse({"result":result}, status=200)    

class DetailView(View): 
    def get(self, request, product_id): 
        color = request.GET.get('color', None)
        product_data = ProductColor.objects.filter(product_id=product_id)

        if color != None:
            product_data = ProductColor.objects.filter(product_id=product_id, color_id=color)
 
        result=[{
            "name"      : product.product.name,
            "price"     : product.product.price,
            "color"     : product.color.name,
            "image_list": [image.image_url for image in Image.objects.filter(product_color_id = product.color.id)]
        }for product in product_data]

            
        return JsonResponse({"result" : result}, status=200)