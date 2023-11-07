from django.db import models
from app.models import Base

# Create your models here.

class MetaData(Base):
    website_name = models.CharField(max_length=45)
    logo = models.ImageField(null=False, blank=False, upload_to='metdata/')
    email = models.EmailField(max_length=20)
    phone_number = models.CharField(max_length=14, null=True)
    landline_number = models.CharField(max_length=8, null=True)
    address_one = models.CharField(max_length=20, null=True)
    address_two = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.website_name

    class Meta:
        db_table = 'metadata'
