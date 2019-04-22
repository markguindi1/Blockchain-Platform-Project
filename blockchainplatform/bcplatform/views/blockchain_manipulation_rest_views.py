from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import *
from .util_views import *


class DuplicateBlockchainMineBlockView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        """
        """

        # To do: If block_i is higher than actual last block for either dup_bc or twin, use actual last block i + 1

        dup_bc_pk = kwargs['dup_bc_pk']
        block_i = kwargs['block_i']

        # Get block to mine
        dup_bc = DuplicateBlockchain.objects.get(pk=dup_bc_pk)
        block_to_mine = dup_bc.get_block_by_i(block_i)
        twin_block_to_mine = dup_bc.get_twin_block_by_i(block_i)

        # If there is a block to mine, mine it and return it
        if block_to_mine is not None:
            dup_bc.mine_block(block_i)
        # If there is no block to mine, but the twin has a block
        elif twin_block_to_mine is not None:
            dup_bc.duplicate_from_twin(block_i)
            dup_bc.mine_block(block_i)
        # Neither has a block to mine, so create the block from scratc
        else:
            data = self.get_random_quote()
            # append_data() does the mining itself
            dup_bc.append_data(data)

        newly_mined_block_queryset = dup_bc.get_block_by_i_queryset(block_i)
        return JsonResponse(self.block_to_json(newly_mined_block_queryset), safe=False)

    def get_random_quote(self):
        url = "http://quotes.stormconsultancy.co.uk/random.json"
        return "I am a random quote placeholder"

    def block_to_json(self, block_queryset):
        return serializers.serialize("json", block_queryset)
