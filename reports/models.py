from django.db import models
from django.utils import timezone

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.CharField(max_length=255)
    ferry = models.CharField(max_length=255, default="")
    
    class Meta:
        db_table = 'business'
        managed = True

    def __str__(self):
        return self.business
    
class User(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    business_id = models.ForeignKey('Business', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Credential(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='credentials')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'credentials'

    def __str__(self):
        return self.email

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    business_id = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='business_id', default=1)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    price = models.PositiveIntegerField(default=0)
    route = models.CharField(max_length=50)
    time = models.CharField(max_length=10)
    ferry = models.CharField(max_length=50)
    intermediary = models.CharField(max_length=50, default='Oficina')
    date = models.DateField(default=timezone.now)
    seller = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='sales')
    notes = models.CharField(max_length=200, default='')
    passport = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    status = models.CharField(max_length=50, default='Residente')
    payed = models.BooleanField(default=False)
    payment = models.CharField(max_length=50, default='')
    mail = models.CharField(max_length=50, default='')

    class Meta:
        db_table = 'sales'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.route})"

