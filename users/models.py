from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


ORDINARY_USER, ADMIN = ('ordinary_user','admin')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')

class CustomUser(AbstractUser):
    USER_ROLES=(
        (ORDINARY_USER,ORDINARY_USER),
        (ADMIN,ADMIN)
    )
    USER_AUTH_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    )
    user_role = models.CharField(max_length=20,choices=USER_ROLES,default=ORDINARY_USER)
    email=models.EmailField(unique=True,null=True,blank=True)
    phone=models.CharField(max_length=20,blank=True,null=True,unique=True)
    user_auth_type=models.CharField(max_length=30,choices=USER_AUTH_TYPE,default=VIA_EMAIL)
    photo = models.ImageField(upload_to='users/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'heic'])])

    def __str__(self):
        return self.username

