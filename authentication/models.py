from django.db import models
from reports.models import Business

class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, default="")
    ruc = models.CharField(max_length=13, default="")
    phone = models.CharField(max_length=15, default="")
    email = models.EmailField(default="")

    def __str__(self):
        return f"{self.name} (RUC: {self.ruc})"

    class Meta:
        db_table = 'owner'

class Crew(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE
    )
    # 1. Capacidades del barco
    crew_capacity = models.PositiveIntegerField(default=0)
    passenger_capacity = models.PositiveIntegerField(default=0)

    # 2. Responsable del Embarque
    responsible_name = models.CharField(max_length=100, default="")
    responsible_passport = models.CharField(max_length=20, default="")
    responsible_phone = models.CharField(max_length=15, default="")
    responsible_email = models.EmailField(default="")

    # 3. Capitán (datos adicionales)
    captain_name = models.CharField(max_length=100, default="")
    captain_passport = models.CharField(max_length=20, default="")

    # 4. Marinero 1 (opcional, si siempre hay al menos uno)
    sailor1_name = models.CharField(max_length=100, blank=True, null=True, default="")
    sailor1_passport = models.CharField(max_length=20, blank=True, null=True, default="")

    # 5. Marinero 2 (opcional)
    sailor2_name = models.CharField(max_length=100, blank=True, null=True, default="")
    sailor2_passport = models.CharField(max_length=20, blank=True, null=True, default="")

    sailor2_passport = models.CharField(max_length=20, blank=True, null=True, default="")

    ferry_registration = models.CharField(max_length=20, blank=True, null=True, default="")

    def __str__(self):
        return f"Tripulación de {self.responsible_name} (Capacidad: {self.passenger_capacity} pasajeros)"

    class Meta:
        db_table = 'crew'
        managed = True
