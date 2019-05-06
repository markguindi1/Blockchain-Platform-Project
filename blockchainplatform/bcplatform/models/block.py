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
        return f"{self.chain}, Block # {self.index}"

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.pk}>"

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

    def current_hash_is_correct(self):
        return self.hash == self.generate_hash()

    @staticmethod
    def is_valid_proof(proof, difficulty=2):
        return proof[:difficulty] == '0'*difficulty

    def to_dict(self):
        return {
            "chain_pk": self.chain.pk,
            "data": self.data,
            "index": self.index,
            "timestamp": self.timestamp.strftime("%B %-d, %Y, %-I:%M %p"),
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Block(AbstractBlock):
    pass


class DuplicateBlock(AbstractBlock):
    chain = models.ForeignKey('DuplicateBlockchain', on_delete=models.CASCADE)
