from django.db import models
from .block import *

class Blockchain(models.Model):
    name = models.CharField(max_length=255, blank=False)
    admin = models.ForeignKey('BlockchainUser', on_delete=models.CASCADE, related_name='blockchains')
    members = models.ManyToManyField('BlockchainUser', blank=True, related_name='other_blockchains')
    # Without related name^^, throws error

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return str(self)

    def genesis_block(self):
        pass

    def add_data(self, data):
        # Get hash of previous block
        prev_block = self.get_previous_block()
        previous_hash = prev_block.hash
        previous_ind = prev_block.index

        # Create Block with hash of previous block
        new_block = Block(
            data=data,
            index = previous_ind+1,
            timestamp=datetime.datetime.now(),
            previous_hash=previous_hash,
            chain=self
        )
        # Calculate proof of work
        new_block.calculate_proof_of_work()
        new_block.save()

    def is_chain_valid(self):


    def print_chain(self):
        pass

    def get_blocks(self):
        return self.block_set.all().order_by('index')

    def get_members(self):
        return self.members.all()

    def get_previous_block(self):
        self.get_blocks().last()
