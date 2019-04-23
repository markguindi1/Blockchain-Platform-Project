from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from ..models import *
from .util_views import *


class BlockchainCorruptFormView(LoginRequiredMixin, View):

    template_name = "bcplatform/blockchain_corrupt_form_view.html"
    # success_url = reverse_lazy("bcplatform:homepage")

    def get(self, request, *args, **kwargs):
        """
        This method handles getting the template for allowing the user to submit altered data
        """
        bc_pk = kwargs['bc_pk']
        bc = self.get_blockchain(bc_pk)
        bc_blocks = bc.get_blocks()
        context = {
            'bc': bc,
            'bc_blocks': bc_blocks,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        This method handles getting the block that the user altered the data of, as well as the altered data itself. It
        then creates a duplicate blockchain
        """
        # Get block to alter, and its blockchain
        block_id = int(request.POST['block_id'])
        block = Block.objects.get(pk=block_id)
        block_index = block.index
        bc_pk = block.chain.pk

        # Create new duplicate blockchains
        dup_bc = DuplicateBlockchain()
        valid_dup_bc = DuplicateBlockchain()

        # Initialize them from the same blockchain
        dup_bc.init_from_blockchain(bc_pk)
        valid_dup_bc.init_from_blockchain(bc_pk)
        valid_dup_bc.first_invalid_block_index = None

        # Set them to reference each other
        dup_bc.twin_blockchain = valid_dup_bc
        valid_dup_bc.twin_blockchain = dup_bc

        # Alter the data of the duplicate blockchain
        new_data = request.POST['new_data']
        dup_bc.alter_data(new_data, block_index)

        # Save both blockchains
        dup_bc.save()
        valid_dup_bc.save()

        # Redirect to homepage
        redirect_url = self.get_success_url(dup_bc.pk)
        return redirect(redirect_url)

    def get_success_url(self, dup_bc_pk):
        url_kwargs = {
            'corrupt_bc_pk': dup_bc_pk
        }
        return reverse("bcplatform:blockchain_corrupted_view", kwargs=url_kwargs)

    def get_blockchain(self, bc_pk):
        return Blockchain.objects.get(pk=bc_pk)

    def get_object(self):
        bc_pk = self.kwargs['bc_pk']
        return self.get_blockchain(bc_pk)


class BlockchainCorruptedView(LoginRequiredMixin, TemplateView):

    template_name = "bcplatform/blockchain_corrupted_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        corrupt_bc_pk = self.kwargs['corrupt_bc_pk']
        corrupt_bc = DuplicateBlockchain.objects.get(pk=corrupt_bc_pk)

        corrupt_bc_blocks = corrupt_bc.get_blocks()

        valid_bc = DuplicateBlockchain.objects.get(twin_blockchain=corrupt_bc)
        valid_bc_blocks = valid_bc.get_blocks()

        context['corrupt_bc'] = corrupt_bc
        context['corrupt_bc_blocks'] = corrupt_bc_blocks
        context['valid_bc'] = valid_bc
        context['valid_bc_blocks'] = valid_bc_blocks

        return context


class BlockchainReconcileView(LoginRequiredMixin, TemplateView):

    template_name = "bcplatform/blockchain_manipulation_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        corrupt_bc_pk = self.kwargs['corrupt_bc_pk']
        corrupt_bc = DuplicateBlockchain.objects.get(pk=corrupt_bc_pk)

        corrupt_bc_valid_blocks = corrupt_bc.get_valid_blocks()

        valid_bc = DuplicateBlockchain.objects.get(twin_blockchain=corrupt_bc)
        valid_bc_valid_blocks = valid_bc.get_valid_blocks()

        context['corrupt_bc'] = corrupt_bc
        context['corrupt_bc_valid_blocks'] = corrupt_bc_valid_blocks
        context['valid_bc'] = valid_bc
        context['valid_bc_valid_blocks'] = valid_bc_valid_blocks

        # Setting other context vars
        context['title'] = "Reconciliation Attempt"
        context['corrupt_bc_interval'] = 2
        context['valid_bc_interval'] = 2
        context['timeout'] = 15

        return context


class BlockchainAttackView(LoginRequiredMixin, TemplateView):

    template_name = "bcplatform/blockchain_manipulation_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        corrupt_bc_pk = self.kwargs['corrupt_bc_pk']
        corrupt_bc = DuplicateBlockchain.objects.get(pk=corrupt_bc_pk)

        corrupt_bc_valid_blocks = corrupt_bc.get_valid_blocks()

        valid_bc = DuplicateBlockchain.objects.get(twin_blockchain=corrupt_bc)
        valid_bc_valid_blocks = valid_bc.get_valid_blocks()

        context['corrupt_bc'] = corrupt_bc
        context['corrupt_bc_valid_blocks'] = corrupt_bc_valid_blocks
        context['valid_bc'] = valid_bc
        context['valid_bc_valid_blocks'] = valid_bc_valid_blocks

        # Setting other context vars
        context['title'] = "51% Attack"
        context['corrupt_bc_interval'] = 1
        context['valid_bc_interval'] = 2
        context['timeout'] = 15

        return context


