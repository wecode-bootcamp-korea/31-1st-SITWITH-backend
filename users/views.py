import json, bcrypt, jwt

from django.forms import ValidationError
from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models       import User
from users.validator    import username_validate, password_validate, email_validate

class SignUpView(View):
    def post(self, request):
        try: 
            data           = json.loads(request.body)
            input_username = data['username']
            input_password = data['password']
            input_email    = data['email']
            
            username_validate(input_username)
            password_validate(input_password)
            email_validate(input_email)
            
            if User.objects.filter(username = input_username).exists():
                return JsonResponse({'message' : 'Username already exists'}, status=401)
            
            if User.objects.filter(email = input_email).exists():
                return JsonResponse({'message' : 'Email already exists'}, status=401)

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
            
            access_token = jwt.encode({'id':user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return JsonResponse({'token' : access_token}, status=200)
            
        except User.DoesNotExist:
            return JsonResponse({'message' : 'User does not exist'}, status=401)
        
        except KeyError:
            return JsonResponse({'message' : 'Key error'}, status=400)