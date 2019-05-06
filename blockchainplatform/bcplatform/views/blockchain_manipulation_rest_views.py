from django.db.models import ForeignKey
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import *
from .util_views import *
import requests
from datetime import datetime, timedelta


class DuplicateBlockchainMineBlockView(LoginRequiredMixin, View):

    # If a quote is part of the following list, we don't want it showing up on the blockchain
    INAPPROPRIATE_QUOTES = [
        "C++ : Where friends have access to your private members.",
        "Computers are like bikinis. They save people a lot of guesswork.",
        "Documentation is like sex; when it's good, it's very, very good, and when it's bad, it's better than nothing.",
        "Programming is like sex: one mistake and you’re providing support for a lifetime.",
        "There are only two kinds of programming languages: those people always bitch about and those nobody uses.",
        "Saying that Java is good because it works on all platforms is like saying anal sex is good because it works \
        on all genders.",
    ]

    def get(self, request, *args, **kwargs):
        """This view mines a block of given index, and returns the full data of the mined block. If the block does not
        exist, it will first create the block (either from its twin blockchain, or from scratch) and then mine it.
         """

        dup_bc_pk = int(kwargs['dup_bc_pk'])
        block_i = int(kwargs['block_i'])

        # Get relevant blockchains
        dup_bc = DuplicateBlockchain.objects.get(pk=dup_bc_pk)
        twin_dup_bc = dup_bc.get_twin_blockchain()

        # Get appropriate block index to mine. The block index to mine should either be an existing block index, or the
        # index of the next block to be added. Anything else would produce inconsistencies between a duplicate BC and
        # its twin
        previous_block_i = dup_bc.get_previous_block_index()
        if (previous_block_i + 1) < block_i:
            block_i = previous_block_i + 1

        # Get block to mine (as well as block to duplicate from)
        block_to_mine = dup_bc.get_block_by_i(block_i)
        twin_block_to_mine = twin_dup_bc.get_block_by_i(block_i)

        # If there is a block to mine, mine it and return it
        if block_to_mine is not None:
            dup_bc.mine_block(block_i)
            dup_bc.save()
        # If there is no block to mine, but the twin has a block
        elif twin_block_to_mine is not None:
            dup_bc.duplicate_block_from_twin(block_i)
            dup_bc.mine_block(block_i)
            dup_bc.save()
        # Neither has a block to mine, so create the block from scratch
        else:
            data = self.get_random_quote()
            # append_data() does the mining itself
            dup_bc.append_data(data)
            dup_bc.save()

        newly_mined_block = dup_bc.get_block_by_i(block_i)
        newly_mined_block_dict = newly_mined_block.to_dict()
        return JsonResponse(newly_mined_block_dict, json_dumps_params={'indent': 2})

    def get_random_quote(self):
        url = "http://quotes.stormconsultancy.co.uk/random.json"
        try:
            r = requests.get(url)
            response_json = r.json()
            quote = response_json['quote']
            if quote in self.INAPPROPRIATE_QUOTES:
                quote = "Couldn't get a quote"
        except requests.exceptions.RequestException:
            quote = "Couldn't get a quote"
        return quote


class ClearDuplicateBlockchainsView(View):

    def get(self, request, *args, **kwargs):
        """Deletes all DuplicateBlockchains created over 24 hours ago
        """
        # Time Threshold Represents 12 hours ago
        time_threshold = datetime.now() - timedelta(hours=24)
        # Query for Duplicate Blockchains older than time threshold
        old_dup_blockchains = DuplicateBlockchain.objects.filter(creation_time__lt=time_threshold)
        old_dup_blockchains.delete()

        response = {
            "status": True,
            "message": "Duplicate Blockchains successfully deleted",
        }
        return JsonResponse(response, json_dumps_params={'indent': 2})


