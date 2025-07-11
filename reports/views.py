from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reports.models import Sale, User, Business, Credential
from authentication.models import Owner, Crew
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist

#from . import utils
import uuid
import json


from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from django.utils.dateparse import parse_date
from reports.pdf_report import generate_daily_report
from datetime import datetime

@csrf_exempt
def save_data(request):
    if request.method == "POST":
        # Crear nueva venta
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        try:
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
                status=data["status"],
                payed=data["payed"],
                payment=data["payment"]
            )
            
            return JsonResponse({"answer": sale.id}, status=201)  # 201 para creación exitosa
            
        except ObjectDoesNotExist as e:
            return JsonResponse({"error": str(e)}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "PUT":
        # Actualizar venta existente
        try:
            data = json.loads(request.body)
            if "id" not in data:
                return JsonResponse({"error": "ID is required for update"}, status=400)
                
            try:
                sale = Sale.objects.get(id=data["id"])
                user_instance = Credential.objects.get(email=data["seller_email"])
                seller_instance = User.objects.get(id=user_instance.id)
                business_instance = Business.objects.get(business=data["business"])
                
                # Actualizar todos los campos
                sale.business_id = business_instance
                sale.name = data["name"]
                sale.age = data["age"]
                sale.price = data["price"]
                sale.route = data["route"]
                sale.time = data["time"]
                sale.ferry = data["ferry"]
                sale.intermediary = data["intermediary"]
                sale.seller = seller_instance
                sale.date = data["date"]
                sale.notes = data["notes"]
                sale.passport = data["passport"]
                sale.phone = data["phone"]
                sale.status = data["status"]
                sale.payed = data["payed"]
                sale.payment = data["payment"]
                
                sale.save()
                
                return JsonResponse({"answer": "Sale updated successfully"}, status=200)
                
            except Sale.DoesNotExist:
                return JsonResponse({"error": "Sale not found"}, status=404)
            except ObjectDoesNotExist as e:
                return JsonResponse({"error": str(e)}, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    else:   
        return HttpResponse("Método inválido, solo POST o PUT requests", status=405)

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
        sales = Sale.objects.filter(business_id=business_instance.id, time=time, date=date).order_by('created_at')

        buffer = generate_daily_report(sales, date, time)
        current_time = datetime.now().strftime("%H-%M")
        filename = f"{business} {time} {date} {current_time}.xlsx"
        filename = (
            filename.strip()
            .replace('\n', '')
            .replace('\r', '')
            .replace('"', '')
            )

        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Access-Control-Allow-Origin'] = '*'
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
                'price':sale.price,
                'intermediary': sale.intermediary,
                'date': sale.date.strftime('%Y-%m-%d'),
                'seller': f"{sale.seller.first_name} {sale.seller.last_name}" if sale.seller else None,
                'passport':sale.passport,
                'phone':sale.phone,
                'status':sale.status,
                'notes':sale.notes,
                'payed':"Si" if sale.payed else "No",
                'payment':sale.payment
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
                'price':sale.price,
                'intermediary': sale.intermediary,
                'date': sale.date.strftime('%Y-%m-%d'),
                'seller': f"{sale.seller.first_name} {sale.seller.last_name}" if sale.seller else None,
                'passport':sale.passport,
                'phone':sale.phone,
                'status':sale.status,
                'notes':sale.notes,
                'payed':"Si" if sale.payed else "No",
                'payment':sale.payment
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


@csrf_exempt  # Only needed if making POST/PUT/DELETE requests
def get_owner(request):
    if request.method != "GET":
        return JsonResponse({
            'status': 'error',
            'message': 'Only GET requests are allowed'
        }, status=405)
    
    try:
        business = request.GET.get("business")
        business_instance = Business.objects.get(business=business)
        owner = Owner.objects.get(business_id=business_instance.id)
        data = {
                'id': owner.id,
                'business': owner.business_id,
                'name': owner.name,
                'ruc': owner.ruc,
                'phone': owner.phone,
                'email': owner.email
            }
        return JsonResponse(data)
    
    except Owner.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Owner not found for this business'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

import json

@csrf_exempt
def update_owner(request):
    if request.method != "POST":
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed'
        }, status=405)
    
    try:
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        
        # Get the owner ID from parsed data
        business = data.get("business")
        
        # Get the owner instance
        business_instance = Business.objects.get(business=business)
        owner = Owner.objects.get(business=business_instance.id)
        
        # Update only these allowed fields
        allowed_fields = ['name', 'ruc', 'phone', 'email']
        updated_fields = []
        
        for field in allowed_fields:
            if field in data:  # Changed from request.POST to data
                setattr(owner, field, data[field])  # Direct access to data
                updated_fields.append(field)
        
        # Save only if there were actual updates
        if updated_fields:
            owner.save()
        
        # Return the updated owner data
        response_data = {
            'id': owner.id,
            'business': owner.business_id,
            'name': owner.name,
            'ruc': owner.ruc,
            'phone': owner.phone,
            'email': owner.email,
            'status': 'success',
            'message': f'Owner updated successfully. Updated fields: {", ".join(updated_fields)}' if updated_fields else 'No fields were updated'
        }
        return JsonResponse(response_data)
    
    except Owner.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Owner not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
