from django.shortcuts import render
from reports.models import Credential, User, Business
from authentication.models import Owner, Crew

# views.py
import jwt
import datetime
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.contrib.auth.hashers import check_password, make_password



@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Datos inválidos'}, status=400)

    try:
        cred = Credential.objects.get(email=email)
    except Credential.DoesNotExist:
        return JsonResponse({'error': 'Credenciales inválidas'}, status=401)

    if check_password(password, cred.password):
        payload = {
            'user_id': cred.user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
            'iat': datetime.datetime.now(datetime.timezone.utc),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        try:
            user = User.objects.get(id=cred.user.id)
            data = {
                'name': user.first_name + " " + user.last_name,
                'email':email,
                'business': user.business_id.business,
                'token':token  
            }
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
    

@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({'error': 'Datos inválidos o incompletos'}, status=400)

    # Validar si ya existe ese email
    if Credential.objects.filter(email=email).exists():
        return JsonResponse({'error': 'El email ya está registrado'}, status=409)
    
    business_instance = Business.objects.get(id=int(data["business_id"]))

    # Crear usuario
    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        business_id=business_instance
    )

    # Crear credencial con contraseña hasheada
    Credential.objects.create(
        user=user,
        email=email,
        password=make_password(password)
    )
    
    return JsonResponse({'message': 'Usuario creado exitosamente', 'user_id': user.id}, status=201)

@csrf_exempt
def refresh_token(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        token = data.get('token')
        
        if not token:
            return JsonResponse({'error': 'Token no proporcionado'}, status=400)
            
        try:
            # Decodificar el token (tanto para token normal como refresh token)
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # Verificar si el token está expirado (excepto si es un refresh token)
            current_time = datetime.datetime.now(datetime.timezone.utc)
            expiration_time = datetime.datetime.fromtimestamp(payload['exp'], tz=datetime.timezone.utc)
            
            # Si es un token normal (no refresh) y está expirado, rechazar
            if not payload.get('refresh') and expiration_time < current_time:
                return JsonResponse({'error': 'Token expirado'}, status=401)
                
            # Crear nuevo refresh token (2 semanas de expiración)
            refresh_payload = {
                'user_id': payload['user_id'],
                'exp': current_time + datetime.timedelta(weeks=2),
                'iat': current_time,
                'refresh': True  # Marcar como refresh token
            }
            new_refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
            
            return JsonResponse({
                'refresh_token': new_refresh_token
            }, status=200)
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expirado'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Token inválido'}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos'}, status=400)