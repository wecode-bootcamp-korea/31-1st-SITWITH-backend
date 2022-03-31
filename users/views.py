import json, bcrypt, jwt

from datetime import datetime, timedelta

from django.forms import ValidationError
from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models       import User
from users.validator    import validate_username, validate_password, validate_email

class SignUpView(View):
    def post(self, request):
        try: 
            data           = json.loads(request.body)
            input_username = data['username']
            input_password = data['password']
            input_email    = data['email']
            
            validate_username(input_username)
            validate_password(input_password)
            validate_email(input_email)
            
            if User.objects.filter(username = input_username).exists():
                return JsonResponse({'message' : 'Username already exists'}, status=409)
            
            if input_email == "" :
                pass
            elif User.objects.filter(email = input_email).exists():
                return JsonResponse({'message' : 'Email already exists'}, status=409)

            hashed_password = bcrypt.hashpw(input_password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                username = input_username,
                password = hashed_password,
                email    = input_email,
            )
            
            return JsonResponse({'message' : 'Success'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'Key error'}, status=400)
        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            input_username = data['username']
            input_password = data['password']
            user           = User.objects.get(username = input_username)
            
            if not bcrypt.checkpw(input_password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'Password does not match'}, status=401)
            
            access_token = jwt.encode({'id':user.id, 'exp':datetime.utcnow()+timedelta(days=3)}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return JsonResponse({'token' : access_token}, status=200)
            
        except User.DoesNotExist:
            return JsonResponse({'message' : 'User does not exist'}, status=401)
        
        except KeyError:
            return JsonResponse({'message' : 'Key error'}, status=400)