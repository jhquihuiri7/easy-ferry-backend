from django.db import models
from django.utils import timezone
from reports.models import Business

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now,)
    
    class Meta:
        managed = True
        db_table = 'notifications'
        ordering = ['-date']  # Ordenar por fecha descendente por defecto
    
    def __str__(self):
        return f"Notificación para {self.business} - {self.date.strftime('%Y-%m-%d')}"