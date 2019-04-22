from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from ..models import *
from .util_views import *
from ..forms import BlockForm

BLOCK_FORM_FIELDS = ['data']


class BlockCreateView(OwnerOrMemberRequiredMixin, LoginRequiredMixin, FormView):
    """This view allows a user to add data to a blockchain. Handles both the GET and POST"""
    # model = Block
    # fields = BLOCK_FORM_FIELDS
    template_name = "bcplatform/block_create_form.html"
    form_class = BlockForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        bc = self.get_object()
        context['bc'] = bc
        return context

    def form_valid(self, form):
        chain_pk = self.kwargs['bc_pk']
        bc = Blockchain.objects.get(pk=chain_pk)
        data = form.cleaned_data['data']
        bc.append_data(data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("bcplatform:blockchain_detail_view", kwargs={'pk': self.kwargs['bc_pk']})

    # Method added so the OwnerOrMemberRequiredMixin can get the proper blockchain in order to check if the user is an
    # admin/member.
    def get_object(self, queryset=None):
        chain_pk = self.kwargs['bc_pk']
        return Blockchain.objects.get(pk=chain_pk)


