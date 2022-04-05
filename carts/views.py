import json

from django.http  import JsonResponse
from django.views import View
from django.forms import ValidationError

from carts.models    import Cart
from carts.validator import validate_zero_quantity, validate_total_quantity
from products.models import ProductColor, Image
from cores.decorator import login_authorization

class CartView(View):
    @login_authorization
    def post(self, request):
        try:
            data             = json.loads(request.body)
            user             = request.user
            product_id       = data['product_id']
            color_id         = data['color_id']
            quantity         = data['quantity']
            product_color    = ProductColor.objects.get(product_id = product_id, color_id = color_id)
            inventory        = product_color.inventory
            
            validate_zero_quantity(quantity)
            
            cart, is_created  = Cart.objects.get_or_create(
                user          = user,
                product_color = product_color,
                defaults      = {'quantity' : 0}
            )
            cart.quantity += quantity
            
            validate_total_quantity(cart.quantity, inventory)
            
            cart.save()
            
            if is_created:
                return JsonResponse({'message' : 'Cart created'}, status=200)
            else:
                return JsonResponse({'message' : 'Cart updated'}, status=200)
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
        
        if not cart_data.exists():
            return JsonResponse({'result' : []}, status=404)

        result = [{
            'cart_id'      : cart.id,
            'category_name': cart.product_color.product.category.name,
            'quantity'     : cart.quantity,
            'product_name' : cart.product_color.product.name,
            'product_price': cart.product_color.product.price,
            'color_name'   : cart.product_color.color.name,
            'image_url'    : Image.objects.get(
                            product_color_id = cart.product_color.id,
                            sequence = 1).image_url
        } for cart in cart_data]
        
        return JsonResponse({'result' : result}, status=200)

    @login_authorization
    def patch(self, request, cart_id):
        try:
            data      = json.loads(request.body)
            user      = request.user
            quantity  = data['quantity']
            cart      = Cart.objects.get(user = user, id = int(cart_id))
            inventory = cart.product_color.inventory

            if not cart_id:
                return JsonResponse({'message' : 'Url path is wrong'}, status=400)

            validate_zero_quantity(quantity)
            
            cart.quantity = quantity
            
            validate_total_quantity(cart.quantity, inventory)
            
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
        user = request.user
        cart_id_list = request.GET.getlist('id')
        
        if not cart_id_list:
            return JsonResponse({'message' : 'Cart does not exist'}, status=400)
        
        cart = Cart.objects.filter(user = user, id__in = cart_id_list)
        
        if not cart:
            return JsonResponse({'message' : 'Cart does not exist'}, status=400)
        
        cart.delete()
        
        return JsonResponse({'message' : 'Cart deleted'}, status=200)
