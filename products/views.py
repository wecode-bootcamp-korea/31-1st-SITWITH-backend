from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View

from .models         import Product, Color, Category, Image, ProductColor

class CategoryView(View): 
    def get(self, request, category_name): 
        try: 
            result       = []
            category_id  = Category.objects.get(name=category_name)
            product_data = Product.objects.filter(category_id=category_id)

            for product in product_data: 
                productcolor_data = ProductColor.objects.filter(product_id = product.id)
                for productcolor in productcolor_data: 
                    image_data = Image.objects.filter(product_color_id = productcolor.id)
                    color_data = Color.objects.filter(id = productcolor.color_id)

                    result.append({
                        "cate_id"       : category_id.id,
                        "name"          : product.name,
                        "price"         : product.price,
                        "color"         : [color.name for color in color_data],
                        "image_sequence": [image.sequence for image in image_data][0],
                        "image"         : [image.image_url for image in image_data][0]
                    })
            
            return JsonResponse({"message":"Success",'result':result}, status = 200)

        except Image.DoesNotExist: 
            return JsonResponse({"message":"Image does not exist"}, status = 401)

        except: 
            return JsonResponse({"error":"Not found"}, status = 404)

class detailView(View): 
    def get(self, request, product_name): 
        try: 
            result       = []
            product_data = Product.objects.filter(name=product_name)
            
            if not product_data: 
                return JsonResponse({"message":"Product does not exist"}, status = 400)

            for product in product_data:
                color_data = ProductColor.objects.filter(product_id = product.id)
                for data in color_data: 
                    colors    = Color.objects.filter(id = data.color_id)
                    image_data = Image.objects.filter(product_color_id = data.id)
    
                    result.append({
                        "name"      : product.name,
                        "price"     : product.price,
                        "color"     : [color.name for color in colors],
                        "image_list": [image.image_url for image in image_data]
                    })

                return JsonResponse({"message":"Success", "result":result}, status = 200)

        except: 
            return JsonResponse({"error":"Value error"}, status = 400)

class ColorDetailView(View): 
    def get(self, request, product_name,color_name): 
        try: 
            result  = []

            color                   = Color.objects.get(name = color_name)
            product                 = Product.objects.get(name = product_name)
            images                  = Image.objects.filter(product_color_id = color.id)
            product_color_data      = ProductColor.objects.filter(color_id = color.id , product_id = product.id)
            
            if not product_color_data:
                return JsonResponse({"error":"Product does not exist"}, status = 400)

            if not images: 
                return JsonResponse({"message":"Does not exist"}, status = 401)

            for products in product_color_data: 
                result.append({
                    "name"      : products.product.name,
                    "price"     : product.price,
                    "color"     : products.color.name,
                    "image_list": [image.image_url for image in images]
                })
            
            return JsonResponse({"message":"Success", "result" : result}, status=200)

        except: 
            return JsonResponse({"error":"Not found"}, status = 404)
 
class SearchView(View): 
    def get(self, request): 
        try: 
            result        = []
            category_data = Category.objects.all()
            for category in category_data: 
                product_data = Product.objects.filter(category_id=category.id)
                res          = []
                for product in product_data: 
                    productcolor_data = ProductColor.objects.filter(product_id = product.id)
                    for color in productcolor_data: 
                        images = Image.objects.filter(product_color_id = color.id)
                        color  = [Color.objects.get(id=color.color_id).name]
                        res.append({
                            "name" : product.name,
                            "price": product.price,
                            "color": color,
                            "image": [image.image_url for image in images]
                        })
                result.append({
                    "category": category.id,
                    "product" : res
                })
                
            return JsonResponse({"message":"Success",'result':result}, status = 200)

        except Image.DoesNotExist: 
            return JsonResponse({"message":"Image does not exist"}, status = 401)

        except: 
            return JsonResponse({"error":"Not found"}, status = 404)
