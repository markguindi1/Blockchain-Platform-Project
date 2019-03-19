from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class BlockchainUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_own_blockchains(self):
        pass

    def get_other_blockchains(self):
        pass


class Block(models.Model):
    data = models.TextField(max_length=255)
    index = models.IntegerField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) # Auto-sets the field to the time this object was created
    previous_hash = models.CharField(max_length=255)
    nonce = models.CharField(max_length=255)
    hash = models.CharField(max_length=255, blank=True)
    chain = models.ForeignKey('Blockchain', on_delete=models.CASCADE)


class Blockchain(models.Model):
    name = models.CharField(max_length=255, blank=False)
    admin = models.OneToOneField(BlockchainUser, on_delete=models.CASCADE, related_name='+')
    members = models.ManyToManyField(BlockchainUser, related_name='+')




