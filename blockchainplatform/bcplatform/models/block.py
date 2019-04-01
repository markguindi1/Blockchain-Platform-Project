from django.db import models
import datetime
from hashlib import sha256

class Block(models.Model):
    data = models.TextField(max_length=255)
    index = models.IntegerField(blank=True)
    timestamp = models.DateTimeField()
    previous_hash = models.CharField(max_length=255)
    nonce = models.CharField(max_length=255)
    hash = models.CharField(max_length=255, blank=True)
    chain = models.ForeignKey('Blockchain', on_delete=models.CASCADE)

    def __str__(self):
        return f"Block # {self.index}"

    def __repr__(self):
        return str(self)

    def generate_hash(self):
        block_header = f"{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        block_hash = sha256(block_header.encode())
        return block_hash.hexdigest()

    def print_block(self):
        pass
