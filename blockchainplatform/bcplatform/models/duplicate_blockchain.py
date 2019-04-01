from django.db import models
from .blockchain import *

class DuplicateBlockchain(Blockchain):
    latest_valid_block_index = models.IntegerField(blank=True)

    def __str__(self):
        return f"Blockchain {self.name}"

    def __repr__(self):
        return str(self)

    def init_from_blockchain(self, blockchain):
        pass

    def alter_data(self, data, block_i):
        pass

    def recalculate_block_hashes(self):
        pass
