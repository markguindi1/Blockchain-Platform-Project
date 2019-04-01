from django.db import models

class Block(models.Model):
    data = models.TextField(max_length=255)
    index = models.IntegerField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) # Auto-sets the field to the time this object was created
    previous_hash = models.CharField(max_length=255)
    nonce = models.CharField(max_length=255)
    hash = models.CharField(max_length=255, blank=True)
    chain = models.ForeignKey('Blockchain', on_delete=models.CASCADE)

    def __str__(self):
        return f"Block # {self.index}"

    def __repr__(self):
        return str(self)

    def generate_hash(self):
        pass

    def print_block(self):
        pass
