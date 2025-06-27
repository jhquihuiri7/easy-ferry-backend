from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reports.models import Sale, User, Business, Credential
from django.db.models import F, Value
from django.db.models.functions import Concat

#from . import utils
import uuid
import json


from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from django.utils.dateparse import parse_date
from reports.pdf_report import generate_daily_report

@csrf_exempt
def save_data(request):
    if request.method == "PUT":

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        user_instance = Credential.objects.get(email=data["seller_email"])
        seller_instance = User.objects.get(id=user_instance.id)
        business_instance = Business.objects.get(business=data["business"])
        sale = Sale.objects.create(
            business_id=business_instance,
            name=data["name"],
            age=data["age"],
            price=data["price"],
            route=data["route"],
            time=data["time"],
            ferry=data["ferry"],
            intermediary=data["intermediary"],
            seller=seller_instance,
            date=data["date"],
            notes=data["notes"],
            passport=data["passport"],
            phone=data["phone"],
            status=data["status"]
        )
        
        return JsonResponse({"answer":sale.id}, status=200)
    else:   
        return HttpResponse("Methodo invalido, solo POST requests", status=405)

@csrf_exempt
def generate_marine_report(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            business = data.get("business")  # O el nombre del campo que esperas
            time = data.get("time")
            date = data.get("date")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        business_instance = Business.objects.get(business=business)
        sales = Sale.objects.filter(business_id=business_instance.id, time=time, date=date)
        print(sales)
        buffer = generate_daily_report(sales)

        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="reporte_diario.xlsx"'
        return response
    else:   
        return HttpResponse("Methodo invalido, solo POST requests", status=405)
    
@csrf_exempt
def get_sells_data(request):
    if request.method == "GET":
        try:
            business = request.GET.get("business")
            start_date = request.GET.get("start_date")
            end_date = request.GET.get("end_date")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        start_date_obj = parse_date(start_date) if start_date else None
        end_date_obj = parse_date(end_date) if end_date else None

        business_instance = Business.objects.get(business=business)
        data = [
            {
                'id': sale.id,
                'name': sale.name,
                'age': sale.age,
                'route': sale.route,
                'time': sale.time,
                'ferry': sale.ferry,
                'intermediary': sale.intermediary,
                'date': sale.date.strftime('%Y-%m-%d'),
                'seller': f"{sale.seller.first_name} {sale.seller.last_name}" if sale.seller else None,
                'passport':sale.passport,
                'phone':sale.phone,
                'status':sale.status
            }
            for sale in Sale.objects.filter(
                business_id=business_instance.id,
                date__range=(start_date_obj, end_date_obj)
            ).exclude(ferry=business_instance.ferry).select_related('seller') 
        ]
        sales_list = list(data)
        return JsonResponse({"data": sales_list})
    else:   
        return HttpResponse("Methodo invalido, solo POST requests", status=405)


@csrf_exempt
def get_sells_ferry(request):
    if request.method == "GET":
        try:
            business = request.GET.get("business")
            start_date = request.GET.get("start_date")
            end_date = request.GET.get("end_date")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        start_date_obj = parse_date(start_date) if start_date else None
        end_date_obj = parse_date(end_date) if end_date else None

        business_instance = Business.objects.get(business=business)
        data = [
            {
                'id': sale.id,
                'name': sale.name,
                'age': sale.age,
                'route': sale.route,
                'time': sale.time,
                'ferry': sale.ferry,
                'intermediary': sale.intermediary,
                'date': sale.date.strftime('%Y-%m-%d'),
                'seller': f"{sale.seller.first_name} {sale.seller.last_name}" if sale.seller else None,
                'passport':sale.passport,
                'phone':sale.phone,
                'status':sale.status
            }
            for sale in Sale.objects.filter(
                business_id=business_instance.id,
                date__range=(start_date_obj, end_date_obj),
                ferry=business_instance.ferry
            ).select_related('seller') 
        ]
        sales_list = list(data)
        return JsonResponse({"data": sales_list})
    else:   
        return HttpResponse("Methodo invalido, solo POST requests", status=405)

@csrf_exempt  # Quita esto si manejas CSRF de otra forma
def delete_sales(request):
    if request.method != "POST":
        return HttpResponse("Methodo invalido, solo POST requests", status=405)
    
    try:
        data = json.loads(request.body)
        ids = data.get("ids", [])
        
        if not isinstance(ids, list) or not all(isinstance(i, int) for i in ids):
            return HttpResponse("Invalid 'ids' format. Must be a list of integers.", status=405)
        
        deleted_count, _ = Sale.objects.filter(id__in=ids).delete()
        
        return JsonResponse({"deleted_count": deleted_count})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt  # Solo si no manejas CSRF de otra forma
def update_sale(request):
    if request.method != "POST":
        return HttpResponse("Methodo invalido, solo POST requests", status=405)
    
    try:
        data = json.loads(request.body)
        sale_id = data.get("id")
        if not sale_id:
            return HttpResponse("Missing 'id' in request data.", status=405)
        
        # Obtener el registro a actualizar
        try:
            sale = Sale.objects.get(id=sale_id)
        except Sale.DoesNotExist:
            raise HttpResponse("Sale not found.", status=404)
        
        # Aquí define los campos que puedes actualizar
        allowed_fields = ["name", "age", "route", "time", "ferry", "intermediary"]
        updated = False
        
        for field in allowed_fields:
            if field in data:
                setattr(sale, field, data[field])
                updated = True
        
        if updated:
            sale.save()
            return JsonResponse({"message": "Sale updated successfully."})
        else:
            return HttpResponse("No valid fields to update were provided.",status=405)
    
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON.", status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)