@csrf_exempt
def get_crew(request):
    if request.method != "GET":
        return JsonResponse({
            'status': 'error',
            'message': 'Only GET requests are allowed'
        }, status=405)
    
    try:
        business = request.GET.get("business")
        if not business:
            return JsonResponse({
                'status': 'error',
                'message': 'Business parameter is required'
            }, status=400)
        
        business_instance = Business.objects.get(business=business)
        crew = Crew.objects.get(business_id=business_instance.id)
        data = {
            'id': crew.id,
            'business': crew.business_id,
            # 1. Boat capacities
            'crew_capacity': crew.crew_capacity,
            'passenger_capacity': crew.passenger_capacity,
            # 2. Responsible person
            'responsible_name': crew.responsible_name,
            'responsible_passport': crew.responsible_passport,
            'responsible_phone': crew.responsible_phone,
            'responsible_email': crew.responsible_email,
            # 3. Captain
            'captain_name': crew.captain_name,
            'captain_passport': crew.captain_passport,
            # 4. Sailor 1 (only if exists)
            'sailor1_name': crew.sailor1_name if crew.sailor1_name else None,
            'sailor1_passport': crew.sailor1_passport if crew.sailor1_passport else None,
            # 5. Sailor 2 (only if exists)
            'sailor2_name': crew.sailor2_name if crew.sailor2_name else None,
            'sailor2_passport': crew.sailor2_passport if crew.sailor2_passport else None,
            'ferry_registration': crew.ferry_registration if crew.ferry_registration else None
        }
        return JsonResponse(data)
    
    except Crew.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Crew not found for this business'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def update_crew(request):
    if request.method != "POST":
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed'
        }, status=405)
    
    try:
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)

        # Get the owner ID from parsed data
        business = data.get("business")
        
        # Get the owner instance
        business_instance = Business.objects.get(business=business)
        # Get the crew instance
        crew = Crew.objects.get(business=business_instance.id)
        
        # Define all updatable fields
        updatable_fields = {
            # Boat capacities
            'crew_capacity': int,
            'passenger_capacity': int,
            # Responsible person
            'responsible_name': str,
            'responsible_passport': str,
            'responsible_phone': str,
            'responsible_email': str,
            # Captain
            'captain_name': str,
            'captain_passport': str,
            # Sailors
            'sailor1_name': str,
            'sailor1_passport': str,
            'sailor2_name': str,
            'sailor2_passport': str,
            'ferry_registration': str
        }
        
        updated_fields = []
        
        # Update each field if it exists in the request data
        for field, field_type in updatable_fields.items():
            if field in data:
                value = data[field]
                if value is not None:
                    try:
                        setattr(crew, field, field_type(value))
                    except (ValueError, TypeError):
                        return JsonResponse({
                            'status': 'error',
                            'message': f'Invalid value type for {field}'
                        }, status=400)
                else:
                    setattr(crew, field, None)
                updated_fields.append(field)
        
        # Save only if there were actual updates
        if updated_fields:
            crew.save()
        
        # Return the updated crew data
        response_data = {
            'id': crew.id,
            'business': crew.business_id,
            'crew_capacity': crew.crew_capacity,
            'passenger_capacity': crew.passenger_capacity,
            'responsible_name': crew.responsible_name,
            'responsible_passport': crew.responsible_passport,
            'responsible_phone': crew.responsible_phone,
            'responsible_email':crew.responsible_email,
            'captain_name': crew.captain_name,
            'captain_passport': crew.captain_passport,
            'sailor1_name': crew.sailor1_name,
            'sailor1_passport': crew.sailor1_passport,
            'sailor2_name': crew.sailor2_name,
            'sailor2_passport': crew.sailor2_passport,
            'ferry_registration':crew.ferry_registration,
            'status': 'success',
            'message': f'Updated fields: {", ".join(updated_fields)}' if updated_fields else 'No fields updated'
        }
        return JsonResponse(response_data)
    
    except Crew.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Crew not found with this ID'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)