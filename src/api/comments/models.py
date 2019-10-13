"""Comments model"""
from django.db import models

from api.users.models import CustomUser as User
from api.blogs.models import Blog
from helpers.base_model import BaseModel

class Comments(BaseModel):
    """The class to generate tables for the comments"""
    body = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)