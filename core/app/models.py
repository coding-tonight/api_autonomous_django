import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


def uuid_generator():
    return uuid.uuid4().hex


class Base(models.Model):
    reference_id = models.CharField(default=uuid_generator(), max_length=32)
    created_at = models.DateTimeField(auto_now=False)
    created_by = models.ForeignKey(
        User, related_name="+", on_delete=models.PROTECT, db_column="created_by", null=True)
    updated_at = models.DateTimeField(auto_now=False, null=True)
    updated_by = models.ForeignKey(
        User, related_name="+", on_delete=models.PROTECT, db_column="updated_by", null=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ForgetPasswordOtp(models.Model):
    otp = models.CharField(max_length=32)
    email = models.EmailField(max_length=45)
    created_at = models.DateTimeField(auto_now=False)
