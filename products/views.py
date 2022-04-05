from django.db.models       import Q
from django.http            import JsonResponse
from django.views           import View

from products.models import *

class ProductListView(View): 
    def get(self, request):
        products = Product.objects.filter()

        result=[{ 
            "category" : Category.objects.get(id=product.category_id).id,
            "name" : product.name,
            "price" : product.price,
            "colors" : [{
                    "id" : color.id,
                    "color" : color.color.name,
                    "image" : [image.image_url for image in Image.objects.filter(product_color_id=color.id, sequence=1)][0]
                }for color in ProductColor.objects.filter(product_id = product.id)]
        }for product in products]
    
        return JsonResponse({"result":result}, status=200)


class DetailView(View): 
    def get(self, request, product_id): 
        
        color = request.GET.get('color', None)
        product_data = ProductColor.objects.filter(product_id=product_id)
        res=[]
        
        if color != None:
            product_data = ProductColor.objects.filter(product_id=product_id, color_id=color)

        for product in product_data:
            res.append({
                "primary_key" : product.id,
                "color"     : product.color.name,
                "image_list": [image.image_url for image in Image.objects.filter(product_color_id = product.color.id)]
            })
        result=[{
            "name"      : product.product.name,
            "price"     : product.product.price,
            "result"    : res
        }]
        
        return JsonResponse({"result" : result}, status=200)
