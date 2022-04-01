import jwt

from django.http import JsonResponse
from django.conf import settings

from users.models import User

def login_authorization(func):
    def wrapper(self, request, *args, **kwargs) :
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(
                                access_token,
                                settings.SECRET_KEY,
                                algorithms=settings.ALGORITHM
                            )
            user         = User.objects.get(id = payload['id'])
            request.user = user
            return func(self, request, *args, **kwargs)
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'Invalid token'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'Invalid user'}, status=400)
        
    
    return wrapper