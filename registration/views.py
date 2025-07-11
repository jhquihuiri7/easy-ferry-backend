from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.conf import settings
import json
from django.utils import timezone

from registration.models import RegistrationToken

@csrf_exempt  # Solo si no estás usando el token CSRF (por ejemplo, para peticiones desde frontend JS)
def request_registration_token(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed."}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
    except Exception:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    if not email:
        return JsonResponse({"error": "Email is required."}, status=400)

    # Elimina tokens anteriores del mismo email (opcional)
    RegistrationToken.objects.filter(email=email).delete()

    # Crea un nuevo token
    token_obj = RegistrationToken.objects.create(email=email)

    # Construye el link de verificación
    verification_url = f"https://tu-frontend.com/registro/verificar?token={token_obj.token}"

    # Envía el correo
    send_mail(
        subject="Verifica tu correo",
        message=f"Haz clic aquí para completar tu registro: {verification_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    return JsonResponse({"message": "Correo enviado con el enlace de verificación."})


def validate_registration_token(request):
    token = request.GET.get("token")

    if not token:
        return JsonResponse({"error": "Token is required."}, status=400)

    try:
        token_obj = RegistrationToken.objects.get(token=token)
    except RegistrationToken.DoesNotExist:
        return JsonResponse({"valid": False, "message": "Token not found."}, status=404)

    if token_obj.used:
        return JsonResponse({"valid": False, "message": "Token has already been used."}, status=400)

    if token_obj.expires_at < timezone.now():
        return JsonResponse({"valid": False, "message": "Token has expired."}, status=400)

    # ✅ Token is valid
    return JsonResponse({"valid": True, "email": token_obj.email})
