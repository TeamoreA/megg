from django.contrib.auth.models import AbstractUser
from helpers.base_model import BaseModel

class CustomUser(BaseModel, AbstractUser):
   pass
