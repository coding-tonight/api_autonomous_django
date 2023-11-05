from django.db import models
from app.models import Base

# Create your models here.


class Clients(Base):
    client_name = models.CharField(max_length=45)
    logo_url = models.ImageField(
        null=False, blank=False, upload_to='uploads/clients/')

    class Meta:
        db_table = 'clients'
