from django.db import models


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
        pass

    def is_chain_valid(self):
        pass

    def proof_of_work(self):
        pass

    def print_chain(self):
        pass

    def get_blocks(self):
        return self.block_set.all().order_by('index')

    def get_members(self):
        return self.members.all()
