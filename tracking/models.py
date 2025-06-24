from django.db import models
from django.utils import timezone
from reports.models import Business

class Coordinates(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='coordinates')
    lat = models.FloatField()
    long = models.FloatField()
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'coordinates'
        managed = True
        ordering = ['-time']

    def __str__(self):
        return f"{self.business.name} - ({self.lat}, {self.long})"
