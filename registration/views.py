from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
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
        business = data.get("business")
    except Exception:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    if not email or not business:
        return JsonResponse({"error": "Email and Business are required."}, status=400)

    # Elimina tokens anteriores del mismo email (opcional)
    RegistrationToken.objects.filter(email=email).delete()

    # Crea un nuevo token
    token_obj = RegistrationToken.objects.create(email=email, business=business)

    # Construye el link de verificación
    verification_url = f"https://easy-ferry.vercel.app/register?token={token_obj.token}"

    subject = "Completa tu registro en Easy Ferry"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]

    # Renderiza el template HTML
    html_content = render_to_string("emails/registration_email.html", {
        "verification_url": verification_url,
    })

    # Alternativa en texto plano (opcional, recomendado)
    text_content = f"Haz clic en el siguiente enlace para completar tu registro: {verification_url}"

    # Crea y envía el correo
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


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
    return JsonResponse({"valid": True, "email": token_obj.email, "business": token_obj.business})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

from .models import RegistrationToken

@csrf_exempt
def use_token(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed."}, status=405)

    try:
        data = json.loads(request.body)
        token = data.get("token")
    except Exception:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    if not token:
        return JsonResponse({"error": "Token is required."}, status=400)

    try:
        token_obj = RegistrationToken.objects.get(token=token)
    except RegistrationToken.DoesNotExist:
        return JsonResponse({"success": False, "message": "Token not found."}, status=404)

    if token_obj.used:
        return JsonResponse({"success": False, "message": "Token has already been used."}, status=400)

    if token_obj.expires_at < timezone.now():
        return JsonResponse({"success": False, "message": "Token has expired."}, status=400)

    # Marcar como usado
    token_obj.used = True
    token_obj.save()

    return JsonResponse({"success": True, "message": "Token marked as used."})

from django.http import JsonResponse
from .models import RegistrationToken
from django.utils import timezone

def get_token_mail(request):
    token = request.GET.get("token")

    if not token:
        return JsonResponse({"error": "Token is required."}, status=400)

    try:
        token_obj = RegistrationToken.objects.get(token=token)
    except RegistrationToken.DoesNotExist:
        return JsonResponse({"error": "Token not found."}, status=404)

    if token_obj.expires_at < timezone.now():
        return JsonResponse({"error": "Token has expired."}, status=400)

    return JsonResponse({"email": token_obj.email})
