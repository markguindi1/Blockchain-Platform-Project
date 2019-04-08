from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from ..models import *
from .util_views import *


class BlockchainCorruptFormView(LoginRequiredMixin, View):

    template_name = "bcplatform/blockchain_corrupt_form_view.html"
    success_url = reverse_lazy("bcplatform:homepage")

    def get(self, request, *args, **kwargs):
        bc_pk = kwargs['bc_pk']
        bc = self.get_blockchain(bc_pk)
        bc_blocks = bc.get_blocks()
        context = {
            'bc': bc,
            'bc_blocks': bc_blocks,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        block_id = int(request.POST['block_id'])
        block = Block.objects.get(pk=block_id)
        block_index = block.index

        bc_pk = block.chain.pk

        # Create new duplicate blockchain
        dup_bc = DuplicateBlockchain()

        dup_bc.init_from_blockchain(bc_pk)

        new_data = request.POST['new_data']
        dup_bc.alter_data(new_data, block_index)

        # Redirect to homepage
        return redirect(self.success_url)

    def get_blockchain(self, bc_pk):
        return Blockchain.objects.get(pk=bc_pk)

    def get_object(self):
        bc_pk = self.kwargs['bc_pk']
        return self.get_blockchain(bc_pk)

