import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

class RegistrationToken(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # El token expira 24 horas después de su creación
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_valid(self):
        """Verifica si el token es válido"""
        return not self.used and timezone.now() < self.expires_at

    def __str__(self):
        return f"Token for {self.email} - Used: {self.used}"
    
    class Meta:
        db_table = 'registration_token'
        managed = True
