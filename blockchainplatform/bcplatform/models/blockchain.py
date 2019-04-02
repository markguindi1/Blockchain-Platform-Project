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

    def create_genesis_block(self):
        # If blocks already exist, do not create a genesis block
        if self.get_previous_block():
            return
        genesis_block = Block()
        self.populate_block(genesis_block, data="")
        genesis_block.save()

    def populate_block(self, block, data=None):
        # Get hash & index of previous block
        previous_hash = self.get_previous_block_hash()
        previous_ind = self.get_previous_block_index()

        # Set data attributes of block
        if data:
            block.data = data
        block.index = previous_ind + 1
        block.timestamp = datetime.datetime.now()
        block.previous_hash = previous_hash
        block.chain = self

        # Calculate proof of work
        block.calculate_proof_of_work()

    def is_chain_valid(self):
        pass

    def print_chain(self):
        pass

    def get_blocks(self):
        return self.block_set.all().order_by('index')

    def get_members(self):
        return self.members.all()

    def get_previous_block(self):
        return self.get_blocks().last()

    def get_previous_block_hash(self):
        prev_block = self.get_blocks().last()
        if prev_block:
            return prev_block.hash
        return "0"

    def get_previous_block_index(self):
        prev_block = self.get_blocks().last()
        if prev_block:
            return prev_block.index
        return 0
