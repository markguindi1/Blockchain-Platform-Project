from django.db import models
from django.contrib.auth.models import User


class BlockchainUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return f"<BlockchainUser: {self.user.username}>"
