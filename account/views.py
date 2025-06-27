from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Notification,Business
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  
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
                'id':notif.id,
                'message': notif.message,
                'date': notif.date.strftime('%Y-%m-%d'),
                'read': notif.read
            }
            for notif in notifications
        ]
        
        return JsonResponse({"notifications":data}, status=200, encoder=DjangoJSONEncoder)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt  
def mark_read_notification(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        
        if not notification_id:
            return JsonResponse({
                'success': False,
                'error': 'notification_id is required in the request body'
            }, status=400)
        
        # Get the notification and update its read status
        notification = Notification.objects.get(id=notification_id)
        notification.read = True
        notification.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Notification {notification_id} marked as read'
        }, status=200)
    
    except Notification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Notification not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)