# views.py
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from reports.models import Business
from tracking.models import Coordinates

def get_coordinates(request):
    if request.method != "GET":
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)

    business = request.GET.get('business')
    if not business:
        return JsonResponse({'error': 'Missing business parameter.'}, status=400)

    try:
        business_instance = Business.objects.get(business=business)
    except Business.DoesNotExist:
        return JsonResponse({'error': 'Business not found.'}, status=404)

    # Obtener el tiempo límite: ahora menos 3 horas
    three_hours_ago = timezone.now() - timedelta(hours=3)

    # Filtrar coordenadas por tiempo
    coordinates = Coordinates.objects.filter(
        business=business_instance,
        time__gte=three_hours_ago
    ).order_by('-time')

    data = [
        {
            "lat": c.lat,
            "long": c.long,
            "time": c.time.isoformat(),
        }
        for c in coordinates
    ]

    return JsonResponse(data, safe=False)

def save_coordinates(request):
    if request.method != "GET":
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)

    lat = request.GET.get('lat')
    long = request.GET.get('long')
    business = request.GET.get('business')

    if not lat and not long and not business:
        return JsonResponse({'error': 'Missing business_id parameter.'}, status=400)

    business_instance = Business.objects.get(business=business)
    try:
        coordinates = Coordinates.objects.create(
            business = business_instance,
            lat=lat,
            long=long
        )
    except:
        return JsonResponse({"error":"Failed to save coordinate"}, safe=False)    

    return JsonResponse({"message":"success"}, safe=False)
