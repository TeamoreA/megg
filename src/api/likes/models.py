"""Blog models"""
from django.db import models
from django.conf import settings

from api.users.models import CustomUser as User
from api.blogs.models import Blog
from helpers.base_model import BaseModel


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='likes', on_delete=models.CASCADE)
