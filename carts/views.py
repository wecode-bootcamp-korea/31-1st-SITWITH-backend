import json

from django.http  import JsonResponse, HttpResponse
from django.views import View
from django.forms import ValidationError

from carts.models    import Cart
from carts.validator import validate_quantity
from cores.decorator import login_authorization
from products.models import ProductColor, Image

class CartView(View):
    @login_authorization
    def post(self, request):
        try:
            data            = json.loads(request.body)
            user            = request.user
            productcolor_id = data['productcolor_id']
            quantity        = data['quantity']
            product_color   = ProductColor.objects.get(id = productcolor_id)
            
            validate_quantity(quantity)
            
            cart, is_created  = Cart.objects.get_or_create(
                user          = user,
                product_color = product_color,
                defaults      = {'quantity' : 0}
            )
            cart.quantity += quantity
            cart.save()
            
            return HttpResponse(status=200)
        except ProductColor.DoesNotExist:
            return JsonResponse({'message' : 'Product does not exist'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'Key error'}, status=400)
        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status=400)

    @login_authorization
    def get(self, request):
        user      = request.user
        cart_data = Cart.objects.filter(user = user)            
        
        result = [{
            'cart_id'      : cart.id,
            'product_id'   : cart.product_color_id,
            'category_name': cart.product_color.product.category.name,
            'quantity'     : cart.quantity,
            'product_name' : cart.product_color.product.name,
            'product_price': cart.product_color.product.price,
            'color_name'   : cart.product_color.color.name,
            'image_url'    : Image.objects.get(
                                sequence         = 1,
                                product_color_id = cart.product_color.id
                             ).image_url
        } for cart in cart_data]
        
        return JsonResponse({'result' : result}, status=200)

    @login_authorization
    def patch(self, request, cart_id):
        try:
            data      = json.loads(request.body)
            user      = request.user
            quantity  = data['quantity']
            cart      = Cart.objects.get(user = user, id = int(cart_id))

            validate_quantity(quantity)
            
            cart.quantity = quantity
            cart.save()

            return JsonResponse({'quantity': cart.quantity}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'Cart does not exist'}, status=400)  
        except KeyError:
            return JsonResponse({'message' : 'Key error'}, status=400)
        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status=400)

    @login_authorization
    def delete(self, request):
        user         = request.user
        cart_id_list = request.GET.getlist('id')
        
        if not cart_id_list:
            return JsonResponse({'message' : 'Cart does not exist'}, status=400)
        
        cart = Cart.objects.filter(user = user, id__in = cart_id_list)
        cart.delete()
        
        return HttpResponse(status=204)
