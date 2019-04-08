from django.db import models
from django.utils import timezone
import pytz
from .block import *


class AbstractBlockchain(models.Model):
    name = models.CharField(max_length=255, blank=False)
    admin = models.ForeignKey('BlockchainUser', on_delete=models.CASCADE, related_name='blockchains')
    members = models.ManyToManyField('BlockchainUser', blank=True, related_name='other_blockchains')
    # Without related name^^, throws error

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return str(self)

    def create_genesis_block(self):
        # If blocks already exist, do not create a genesis block
        if self.get_previous_block():
            return
        genesis_block = Block()
        self.populate_block(genesis_block, data="Genesis Block")
        genesis_block.save()

    def populate_block(self, block, data=None):
        # Get hash & index of previous block
        previous_hash = self.get_previous_block_hash()
        previous_ind = self.get_previous_block_index()

        # Set data attributes of block
        if data:
            block.data = data
        block.index = previous_ind + 1
        block.timestamp = timezone.now()
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
        prev_block = self.get_previous_block()
        if prev_block:
            return prev_block.hash
        return "0"

    def get_previous_block_index(self):
        prev_block = self.get_previous_block()
        if prev_block:
            return prev_block.index
        return -1


class Blockchain(AbstractBlockchain):
    pass


class DuplicateBlockchain(AbstractBlockchain):
    admin = models.ForeignKey('BlockchainUser', on_delete=models.CASCADE, related_name='dup_blockchains')
    members = models.ManyToManyField('BlockchainUser', blank=True, related_name='dup_other_blockchains')

    latest_valid_block_index = models.IntegerField(blank=True)

    def __str__(self):
        return f"Blockchain {self.name}"

    def __repr__(self):
        return str(self)

    def init_from_blockchain(self, blockchain_id):
        pass

    def copy_block(self, block, new_data=None):
        pass

    def alter_data(self, data, block_i):
        pass

    def recalculate_block_hashes(self):
        pass
