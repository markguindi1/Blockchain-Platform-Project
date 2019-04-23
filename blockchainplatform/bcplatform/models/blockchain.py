from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import pytz
from .block import *
import random


class AbstractBlockchain(models.Model):
    name = models.CharField(max_length=255, blank=False)
    admin = models.ForeignKey('BlockchainUser', on_delete=models.CASCADE, related_name='blockchains')
    members = models.ManyToManyField('BlockchainUser', blank=True, related_name='other_blockchains')
    # Without related name^^, throws error

    blockClass = Block

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.pk}, Name: {self.name}>"

    def create_genesis_block(self):
        # If blocks already exist, do not create a genesis block
        if self.get_previous_block():
            return
        self.append_data("Genesis Block")
        # genesis_block = Block()
        # self.populate_block(genesis_block, data="Genesis Block")
        # genesis_block.save()

    def append_data(self, data):
        new_block = self.blockClass()
        self._populate_block(new_block, data)
        new_block.save()

    def _populate_block(self, block, data=None):
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

    def get_block_by_i(self, i):
        try:
            return self.get_blocks().get(index=i)
        except ObjectDoesNotExist:
            return None

    def get_block_by_i_queryset(self, i):
        return self.get_blocks().filter(index=i)

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

    def mine_block(self, block_i):
        block_to_mine = self.get_block_by_i(block_i)
        if block_to_mine is not None:
            prev_block = self.get_block_by_i(block_i-1)
            block_to_mine.previous_hash = prev_block.hash
            block_to_mine.calculate_proof_of_work()
            block_to_mine.save()


class Blockchain(AbstractBlockchain):

    def get_absolute_url(self):
        url_kwargs = {
            'pk': str(self.pk)
        }
        return reverse("bcplatform:blockchain_detail_view", kwargs=url_kwargs)


class DuplicateBlockchain(AbstractBlockchain):
    admin = models.ForeignKey('BlockchainUser', on_delete=models.CASCADE, related_name='dup_blockchains')
    members = models.ManyToManyField('BlockchainUser', blank=True, related_name='dup_other_blockchains')
    creation_time = models.DateTimeField(null=True)
    original_blockchain = models.ForeignKey('Blockchain', on_delete=models.CASCADE)
    twin_blockchain = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    first_invalid_block_index = models.IntegerField(null=True)

    blockClass = DuplicateBlock

    def get_absolute_url(self):
        url_kwargs = {
            'bc_pk': str(self.original_blockchain.pk),
            'corrupt_bc_pk': str(self.pk)
        }
        return reverse("bcplatform:blockchain_corrupted_view", kwargs=url_kwargs)

    def is_corrupted(self):
        return self.first_invalid_block_index is not None

    # Overriden to get duplicate blocks
    def get_blocks(self):
        return self.duplicateblock_set.all().order_by('index')

    def get_valid_blocks(self):
        all_blocks = self.get_blocks()
        if self.first_invalid_block_index is None:
            return all_blocks
        return all_blocks.filter(index__lt=self.first_invalid_block_index).order_by('index')

    def get_twin_blockchain(self):
        return self.twin_blockchain

    def init_from_blockchain(self, blockchain_id):
        self.original_blockchain = Blockchain.objects.get(pk=blockchain_id)
        self.name = f"Duplicate of {self.original_blockchain.name}"
        self.admin = self.original_blockchain.admin
        # Need to save self before setting members
        self.save()
        self.members.set(self.original_blockchain.get_members())
        self.creation_time = timezone.now()
        self.first_invalid_block_index = None
        self.save()

        self._add_blocks_from_orig_blockchain()

    def _add_blocks_from_orig_blockchain(self):
        original_blocks = self.original_blockchain.get_blocks()

        for orig_block in original_blocks:
            self._add_copy_of_orig_block(orig_block)

    def _add_copy_of_orig_block(self, og_block):
        new_dup_block = DuplicateBlock()
        self._populate_from_orig_block(new_dup_block, og_block)
        new_dup_block.save()

    def _populate_from_orig_block(self, new_block, og_block):
        new_block.data = og_block.data
        new_block.index = og_block.index
        new_block.timestamp = og_block.timestamp
        new_block.previous_hash = og_block.previous_hash
        new_block.nonce = og_block.nonce
        new_block.hash = og_block.hash
        new_block.chain = self

    def alter_data(self, data, block_i):
        blocks = self.get_blocks()

        for block in blocks:
            if block.index < block_i:
                continue
            if block.index == block_i:
                block.data = data
                block.nonce = 0
                block.hash = block.generate_hash()
                # block.calculate_proof_of_work()
                block.save()

                if (self.first_invalid_block_index is None) or (self.first_invalid_block_index > block_i):
                    self.first_invalid_block_index = block_i
                break

    def duplicate_from_twin(self, block_i):
        twin_block = self.get_twin_block_by_i(block_i)
        if twin_block is not None:
            new_block = self.blockClass()

            new_block.data = twin_block.data
            new_block.index = twin_block.index
            new_block.timestamp = twin_block.timestamp
            new_block.previous_hash = twin_block.previous_hash
            new_block.nonce = twin_block.nonce
            new_block.hash = twin_block.hash
            new_block.chain = self
            new_block.save()

    def mine_block(self, block_i):
        super().mine_block(block_i)
        self.update_first_invalid_block()

    def update_first_invalid_block(self):
        blocks = self.get_blocks()
        for block in blocks:
            if not block.current_hash_is_correct():
                self.first_invalid_block_index = block.index
                return
            self.first_invalid_block_index = None

    def get_twin_block_by_i(self, block_i):
        return self.twin_blockchain.get_block_by_i(block_i)

    def recalculate_block_hashes(self, start_block_i):
        pass
