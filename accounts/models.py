from django.db import models

from django.contrib.auth.models import User

class TopBuyers(User):
    class Meta:
        proxy = True
        verbose_name = "User with the most movies purchased"
        verbose_name_plural = "User with the most movies purchased"
                
