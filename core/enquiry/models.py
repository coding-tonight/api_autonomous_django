from django.db import models
from app.models import Base
# Create your models here.


class Enquiry(Base):
    full_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=20)
    contact = models.CharField(max_length=14)
    message = models.TextField(max_length=200)

    class Meta:
        db_table = 'enquiry'
