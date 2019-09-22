"""Blog models"""
from django.db import models

from api.users.models import CustomUser as User
from helpers.base_model import BaseModel


class Blog(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField(blank=True)
    picture = models.CharField(blank=True, max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
