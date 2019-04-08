from django.db import models
import datetime
from hashlib import sha256


class AbstractBlock(models.Model):
    data = models.TextField(max_length=255)
    index = models.IntegerField(blank=True)
    timestamp = models.DateTimeField()
    previous_hash = models.CharField(max_length=255)
    nonce = models.CharField(max_length=255)
    hash = models.CharField(max_length=255, blank=True)
    chain = models.ForeignKey('Blockchain', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Block # {self.index}"

    def __repr__(self):
        return str(self)

    def generate_hash(self):
        block_header = f"{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        block_hash = sha256(block_header.encode())
        return block_hash.hexdigest()

    def calculate_proof_of_work(self, difficulty=2):
        self.nonce = 0
        proof = self.generate_hash()
        while not self.is_valid_proof(proof):
            self.nonce += 1
            proof = self.generate_hash()
        self.hash = proof

    @staticmethod
    def is_valid_proof(proof, difficulty=2):
        return proof[:difficulty] == '0'*difficulty

    def print_block(self):
        pass


class Block(AbstractBlock):
    pass


class DuplicateBlock(AbstractBlock):
    chain = models.ForeignKey('DuplicateBlockchain', on_delete=models.CASCADE)

    def populate_from_block(self, block_id):
        og_block = Block.objects.get(pk=block_id)

        self.data = og_block.data
        self.index = og_block.index
        self.timestamp = og_block.timestamp
        self.previous_hash = og_block.previous_hash
        self.nonce = og_block.nonce
        self.hash = og_block.hash
