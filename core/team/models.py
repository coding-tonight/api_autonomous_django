from django.db import models
from app.models import Base

# Create your models here.


class Team(Base):
    member_name = models.CharField(max_length=45)
    position = models.CharField(max_length=45)
    image = models.CharField(null=False, blank=False, upload_to='uploads/team/')

    class Meta:
        db_table = 'team'

    def __str__(self):
        return self.member_name     
        