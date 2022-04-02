from django.http            import JsonResponse
from django.views           import View

from .models import Product, Color, Image, ProductColor


class ProductListView(View): 
    def get(self, request): 
        category = request.GET.get('category', "all")
        
        if category != 'all':
           product_data = Product.objects.filter(category_id=category)

        else: 
            product_data = Product.objects.all()

        if not product_data: 
            return JsonResponse({"message":"Category does not exist"}, status = 400)

        for product in product_data: 
            productcolor_data = ProductColor.objects.filter(product_id = product.id)
            res=[{
                "name" : product.name,
                "price": product.price,
                "color": productcolor.color.name,
                "main_image": [image.image_url for image in Image.objects.filter(product_color_id = productcolor.id)][0]
            }for productcolor in productcolor_data]

            result=[{
                "category_id" : category,
                "product_info": res
            }]
        
        return JsonResponse({"message":"Success", "result":result}, status = 200)
    
class DetailView(View): 
    def get(self, request, product_id): 
        color = request.GET.get('color', None)
        product_data = Product.objects.filter(id=product_id)

        if not product_data: 
            return JsonResponse({"message":"Product does not exist"}, status = 400)
        
        for product in product_data:
            if color == None:  
                color_data = ProductColor.objects.filter(product_id = product.id)

            else: 
                color   = int(Color.objects.get(id = color).id)
                color_data = ProductColor.objects.filter(product_id = product.id, color_id = color)   

            if not color_data:
                return JsonResponse({"message":"Color does not exist"}, status = 400)
            
            result = [{
                "name"      : data.product.name,
                "price"     : product.price,
                "color"     : data.color.name,
                "image_list": [image.image_url for image in Image.objects.filter(product_color_id = data.id)]
            }for data in color_data]

        return JsonResponse({"message":"Success", "result" : result}, status=200)