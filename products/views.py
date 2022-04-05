from django.db.models       import Q
from django.http            import JsonResponse
from django.views           import View

from products.models import *

class ProductListView(View): 
    def get(self, request):
        offset      = int(request.GET.get('offset', 0))
        limit       = int(request.GET.get('limit', 100))
        
        products = Product.objects.all()[offset:limit]
        
        result=[{ 
            "category": Category.objects.get(id=product.category_id).id,
            "name"    : product.name,
            "price"   : product.price,
            "colors"  : [{
                "id"   : color.id,
                "color": color.color.name,
                "image": [image.image_url for image in Image.objects.filter(product_color_id=color.id, sequence=1)][0]
            }for color in ProductColor.objects.filter(product_id = product.id)]
        }for product in products]
    
        return JsonResponse({"result":result}, status=200)

class DetailView(View): 
    def get(self, request, product_id): 
        color        = request.GET.get('color', None)
        product_data = ProductColor.objects.filter(product_id=product_id)
        res          = []
        
        if color != None:
            product_data = ProductColor.objects.filter(product_id=product_id, color_id=color)

        for product in product_data:
            res.append({
                "primary_key": product.id,
                "color"      : product.color.name,
                "image_list" : [image.image_url for image in Image.objects.filter(product_color_id = product.color.id)]
            })
        result=[{
            "name"      : product.product.name,
            "price"     : product.product.price,
            "result"    : res
        }]
        
        return JsonResponse({"result" : result}, status=200)

class SmartSearchView(View): 
    def get(self, request): 
        categories = request.GET.getlist('category', None)
        colors     = request.GET.getlist('color',None)
        product    = request.GET.get('product',None)
        max_price  = request.GET.get('max_price',100000000)
        min_price  = request.GET.get('min_price',0)
        result     = []
    
        q &= Q(product__price__range = (min_price, max_price))

        if categories:
            q &= Q(product__category_id__in = categories)

        if product:
            q &= Q(product__name__icontains = product)
                       
        if colors:
            q &= Q(color__name__in = colors)

        products = ProductColor.objects.filter(q)

        result=[{
            "primary_key": product.id,
            "category"   : product.product.category.name,
            "name"       : (product.product.name),
            "color"      : product.color.name,
            "price"      : product.product.price,
            "image"      : [image.image_url for image in Image.objects.filter(product_color_id = product.id, sequence=1)]
        }for product in products]
     
        return JsonResponse({"result":result}, status=200)    