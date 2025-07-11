"""
URL configuration for easy_ferry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reports.views import *
from authentication.views import *
from account.views import *
from tracking.views import *
from registration.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales', save_data),
    path('marine-report', generate_marine_report),
    path('get-sales', get_sells_data),
    path('get-sales-ferry', get_sells_ferry),
    path('get-owner', get_owner),
    path('get-crew', get_crew),
    path('update-owner', update_owner),
    path('update-crew', update_crew),
    path('login', login),
    path('refresh', refresh_token),
    path('register', register_user),
    path('delete-sales', delete_sales),
    path('update-sale', update_sale),
    path('get-notifications', business_notifications),
    path('get-coordinates', get_coordinates),
    path('save-coordinates', save_coordinates),
    path('mark-as-read-notifications', mark_read_notification),
    path("registrar-token", request_registration_token),
    path("validar-token", validate_registration_token),
]
