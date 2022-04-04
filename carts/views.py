import json

from django.http  import JsonResponse
from django.views import View

from carts.models    import Cart
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
            product_color_id = ProductColor.objects.get(product_id = product_id, color_id = color_id)
            inventory        = product_color_id.inventory
            
            if quantity <= 0:
                return JsonResponse({'message' : 'Quantity must be positive number'}, status=400)
            
            if quantity > inventory:
                return JsonResponse({'message' : 'Quantity cannot be more than inventory'}, status=400)
            
            if not Cart.objects.filter(
                user = user,
                product_color = product_color_id).exists():
                Cart.objects.create(
                    user          = user,
                    product_color = product_color_id,
                    quantity      = quantity
                )
                return JsonResponse({'message' : 'Cart created'}, status=201)
            
            cart           = Cart.objects.get(user = user, product_color = product_color_id)
            cart.quantity += quantity
            cart.save()
            return JsonResponse({'message' : 'Cart upgraded'}, status=200)
        except ProductColor.DoesNotExist:
            return JsonResponse({'message' : 'Product does not exist'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'Key error'}, status=400)
    
    @login_authorization
    def get(self, request):
        user      = request.user
        cart_data = Cart.objects.filter(user = user)            
        
        if not cart_data.exists():
            return JsonResponse({'message' : 'Cart does not exist'}, status=401)

        result = [{
            'cart_id'      : cart.id,
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
    def patch(self, request):
        try:
            data      = json.loads(request.body)
            user      = request.user
            cart_id   = request.GET.get('id')
            quantity  = data['quantity']
            cart      = Cart.objects.get(id = int(cart_id))
            inventory = cart.product_color.inventory

            if not cart_id:
                return JsonResponse({'message' : 'Url path is wrong'}, status=400)

            if quantity <= 0:
                return JsonResponse({'message' : 'Quantity must be positive number'}, status=400)
            
            if quantity > inventory:
                return JsonResponse({'message' : 'Quantity cannot be more than inventory'}, status=400)
            
            cart          = Cart.objects.get(user = user, id = cart_id)
            cart.quantity = quantity
            cart.save()
            
            return JsonResponse({
                'message' : 'Quantity changed',
                'quantity': cart.quantity
                }, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'Cart does not exist'}, status=400)  
        except KeyError:
            return JsonResponse({'message' : 'Key error'}, status=400)

    @login_authorization
    def delete(self, request):
        try:
            user = request.user
            cart_id_list = request.GET.getlist('id')

            if not cart_id_list:
                return JsonResponse({'message' : 'Cart does not exist'}, status=400)

            for cart_id in cart_id_list:
                cart = Cart.objects.get(user = user, id = cart_id)
                cart.delete()
            return JsonResponse({'message' : 'Cart deleted'}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'Cart does not exist'}, status=400)
    