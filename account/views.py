from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Notification,Business
import json
from django.core.serializers.json import DjangoJSONEncoder

def business_notifications(request):
    
    # Validar que sea una petición GET
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    try:
        business_instance = Business.objects.get(business=request.GET.get("business"))
        notifications = Notification.objects.filter(business_id=business_instance.id).order_by('-date')
        
        # Preparar los datos para la respuesta
        data = [
            {
                'message': notif.message,
                'date': notif.date.strftime('%Y-%m-%d')
            }
            for notif in notifications
        ]
        
        return JsonResponse({"notifications":data}, status=200, encoder=DjangoJSONEncoder)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)