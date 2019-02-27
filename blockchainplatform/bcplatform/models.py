from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class BlockchainUser(models.Model):
    USER_TYPE_CHOICES = (
        ('bcadmin', "Blockchain Admin"),
        ('bcmember', "Blockchain Member"),
        ('simpleuser', "Simple User"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=16, choices=USER_TYPE_CHOICES)

