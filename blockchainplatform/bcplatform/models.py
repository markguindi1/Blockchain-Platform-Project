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

    def generate_hash(self):
        pass

    def print_block(self):
        pass


class Blockchain(models.Model):
    name = models.CharField(max_length=255, blank=False)
    admin = models.OneToOneField(BlockchainUser, on_delete=models.CASCADE, related_name='+')
    members = models.ManyToManyField(BlockchainUser, related_name='+')
    # Without related name^^, throws error

    def genesis_block(self):
        pass

    def add_data(self, data):
        pass

    def is_chain_valid(self):
        pass

    def proof_of_work(self):
        pass

    def print_chain(self):
        pass


class DuplicateBlockchain(Blockchain):
    latest_valid_block_index = models.IntegerField(blank=True)

    def init_from_blockchain(self, blockchain):
        pass

    def alter_data(self, data, block_i):
        pass

    def recalculate_block_hashes(self):
        pass

