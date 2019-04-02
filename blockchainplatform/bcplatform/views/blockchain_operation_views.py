from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from ..models import *
from .util_views import *

BLOCK_FORM_FIELDS = ['data']


class BlockCreateView(LoginRequiredMixin, CreateView):
    model = Block
    fields = BLOCK_FORM_FIELDS
    template_name = "bcplatform/blockchain_create_update_form.html"

    def form_valid(self, form):
        chain_pk = self.kwargs['bc_pk']
        bc = Blockchain.objects.get(pk=chain_pk)
        print(f"{form.instance}, {type(form.instance)}")
        bc.populate_block(form.instance)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("bcplatform:blockchain_detail_view", kwargs={'pk': self.kwargs['bc_pk']})

